# -*- coding:utf-8 -*-
import sys
import re
import hashlib

p_space = re.compile(r'\s') # 공백 문자 제거를 위한 정규 표현식

# -------------------------------------------------------------------------
# sigtool.log의 로그 한 줄을 분석한 뒤 파일 내용을 정형화 하는 작업을 수행하는 함수
# -------------------------------------------------------------------------
def normfile(fname):
    buf = open(fname, 'rb').read() # 파일 읽기
    buf = p_space.sub('', buf) # 공백 제거
    buf = buf.lower() # 영어 소문자로 통일
    # 정형화된 내용의 파일을 새로 생성
    new_fname = 'm_' + fname
    open(new_fname, 'wb').write(buf)
    # 악성코드 패턴 파일 생성
    fsize = len(buf)
    fmd5 = hashlib.md5(buf).hexdigest()
    msg = '%d:%s:WebShell  # %s\n' % (fsize, fmd5, new_fname)
    open('sigtool_md5.log', 'at').write(msg)

def main(log_fname):
    normfile(log_fname) # 정형화 함수
    
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage : normfile.py [file]'
        exit(0)
    main(sys.argv[1])
