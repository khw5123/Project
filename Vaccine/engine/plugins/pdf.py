# -*- coding:utf-8 -*-
import re
import zlib

class KavMain:
    # ---------------------------------------------------------------------
    # init(self, plugins_path)
    # 플러그인 엔진을 초기화 한다.
    # 입력값 : plugins_path - 플러그인 엔진의 위치
    # 리턴값 : 0 - 성공, 0 이외의 값 - 실패
    # ---------------------------------------------------------------------
    def init(self, plugins_path):
        pat = r'^s*%PDF-1.' # PDF 헤더 정규표현식
        self.p_pdf_header = re.compile(pat, re.IGNORECASE)
        pat = r'(\d+)\s+0\s+obj\s*<<.+>>\s*?stream\s*([\d\D]+?)\s*endstream\s+endobj'
        self.p_pdf_obj = re.compile(pat, re.IGNORECASE)
        pat = '/Filter\s*/(\w+)' # /Filter 정규표현식
        self.p_pdf_filter = re.compile(pat, re.IGNORECASE)
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
        mm = filehandle
        buf = mm[:4096]
        if self.p_pdf_header.match(buf): # PDF 헤더일 경우
            ret = {'ff_pdf': 'PDF'} # ff_pdf 파일 포맷 등록
            return ret
        return None

    # ---------------------------------------------------------------------
    # arclist(self, filename, fileformat)
    # 압축 파일 내부의 파일 목록을 얻는다.
    # 입력값 : filename   - 파일 이름
    #         fileformat - 파일 포맷 분석 정보
    # 리턴값 : [[압축 엔진 ID, 압축된 파일 이름(실제 압축 파일이 아니므로 임의의 문자열로 대신함)]]
    # ---------------------------------------------------------------------
    def arclist(self, filename, fileformat):
        file_scan_list = [] # 검사 대상의 압축 엔진 ID 및 임의의 문자열이 저장될 리스트
        if 'ff_pdf' in fileformat: # format 함수에 의해 분석된 PDF 파일 포맷이 있을 경우
            buf = ''
            try:
                with open(filename, 'rb') as fp:
                    buf = fp.read()
            except IOError:
                return []
            for obj in self.p_pdf_obj.finditer(buf): # Stream 을 가진 Object 를 찾는 정규표현식으로 발견했을 경우
                obj_id = obj.groups()[0] # Stream 이 존재하는 Object 의 ID 저장
                file_scan_list.append(['arc_pdf', 'PDF #%s' % obj_id]) # 압축 파일 내부 파일 목록으로(출력용 문자열) ID 사용
        return file_scan_list # 리스트 반환
    
    # ---------------------------------------------------------------------
    # unarc(self, arc_engine_id, arc_name, fname_in_arc)
    # 입력값 : arc_engine_id - 압축 엔진 ID
    #         arc_name      - 압축 파일
    #         fname_in_arc  - 압축 해제할 파일 이름
    # 리턴값 : 압축 해제된 내용 or None
    # ---------------------------------------------------------------------
    def unarc(self, arc_engine_id, arc_name, fname_in_arc):
        if arc_engine_id == 'arc_pdf': # 압축 엔진 ID 가 arc_pdf 일 경우
            buf = ''
            try:
                with open(arc_name, 'rb') as fp:
                    buf = fp.read()
            except IOError:
                return None
            for obj in self.p_pdf_obj.finditer(buf): # Stream 을 가진 Object 를 찾는 정규표현식으로 발견했을 경우
                obj_id = obj.groups()[0] # Stream 이 존재하는 Object 의 ID 저장
                if obj_id == fname_in_arc[5:]: # 압축 해제 대상일 경우(arclist 함수에서 Stream 이 존재하는 Object ID를 PDF #n 문자열 에서 n 에 저장 했으므로 그것과 비교해서 같을 경우)
                    data = obj.groups()[1] # Stream 데이터 추출
                    t = self.p_pdf_filter.search(obj.group())
                    if (t is not None) and (t.groups()[0].lower() == 'flatedecode'): # /Filter 의 값이 FlateDecode 일 경우
                        try:
                            data = zlib.decompress(data) # zlib 로 압축 해제
                        except zlib.error:
                            pass
                    # print data # 자바스크립트 코드 출력(테스트용)
                    return data # 압축 해제 데이터 반환
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
        info['title'] = 'PDF Engine' # 엔진 설명
        info['kmd_name'] = 'pdf' # 엔진 파일 이름
        return info

    # ---------------------------------------------------------------------
    # uninit(self)
    # 플러그인 엔진을 종료한다.
    # 리턴값 : 0 - 성공, 0 이외의 값 - 실패
    # ---------------------------------------------------------------------
    def uninit(self):
        return 0 # 플러그인 엔진 종료 성공
