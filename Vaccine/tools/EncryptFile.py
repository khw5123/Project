#-*- coding: utf-8 -*-
import struct
import hashlib
import zlib
import marshal
import sys
import os
import py_compile
import random
import shutil
import time
import base64

# ---------------------------------------------------------------------
# get_now_date(now=None)
# 현재 날짜를 2byte 날짜 값으로 변환한다.
# 입력값 : now - 현재 날짜/시간값 (생략 가능)
# 리턴값 : 2byte 날짜 값
# ---------------------------------------------------------------------
def get_now_date(now=None):
    if not now:
        now = time.gmtime()
    t_y = now.tm_year - 1980
    t_y = (t_y << 9) & 0xFE00
    t_m = (now.tm_mon << 5) & 0x01E0
    t_d = now.tm_mday & 0x001F
    return (t_y | t_m | t_d) & 0xFFFF

# ---------------------------------------------------------------------
# get_time_value(now=None)
# 현재 시간을 2byte 시간 값으로 변환한다.
# 입력값 : now - 현재 날짜/시간값 (생략 가능)
# 리턴값 : 2byte 시간 값
# ---------------------------------------------------------------------
def get_now_time(now=None):
    if not now:
        now = time.gmtime()
    t_h = (now.tm_hour << 11) & 0xF800
    t_m = (now.tm_min << 5) & 0x07E0
    t_s = (now.tm_sec / 2) & 0x001F
    return (t_h | t_m | t_s) & 0xFFFF

# ---------------------------------------------------------------------
# __value_to_string(val)
# 숫자를 문자열로 변환한다. 암호화를 쉽게 하기 위해 문자열을 숫자로 바꾼다.
# 인자값 : val - 숫자
# 리턴값 : 문자열
# ---------------------------------------------------------------------
def __value_to_string(val):
    ret = ''
    for i in range(32):
        b = val & 0xff
        val >>= 8
        ret += chr(b)
        if val == 0:
            break
    return ret

# ---------------------------------------------------------------------
# __string_to_value(buf)
# 암호화를 쉽게 하기 위해 문자열을 숫자로 바꾼다.
# 인자값 : buf - 문자열
# 리턴값 : 숫자
# ---------------------------------------------------------------------
def __string_to_value(buf):
    plantext_ord = 0
    for i in range(len(buf)):
        plantext_ord |= ord(buf[i]) << (i * 8)
    return plantext_ord

# ---------------------------------------------------------------------
# read_key(key_filename)
# 주어진 key 파일을 읽어 rsa 키로 변환한다.
# 인자값 : key_filename - rsa 키 파일
# 리턴값 : rsa 키
# ---------------------------------------------------------------------
def read_key(key_filename):
    try:
        with open(key_filename, 'rt') as fp:
            b = fp.read()
            s = base64.b64decode(b)
            key = marshal.loads(s)
        return key
    except IOError:
        return None

# ---------------------------------------------------------------------
# crypt(buf, key)
# 주어진 버퍼와 rsa 키를 이용해서 암/복호화를 한다.
# 인자값 : buf - 암/복호화 대상 버퍼
#         key - rsa 키
# 리턴값 : 암/복호화된 결과물
# ---------------------------------------------------------------------
def crypt(buf, key):
    plantext_ord = __string_to_value(buf)
    # 주어진 키로 암/복호화
    val = pow(plantext_ord, key[0], key[1])
    return __value_to_string(val)

