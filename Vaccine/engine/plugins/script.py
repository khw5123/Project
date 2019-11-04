# -*- coding:utf-8 -*-
import re
import os
import glob
import hashlib
import kavutil

class KavMain:
    # ---------------------------------------------------------------------
    # init(self, plugins_path)
    # 플러그인 엔진을 초기화 한다.
    # 입력값 : plugins_path - 플러그인 엔진의 위치
    # 리턴값 : 0 - 성공, 0 이외의 값 - 실패
    # ---------------------------------------------------------------------
    def init(self, plugins_path):
        self.plugins = plugins_path # 플러그인 엔진 디렉터리
        self.sig_key = 'script' # 악성코드 패턴 파일 이름(확장자 제외)
        self.vlist = list() # 악성코드 이름
        self.get_virusname() # 악성코드 이름 저장
        self.p_script_head = re.compile(r'\s*<\s*(script|iframe)', re.IGNORECASE) # 파일 시작이 <script, <iframe 인지 확인하는 정규표현식
        self.p_script_in_html = re.compile(r'<\s*(script|iframe).*?>([\d\D]*?)<\s*/(script|iframe)\s*>', re.IGNORECASE) # script/iframe 정보가 HTML 내부에 있는지 확인하는 정규표현식
        self.p_http = re.compile(r'https?://') # 자바스크립트 주석인 // 문자로 인해 http(s):// 뒤가 모두 주석처리될 수 있으므로 미리 https:// 를 제거하기 위한 정규 표현식
        self.p_script_cmt1 = re.compile(r'//.*|/\*[\d\D]*?\*/') # 자바 스크립트 주석(//, /* */) 제거를 위한 정규 표현식
        self.p_script_cmt2 = re.compile(r'(#|\bREM\b).*', re.IGNORECASE) # 파이썬, 배치파일, 비주얼 베이직 스크립트 주석(#, REM) 제거를 위한 정규 표현식
        self.p_space = re.compile(r'\s') # 공백 문자 제거를 위한 정규 표현식
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
        mm = filehandle # 파일 핸들 저장
        buf = mm[:4096] # 파일의 4096 Byte 를 읽어서 저장
        n_buf = len(buf)
        p_text = re.compile(r'[\w\s!"#$%&\'()*+,\-./:;<=>?@\[\\\]\^_`{\|}~]')
        n_text = len(p_text.findall(buf))
        if n_text / float(n_buf) > 0.8: # 해당 글자가 차지하는 비율이 80% 이상일 경우(텍스트 파일일 경우)
            obj = self.p_script_head.match(buf) # script 태그가 존재하는지 확인
            if obj: # script 태그가 존재할 경우
                obj_script = self.p_script_in_html.search(mm[:]) # 내부 스크립트가 존재하는지 확인
                if obj_script: # 내부 스크립트가 존재할 경우
                    buf_script = obj_script.groups()[1].strip() # 내부 스크립트의 script 태그를 제외한 스크립트만 추출
                    n_buf_script = len(buf_script)
                    fileformat['size'] = n_buf_script # 추출된 스크립트의 크기 저장
                    if n_buf_script: # 내부 스크립트일 경우
                        if obj_script.groups()[0].lower() == 'script':
                            ret = {'ff_script': fileformat}
                        else:
                            ret = {'ff_iframe': fileformat}
                    else: # 외부 스크립트일 경우
                        if obj_script.groups()[0].lower() == 'script':
                            ret = {'ff_script_external': fileformat}
                        else:
                            ret = {'ff_iframe_external': fileformat}
                else: # 내부 스크립트가 존재하지 않을 경우(외부 스크립트가 있을 수 있음)
                    fileformat['size'] = 0
                    if obj.group().lower().find('script') != -1:
                        ret = {'ff_script_external': fileformat}
                    else:
                        ret = {'ff_iframe_external': fileformat}
                return ret
        return None

    # ---------------------------------------------------------------------
    # arclist(self, filename, fileformat)
    # 압축 파일 내부의 파일 목록을 얻는다.
    # 스크립트 파일이 압축 파일이라고 한다면 스크립트 태그를 제외한 스크립트를 압축 파일 내부 파일이라고 생각하면 된다.
    # 입력값 : filename   - 파일 이름
    #         fileformat - 파일 포맷 분석 정보
    # 리턴값 : [[압축 엔진 ID, 압축된 파일 이름(실제 압축 파일이 아니므로 임의의 문자열로 대신함)]]
    # ---------------------------------------------------------------------
    def arclist(self, filename, fileformat):
        file_scan_list = [] # 검사 대상의 압축 엔진 ID 및 임의의 문자열이 저장될 리스트
        if 'ff_script' in fileformat: # format 함수에 의해 분석된 스크립트 파일 포맷이 있을 경우
            file_scan_list.append(['arc_script', 'JavaScript']) # 압축 엔진 ID와 압축 파일 정보(압축 파일이 아니므로 존재하지 않으므로 임의로 설정)리스트에 등록
        elif 'ff_iframe' in fileformat:
            file_scan_list.append(['arc_iframe', 'IFrame']) # 압축 엔진 ID와 압축 파일 정보(압축 파일이 아니므로 존재하지 않으므로 임의로 설정)리스트에 등록
        return file_scan_list # 리스트 반환

    # ---------------------------------------------------------------------
    # unarc(self, arc_engine_id, arc_name, fname_in_arc)
    # 입력값 : arc_engine_id - 압축 엔진 ID
    #         arc_name      - 압축 파일
    #         fname_in_arc  - 압축 해제할 파일 이름
    # 리턴값 : 압축 해제된 내용 or None
    # ---------------------------------------------------------------------
    def unarc(self, arc_engine_id, arc_name, fname_in_arc):
        if arc_engine_id == 'arc_script' or arc_engine_id == 'arc_iframe': # 압축 엔진 ID가 arc_script 또는 arc_iframe 일 경우
            buf = ''
            try:
                with open(arc_name, 'rb') as fp:
                    buf = fp.read() # HTML 파일을 읽어서 저장
            except IOError:
                return None
            obj = self.p_script_in_html.search(buf) # 내부 스크립트가 존재하는지 확인
            if obj: # 내부 스크립트가 존재할 경우
                data = obj.groups()[1] # 스크립트 태그를 제외한 스크립트 추출
                return data
        return None

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
                buf = self.p_http.sub('', buf) # http:// 제거
                buf = self.p_script_cmt1.sub('', buf) # 주석문 제거
                buf = self.p_script_cmt2.sub('', buf) # 주석문 제거
                buf = self.p_space.sub('', buf)  # 공백 제거
                buf = buf.lower() # 영어 소문자로 통일
                size = len(buf) # 정형화 작업 후의 크기
                if kavutil.handle_pattern_md5.match_size(self.sig_key, size): # 파일명이 script 인 악성코드 패턴 파일에 해당 정형화 작업 후의 크기가 존재할 경우
                    fmd5 = hashlib.md5(buf).hexdigest() # MD5 해시 구하기
                    vname = kavutil.handle_pattern_md5.scan(self.sig_key, size, fmd5) # 스크립트 악성코드 검사(악성코드 발견 시 악성코드 이름 반환)
                    if vname: # 악성코드를 발견했을 경우
                        return True, vname, 0 # 악성코드 발견 여부, 악성코드 이름, 악성코드 ID 반환
        except IOError:
            pass
        return False, '', -1 # 악성코드를 발견하지 못했을 때의 반환

    # ---------------------------------------------------------------------
    # disinfect(self, filename, malware_id)
    # 악성코드를 치료한다.
    # 입력값 : filename    - 파일 이름
    #         malware_id  - 치료할 악성코드 ID
    # 리턴값 : 악성코드 치료 여부
    # ---------------------------------------------------------------------
    def disinfect(self, filename, malware_id):
        try:
            if malware_id == 0: # 악성코드 진단 결과에서 받은 ID 값(scan 함수의 반환값 중 악성코드 ID)이 0일 경우
                os.remove(filename) # 파일 삭제
                return True # 치료 완료 반환
        except IOError:
            pass
        return False # 치료 실패 반환

    # ---------------------------------------------------------------------
    # getinfo(self)
    # 플러그인 엔진의 주요 정보를 알려준다. (제작자, 버전, ...)
    # 리턴값 : 플러그인 엔진 정보
    # ---------------------------------------------------------------------
    def getinfo(self):
        info = dict()
        info['author'] = 'MINE' # 제작자
        info['version'] = '1.0' # 버전
        info['title'] = 'Script Engine' # 엔진 설명
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
