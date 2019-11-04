# -*- coding:utf-8 -*-
import zipfile
import kernel

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
    # format(self, filehandle, filename)
    # 파일 포맷을 분석한다.
    # 입력값 : filehandle - 파일 핸들
    #         filename   - 파일 이름
    # 리턴값 : {파일 포맷 분석 정보} or None
    # ---------------------------------------------------------------------
    def format(self, filehandle, filename):
        fileformat = {} # 포맷 정보를 담을 공간
        mm = filehandle
        if mm[0:4] == 'PK\x03\x04': # ZIP 파일 시그니처 체크
            fileformat['size'] = len(mm) # ZIP 파일 크기 정보 저장
            ret = {'ff_zip' : format} # ff_zip 을 키로 하는 딕셔너리 자료형에 저장. arclist 함수에서 ff_zip 을 보고 ZIP 파일임을 알 수 있음
            return ret # 파일 포맷 분석 정보 반환
        return None

    # ---------------------------------------------------------------------
    # arclist(self, filename, fileformat)
    # 압축 파일 내부의 파일 목록을 얻는다.
    # 입력값 : filename   - 파일 이름
    #         fileformat - 파일 포맷 분석 정보
    # 리턴값 : [[압축 엔진 ID, 압축된 파일 이름]]
    # ---------------------------------------------------------------------
    def arclist(self, filename, fileformat):
        file_scan_list = [] # 압축 엔진과 압축된 파일 이름이 저장될 리스트
        if 'ff_zip' in fileformat: # 미리 분석된 파일 포맷중에 ZIP 포맷이 있을 경우
            zfile = zipfile.ZipFile(filename) # ZIP 파일 내부 목록 저장
            for name in zfile.namelist():
                file_scan_list.append(['arc_zip', name]) # 얻은 파일 목록을 한 개씩 압축 엔진 정보인 arc_zip 과 함께 리스트에 저장. unarc 함수에서 arc_zip 을 보고 ZIP 파일에서 추출된 파일임을 확신함
            zfile.close()
        return file_scan_list # 리스트 반환

    # ---------------------------------------------------------------------
    # unarc(self, arc_engine_id, arc_name, fname_in_arc)
    # 압축 파일 내부에 존재하는 악성코드를 검사하기 위해서 압축을 해제한다.
    # 입력값 : arc_engine_id - 압축 엔진 ID
    #         arc_name      - 압축 파일
    #         fname_in_arc  - 압축 해제할 파일 이름
    # 리턴값 : 압축 해제된 내용 or None
    # ---------------------------------------------------------------------
    def unarc(self, arc_engine_id, arc_name, fname_in_arc):
        if arc_engine_id == 'arc_zip': # 압축 엔진 ID가 arc_zip 일 경우
            zfile = zipfile.ZipFile(arc_name)
            data = zfile.read(fname_in_arc) # 압축 해제한 내용 저장
            zfile.close()
            return data # 압축 해제된 내용 반환
        return None

    # ---------------------------------------------------------------------
    # mkarc(self, arc_engine_id, arc_name, file_infos)
    # 입력값 : arc_engine_id - 압축 가능 엔진 ID
    #         arc_name      - 최종적으로 압축될 압축 파일 이름
    #         file_infos    - 압축 대상 파일 정보 구조체
    # 리턴값 : 압축 성공 여부 (True or False)
    # ---------------------------------------------------------------------
    def mkarc(self, arc_engine_id, arc_name, file_infos):
        if arc_engine_id == 'arc_zip': # 압축 가능 대상일 경우
            zfile = zipfile.ZipFile(arc_name, 'w')
            for file_info in file_infos: # 파일 정보 구조체
                rname = file_info.get_filename() # 검사 대상 파일 저장
                try:
                    with open(rname, 'rb') as fp:
                        buf = fp.read() # 해당 파일을 읽음
                        a_name = file_info.get_filename_in_archive() # 압축 해제 대상 파일 이름 저장
                        zfile.writestr(a_name, buf) # 압축 해제 대상 파일 이름으로 압축 진행
                except IOError:
                    pass
            zfile.close()
            return True
        return False

    # ---------------------------------------------------------------------
    # getinfo(self)
    # 플러그인 엔진의 주요 정보를 알려준다. (제작자, 버전, ...)
    # 리턴값 : 플러그인 엔진 정보
    # ---------------------------------------------------------------------
    def getinfo(self):
        info = dict()
        info['author'] = 'MINE' # 제작자
        info['version'] = '1.0' # 버전
        info['title'] = 'Zip Archive Engine' # 엔진 설명
        info['kmd_name'] = 'zip' # 엔진 파일 이름
        info['engine_type'] = kernel.ARCHIVE_ENGINE # 엔진 타입
        return info

    # ---------------------------------------------------------------------
    # uninit(self)
    # 플러그인 엔진을 종료한다.
    # 리턴값 : 0 - 성공, 0 이외의 값 - 실패
    # ---------------------------------------------------------------------
    def uninit(self):
        return 0 # 플러그인 엔진 종료 성공