# ---------------------------------------------------------------------
# RC4 클래스
# rc4.set_key : 암호 문자열 정의
# rc4.crypt   : 주어진 버퍼 암/복호화
# ---------------------------------------------------------------------
class RC4:
    # -----------------------------------------------------------------
    # __init__(self)
    # 멤버 변수를 초기화한다.
    # -----------------------------------------------------------------
    def __init__(self):
        self.__S = []
        self.__T = []
        self.__Key = []
        self.__K_i = 0
        self.__K_j = 0

    # -----------------------------------------------------------------
    # set_key(self, password)
    # 암호를 설정한다.
    # 인자값 : password - rc4의 암호문
    # -----------------------------------------------------------------
    def set_key(self, password):
        for i in range(len(password)):
            self.__Key.append(ord(password[i]))
        self.__init_rc4()

    # -----------------------------------------------------------------
    # crypt(self, data):
    # 주어진 데이터를 암/복호화한다.
    # 인자값 : data - 암/복호화할 데이터
    # 리턴값 : 암/복호화 결과 데이터
    # -----------------------------------------------------------------
    def crypt(self, data):
        t_str = []
        for i in range(len(data)):
            t_str.append(ord(data[i]))
        for i in range(len(t_str)):
            t_str[i] ^= self.__gen_k()
        ret_s = ''
        for i in range(len(t_str)):
            ret_s += chr(t_str[i])
        return ret_s

    # -----------------------------------------------------------------
    # __init_rc4(self)
    # rc4의 테이블을 초기화한다.
    # -----------------------------------------------------------------
    def __init_rc4(self):
        # S 초기화
        for i in range(256):
            self.__S.append(i)
            self.__T.append(self.__Key[i % len(self.__Key)])
        # S의 초기 순열 (치환)
        j = 0
        for i in range(256):
            j = (j + self.__S[i] + self.__T[i]) % 256
            self.__swap(i, j)

    # -----------------------------------------------------------------
    # __swap(self, i, j):
    # 주어진 두 인덱스의 데이터를 교환한다.
    # -----------------------------------------------------------------
    def __swap(self, i, j):
        temp = self.__S[i]
        self.__S[i] = self.__S[j]
        self.__S[j] = temp

    # -----------------------------------------------------------------
    # __gen_k(self)
    # 암/복호화에 필요한 스트림을 생성한다.
    # -----------------------------------------------------------------
    def __gen_k(self):
        i = self.__K_i
        j = self.__K_j
        i = (i + 1) % 256
        j = (j + self.__S[i]) % 256
        self.__swap(i, j)
        t = (self.__S[i] + self.__S[j]) % 256
        self.__K_i = i
        self.__K_j = j
        return self.__S[t]

