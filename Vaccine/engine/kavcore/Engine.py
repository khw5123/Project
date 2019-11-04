# -*- coding:utf-8 -*-
import os
import sys
import imp
import StringIO
import datetime
import types
import mmap
import glob
import re
import shutil
import struct
import zipfile
import tempfile
import MakeRSAKey
import KmdFile
import FileInfo

installDirectory = 'D:\\Python\\Workspace\\vaccine\\myWorkspace' # 백신 설치 디렉터리
pluginDirectory = installDirectory + os.sep + 'engine\\plugins' # 플러그인 엔진 디렉터리
publicKey = 'key.pkr' # 공개키 파일명
pulginPriorityFile = 'PluginEnginePriority.kmd' # 암호화된 플러그인 우선순위 파일명

# 악성코드 치료를 지시하는 상수로 scan 콜백 함수에서 리턴 값으로 사용
K2_ACTION_IGNORE = 0
K2_ACTION_DISINFECT = 1
K2_ACTION_DELETE = 2
K2_ACTION_QUIT = 3

class Engine:
    # ---------------------------------------------------------------------
    # __init__(self, debug=False)
    # 클래스를 초기화 한다.
    # 인자값 : debug - 디버그 여부
    # ---------------------------------------------------------------------
    def __init__(self, debug=False):
        self.debug = debug # 디버깅 여부
        self.plugins_path = None # 플러그인 디렉터리
        self.kmdfiles = [] # 플러그인 엔진 로딩 우선순위 목록(암호화된 플러그인 파일명(xxxx.kmd)이 저장됨)
        self.kmd_modules = [] # 메모리에 로딩된 모듈(플러그인 엔진)
        self.max_datetime = datetime.datetime(1980, 1, 1, 0, 0, 0, 0) # 플러그인 엔진이 최근 실행된 시간(백신의 최종 업데이트 시간 값)
        
    # ---------------------------------------------------------------------
    # set_plugins(self, plugins_path)
    # 주어진 경로에서 플러그인 엔진을 로딩 준비한다.
    # 인자값 : plugins_path - 플러그인 엔진 경로
    # 리턴값 : 성공 여부
    # ---------------------------------------------------------------------
    def set_plugins(self, plugins_path):
        self.plugins_path = plugins_path # 플러그인 디렉터리 저장
        pu = MakeRSAKey.read_key(plugins_path + os.sep + publicKey) # 공개키 로딩
        if not pu:
            return False
        ret = self.__get_kmd_list(plugins_path + os.sep + pulginPriorityFile, pu) # 플러그인 엔진 우선순위 파일 로딩
        if not ret:
            return False
        if self.debug:
            tmp = None
            # print '\n[*] '+pulginPriorityFile+':'
            # print '\t', self.kmdfiles
        for kmd_name in self.kmdfiles: # 우선순위대로 KMD 파일 로딩
            kmd_path = plugins_path + os.sep + kmd_name
            k = KmdFile.KMD(kmd_path, pu) # 암호화된 플러그인 파일(xxxx.kmd) 복호화
            module = KmdFile.load(kmd_name.split('.')[0], k.body) # 복호화된 코드 메모리에 로딩
            if module: # 메모리 로딩에 성공했을 경우
                self.kmd_modules.append(module) # 메모리 로딩에 성공한 모듈(플러그인 엔진) 추가
                self.__get_last_kmd_build_time(k) # 메모리 로딩에 성공한 모듈(플러그 엔진)의 시간 값 읽기(최신 업데이트 날짜)
        # 악성코드 패턴에서 최신 시간 값을 얻음
        fl = glob.glob(plugins_path + os.sep + '*.n??') # 플러그인 엔진 로딩이 끝난 후 확장자가 .n[id] 인 파일(악성코드 패턴 파일)을 찾음
        for fname in fl:
            try:
                buf = open(fname, 'rb').read(12) # 찾은 파일의 첫 12Byte(헤더(4Byte) + 악성코드 패턴 개수(4Byte) + 날짜(2Byte) + 시간(2Byte)) 만 읽음
                if buf[0:4] == 'KAVS': # 헤더가 KAVS 일 경우
                    sdate = KmdFile.convert_date(struct.unpack('<H', buf[8:10])[0]) # 날짜 저장
                    stime = KmdFile.convert_time(struct.unpack('<H', buf[10:12])[0]) # 시간 저장
                    t_datetime = datetime.datetime(sdate[0], sdate[1], sdate[2], stime[0], stime[1], stime[2])
                    if self.max_datetime < t_datetime: # 읽은 날짜와 시간 값이 최신 값일 경우
                        self.max_datetime = t_datetime # 최신 백신 업데이트 날짜 갱신
            except IOError:
                pass
        if self.debug:
            tmp = None
            # print '\n[*] kmd_modules:'
            # print '\t', self.kmd_modules
            # print '\n[*] Last updated %s UTC' % self.max_datetime.ctime()
        return True

    # ---------------------------------------------------------------------
    # __get_kmd_list(self, kicom_kmd_file, pu)
    # 플러그인 엔진의 로딩 우선순위를 알아낸다.
    # 인자값 : kicom_kmd_file - kicom.kmd 파일의 전체 경로
    #         pu             - 공개키
    # 리턴값 : 성공 여부
    # ---------------------------------------------------------------------
    def __get_kmd_list(self, priority_kmd_file, pu):
        kmdfiles = [] # 플러그인 엔진 우선순위 임시 목록
        k = KmdFile.KMD(priority_kmd_file, pu) # 암호화된 플러그인 엔진 우선순위 파일 복호화
        lst_data = k.body
        if lst_data: # 암호화된 플러그인 엔진 우선순위 파일이 복호화돼서 읽혔을 경우
            msg = StringIO.StringIO(lst_data) # 플러그인 엔진 우선순위 파일 내용 저장
            while True:
                line = msg.readline().strip() # 플러그인 엔진 우선순위 파일 내용 한 줄(플러그인 엔진 파일명) 저장
                if not line: # 읽혀진 내용이 없을 경우
                    break # 종료
                elif line.find('.kmd') != -1: # KMD 확장자가 존재할 경우
                    kmdfiles.append(line) # 플러그인 엔진 로딩 우선순위 임시 목록에 추가
                else: # 확장자가 KMD가 아닐 경우
                    continue
        if len(kmdfiles): # 우선순위 임시 목록이 있을 경우
            self.kmdfiles = kmdfiles # 임시 목록을 진짜 목록에 저장
            return True
        else: # 우선순위 임시 목록이 없을 경우
            return False

    # ---------------------------------------------------------------------
    # __get_last_kmd_build_time(self, kmd_info)
    # 복호화 된 플러그인 엔진의 빌드 시간 값 중 최신 값을 보관한다.
    # 입력값 : kmd_info - 복호화 된 플러그인 엔진 정보
    # ---------------------------------------------------------------------
    def __get_last_kmd_build_time(self, kmd_info):
        d_y, d_m, d_d = kmd_info.date
        t_h, t_m, t_s = kmd_info.time
        t_datetime = datetime.datetime(d_y, d_m, d_d, t_h, t_m, t_s)
        if self.max_datetime < t_datetime:
            self.max_datetime = t_datetime

    # ---------------------------------------------------------------------
    # create_instance(self)
    # 백신 엔진의 인스턴스를 생성한다.
    # ---------------------------------------------------------------------
    def create_instance(self):
        ei = EngineInstance(self.plugins_path, self.max_datetime, self.debug) # EngineInstance 인스턴스 생성
        if ei.create(self.kmd_modules): # 플러그인 엔진의 KavMain 인스턴스 생성
            return ei # 플러그인 엔진의 KavMain 인스턴스 반환
        else:
            return None

