# -*- coding:utf-8 -*-
import re
import sys
import os
import struct
import marshal
sys.path.insert(0, 'D:\\Python\\Workspace\\vaccine\\myWorkspace\\engine\\kavcore')
import KmdFile

MAX_COUNT = 100000 # 한 파일에 생성할 악성코드 패턴 최대 개수

re_comment = r'#.*' # virus.db 파일에서 사용할 주석문 정규표현식

size_sig = [] # 크기와 ID 저장
p1_sig = {} # MD5 앞쪽 6Byte
p2_sig = [] # MD5 뒤쪽 10Byte
name_sig = [] # 악성코드 이름

# -------------------------------------------------------------------------
# 텍스트 형태의 악성코드 패턴 DB 파일을 분석해서 악성코드 패턴 파일들을 생성하는 함수
# -------------------------------------------------------------------------
def make_signature(fname, _id):
    fp = open(fname, 'rb')
    idx = 0
    while True:
        line = fp.readline()
        if not line:
            break
        line = re.sub(re_comment, '', line) # 주석 제거
        line = re.sub(r'\s', '', line) # 공백 제거
        if len(line) == 0: # 아무것도 없을 경우
            continue # 다음줄로
        add_signature(line) # 악성코드 패턴 등록
        idx += 1
        if idx >= MAX_COUNT:
            print '[*] %s : %d' % (fname, _id)
            save_sig_file(fname, _id)
            idx = 0
            _id += 1
    fp.close()
    save_sig_file(fname, _id)
    
# -------------------------------------------------------------------------
# 텍스트 라인을 분석해서 악성코드 패턴을 위한 데이터를 저장하는 함수
# -------------------------------------------------------------------------
def add_signature(line):
    t = line.split(':')
    size = int(t[0]) # 악성코드 크기
    fmd5 = t[1].decode('hex') # MD5를 텍스트에서 바이너리로 변경
    name = t[2] # 악성코드 이름
    size_sig.append(size) # 크기 저장
    p1 = fmd5[:6] # MD5 앞쪽 6Byte
    p2 = fmd5[6:] # MD5 뒤쪽 10Byte
    p2_sig.append(p2) # 2차 악성코드 패턴(MD5 뒤쪽 10Byte) 저장
    p2_id = p2_sig.index(p2) # 2차 악성코드 패턴의 인덱스 저장
    if p1 in p1_sig: # 기존 1차 악성코드 패턴이 존재할 경우
        p1_sig[p1].append(p2_id) # 1차 악성코드 패턴에 2차 악성코드 패턴의 인덱스 저장
    else:
        p1_sig[p1] = [p2_id]
    name_sig.append(name) # 악성코드 이름 저장

# -------------------------------------------------------------------------
# 저장한 데이터를 악성코드 패턴 파일로 저장하는 함수
# -------------------------------------------------------------------------
def save_signature(fname, _id):
    # 현재 날짜와 시간을 구한다.
    ret_date = KmdFile.get_now_date()
    ret_time = KmdFile.get_now_time()
    # 날짜와 시간 값을 2Byte로 변경한다.
    val_date = struct.pack('<H', ret_date)
    val_time = struct.pack('<H', ret_time)
    # 크기 파일 저장 : ex) script.s01
    sname = '%s.s%02d' % (fname, _id)
    t = marshal.dumps(set(size_sig)) # 중복된 데이터 삭제 후 저장
    t = 'KAVS' + struct.pack('<L', len(size_sig)) + val_date + val_time + t # 헤더 + 악성코드 패턴 개수 + 날짜 + 시간
    save_file(sname, t)
    # 패턴 p1 파일 저장 : ex) script.i01
    sname = '%s.i%02d' % (fname, _id)
    t = marshal.dumps(p1_sig) # 중복된 데이터 삭제 후 저장
    t = 'KAVS' + struct.pack('<L', len(p1_sig)) + val_date + val_time + t # 헤더 + 악성코드 패턴 개수 + 날짜 + 시간
    save_file(sname, t)
    # 패턴 p2 파일 저장 : ex) script.c01
    sname = '%s.c%02d' % (fname, _id)
    t = marshal.dumps(p2_sig) # 중복된 데이터 삭제 후 저장
    t = 'KAVS' + struct.pack('<L', len(p2_sig)) + val_date + val_time + t # 헤더 + 악성코드 패턴 개수 + 날짜 + 시간
    save_file(sname, t)
    # 악성코드 이름 파일 저장 : ex) script.n01
    sname = '%s.n%02d' % (fname, _id)
    t = marshal.dumps(name_sig) # 중복된 데이터 삭제 후 저장
    t = 'KAVS' + struct.pack('<L', len(name_sig)) + val_date + val_time + t # 헤더 + 악성코드 패턴 개수 + 날짜 + 시간
    save_file(sname, t)
    
def save_file(fname, data):
    fp = open(fname, 'wb')
    fp.write(data)
    fp.close()

# -------------------------------------------------------------------------
# ID별로 파일을 생성하는 함수
# -------------------------------------------------------------------------
def save_sig_file(fname, _id):
    # 패턴 파일명을 이용해서 sig 파일을 만든다
    t = os.path.abspath(fname)
    _, t = os.path.split(t)
    name = os.path.splitext(t)[0]
    save_signature(name, _id)
    # 초기화
    global size_sig
    global p1_sig
    global p2_sig
    global name_sig
    size_sig = [] # 크기와 ID
    p1_sig = [] # MD5 앞쪽 6Byte
    p2_sig = [] # MD5 뒤쪽 10Byte
    name_sig = [] # 악성코드 이름

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage : sigtool_md5.py [sig text] [id]'
        exit(0)
    if len(sys.argv) == 2:
        sin_fname = sys.argv[1]
        _id = 1
    elif len(sys.argv) == 3:
        sin_fname = sys.argv[1]
        _id = int(sys.argv[2])
    make_signature(sin_fname, _id)
