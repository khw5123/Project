# -*- coding:utf-8 -*-
import os
import re
import struct
import glob
import marshal
import time

handle_pattern_md5 = None  # 악성코드 패턴 핸들 (MD5 해시)
p_text = re.compile(r'[\w\s!"#$%&\'()*+,\-./:;<=>?@\[\\\]\^_`{\|}~]') # 텍스트 파일인지 확인하기 위한 정규표현식
p_md5_pattern_ext = re.compile(r'\.s(\d\d)$', re.IGNORECASE) # 악성코드 패턴 크기가 저장돼 있는 xxxx.s[id] 파일의 [id] 부분이 숫자인지 확인하기 위한 정규표현식

class PatternMD5:
    # ---------------------------------------------------------------------
    # __init__(self, plugins_path)
    # 악성코드 패턴을 초기화한다.
    # 입력값 : plugins_path - 악성코드 패턴의 위치
    # ---------------------------------------------------------------------
    def __init__(self, plugins_path):
        self.sig_sizes = {}
        self.sig_p1s = {}
        self.sig_p2s = {}
        self.sig_names = {}
        self.sig_times = {} # 메모리 관리를 위한 시간 정보
        self.plugins = plugins_path
        fl = glob.glob(os.path.join(plugins_path, '*.s??')) # 변환한 악성코드 패턴 중 악성코드 크기만을 저장한 악성코드 패턴을 로딩하기 위해 확장자가 .s[id] 인 파일을 찾음
        fl.sort()
        for name in fl:
            obj = p_md5_pattern_ext.search(name) # .s?? 부분에서 ? 부분이 숫자가 아닐 수도 있기 때문에 정규표현식을 사용하여 숫자임을 확인
            if obj:
                idx = obj.groups()[0] # 악성코드 패턴 파일 이름에서 확장자의 [id] 부분 저장
                sig_key = os.path.split(name)[1].lower().split('.')[0] # 악성코드 패턴 파일 이름에서 파일 이름 부분 저장
                sp = self.__load_sig(name) # 악성코드 패턴 로딩
                if sp is None:
                    continue
                if len(sp): # 로딩된 패턴이 있을 경우
                    if not (sig_key in self.sig_sizes): # self.sig_sizes 에 악성코드 패턴 파일 이름에서 파일 이름 부분이 저장돼 있지 않을 경우
                        self.sig_sizes[sig_key] = {} # 파일 이름 부분 저장
                    for psize in list(sp):
                        if psize in self.sig_sizes[sig_key]: # 전에 해당 크기가 등록된 적이 있을 경우
                            self.sig_sizes[sig_key][psize].append(idx) # 해당 크기에 [id] 저장
                        else: # 전에 해당 크기가 등록된 적이 없을 경우
                            self.sig_sizes[sig_key][psize] = [idx] # 새롭게 만들고 [id] 저장
        
    # ---------------------------------------------------------------------
    # __load_sig(self, fname)
    # 악성코드 패턴을 로딩한다.
    # 입력값 : fname - 악성코드 패틴 파일 이름
    # 리턴값 : 악성코드 패턴 자료 구조
    # ---------------------------------------------------------------------
    def __load_sig(self, fname):
        try:
            data = open(fname, 'rb').read()
            if data[0:4] == 'KAVS': # 악성코드 패턴 파일의 헤더 체크(sigtool_md5.py 의 save_signature 함수에서 설정한 것임)
                sp = marshal.loads(data[12:]) # 헤더(4Byte) + 악성코드 패턴 개수(4Byte) + 날짜(2Byte) + 시간(2Byte) = 12Byte 를 제외한 데이터 읽음
                return sp
        except Exception, e:
            return None

    # ---------------------------------------------------------------------
    # scan(self, sig_key, sig_size, sig_md5)
    # 악성코드 패턴을 검사한다.
    # 입력값 : sig_key  - 지정한 악성코드 패턴
    #         sig_size - 크기
    #         sig_md5  - MD5
    # 리턴값 : 발견한 악성코드 이름
    # ---------------------------------------------------------------------
    def scan(self, sig_key, sig_size, sig_md5):
        sig_key = sig_key.lower() # 대문자로 입력될 가능성 때문에 모두 소문자로 변환
        if self.match_size(sig_key, sig_size): # 악성코드 패턴에 해당 크기가 존재할 경우
            idxs = self.sig_sizes[sig_key][sig_size] # 어떤 파일에 1차 패턴이 존재하는지 확인
            fmd5 = sig_md5.decode('hex') # MD5를 텍스트에서 바이너리로 변경
            sig_p1 = fmd5[:6] # 1차 패턴
            sig_p2 = fmd5[6:] # 2차 패턴
            for idx in idxs:
                # 1차 패턴 비교 진행
                if self.__load_sig_ex(self.sig_p1s, 'i', sig_key, idx) is False: # 1차 패턴이 로딩되어 있지 않을 경우 메모리에 로딩
                    continue
                if sig_p1 in self.sig_p1s[sig_key][idx]: # 로딩된 악성코드 패턴에 MD5 해시값의 1차 패턴이 존재할 경우
                    p2_offs = self.sig_p1s[sig_key][idx][sig_p1]
                    # 2차 패턴 비교 진행
                    if self.__load_sig_ex(self.sig_p2s, 'c', sig_key, idx) is False: # 2차 패턴이 로딩되어 있지 않을 경우 메모리에 로딩
                        continue
                    for off in p2_offs: # 2차 패턴이 존재하는 여러 개의 위치가 있을 수 있으므로 반복문을 통해 처리
                        if self.sig_p2s[sig_key][idx][off] == sig_p2: # 2차 패턴이 존재할 경우
                            if self.__load_sig_ex(self.sig_names, 'n', sig_key, idx) is False: # 악성코드 이름 패턴이 로딩되어 있지 않을 경우 메모리에 로딩
                                continue
                            return self.sig_names[sig_key][idx][off] # 악성코드 이름 반환
        self.__save_mem() # 메모리 용량을 낮추기 위해 오랫동안 사용되지 않은 악성코드 패턴을 메모리에서 제거
        return None

    # ---------------------------------------------------------------------
    # match_size(self, sig_key, sig_size)
    # 지정한 악성코드 패턴을 해당 크기가 존재하는지 확인한다.
    # 입력값 : sig_key  - 지정한 악성코드 패턴
    #         sig_size - 크기
    # 리턴값 : 악성코드 패턴 내부에 해당 크기가 존재하는지 여부 (True or False)
    # ---------------------------------------------------------------------
    def match_size(self, sig_key, sig_size):
        sig_key = sig_key.lower() # 대문자로 입력될 가능성 때문에 모두 소문자로 변환
        if sig_key in self.sig_sizes: # sig_key 가 로딩되어 있을 경우
            if sig_size in self.sig_sizes[sig_key]: # 악성코드 패턴에 해당 크기가 존재할 경우
                return True
        return False

    # ---------------------------------------------------------------------
    # __load_sig_ex(self, sig_dict, sig_prefix, sig_key, idx)
    # 악성코드 패턴을 로딩한다.
    # 단, 어떤 자료구조에 로딩되는지의 여부도 결정할 수 있다.
    # 입력값 : sig_dict   - 악성코드 패틴이 로딩될 자료 구조
    #         sig_prefix - 악성코드 패턴 이름 중 확장자 prefix
    #         sig_key    - 악성코드 패턴 이름 중 파일 이름
    #         idx        - 악성코드 패턴 이름 중 확장자 번호
    # 리턴값 : 악성코드 패턴 로딩 성공 여부
    # ---------------------------------------------------------------------
    def __load_sig_ex(self, sig_dict, sig_prefix, sig_key, idx):
        if not (sig_key in sig_dict) or not (idx in sig_dict[sig_key]):
            # 패턴 로딩
            try:
                name_fname = os.path.join(self.plugins, '%s.%s%s' % (sig_key, sig_prefix, idx)) # 악성코드 패턴 파일
                sp = self.__load_sig(name_fname) # 악성코드 패턴 로딩
                if sp is None:
                    return False
            except IOError:
                return False
            sig_dict[sig_key] = {idx: sp}
        # 현재 시간을 sig_time 에 기록
        if not (sig_key in self.sig_times):
            self.sig_times[sig_key] = {}
        if not (sig_prefix in self.sig_times[sig_key]):
            self.sig_times[sig_key][sig_prefix] = {}
        self.sig_times[sig_key][sig_prefix][idx] = time.time() # 현재 시간 저장
        return True

    # ---------------------------------------------------------------------
    # __save_mem(self)
    # 오랫동안 사용하지 않은 악성코드 패턴을 메모리에서 제거한다.
    # ---------------------------------------------------------------------
    def __save_mem(self):
        n = time.time() # 현재 시간 저장
        for sig_key in self.sig_times.keys():
            for sig_prefix in self.sig_times[sig_key].keys():
                for idx in self.sig_times[sig_key][sig_prefix].keys():
                    if n - self.sig_times[sig_key][sig_prefix][idx] > (3 * 60): # 3분 이상 지났을 경우
                        # 악성코드 패턴을 메모리에서 제거
                        if sig_prefix == 'i': # 1차 패턴일 경우
                            self.sig_p1s[sig_key].pop(idx)
                        elif sig_prefix == 'c':  # 2차 패턴일 경우
                            self.sig_p2s[sig_key].pop(idx)
                        elif sig_prefix == 'n':  # 악성코드 이름 패턴일 경우
                            self.sig_names[sig_key].pop(idx)
                        self.sig_times[sig_key][sig_prefix].pop(idx) # 시간 제거

    # ---------------------------------------------------------------------
    # get_sig_num(self, sig_key)
    # 주어진 sig_key에 해당하는 악성코드 패턴의 누적된 수를 알려준다.
    # 입력값 : sig_key - 악성코드 패턴 파일 이름
    # 리턴값 : 악성코드 패턴 수
    # ---------------------------------------------------------------------
    def get_sig_num(self, sig_key):
        sig_num = 0
        fl = glob.glob(self.plugins + os.sep + '%s.n??' % sig_key)
        for fname in fl:
            try:
                buf = open(fname, 'rb').read(12)
                if buf[0:4] == 'KAVS':
                    sig_num += struct.unpack('<L', buf[4:4+4])[0]
            except IOError:
                return None
        return sig_num

