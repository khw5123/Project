# -*- coding:utf-8 -*-
import re
import os

HTML_KEY_COUNT = 3 # HTML 파일인지 판단하기 위한 HTML 태그 개수

class KavMain:
    # ---------------------------------------------------------------------
    # init(self, plugins_path)
    # 플러그인 엔진을 초기화 한다.
    # 입력값 : plugins_path - 플러그인 엔진의 위치
    # 리턴값 : 0 - 성공, 0 이외의 값 - 실패
    # ---------------------------------------------------------------------
    def init(self, plugins_path):
        pat = r'<\s*html\b|\bdoctype\b|<\s*head\b|<\s*title\b|<\s*meta\b|\bhref\b|<\s*link\b|<\s*body\b|<\s*script\b|<\s*iframe\b|<\?(php\b)?' # HTML 주요 태그
        self.p_html = re.compile(pat, re.IGNORECASE)
        pat = r'<script.*?>[\d\D]*?</script>|<iframe.*?>[\d\D]*?</iframe>|<\?(php\b)?[\d\D]*?\?>' # script, iframe, php 태그
        self.p_script = re.compile(pat, re.IGNORECASE)
        return 0 # 플러그인 엔진 초기화 성공

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
            ret = self.p_html.findall(buf) # HTML 파일의 주요 태그들을 찾음
            if len(ret) >= HTML_KEY_COUNT: # HTML 파일의 주요 태그가 3개 이상일 경우
                fileformat['keyword'] = list(set(ret)) # 존재하는 HTML 태그 보관
                ret = {'ff_html': fileformat} # ff_html 파일 포맷 등록
                return ret
        return None

    # ---------------------------------------------------------------------
    # arclist(self, filename, fileformat)
    # 압축 파일 내부의 파일 목록을 얻는다.
    # 압축 파일의 경우 내부 파일에 악성 파일이 있을 수 있는데, HTML 파일의 경우 내부에 악성 스크립트를 포함하고 있을 수 있으므로 HTML 파일을 압축 파일이라고 표현한 것이다.
    # 입력값 : filename   - 파일 이름
    #         fileformat - 파일 포맷 분석 정보
    # 리턴값 : [[압축 엔진 ID, 압축된 파일 이름(실제 압축 파일이 아니므로 임의의 문자열로 대신함)]]
    # ---------------------------------------------------------------------
    def arclist(self, filename, fileformat):
        file_scan_list = [] # 검사 대상의 압축 엔진 ID 및 임의의 문자열이 저장될 리스트
        if 'ff_html' in fileformat: # format 함수에 의해 분석된 HTML 파일 포맷이 있을 경우
            buf = ''
            try:
                with open(filename, 'rb') as fp:
                    buf = fp.read() # HTML 파일을 읽어서 저장
            except IOError:
                return []
            s_count = 1 # Script 개수
            i_count = 1 # iframe 개수
            p_count = 1 # PHP 개수
            for obj in self.p_script.finditer(buf): # init 함수에서 정의한 스크립트 추출 정규표현식 패턴을 가져옴
                t = obj.group() # 정규표현식으로 추출된 결과
                p = t.lower() # 소문자로 변환
                if p.find('<script') != -1: # 추출된 스크립트 영역에서 <script 가 존재할 경우
                    file_scan_list.append(['arc_html', 'HTML/Script #%d' % s_count]) # 압축 엔진 ID와 압축 파일 정보(압축 파일이 아니므로 존재하지 않으므로 임의로 설정)리스트에 등록
                    s_count += 1 # 개수 카운트
                elif p.find('<iframe') != -1: # 추출된 스크립트 영역에서 <iframe 가 존재할 경우
                    file_scan_list.append(['arc_html', 'HTML/IFrame #%d' % i_count]) # 압축 엔진 ID와 압축 파일 정보(압축 파일이 아니므로 존재하지 않으므로 임의로 설정)리스트에 등록
                    i_count += 1 # 개수 카운트
                elif p.find('<?') != -1: # 추출된 스크립트 영역에서 <? 가 존재할 경우(PHP 스크립트)
                    file_scan_list.append(['arc_html', 'HTML/PHP #%d' % p_count]) # 압축 엔진 ID와 압축 파일 정보(압축 파일이 아니므로 존재하지 않으므로 임의로 설정)리스트에 등록
                    p_count += 1 # 개수 카운트
        return file_scan_list # 리스트 반환

    # ---------------------------------------------------------------------
    # unarc(self, arc_engine_id, arc_name, fname_in_arc)
    # 입력값 : arc_engine_id - 압축 엔진 ID
    #         arc_name      - 압축 파일
    #         fname_in_arc  - 압축 해제할 파일 이름(실제 압축 파일이 아니므로 임의의 문자열로 대신함)
    # 리턴값 : 압축 해제된 내용 or None
    # ---------------------------------------------------------------------
    def unarc(self, arc_engine_id, arc_name, fname_in_arc):
        if arc_engine_id == 'arc_html': # 압축 엔진 ID가 arc_html 일 경우
            buf = ''
            try:
                with open(arc_name, 'rb') as fp:
                    buf = fp.read() # HTML 파일을 읽어서 저장
            except IOError:
                return None
            s_count = 1 # Script 개수
            i_count = 1 # iframe 개수
            p_count = 1 # PHP 개수
            for obj in self.p_script.finditer(buf): # init 함수에서 정의한 스크립트 추출 정규표현식 패턴을 가져옴
                t = obj.group() # 정규표현식으로 추출된 결과
                pos = obj.span() # 위치 정보
                p = t.lower() # 소문자로 변환
                if p.find('<script') != -1: # 추출된 스크립트 영역에서 <script 가 존재할 경우
                    k = 'HTML/Script #%d' % s_count # 압축 해제 문자열 저장
                    s_count += 1 # 개수 카운트
                elif p.find('<iframe') != -1: # 추출된 스크립트 영역에서 <iframe 가 존재할 경우
                    k = 'HTML/IFrame #%d' % i_count # 압축 해제 문자열 저장
                    i_count += 1 # 개수 카운트
                elif p.find('<?') != -1: # 추출된 스크립트 영역에서 <? 가 존재할 경우(PHP 스크립트)
                    k = 'HTML/PHP #%d' % p_count # 압축 해제 문자열 저장
                    p_count += 1 # 개수 카운트
                else:
                    k = ''
                if k == fname_in_arc: # 만들어진 문자열이 압축 해제를 요청하는 파일 목록 이름과 같을 경우
                    data = buf[pos[0]:pos[1]] # 위치 정보를 이용해서 영역 추출
                    return data
        return None

    # ---------------------------------------------------------------------
    # getinfo(self)
    # 플러그인 엔진의 주요 정보를 알려준다. (제작자, 버전, ...)
    # 리턴값 : 플러그인 엔진 정보
    # ---------------------------------------------------------------------
    def getinfo(self):
        info = dict()
        info['author'] = 'MINE' # 제작자
        info['version'] = '1.0' # 버전
        info['title'] = 'HTML Engine' # 엔진 설명
        info['kmd_name'] = 'html' # 엔진 파일 이름
        return info

    # ---------------------------------------------------------------------
    # uninit(self)
    # 플러그인 엔진을 종료한다.
    # 리턴값 : 0 - 성공, 0 이외의 값 - 실패
    # ---------------------------------------------------------------------
    def uninit(self):
        return 0 # 플러그인 엔진 종료 성공
