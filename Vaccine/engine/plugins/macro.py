# -*- coding:utf-8 -*-
import os
import re
import glob
import ahocorasick
import kavutil
import cryptoSharedLibrary

class KavMain:
    # ---------------------------------------------------------------------
    # init(self, plugins_path)
    # 플러그인 엔진을 초기화 한다.
    # 입력값 : plugins_path - 플러그인 엔진의 위치
    # 리턴값 : 0 - 성공, 0 이외의 값 - 실패
    # ---------------------------------------------------------------------
    def init(self, plugins_path):
        self.plugins = plugins_path # 플러그인 엔진 디렉터리
        self.sig_key = 'macro' # 악성코드 패턴 파일 이름(확장자 제외)
        self.vlist = list() # 악성코드 이름
        self.get_virusname() # 악성코드 이름 저장
        self.p_vba = re.compile(r'^\s*Attribute\s+VB_Name.+|^\s*Attribute\s+.+VB_Invoke_Func.+|\s+_\r?\n', re.IGNORECASE|re.MULTILINE) # Laroux 매크로 바이러스의 불필요한 정보를 제거하기 위한 정규표현식
        self.p_vba_cmt = re.compile(r'(\'|\bREM\b).*', re.IGNORECASE) # 매크로 바이러스의 주석을 제거하기 위한 정규표현식
        slef.p_space = re.compile(r'\s') # 매크로 바이러스의 공백을 제거하기 위한 정규표현식
        laroux_strings = ['auto_open()', 'application.onsheetactivate', 'activeworkbook.modules.count', 'c4$=curdir()', 'workbooks(n4$).sheets'] # Laroux 매크로 바이러스 변종에 대한 패턴
        self.aho_laroux = ahocorasick.aho_corasick()
        self.aho_laroux.make_tree(laroux_strings) # 아호 코라식 알고리즘으로 트리 생성
        return 0 # 플러그인 엔진 초기화 성공

    def get_virusname(self): # 악성코드 패턴 파일에서 바이러스 이름을 찾는 함수
        try:
            fl = glob.glob(self.plugins + os.sep + '%s.n??' % self.sig_key)
            vname= ''
            for fname in fl:
                buf = open(fname, 'rb').read()
                for i in range(17, len(buf)):
                    if buf[i:i+1] == '`':
                        self.vlist.append(vname[5:]) # 읽은 문자가 임시 악성코드 패턴 DB 파일(sigtool_md5.log)에서 설정한 악성코드 이름의 끝을 뜻하는 ` 문자일 경우
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
    # format(self, filehandle, filename)
    # 파일 포맷을 분석한다.
    # 입력값 : filehandle - 파일 핸들
    #         filename   - 파일 이름
    # 리턴값 : {파일 포맷 분석 정보} or None
    # ---------------------------------------------------------------------
    def format(self, filehandle, filename):
        fileformat = {} # 포맷 정보를 담을 공간
        ret = {}
        mm = filehandle
        if mm[:17] == 'Attribute VB_Name': # Laroux 매크로 바이러스의 소스코드 첫 번째 줄이 Attribute VB_Name 일 경우
            ret['ff_macro'] = 'MACRO' # ff_macro 파일 포맷 생성
        return ret

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
            if 'ff_macro' in fileformat:
                buf = mm[:]
                buf = self.p_vba_cmt.sub('', buf) # 주석 제거
                buf = self.p_vba.sub('', buf) # 불필요한 정보 제거
                buf = self.p_space.sub('', buf) # 공백 제거
                buf = buf.lower() # 영어 소문자로 변환
                fmd5 = cryptoSharedLibrary.md5(buf) # 정형화된 버퍼에 대해 MD5 해시 구함
                fsize = len(buf) # 정형화된 버퍼의 크기 저장
                vname = kavutil.handle_pattern_md5.scan(self.sig_key, fsize, fmd5) # macro 악성코드 패턴에서 MD5 검사
                if vname: # 악성코드가 발견 됐을 경우
                    return True, vname, 0 # 악성코드를 발견했을 경우의 반환
                else:
                    vstring = []
                    ret = self.aho_laroux.search(buf)
                    for n in ret:
                        vstring.append(n[1])
                    if len(set(vstring)) == 5:
                        return True, 'Virus.MSExcel.Laroux.Gen', 0
        except IOError:
            pass
        return False, '', -1 # 악성코드를 발견하지 못했을 경우의 반환

    # ---------------------------------------------------------------------
    # getinfo(self)
    # 플러그인 엔진의 주요 정보를 알려준다. (제작자, 버전, ...)
    # 리턴값 : 플러그인 엔진 정보
    # ---------------------------------------------------------------------
    def getinfo(self):
        info = dict()
        info['author'] = 'MINE' # 제작자
        info['version'] = '1.0'  # 버전
        info['title'] = 'Macro Engine' # 엔진 설명
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