class KavMain:
    # ---------------------------------------------------------------------
    # init(self, plugins_path)
    # 플러그인 엔진을 초기화 한다.
    # 입력값 : plugins_path - 플러그인 엔진의 위치
    # 리턴값 : 0 - 성공, 0 이외의 값 - 실패
    # ---------------------------------------------------------------------
    def init(self, plugins_path):
        global handle_pattern_md5
        handle_pattern_md5 = PatternMD5(plugins_path) # 악성코드 패턴 초기화
        return 0 # 플러그인 엔진 초기화 성공

    # ---------------------------------------------------------------------
    # getinfo(self)
    # 플러그인 엔진의 주요 정보를 알려준다. (제작자, 버전, ...)
    # 리턴값 : 플러그인 엔진 정보
    # ---------------------------------------------------------------------
    def getinfo(self):
        info = dict()
        info['author'] = 'MINE' # 제작자
        info['version'] = '1.0'  # 버전
        info['title'] = 'Utility Library' # 엔진 설명
        info['kmd_name'] = 'kavutil' # 엔진 파일 이름
        return info

    # ---------------------------------------------------------------------
    # uninit(self)
    # 플러그인 엔진을 종료한다.
    # 리턴값 : 0 - 성공, 0 이외의 값 - 실패
    # ---------------------------------------------------------------------
    def uninit(self):
        return 0 # 플러그인 엔진 종료 성공
