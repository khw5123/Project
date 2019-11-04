#-*- coding: utf-8 -*-
import struct
import hashlib
import zlib
import sys
import marshal
import base64
import imp

# ---------------------------------------------------------------------
# convert_date(t)
# 주어진 정수에서 날짜를 얻는다.
# 입력값 : 년,월,일이 포함된 2Byte 정수
# 리턴값 : 년, 월, 일
# ---------------------------------------------------------------------
def convert_date(t):
    y = ((t & 0xFE00) >> 9) + 1980
    m = (t & 0x01E0) >> 5
    d = (t & 0x001F)
    # print '%04d-%02d-%02d' % (y, m, d)
    return y, m, d

# ---------------------------------------------------------------------
# convert_time(t)
# 주어진 정수에서 시간를 얻는다.
# 입력값 : 시,분,초가 포함된 2Byte 정수
# 리턴값 : 시, 분, 초
# ---------------------------------------------------------------------
def convert_time(t):
    h = (t & 0xF800) >> 11
    m = (t & 0x07E0) >> 5
    s = (t & 0x001F) * 2
    # print '%02d:%02d:%02d' % (h, m, s)
    return h, m, s

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
# ntimes_md5(buf, ntimes)
# 주어진 버퍼에 대해 n회 반복해서 MD5 해시 결과를 리턴한다.
# 입력값 : buf    - 버퍼
#         ntimes - 반복 횟수
# 리턴값 : MD5 해시
# ---------------------------------------------------------------------
def ntimes_md5(buf, ntimes):
    md5 = hashlib.md5()
    md5hash = buf
    for i in range(ntimes):
        md5.update(md5hash)
        md5hash = md5.hexdigest()
    return md5hash

class KMDFormatError(Exception): # KMD 오류 메시지를 정의
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class KMDConstants: # KMD 관련 상수
    KMD_SIGNATURE = 'KAVM'  # 시그너처
    KMD_DATE_OFFSET = 4  # 날짜 위치
    KMD_DATE_LENGTH = 2  # 날짜 크기
    KMD_TIME_OFFSET = 6  # 시간 위치
    KMD_TIME_LENGTH = 2  # 시간 크기
    KMD_RESERVED_OFFSET = 8  # 예약 영역 위치
    KMD_RESERVED_LENGTH = 28  # 예약 영역 크기
    KMD_RC4_KEY_OFFSET = 36  # RC4 Key 위치
    KMD_RC4_KEY_LENGTH = 32  # RC4 Key 길이
    KMD_MD5_OFFSET = -32  # MD5 위치

class KMD(KMDConstants): # KMD 클래스
    # ---------------------------------------------------------------------
    # __init__(self, fname, pu)
    # 클래스를 초기화 한다.
    # 인자값 : fname - KMD 파일 이름
    #         pu    - 복호화를 위한 공개키
    # ---------------------------------------------------------------------
    def __init__(self, fname, pu):
        self.filename = fname  # KMD 파일 이름
        self.date = None  # KMD 파일의 날짜
        self.time = None  # KMD 파일의 시간
        self.body = None  # 복호화 된 파일 내용
        self.__kmd_data = None  # KMD 암호화 된 파일 내용
        self.__rsa_pu = pu  # RSA 공개키
        self.__rc4_key = None  # RC4 키
        if self.filename:
            self.__decrypt(self.filename)  # 파일을 복호화한다.

    # ---------------------------------------------------------------------
    # __decrypt(self, fname)
    # kmd 파일을 복호화 한다.
    # 인자값 : fname - KMD 파일 이름
    # ---------------------------------------------------------------------
    def __decrypt(self, fname, debug=False):
        # KMD 파일을 열고 시그너처를 체크한다.
        with open(fname, 'rb') as fp:
            if fp.read(4) == self.KMD_SIGNATURE:  # KMD 파일이 맞는지 체크 함
                self.__kmd_data = self.KMD_SIGNATURE + fp.read()  # 파일을 읽어 들임
            else:
                raise KMDFormatError('KMD Header magic not found.')
        # KMD 파일 날짜 읽기
        tmp = self.__kmd_data[self.KMD_DATE_OFFSET:
                              self.KMD_DATE_OFFSET + self.KMD_DATE_LENGTH]
        self.date = convert_date(struct.unpack('<H', tmp)[0])
        # print self.date
        # KMD 파일 시간 읽기
        tmp = self.__kmd_data[self.KMD_TIME_OFFSET:
                              self.KMD_TIME_OFFSET + self.KMD_TIME_LENGTH]
        self.time = convert_time(struct.unpack('<H', tmp)[0])
        # print self.time
        # KMD 파일에서 MD5 읽기
        e_md5hash = self.__get_md5()
        # 무결성 체크
        md5hash = ntimes_md5(self.__kmd_data[:self.KMD_MD5_OFFSET], 3)
        if e_md5hash != md5hash.decode('hex'):
            raise KMDFormatError('Invalid KMD MD5 hash.')
        # KMD 파일에서 RC4 키 읽기
        self.__rc4_key = self.__get_rc4_key()
        # KMD 파일에서 본문 읽기
        e_kmd_data = self.__get_body()
        if debug:
            print len(e_kmd_data)
        # 압축 해제하기
        self.body = zlib.decompress(e_kmd_data)
        if debug:
            print len(self.body)

    # ---------------------------------------------------------------------
    # __get_rc4_key(self)
    # kmd 파일의 rc4 키를 얻는다.
    # 리턴값 : rc4 키
    # ---------------------------------------------------------------------
    def __get_rc4_key(self):
        e_key = self.__kmd_data[self.KMD_RC4_KEY_OFFSET:
                                self.KMD_RC4_KEY_OFFSET + self.KMD_RC4_KEY_LENGTH]
        return crypt(e_key, self.__rsa_pu)

    # ---------------------------------------------------------------------
    # __get_body(self)
    # kmd 파일의 body를 얻는다.
    # 리턴값 : body
    # ---------------------------------------------------------------------
    def __get_body(self):
        e_kmd_data = self.__kmd_data[self.KMD_RC4_KEY_OFFSET
                                     + self.KMD_RC4_KEY_LENGTH:self.KMD_MD5_OFFSET]
        r = RC4()
        r.set_key(self.__rc4_key)
        return r.crypt(e_kmd_data)

    # ---------------------------------------------------------------------
    # __get_md5(self)
    # kmd 파일의 md5를 얻는다.
    # 리턴값 : md5
    # ---------------------------------------------------------------------
    def __get_md5(self):
        e_md5 = self.__kmd_data[self.KMD_MD5_OFFSET:]
        return crypt(e_md5, self.__rsa_pu)

