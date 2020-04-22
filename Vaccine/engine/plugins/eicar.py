# -*- coding:utf-8 -*-
import os
import cryptoSharedLibrary # 기존 라이브러리(hashlib) 사용 안하고 공유 라이브러러리 이용

class KavMain:
    # ---------------------------------------------------------------------
    # init(self, plugins_path)
    # 플러그인 엔진을 초기화 한다.
    # 입력값 : plugins_path - 플러그인 엔진의 위치
    # 리턴값 : 0 - 성공, 0 이외의 값 - 실패
    # ---------------------------------------------------------------------
    def init(self, plugins_path):
        self.virus_name = 'EICAR-Test-File' # 진단/치료하는 악성코드 이름
        return 0 # 플러그인 엔진 초기화 성공

    # ---------------------------------------------------------------------
    # listvirus(self)
    # 진단/치료 가능한 악성코드의 리스트를 알려준다.
    # 리턴값 : 악성코드 리스트
    # ---------------------------------------------------------------------
    def listvirus(self):
        vlist = list()
        vlist.append(self.virus_name) # 진단/치료하는 악성코드 이름 등록
        return vlist

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
            size = os.path.getsize(filename) # 검사 대상 파일 크기 구함
            if size == 68: # EICAR Test 악성코드의 크기(68Byte)와 일치할 경우
                fmd5 = cryptoSharedLibrary.md5(mm[:68]) # 공유 라이브러리를 이용해 MD5 해시 계산
                if fmd5 == '44d88612fea8a8f36de82e1278abb02f': # 파일에서 얻은 해시 값과 EICAR Test 악성코드의 해시 값이 일치할 경우
                    return True, self.virus_name, 0 # 악성코드 발견 여부, 악성코드 이름, 악성코드 ID 반환
        except IOError:
            pass
        return False, '', -1 # 악성코드를 발견하지 못했음을 반환

    # ---------------------------------------------------------------------
    # disinfect(self, filename, malware_id)
    # 악성코드를 치료한다.
    # 입력값 : filename    - 파일 이름
    #         malware_id  - 치료할 악성코드 ID
    # 리턴값 : 악성코드 치료 여부
    # ---------------------------------------------------------------------
    def disinfect(self, filename, malware_id):
        try:
            if malware_id == 0: # 악성코드 진단 결과에서 받은 ID 값이 0일 경우
                os.remove(filename) # 파일 삭제
                return True
        except IOError:
            pass
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
        info['title'] = 'EICAR Scan Engine' # 엔진 설명
        info['kmd_name'] = 'eicar' # 엔진 파일 이름
        info['sig_num'] = 1 # 진단/치료 가능한 악성코드 수
        return info

    # ---------------------------------------------------------------------
    # uninit(self)
    # 플러그인 엔진을 종료한다.
    # 리턴값 : 0 - 성공, 0 이외의 값 - 실패
    # ---------------------------------------------------------------------
    def uninit(self):
        return 0 # 플러그인 엔진 종료 성공