class EngineInstance:
    # ---------------------------------------------------------------------
    # __init__(self, plugins_path, max_datetime, debug=False)
    # 클래스를 초기화 한다.
    # 인자값 : plugins_path - 플러그인 엔진 경로
    #         max_datetime - 플러그인 엔진의 최신 시간 값
    #         debug        - 디버그 여부
    # ---------------------------------------------------------------------
    def __init__(self, plugins_path, max_datetime, debug=False):
        self.debug = debug # 디버깅 여부
        self.plugins_path = plugins_path # 플러그인 경로
        self.max_datetime = max_datetime # 플러그인 엔진의 가장 최신 시간 값
        self.options = {} # 옵션
        self.set_options() # 기본 옵션 설정
        self.kavmain_inst = [] # 모든 플러그인 엔진의 KavMain 인스턴스 목록
        self.update_info = []  # 압축 파일 최종 치료를 위한 압축 리스트
        self.result = {} # 악성코드 검사 결과
        self.identified_virus = set() # 감염된 파일들의 악성코드 종류의 개수를 구하기 위해 사용(identified_virus의 멤버 변수를 파이썬의 set 함수를 이용해 초기화)
        self.set_result() # 악성코드 검사 결과 초기화

    # ---------------------------------------------------------------------
    # create(self, kmd_modules)
    # 백신 엔진의 인스턴스를 생성한다.
    # 인자값 : kmd_modules - 메모리에 로딩된 KMD 모듈 리스트
    # 리턴값 : 성공 여부
    # ---------------------------------------------------------------------
    def create(self, kmd_modules):
        for mod in kmd_modules: # 메모리에 로딩이 성공한 모듈(플러그인 엔진) 개수만큼 반복
            try:
                t = mod.KavMain() # 각 플러그인 엔진의 KavMain 인스턴스 생성
                self.kavmain_inst.append(t) # 생성된 KavMain 인스턴스를 KavMain 인스턴스 목록에 추가
            except AttributeError: # KavMain 클래스 존재하지 않음
                continue
        if len(self.kavmain_inst): # KavMain 인스턴스가 있을 경우
            if self.debug:
                tmp = None
                # print '\n[*] Count of KavMain : %d' % (len(self.kavmain_inst)) # 생성된 KavMain 인스턴스 개수 출력
            return True
        else:
            return False

    # ---------------------------------------------------------------------
    # init(self)
    # 플러그인 엔진 전체를 초기화한다.
    # 리턴값 : 성공 여부
    # ---------------------------------------------------------------------
    def init(self):
        # 플러그인 엔진(KavMain 인스턴스) 내 init 멤버함수를 실행해서 초기화 성공이 확인 될 때까지 self.kavmain_instk 목록의 KavMain 인스턴스는 최종 인스턴스가 아님
        t_kavmain_inst = [] # 최종 인스턴스 임시 리스트
        if self.debug:
            tmp = None
            # print '\n[*] KavMain.init() :'
        for inst in self.kavmain_inst: # 생성된 KavMain 인스턴스 개수만큼 반복
            try:
                ret = inst.init(self.plugins_path) # 플러그인 엔진(KavMain 인스턴스)에 있는 init 멤버함수 호출
                if not ret: # 플러그인 엔진(KavMain 인스턴스)의 init 멤버함수 호출이 성공했을 경우
                    t_kavmain_inst.append(inst) # KavMain 인스턴스를 최종 인스턴스 임시 리스트에 추가
                    if self.debug:
                        tmp = None
                        # print '\t[-] %s.init() : %d' % (inst.__module__, ret)
            except Exception, e:
                continue
        self.kavmain_inst = t_kavmain_inst # 임시 목록을 진짜 목록에 저장
        if len(self.kavmain_inst): # KavMain 인스턴스가 있을 경우
            if self.debug:
                tmp = None
                # print '\n[*] Count of KavMain.init() : %d' % (len(self.kavmain_inst))
            return True
        else:
            return False

    # ---------------------------------------------------------------------
    # listvirus(self, *callback)
    # 플러그인 엔진이 진단/치료 할 수 있는 악성코드 목록을 얻는다.
    # 입력값 : callback - 콜백함수 (생략 가능)
    # 리턴값 : 악성코드 목록 (콜백함수 사용시 아무런 값도 없음)
    # ---------------------------------------------------------------------
    def listvirus(self, *callback):
        # 계속 악성코드 패턴이 추가되면 엄청나게 많은 악성코드에 대한 플러그인 엔진이 생기게 되는데 하나의 변수에 전체 악성코드 목록을 저장하는 것이 무리여서
        # 저장하지 말고 콜백함수로 목록을 전달해서 목적에 맞게(출력 등) 사용. 만약 콜백함수가 없으면 변수에 악성코드 목록 저장
        vlist = [] # 진단/치료 가능한 악성코드 목록
        argc = len(callback) # 가변인자 확인
        if argc == 0: # 인자가 없는 경우
            cb_fn = None
        elif argc == 1: # callback 함수가 존재할 경우
            cb_fn = callback[0] # 콜백 함수 저장
        else: # 인자가 너무 많을 경우
            return []
        if self.debug:
            tmp = None
            # print '[*] KavMain.listvirus() :'
        for inst in self.kavmain_inst:
            try:
                ret = inst.listvirus()
                if isinstance(cb_fn, types.FunctionType): # callback 함수가 있다면 callback 함수 호출
                    cb_fn(inst.__module__, ret)
                else: # callback 함수가 없으면 악성코드 목록을 누적 저장하여 리턴
                    vlist += ret
                if self.debug:
                    # print '\t[-] %s.listvirus() :' % inst.__module__
                    for vname in ret:
                        print '\t   - %s\n' % vname
            except AttributeError:
                continue
        return vlist

    # -----------------------------------------------------------------
    # set_result(self)
    # 백신 엔진의 악성코드 검사 결과를 초기화 한다.
    # -----------------------------------------------------------------
    def set_result(self):
        self.result['Folders'] = 0 # 폴더 수
        self.result['Files'] = 0 # 파일 수
        self.result['Packed'] = 0 # 압축 파일 수
        self.result['Infected_files'] = 0 # 발견된 전체 악성코드 수        
        self.result['Identified_viruses'] = 0 # 발견된 악성코드 종류의 수
        self.result['Disinfected_files'] = 0 # 치료한 파일 수
        self.result['Deleted_files'] = 0 # 삭제한 파일 수
        self.result['IO_errors'] = 0 # 파일 입출력 에러 발생 수

    # -----------------------------------------------------------------
    # get_result(self)
    # 백신 엔진의 악성코드 검사 결과를 얻는다.
    # 리턴값 : 악성코드 검사 결과
    # -----------------------------------------------------------------
    def get_result(self):
        self.result['Identified_viruses'] = len(self.identified_virus) # 발견된 악성코드 종류의 개수 저장
        return self.result

    # ---------------------------------------------------------------------
    # scan(self, filename, *callback)
    # 플러그인 엔진에게 악성코드 검사를 요청한다.
    # 입력값 : filename - 악성코드 검사 대상 파일 또는 폴더 이름
    #         callback - 검사 시 출력 화면 관련 콜백 함수
    # 리턴값 : 0 - 성공
    #         1 - Ctrl+C를 이용해서 악성코드 검사 강제 종료
    #        -1 - 콜백 함수가 너무 많음
    # ---------------------------------------------------------------------
    def scan(self, filename, *callback):
        scan_callback_fn = None # 악성코드 검사 콜백 함수
        disinfect_callback_fn = None # 악성코드 치료 콜백 함수
        update_callback_fn = None # 악성코드 압축 최종 치료 콜백 함수
        # 악성코드 검사 결과(콜백 함수에게 전달해줄 결과의 형태)
        ret_value = {
            'filename': '', # 파일 이름
            'file_struct': '', # 파일 이름
            'result': False, # 악성코드 발견 여부
            'virus_name': '', # 발견된 악성코드 이름
            'virus_id': -1, # 악성코드 ID
            'engine_id': -1 # 악성코드를 발견한 플러그인 엔진 ID
        }
        try:
            scan_callback_fn = callback[0] # 콜백 함수 저장
            disinfect_callback_fn = callback[1]
            update_callback_fn = callback[2]
        except IndexError:
            pass
        file_info = FileInfo.FileStruct(filename) # 파일 정보 클래스에 검사 대상 파일 등록
        file_scan_list = [file_info] # 악성코드 검사 대상 폴더 및 파일이 저장될 리스트
        while len(file_scan_list):
            try:
                t_file_info = file_scan_list.pop(0) # 검사 대상 파일 하나를 가짐
                real_name = t_file_info.get_filename() # 실제 검사 대상 파일 저장
                if os.path.isdir(real_name): # 검사 대상이 폴더인 경우 내부 파일리스트만 검사 대상 리스트에 등록
                    if real_name[-1] == os.sep:
                        real_name = real_name[:-1] # 폴더 등을 처리할 때를 위해 뒤에 붙는 os.sep는 우선 제거
                    # 콜백 호출 또는 검사 리턴값 생성
                    ret_value['result'] = False # 폴더이므로 악성코드 없음
                    ret_value['filename'] = real_name # 검사 파일 이름
                    ret_value['file_struct'] = t_file_info # 검사 파일 이름
                    self.result['Folders'] += 1 # 폴더 개수 카운트
                    if self.options['opt_list']: # 모든 리스트 출력 옵션일 경우
                        if isinstance(scan_callback_fn, types.FunctionType): # 콜백 함수가 존재할 경우
                            scan_callback_fn(ret_value) # 콜백 함수 호출
                    # 폴더 안의 파일들을 악성코드 검사 대상 리스트에 추가
                    flist = glob.glob(real_name + os.sep + '*')
                    tmp_flist = []
                    for rfname in flist:
                        tmp_info = FileInfo.FileStruct(rfname)
                        tmp_flist.append(tmp_info)
                    file_scan_list = tmp_flist + file_scan_list
                elif os.path.isfile(real_name) or t_file_info.is_archive(): # 검사 대상이 파일 또는 압축 해제 대상인 경우
                    self.result['Files'] += 1 # 파일 개수 카운트
                    ret = self.unarc(t_file_info) # 압축 해제
                    if ret: # 압축 해제 결과물이 존재할 경우
                        t_file_info = ret # 파일 정보 교체
                    ff = self.format(t_file_info) # 파일 포맷 분석
                    ret, vname, mid, eid = self.__scan_file(t_file_info, ff) # 악성코드 검사
                    if ret: # 해당 파일이 악성코드일 경우
                        self.result['Infected_files'] += 1 # 발견된 악성코드 개수 카운트
                        self.identified_virus.update([vname]) # 악성코드 이름 추가(update 함수를 통해 중복 제거)
                    # 콜백 호출 또는 검사 리턴값 생성
                    ret_value['result'] = ret # 악성코드 발견 여부
                    ret_value['engine_id'] = eid # 엔진 ID
                    ret_value['virus_name'] = vname # 악성코드 이름
                    ret_value['virus_id'] = mid # 악성코드 ID
                    ret_value['file_struct'] = t_file_info # 검사 파일 이름
                    if ret_value['result']: # 악성코드를 발견했을 경우
                        if isinstance(scan_callback_fn, types.FunctionType): # 콜백 함수가 존재할 경우
                            action_type = scan_callback_fn(ret_value) # 콜백 함수 호출
                            if action_type == K2_ACTION_QUIT: # 종료 타입일 경우
                                return 0 # 백신 커널의 악성코드 검사 종료
                            self.__disinfect_process(ret_value, disinfect_callback_fn, action_type) # scan 콜백 함수의 리턴값에 따라 악성코드 치료
                    else:
                        if self.options['opt_list']: # 모든 리스트 출력 옵션일 경우
                            if isinstance(scan_callback_fn, types.FunctionType): # 콜백 함수가 존재할 경우
                                scan_callback_fn(ret_value) # 콜백 함수 호출
                    self.__update_process(t_file_info, update_callback_fn) # 압축 파일 최종 치료
                    if not ret: # 해당 파일이 악성코드가 아닐 경우
                        arc_file_list = self.arclist(t_file_info, ff) # 압축 파일 내부 파일 얻음
                        if len(arc_file_list): # 압축 파일인 경우
                            file_scan_list = arc_file_list + file_scan_list # 악성코드 검사 대상 리스트에 추가
            except KeyboardInterrupt:
                return 1 # 키보드 종료
        self.__update_process(None, update_callback_fn, True) # 최종 파일 정리
        return 0 # 정상적으로 검사 종료

    # ---------------------------------------------------------------------
    # __scan_file(self, file_struct, fileformat)
    # 플러그인 엔진에게 악성코드 검사를 요청한다.
    # 입력값 : file_struct - 압축 해제 대상 파일 정보
    #         fileformat  - 미리 분석한 파일 포맷 분석 정보
    # 리턴값 : (악성코드 발견 유무, 악성코드 이름, 악성코드 ID, 악성코드 검사 상태, 플러그인 엔진 ID(악성코드를 발견한 플러그인 엔진의 인덱스))
    # ---------------------------------------------------------------------
    def __scan_file(self, file_struct, fileformat):
        if self.debug:
            tmp = None
            # print '[*] KavMain.scan() :'
        fp = None
        mm = None
        try:
            ret = False
            vname = ''
            mid = -1
            eid = -1
            filename = file_struct.get_filename() # 검사 대상 파일 이름 추출
            filename_ex = file_struct.get_additional_filename() # 압축 파일 내부 파일명
            if os.path.getsize(filename) == 0: # 파일 크기가 0일 경우(검사할 필요 없음)
                return False, '', -1, -1
            fp = open(filename, 'rb')
            mm = mmap.mmap(fp.fileno(), 0, access=mmap.ACCESS_READ) # 입출력 속도를 높이기 위해 운영체제에서 지원하는 캐시 기능 이용(mmap)
            for i, inst in enumerate(self.kavmain_inst):
                try:
                    ret, vname, mid = inst.scan(mm, filename, fileformat, filename_ex)
                    if ret: # 악성코드 발견 시 추가 악성코드 검사 중지
                        eid = i # 악성코드를 발견한 플러그인 엔진 ID 저장
                        if self.debug:
                            tmp = None
                            print '\t[-] %s.scan() : %s' % (inst.__module__, vname)
                        break
                except AttributeError:
                    continue
            if mm:
                mm.close()
            if fp:
                fp.close()
            return ret, vname, mid, eid # 악성코드 발견 유무, 악성코드 이름, 악성코드 ID, 악성코드를 발견한 플러그인 엔진의 인덱스 반환
        except IOError:
            self.result['IO_errors'] += 1 # 파일 입출력 에러 발생 시 카운트
        except Exception, e:
            pass
        return False, '', -1, -1

    # ---------------------------------------------------------------------
    # unarc(self, file_struct)
    # 플러그인 엔진에게 압축 해제를 요청한다.
    # 입력값 : file_struct - 압축 해제 대상 파일 정보
    # 리턴값 : 압축 해제된 파일 정보 or None
    # ---------------------------------------------------------------------
    def unarc(self, file_struct):
        rname_struct = None
        try:
            if file_struct.is_archive(): # 압축 파일인 경우
                arc_engine_id = file_struct.get_archive_engine_name() # 압축 해제 가능한 엔진 ID 저장
                arc_name = file_struct.get_archive_filename() # 실제 압축 파일 이름 저장
                name_in_arc = file_struct.get_filename_in_archive() # 압축 해제 대상 파일 이름 저장
                for inst in self.kavmain_inst:
                    try:
                        unpack_data = inst.unarc(arc_engine_id, arc_name, name_in_arc) # 압축 플러그인 엔진의 unarc 멤버 함수 호출(압축 해제)
                        if unpack_data: # 압축 해제 결과물이 있을 경우
                            rname = tempfile.mktemp(prefix='ktmp') # 임시 폴더에 파일 생성
                            fp = open(rname, 'wb')
                            fp.write(unpack_data)
                            fp.close()
                            rname_struct = file_struct
                            rname_struct.set_filename(rname) # 검사 대상 파일에 해당 임시 파일 이름 등록
                            if self.options['opt_sigtool']: # --sigtool 옵션이 있을 경우
                                # 임시 파일을 현재 폴더에 복사
                                sig_fname = os.path.split(rname)[1]
                                shutil.copy(rname, sig_fname)
                                # sigtool.log 파일 생성
                                msg = '%s : %s\n' % (sig_fname, rname_struct.get_additional_filename()) 
                                fp = open('sigtools.log', 'at')
                                fp.write(msg)
                                fp.close()
                            break # 압축이 풀렸으면 종료
                    except (AttributeError):
                        continue
                return rname_struct # 압축 해제된 파일 정보 반환
        except IOError:
            pass
        return None

    # ---------------------------------------------------------------------
    # arclist(self, file_struct, fileformat)
    # 플러그인 엔진에게 압축 파일의 내부 리스트를 요청한다.
    # 입력값 : file_struct - 압축 해제 대상 파일 정보
    #         format      - 미리 분석한 파일 포맷 분석 정보
    # 리턴값 : [압축 파일 내부 리스트] or []
    # ---------------------------------------------------------------------
    def arclist(self, file_struct, fileformat):
        sys.path.insert(0, pluginDirectory)
        import kernel
        file_scan_list = [] # 악성코드 검사 대상 파일이 저장될 리스트
        rname = file_struct.get_filename() # 실제 작업 대상 파일 이름 저장
        deep_name = file_struct.get_additional_filename() # 압축 파일 내 파일 이름 저장
        mname = file_struct.get_master_filename() # 최상위 파일 이름 저장
        level = file_struct.get_level() # 압축의 깊이 저장
        for inst in self.kavmain_inst:
            is_archive_engine = False # 압축 해제 엔진 판단 값
            try:
                ret_getinfo = inst.getinfo() # 플러그인 엔진의 getinfo 함수 호출
                if 'engine_type' in ret_getinfo: # getinfo 함수에서 해당 플러그인 엔진이 압축 해제 엔진을 의미할 경우
                    if ret_getinfo['engine_type'] == kernel.ARCHIVE_ENGINE: # getinfo 함수에서 해당 플러그인 엔진을 의미하는 상수 값이 압축 해제 엔진 상수 값과 같을 경우
                        is_archive_engine = True # 값 설정
            except AttributeError:
                pass
            try:
                arc_list = [] # 압축 파일 목록
                if self.options['opt_arc']: # 압축 검사 옵션(-r)이 있을 경우
                    arc_list = inst.arclist(rname, fileformat) # 압축 플러그인 엔진의 arclist 멤버 함수 호출(압축 파일 내부 리스트 얻음)
                    if len(arc_list) and is_archive_engine: # 압축 해제 엔진일 경우
                        self.result['Packed'] += 1 # 압축 파일 개수 카운트
                else: # 압축 검사 옵션(-r)이 없을 경우
                    if not is_archive_engine: # 압축 해제 엔진이 아닐 경우
                        arc_list = inst.arclist(rname, fileformat) # 일반 플러그인 엔진의 arclist 멤버 함수 호출
            except AttributeError:
                pass
            if len(arc_list): # 압축 리스트가 존재할 경우
                for alist in arc_list:
                    arc_id = alist[0] # 압축 엔진 ID 저장
                    name = alist[1] # 압축 파일의 내부 파일 이름 저장
                    if len(deep_name):
                        dname = '%s/%s' % (deep_name, name) # 압축 파일 내부 파일 이름 문자열
                    else:
                        dname = '%s' % name
                    fs = FileInfo.FileStruct() # 파일 정보 클래스 생성
                    fs.set_archive(arc_id, rname, name, dname, mname, False, False, level+1) # 기존 level 보다 1 증가시켜 압축 깊이가 깊어졌음을 나타냄
                    file_scan_list.append(fs) # 압축 파일 내부 리스트에 추가
        return file_scan_list # 압축 파일 내부 리스트 반환

    # ---------------------------------------------------------------------
    # format(self, file_struct)
    # 플러그인 엔진에게 파일 포맷 분석을 요청한다.
    # 입력값 : file_struct - 압축 해제 대상 파일 정보
    # 리턴값 : {파일 포맷 분석 정보} or {}
    # ---------------------------------------------------------------------
    def format(self, file_struct):
        ret = {}
        filename = file_struct.get_filename() # 실제 작업 대상 파일 이름 저장
        try:
            fp = open(filename, 'rb')
            mm = mmap.mmap(fp.fileno(), 0, access=mmap.ACCESS_READ)
            for inst in self.kavmain_inst:
                try:
                    ff = inst.format(mm, filename) # 압축 플러그인 엔진의 format 멤버 함수 호출(파일 포맷 정보 얻음)
                    if ff:
                        ret.update(ff) # 파일 포맷 정보 추가
                except AttributeError:
                    pass
            mm.close()
            fp.close()
        except IOError:
            pass
        return ret # 파일 포맷 정보 반환

    # ---------------------------------------------------------------------
    # disinfect(self, filename, malware_id, engine_id)
    # 플러그인 엔진에게 악성코드 치료를 요청한다.
    # 입력값 : filename   - 악성코드 치료 대상 파일 이름
    #         malware_id - 감염된 악성코드 ID
    #         engine_id  - 악성코드를 발견한 플러그인 엔진 ID
    # 리턴값 : 악성코드 치료 성공 여부
    # ---------------------------------------------------------------------
    def disinfect(self, filename, malware_id, engine_id):
        ret = False
        if self.debug:
            tmp = None
            # print '[*] KavMain.disinfect() :'
        try:
            inst = self.kavmain_inst[engine_id] # 악성코드를 탐지한 플러그인 엔진에게만 치료 요청
            ret = inst.disinfect(filename, malware_id)
            if self.debug:
                print '\t[-] %s.disinfect() : %s' % (inst.__module__, ret)
        except AttributeError:
            pass
        return ret

    # ---------------------------------------------------------------------
    # __disinfect_process(self, ret_value, disinfect_callback_fn, action_type)
    # 악성코드를 치료한다.
    # 입력값 : ret_value             - 악성코드 검사 결과
    #         disinfect_callback_fn - disinfect 콜백 함수
    #         action_type           - 악성코드 치료 or 삭제 처리 여부
    # 리턴값 : 치료 성공 여부 (True or False)
    # ---------------------------------------------------------------------
    def __disinfect_process(self, ret_value, disinfect_callback_fn, action_type):
        if action_type == K2_ACTION_IGNORE: # 치료 무시 옵션이 설정됐을 경우
            return False
        t_file_info = ret_value['file_struct'] # 검사 파일 정보
        mid = ret_value['virus_id'] # 악성코드 ID
        eid = ret_value['engine_id'] # 악성코드를 진단한 엔진 ID
        d_fname = t_file_info.get_filename() # 실제 파일 이름 저장
        d_ret = False # 리턴값
        if action_type == K2_ACTION_DISINFECT: # 치료 옵션이 설정됐을 경우
            d_ret = self.disinfect(d_fname, mid, eid) # disinfect 함수를 호출하여 악성코드 치료
            if d_ret: # 치료에 성공했을 경우
                self.result['Disinfected_files'] += 1 # 치료 파일 수 카운트
        elif action_type == K2_ACTION_DELETE: # 삭제 옵션이 설정됐을 경우
            try:
                os.remove(d_fname) # 파일 삭제
                d_ret = True
                self.result['Deleted_files'] += 1 # 삭제 파일 수 카운트
            except IOError:
                d_ret = False
        t_file_info.set_modify(d_ret) # 악성코드 치료로 인한 파일 수정/삭제 여부 표시
        if isinstance(disinfect_callback_fn, types.FunctionType): # 콜백 함수가 존재할 경우
            disinfect_callback_fn(ret_value, action_type) # 콜백 함수 호출
        return d_ret

    # ---------------------------------------------------------------------
    # __update_process(self, file_struct, update_callback_fn, immediately_flag=False)
    # update_info를 갱신한다. 악성코드 검사 및 치료가 끝나면 해당 파일 정보 구조체는 update_info에 추가된다.
    # 압축의 깊이(level) 또는 마스터 파일(master_filename)의 변화를 체크해서 압축 파일의 재압축 여부를 판단하고 악성코드를 치료한 파일을 재압축한다.
    # 입력값 : file_struct        - 파일 정보 구조체
    #         update_callback_fn - update 콜백 함수
    #         immediately_flag   - update_info 모든 정보 갱신 여부
    # ---------------------------------------------------------------------
    def __update_process(self, file_struct, update_callback_fn, immediately_flag=False):
        # 압축 파일 정보의 재압축을 즉시하지 않고 내부 구성을 확인하여 처리
        if immediately_flag is False: # immediately_flag 값이 False 일 경우(이 값이 True 이면 즉각 update_info를 모두 정리하라는 의미임)
            if len(self.update_info) == 0: # update_info 에 아무런 파일이 없을 경우
                self.update_info.append(file_struct) # update_info 에 파일 추가
            else: # update_info 에 파일이 있을 경우
                n_file_info = file_struct # 현재 작업 파일 정보(구조체)
                p_file_info = self.update_info[-1] # 직전 파일 정보(구조체)
                if p_file_info.get_master_filename() == n_file_info.get_master_filename(): # 추가하려는 파일 정보 구조체(현재 작업 파일 정보)와 마지막에 추가된 파일 정보 구조체(직전 파일 정보)의 마스터 파일이 같을 경우
                    if p_file_info.get_level() <= n_file_info.get_level(): # 압축 깊이가 깊어질 경우(현재 파일의 level 이 이전 파일의 level 보다 크거나 같을 경우)
                        self.update_info.append(n_file_info) # update_info 에 파일 누적
                    else: # 압축 깊이가 얕아질 경우(현재 파일의 level 이 이전 파일의 level 보다 작을 경우)
                        ret_file_info = self.__update_arc_file_struct(p_file_info) # update_info 에 이미 추가된 파일 정보들을 재압축해야 하는 시점이므로 재압축 함수 호출
                        self.update_info.append(ret_file_info) # update_info 에 결과 파일 추가
                        self.update_info.append(n_file_info) # update_info 에 다음 파일 추가
                else: # 추가하려는 파일 정보 구조체(현재 작업 파일 정보)와 마지막에 추가된 파일 정보 구조체(직전 파일 정보)의 마스터 파일이 다를 경우
                    immediately_flag = True # 새로운 파일이 시작되므로 update_info 내부 모두 정리(빈 상태로)
        # 압축 파일 정보를 이용해 즉시 압축하여 최종 마스터 파일로 재조립한다.
        if immediately_flag and len(self.update_info) > 1: # immediately_flag 값이 True 이고, update_info 의 파일이 1개 이상일 경우
            ret_file_info = None
            while len(self.update_info):
                p_file_info = self.update_info[-1] # 직전 파일 정보(구조체)
                ret_file_info = self.__update_arc_file_struct(p_file_info) # 재압축 함수 호출
                if len(self.update_info): # update_info 에 파일이 있을 경우(최상위 파일이 아닐 경우)
                    self.update_info.append(ret_file_info) # 하위 결과 파일 추가
            if isinstance(update_callback_fn, types.FunctionType) and ret_file_info:
                update_callback_fn(ret_file_info) # 콜백 함수 호출

    # ---------------------------------------------------------------------
    # __update_arc_file_struct(self, p_file_info)
    # update_info 내부의 압축을 처리한다.(재압축)
    # 입력값 : p_file_info - update_info의 마지막 파일 정보 구조체
    # 리턴값 : 갱신된 파일 정보 구조체
    # ---------------------------------------------------------------------
    def __update_arc_file_struct(self, p_file_info):
        # 실제 압축 파일 이름이 같은 파일을 모두 추출한다.
        t = []
        arc_level = p_file_info.get_level() # update_info 의 마지막 파일 정보 구조체의 압축 깊이 저장
        while len(self.update_info):
            if self.update_info[-1].get_level() == arc_level:
                t.append(self.update_info.pop()) # 파일 정보 구조체를 모두 update_info 에서 빼낸 뒤 리스트 t 에 저장
            else:
                break
        t.reverse() # 파일 정보 구조체가 거꾸로 저장되어 있으므로 뒤집어서 저장
        ret_file_info = self.update_info.pop() # 리턴값이 될 파일 정보(압축 파일의 최상위 파일)를 update_info 에서 빼냄
        # 리스트 t 에 저장된 파일 정보 구조체 중 악성코드 치료로 인해 수정된 파일 정보 구조체가 있는지 탐색
        b_update = False
        for finfo in t:
            if finfo.is_modify():
                b_update = True # 수정된 파일이 있을 경우 값 설정
                break
        if b_update: # 수정된 파일이 있을 경우
            arc_name = t[0].get_archive_filename()
            arc_engine_id = t[0].get_archive_engine_name()
            for inst in self.kavmain_inst:
                try:
                    ret = inst.mkarc(arc_engine_id, arc_name, t) # 압축 플러그인 엔진의 압축 함수를 호출해 재압축 진행
                    if ret: # 최종 압축이 성공했을 경우
                        break
                except AttributeError:
                    continue
            ret_file_info.set_modify(True) # 악성코드 치료로 인한 파일 수정 여부 저장
        for tmp in t: # 리스트 t 에 저장된 압축된 임시 파일들은 필요 없으니
            t_fname = tmp.get_filename()
            if os.path.exists(t_fname): # 플러그인 엔진에 의해 파일이 치료(삭제) 되었을 수 있음
                os.remove(t_fname) # 임시 폴더에서 압축된 임시 파일들 모두 삭제   
        return ret_file_info # 최상위 파일 정보 구조체 반환

    # ---------------------------------------------------------------------
    # uninit(self)
    # 플러그인 엔진 전체를 종료한다.
    # ---------------------------------------------------------------------
    def uninit(self):
        if self.debug:
            tmp = None
            # print '\n[*] KavMain.uninit() :'
        for inst in self.kavmain_inst:
            try:
                ret = inst.uninit()
                if self.debug:
                    tmp = None
                    # print '\t[-] %s.uninit() : %d' % (inst.__module__, ret)
            except AttributeError:
                continue

    # ---------------------------------------------------------------------
    # getinfo(self)
    # 플러그인 엔진 정보를 얻는다.
    # 리턴값 : 플러그인 엔진 정보 리스트
    # ---------------------------------------------------------------------
    def getinfo(self):
        ginfo = [] # 플러그인 엔진 정보
        if self.debug:
            tmp = None
            # print '[*] KavMain.getinfo() :'
        for inst in self.kavmain_inst:
            try:
                ret = inst.getinfo()
                ginfo.append(ret) # 플러그인 엔진의 정보 추가
                if self.debug:
                    print '\t[-] %s.getinfo() :' % inst.__module__
                    for key in ret.keys():
                        print '\t   - %-10s : %s' % (key, ret[key])
            except AttributeError:
                continue
        return ginfo # 전체 플러그인 엔진의 정보 반환

    # ---------------------------------------------------------------------
    # getversion(self)
    # 전체 플러그인 엔진의 최신 버전 정보를 전달한다.
    # 리턴값 : 최신 버전 정보
    # ---------------------------------------------------------------------
    def get_version(self):
        return self.max_datetime

    # -----------------------------------------------------------------
    # get_signum(self)
    # 백신 엔진이 진단/치료 가능한 악성코드 수를 얻는다.
    # 리턴값 : 진단/치료 가능한 악성코드 수
    # -----------------------------------------------------------------
    def get_signum(self):
        signum = 0 # 진단/치료 가능한 악성코드 수
        for inst in self.kavmain_inst:
            try:
                ret = inst.getinfo() # 플러그인 엔진의 getinfo 함수를 통해 정보(리스트) 얻음
                if 'sig_num' in ret: # 리스트에 sig_num 이 존재할 경우
                    signum += ret['sig_num'] # 플러그인 엔진 정보에 진단/치료 가능 악성코드 수 누적
            except AttributeError:
                continue
        return signum

    # ---------------------------------------------------------------------
    # set_options(self, options)
    # 옵션을 설정한다.
    # ---------------------------------------------------------------------
    def set_options(self, options=None):
        if options:
            self.options['opt_list'] = options.opt_list
            self.options['opt_arc'] = options.opt_arc
            self.options['opt_sigtool'] = options.opt_sigtool
        else: # 기본값(옵션 미 입력) 설정
            self.options['opt_list'] = False
            self.options['opt_arc'] = False
            self.options['opt_sigtool'] = False
        return True # 옵션 입력 시