# ---------------------------------------------------------------------
# load(mod_name, buf)
# 주어진 모듈 이름으로 파이썬 코드를 메모리에 로딩한다.
# 입력값 : mod_name - 모듈 이름
#         buf      - 파이썬 코드 (pyc 시그너처 포함)
# 리턴값 : 로딩된 모듈 Object
# ---------------------------------------------------------------------
def load(mod_name, buf):
    if buf[:4] == '03F30D0A'.decode('hex'):  # puc 시그너처가 존재할 경우
        try:
            code = marshal.loads(buf[8:])  # pyc에서 파이썬 코드를 로딩한다. 아직 실행가능한 상태가 아니다.
            module = imp.new_module(mod_name)  # 새로운 빈 모듈을 생성한다. exec 함수로 파이썬 코드를 실행가능한 상태로 만들기 위해서는 모듈 형태여야 한다.
            exec (code, module.__dict__)  # pyc 파이썬 코드와 모듈을 연결한다. 파이썬 코드를 실행가능한 상태로 만든다.
            sys.modules[mod_name] = module  # 전역에서 사용가능하게 등록한다. 모든 플러그인 엔진이 이를 쉽게 호출할 수 있도록 sys.modules에 등록한다.
            print dir(module) # 파이썬 코드 내 클래스와 함수 목록을 출력한다.
            return module
        except:
            return None
    else:
        return None

# load 함수에서 sys.modules에 모듈 이름을 등록하는데 등록된 모듈을 import 해서 사용할 수 있다.
if len(sys.argv) != 3:
    print 'Usage : DecryptFile.py encryptedFile.kmd PublickeyFile'
    exit(0)
pu2 = read_key(sys.argv[2])
k2 = KMD(sys.argv[1], pu2)
load('myModule2', k2.body) # 모듈 이름을 설정해서 플러그인 엔진 모듈 등록

import myModule2

kav2 = myModule2.PluginEngine() # myModule2 플러그인 엔진의 PluginEngine 객체를 생성한다.
kav2.getinfo() # 객체 내 멤버 함수를 이용할 수 있다.

def main():
    if len(sys.argv) != 3:
        print 'Usage : DecryptFile.py encryptedFile.kmd PublickeyFile'
        return
    pu = read_key(sys.argv[2])
    k = KMD(sys.argv[1], pu)
    module = load('myModule', k.body) # 모듈 이름을 설정해서 플러그인 엔진 모듈 등록
    kav = module.PluginEngine() # myModule 플러그인 엔진의 PluginEngine 객체를 생성한다.
    kav.scan() # 객체 내 멤버 함수를 이용할 수 있다.

if __name__ == "__main__":
    main()
