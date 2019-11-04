# -*- coding:utf-8 -*-
import os

class KavMain:
    # ---------------------------------------------------------------------
    # init(self, plugins_path)
    # 플러그인 엔진을 초기화 한다.
    # 입력값 : plugins_path - 플러그인 엔진의 위치
    # 리턴값 : 0 - 성공, 0 이외의 값 - 실패
    # ---------------------------------------------------------------------
    def init(self, plugins_path):
        return 0 # 플러그인 엔진 초기화 성공

    # ---------------------------------------------------------------------
    # arclist(self, filename, fileformat)
    # 압축 파일 내부의 파일 목록을 얻는다.
    # 입력값 : filename   - 파일 이름
    #         fileformat - 파일 포맷 분석 정보
    # 리턴값 : [[압축 엔진 ID, 압축된 파일 이름(압축 파일이 아니므로 존재하지 않으므로 임의로 설정)]]
    # ---------------------------------------------------------------------
    def arclist(self, filename, fileformat):
        file_scan_list = [] # 검사 대상의 압축 엔진 ID 및 임의의 문자열이 저장될 리스트
        if 'ff_attach' in fileformat: # format 함수에 의해 분석된 ff_attach 정보가 있을 경우
            pos = fileformat['ff_attach']['Attached_Pos'] # PE 파일 뒤쪽 추가 정보(악성코드로 많이 활용)의 위치 저장
            file_scan_list.append(['arc_attach:%d' % pos, 'Attached']) # 압축 엔진 ID와 압축 파일 정보(압축 파일이 아니므로 존재하지 않으므로 임의로 설정)리스트에 등록
        return file_scan_list # 리스트 반환

    # ---------------------------------------------------------------------
    # unarc(self, arc_engine_id, arc_name, fname_in_arc)
    # 입력값 : arc_engine_id - 압축 엔진 ID
    #         arc_name      - 압축 파일
    #         fname_in_arc  - 압축 해제할 파일 이름
    # 리턴값 : 압축 해제된 내용 or None
    # ---------------------------------------------------------------------
    def unarc(self, arc_engine_id, arc_name, fname_in_arc):
        if arc_engine_id.find('arc_attach:') != -1: # 압축 해제 엔진 ID 중에서 arc_attach 가 존재할 경우
            pos = int(arc_engine_id[len('arc_attach:'):]) # Attached_Pos 정보를 추출해서 PE 파일 뒤쪽 추가 정보(악성코드로 많이 활용)의 위치 저장
            try:
                with open(arc_name, 'rb') as fp:
                    fp.seek(pos) # Attached_Pos 위치로 이동
                    data = fp.read() # PE 파일 뒤쪽 추가 정보(악성코드로 많이 활용) 저장
                    # print data # 테스트용 출력
            except IOError:
                return None
            return data # PE 파일 뒤쪽 추가 정보(악성코드로 많이 활용) 반환
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
        info['title'] = 'Attach Engine' # 엔진 설명
        info['kmd_name'] = 'attach' # 엔진 파일 이름
        return info

    # ----------------------------------------------------------------------
    # uninit(self)
    # 플러그인 엔진을 종료한다.
    # 리턴값 : 0 - 성공, 0 이외의 값 - 실패
    # ----------------------------------------------------------------------
    def uninit(self):
        return 0 # 플러그인 엔진 종료 성공
