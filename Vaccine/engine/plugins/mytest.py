# -*- coding:utf-8 -*-
import os
import re
import glob
import kavutil
import hashlib

class KavMain:
    # ---------------------------------------------------------------------
    # init(self, plugins_path)
    # 플러그인 엔진을 초기화 한다.
    # 입력값 : plugins_path - 플러그인 엔진의 위치
    # 리턴값 : 0 - 성공, 0 이외의 값 - 실패
    # ---------------------------------------------------------------------
    def init(self, plugins_path):
        self.plugins = plugins_path # 플러그인 엔진 디렉터리
        self.sig_key = 'mytest' # 악성코드 패턴 파일 이름(확장자 제외)
        self.p_space = re.compile(r'\s') # 공백 문자 제거를 위한 정규 표현식
        self.vlist = list() # 악성코드 이름
        self.get_virusname() # 악성코드 이름 저장
        return 0 # 플러그인 엔진 초기화 성공

    def get_virusname(self): # 악성코드 패턴 파일에서 바이러스 이름을 찾는 함수
        try:
            fl = glob.glob(self.plugins + os.sep + '%s.n??' % self.sig_key)
            vname= ''
            for fname in fl:
                buf = open(fname, 'rb').read()
                for i in range(17, len(buf)):
                    if buf[i:i+1] == '`': # 읽은 문자가 임시 악성코드 패턴 DB 파일(sigtool_md5.log)에서 설정한 악성코드 이름의 끝을 뜻하는 ` 문자일 경우
                        self.vlist.append(vname[5:])
                        vname = ''
                    else:
                        vname += buf[i:i+1]
        except Exception, e:
            pass

    # ---------------------------------------------------------------------
    # listvirus(self)
    # 진단/치료 가능한 악성코드의 리스트를 알려준다.
    # 리턴값 : 악성코드 리스트
    # ---------------------------------------------------------------------   
    def listvirus(self):
        return self.vlist

    # ---------------------------------------------------------------------
    # scan(self, filehandle, filename, fileformat, filename_ex)
    # 악성코드를 검사한다.
    # 입력값 : filehandle  - 파일 핸들
    #         filename    - 파일 이름
    #         fileformat  - 파일 포맷
    #         filename_ex - 파일 이름 (압축 내부 파일 이름)
    # 리턴값 : 악성코드 발견 여부, 악성코드 이름, 악성코드 ID
    # ---------------------------------------------------------------------
    def scan(self, filehandle, filename, fileformat, filename_ex):
        try:
            mm = filehandle
            mbuf = mm[:4096] # 파일의 4096 Byte 를 읽어서 저장
            n_buf = len(mbuf)
            p_text = re.compile(r'[\w\s!"#$%&\'()*+,\-./:;<=>?@\[\\\]\^_`{\|}~]')
            n_text = len(p_text.findall(mbuf))
            if n_text / float(n_buf) > 0.8: # 해당 글자가 차지하는 비율이 80% 이상일 경우(텍스트 파일일 경우)
                buf = mm[:]
                buf = self.p_space.sub('', buf) # 공백 제거
                buf = buf.lower() # 영어 소문자로 통일
                size = len(buf) # 정형화 작업 후의 크기
                if kavutil.handle_pattern_md5.match_size(self.sig_key, size): # 파일명이 mytest 인 악성코드 패턴 파일에 해당 정형화 작업 후의 크기가 존재할 경우
                    fmd5 = hashlib.md5(buf).hexdigest() # MD5 해시 구하기
                    vname = kavutil.handle_pattern_md5.scan(self.sig_key, size, fmd5) # 웹셸 악성코드 검사(악성코드 발견 시 악성코드 이름 반환)
                    if vname: # 악성코드를 발견했을 경우
                        return True, vname, 0 # 악성코드 발견 여부, 악성코드 이름, 악성코드 ID 반환
        except IOError:
            pass
        return False, '', -1 # 악성코드를 발견하지 못했을 경우의 반환

    # ---------------------------------------------------------------------
    # disinfect(self, filename, malware_id)
    # 악성코드를 치료한다.
    # 입력값 : filename    - 파일 이름
    #         malware_id  - 치료할 악성코드 ID
    # 리턴값 : 악성코드 치료 여부
    # ---------------------------------------------------------------------
    def disinfect(self, filename, malware_id):
        try:
            if malware_id == 0: # 악성코드 진단 결과에서 받은 ID 값(scan 함수의 반환 값 중 악성코드 ID)이 0 일 경우
                os.remove(filename) # 파일 삭제
                return True # 치료 완료 반환
        except IOError:
            pass # 치료 실패 반환

    # ---------------------------------------------------------------------
    # getinfo(self)
    # 플러그인 엔진의 주요 정보를 알려준다. (제작자, 버전, ...)
    # 리턴값 : 플러그인 엔진 정보
    # ---------------------------------------------------------------------
    def getinfo(self):
        info = dict()
        info['author'] = 'MINE' # 제작자
        info['version'] = '1.0' # 버전
        info['title'] = 'Test Engine' # 엔진 설명
        info['kmd_name'] = self.sig_key # 엔진 파일 이름
        info['sig_num'] = kavutil.handle_pattern_md5.get_sig_num(self.sig_key) # 진단/치료 가능한 악성코드 수
        return info

    # ---------------------------------------------------------------------
    # uninit(self)
    # 플러그인 엔진을 종료한다.
    # 리턴값 : 0 - 성공, 0 이외의 값 - 실패
    # ---------------------------------------------------------------------
    def uninit(self):
        return 0 # 플러그인 엔진 종료 성공