# ---------------------------------------------------------------------
# make(src_fname)
# rsa 개인키를 이용해서 주어진 파일을 암호화하여 KMD 파일을 생성한다.
# 입력값 : src_fname - 암호화 대상 파일
# 리턴값 : kmd 파일 생성 성공 여부
# ---------------------------------------------------------------------
def make(src_fname, publicKey_fname, privateKey_fname, debug=False):
    # 기존 파일을 암호화한 KMD 파일을 생성한다. 구성은 다음과 같다.
    # Header : 시그너처(KAVM) + 날짜 + 시간 + 예약영역
    # Body : 개인키로 암호화한 RC4 키 + RC4로 암호화한 파일
    # Tailer : 개인키로 암호화한 Header와 Body 전체에 대해 MD5를 3번 연산한 결과
    fname = src_fname  # 암호화 대상 파일
    if fname.split('.')[-1] == 'py':  # 파이썬 파일을 컴파일 한다.
        py_compile.compile(fname)    # 컴파일
        pyc_name = fname+'c'         # 컴파일 이후 파일명
    else:  # 파이썬 파일이 아닐 경우 확장자를 pyc로 하여 복사한다.
        pyc_name = fname.split('.')[0]+'.pyc'
        shutil.copy(fname, pyc_name)
    rsa_pu = read_key(publicKey_fname) # 공개키를 로딩한다.
    rsa_pr = read_key(privateKey_fname) # 개인키를 로딩한다.
    if not (rsa_pr and rsa_pu):  # 키 파일을 찾을 수 없다
        if debug:
            print 'ERROR : Canot find the Key files!'
        return False
    kmd_data = 'KAVM' # 시그너처(KAVM)을 추가한다.
    ret_date = get_now_date() # 현재 날짜와 시간을 구한다.
    ret_time = get_now_time()
    val_date = struct.pack('<H', ret_date) # 날짜와 시간 값을 2Byte로 변경한다.
    val_time = struct.pack('<H', ret_time)
    reserved_buf = val_date + val_time + (chr(0) * 28)  # 예약 영역
    kmd_data += reserved_buf # 날짜/시간 값이 포함된 예약 영역을 만들어 추가한다.
    random.seed()
    while 1:
        tmp_kmd_data = ''  # 임시 본문 데이터
        key = '' # RC4 알고리즘에 사용할 128bit 랜덤키
        for i in range(16):
            key += chr(random.randint(0, 0xff)) # RC4 알고리즘에 사용할 128bit 랜덤키 생성
        e_key = crypt(key, rsa_pr)  # 생성된 RC4 키를 개인키로 암호화
        if len(e_key) != 32:  # 암호화에 오류가 존재하면 다시 생성
            continue
        d_key = crypt(e_key, rsa_pu)  # 암호화된 RC4키를 공개키로 복호화
        if key == d_key and len(key) == len(d_key): # 생성된 RC4 키에 문제 없음을 확인한다.
            tmp_kmd_data += e_key # 개인키로 암호화 된 RC4 키를 임시 버퍼에 추가한다.
            buf1 = open(pyc_name, 'rb').read() # 생성된 pyc 파일 압축하기
            buf2 = zlib.compress(buf1)
            e_rc4 = RC4()  # RC4 알고리즘 사용
            e_rc4.set_key(key)  # RC4 알고리즘에 key를 적용한다.
            buf3 = e_rc4.crypt(buf2) # 압축된 pyc 파일 이미지를 RC4로 암호화한다.
            e_rc4 = RC4()  # RC4 알고리즘 사용
            e_rc4.set_key(key)  # RC4 알고리즘에 key를 적용한다.
            if e_rc4.crypt(buf3) != buf2: # 암호화한 압축된 pyc 파일 이미지 복호화하여 결과가 같은지를 확인한다.
                continue
            tmp_kmd_data += buf3 # 개인키로 암호화 한 압축 된 파일 이미지를 임시 버퍼에 추가한다.
            md5 = hashlib.md5()
            md5hash = kmd_data + tmp_kmd_data  # 헤더와 본문을 합쳐서 MD5 계산
            for i in range(3):
                md5.update(md5hash)
                md5hash = md5.hexdigest()
            m = md5hash.decode('hex')
            e_md5 = crypt(m, rsa_pr)  # MD5 결과를 개인키로 암호화
            if len(e_md5) != 32:  # 암호화에 오류가 존재하면 다시 생성
                continue
            d_md5 = crypt(e_md5, rsa_pu)  # 암호화횓 MD5를 공개키로 복호화
            if m == d_md5:  # 원문과 복호화 결과가 같을 경우
                kmd_data += tmp_kmd_data + e_md5 # 헤더, 본문, 꼬리를 모두 합친다.
                break  # 무한 루프를 종료한다.
    if '.\\' in fname: # 인자로 받은 파일명에 .\ 가 있을 경우 ex) .\test.py
        fn = fname.split('.\\')[-1].split('.')[0] # 파일 명만 추출
        kmd_name = fn + '.kmd' # KMD 파일 이름 설정
    else:
        ext = fname.find('.')
        kmd_name = fname[0:ext] + '.kmd' # KMD 파일 이름을 만든다.
    try:
        if kmd_data:
            open(kmd_name, 'wb').write(kmd_data) # KMD 파일을 생성한다.
            os.remove(pyc_name) # pyc 파일은 삭제한다.
            if debug:
                print '    Success : %-13s ->  %s' % (fname, kmd_name)
            return True
        else:
            raise IOError
    except IOError:
        if debug:
            print '    Fail : %s' % fname
        return False

def main():
    if len(sys.argv) != 4:
        print 'Usage : EncryptFile.py PythonFile.py PublickeyFile PrivatekeyFile'
        return
    make(sys.argv[1], sys.argv[2], sys.argv[3], True)

if __name__ == "__main__":
    main()
