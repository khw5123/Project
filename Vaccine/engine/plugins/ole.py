# -*- coding:utf-8 -*-
import os
import sys

class KavMain:
    # ---------------------------------------------------------------------
    # init(self, plugins_path)
    # 플러그인 엔진을 초기화 한다.
    # 입력값 : plugins_path - 플러그인 엔진의 위치
    # 리턴값 : 0 - 성공, 0 이외의 값 - 실패
    # ---------------------------------------------------------------------
    def init(self, plugins_path):
        sys.path.insert(0, plugins_path + os.sep + 'oletools.xmd') # 외부 모듈 사용
        return 0 # 플러그인 엔진 초기화 성공

    # ---------------------------------------------------------------------
    # format(self, filehandle, filename)
    # 파일 포맷을 분석한다.
    # 입력값 : filehandle - 파일 핸들
    #         filename   - 파일 이름
    # 리턴값 : {파일 포맷 분석 정보} or None
    # ---------------------------------------------------------------------
    def format(self, filehandle, filename):
        ret = {}
        mm = filehandle
        if mm[:8] == '\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1': # OLE 헤더일 경우
            ret['ff_ole'] = 'OLE' # ff_ole 파일 포맷 등록
        return ret

    # ---------------------------------------------------------------------
    # arclist(self, filename, fileformat)
    # 압축 파일 내부의 파일 목록을 얻는다.
    # 입력값 : filename   - 파일 이름
    #          fileformat - 파일 포맷 분석 정보
    # 리턴값 : [[압축 엔진 ID, 압축된 파일 이름(실제 압축 파일이 아니므로 임의의 문자열로 대신함)]]
    # ---------------------------------------------------------------------
    def arclist(self, filename, fileformat):
        import oletools.thirdparty.olefile.olefile as olefile
        import oletools.olevba as vba
        file_scan_list = [] # 검사 대상의 압축 엔진 ID 및 임의의 문자열이 저장될 리스트
        if 'ff_ole' in fileformat: # format 함수에 의해 분석된 OLE 파일 포맷이 있을 경우
            # OLE Stream 목록 추출
            o = olefile.OleFileIO(filename)
            for path in o.listdir():
                name = '/'.join(path)
                if o.get_type(name) == olefile.STGTY_STREAM: # 파일인 경우
                    file_scan_list.append(['arc_ole', name])
            o.close()
            # 매크로 목록 추출
            v = vba.VBA_Parser(filename)
            if v.detect_vba_macros(): # 매크로가 존재할 경우
                macros = v.extract_all_macros() # 매크로 추출
                for macro in macros():
                    name = macro[1]
                    print name + '\n' + macro[3] + '\n'
                    file_scan_list.append(['arc_vba', name.encode('ascii', 'ignore')])
            v.close()
        elif 'ff_zip' in fileformat: # OOXML(Open Office XML) 파일 포맷일 경우
            # 매크로 목록 추출
            v = vba.VBA_Parser(filename)
            if v.detect_vba_macros(): # 매크로가 존재할 경우
                macros = v.extract_all_macros() # 매크로 추출
                for macro in macros():
                    name = macro[0] + '/' + macro[1]
                    print name + '\n' + macro[3] + '\n'
                    file_scan_list.append(['arc_vba', name.encode('ascii', 'ignore')])
            v.close()
        return file_scan_list

    # ---------------------------------------------------------------------
    # unarc(self, arc_engine_id, arc_name, fname_in_arc)
    # 입력값 : arc_engine_id - 압축 엔진 ID
    #         arc_name      - 압축 파일
    #         fname_in_arc  - 압축 해제할 파일 이름
    # 리턴값 : 압축 해제된 내용 or None
    # ---------------------------------------------------------------------
    def unarc(self, arc_engine_id, arc_name, fname_in_arc):
        import oletools.thirdparty.olefile.olefile as olefile
        import oletools.olevba as vba
        data = None
        if arc_engine_id == 'arc_ole': # 압축 해제 엔진 ID가 arc_ole 일 경우
            o = olefile.OleFileIO(arc_name)
            fp = o.openstream(fname_in_arc) # OLE 파일 내부 파일 열기
            data = fp.read() # 데이터 추출
            o.close()
            return data
        elif arc_engine_id == 'arc_vba': # 압축 해제 엔진 ID가 arc_vba 일 경우
            v = vba.VBA_Parser(arc_name)
            if v.detect_vba_macros(): # 매크로가 존재할 경우
                macros = v.extract_all_macros() # 매크로 추출
                for macro in macros():
                    if v.type == 'OLE':
                        name = macro[1]
                    elif v.type == 'OpenXML':
                        name = macro[0] + '/' + macro[1]
                    else:
                        name = 'UNKNOWN'
                    if name == fname_in_arc:
                        data = macro[3] # VBA Code
                        break
            v.close()
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
        info['title'] = 'OLE Engine' # 엔진 설명
        info['kmd_name'] = 'ole' # 엔진 파일 이름
        return info

    # ---------------------------------------------------------------------
    # uninit(self)
    # 플러그인 엔진을 종료한다.
    # 리턴값 : 0 - 성공, 0 이외의 값 - 실패
    # ---------------------------------------------------------------------
    def uninit(self):
        return 0 # 플러그인 엔진 종료 성공
