# -*- coding:utf-8 -*-
import sys
import re
import hashlib

p_http = re.compile(r'https?://') # 자바스크립트 주석인 // 문자로 인해 http(s):// 뒤가 모두 주석처리될 수 있으므로 미리 https:// 를 제거하기 위한 정규 표현식
p_script_cmt1 = re.compile(r'//.*|/\*[\d\D]*?\*/') # 자바 스크립트 주석(//, /* */) 제거를 위한 정규 표현식
p_script_cmt2 = re.compile(r'(#|\bREM\b).*', re.IGNORECASE) # 파이썬, 배치파일, 비주얼 베이직 스크립트 주석(#, REM) 제거를 위한 정규 표현식
p_space = re.compile(r'\s') # 공백 문자 제거를 위한 정규 표현식
p_vba = re.compile(r'^\s*Attribute\s+VB_Name.+|^\s*Attribute\s+.+VB_Invoke_Func.+|\s+_\r?\n', re.IGNORECASE|re.MULTILINE) # Laroux 매크로 바이러스의 불필요한 정보를 제거하기 위한 정규 표현식
p_vba_cmt = re.compile(r'(\'|\bREM\b).*', re.IGNORECASE) # 매크로 바이러스의 주석을 제거하기 위한 정규 표현식

# -------------------------------------------------------------------------
# sigtool.log의 로그 한 줄을 분석한 뒤 파일 내용을 정형화 하는 작업을 수행하는 함수
# -------------------------------------------------------------------------
def normfile(fname, ftype):
    buf = open(fname, 'rb').read() # 파일 읽기
    if ftype.find('HTML/Script') >= 0 or ftype.find('HTML/IFrame') >= 0:
        buf = p_http.sub('', buf) # http:// 제거
        buf = p_script_cmt1.sub('', buf) # 주석문 제거
        buf = p_script_cmt2.sub('', buf) # 주석문 제거
    elif ftype.find('VBA/') >= 0 and buf.find('Attribute VB_Name') >= 0: # --sigtool 옵션으로 만들어진 파일의 정보 중 VBA/ 라고 표시된 파일일 경우, Laroux 매크로 바이러스의 소스코드 첫 번째 줄의 Attribute VB_Name 이 존재할 경우
        buf = p_vba_cmt.sub('', buf) # 주석문 제거
        buf = p_vba.sub('', buf) # 불필요한 정보 제거
    else:
        print 'NOT Support : %s' % ftype
        return
    buf = p_space.sub('', buf) # 공백 제거
    buf = buf.lower() # 영어 소문자로 통일
    # 정형화된 내용의 파일을 새로 생성
    new_fname = 'm_' + fname
    open(new_fname, 'wb').write(buf)
    # 악성코드 패턴 파일 생성
    fsize = len(buf)
    fmd5 = hashlib.md5(buf).hexdigest()
    msg = '%d:%s:Malware_Name  # %s, %s\n' % (fsize, fmd5, new_fname, ftype)
    open('sigtool_md5.log', 'at').write(msg)

def main(log_fname):
    fp = open(log_fname)
    while True:
        line = fp.readline()
        if not line:
            break
        line = line.strip()
        f = line.split(':')
        fname = f[0].strip()
        ftype = f[1].strip()
        print fname
        normfile(fname, ftype) # 정형화 함수
    fp.close()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage : normfile.py [sigtool.log]'
        exit(0)
    main(sys.argv[1])
