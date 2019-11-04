# -*- coding:utf-8 -*-
import struct

#---------------------------------------------------------------
# PE 파일을 파싱하여 주요 정보를 리턴한다.
# 입력값 : mm - 파일 핸들
# 리턴값 : {PE 파일 분석 정보} or None
#---------------------------------------------------------------
def pe_parse(mm):
    pe_format = {'PE_Position': 0, 'EntryPoint': 0, 'SectionNumber': 0, 'Sections': None, 'EntryPointRaw': 0, 'FileAlignment': 0}
    try:
        if mm[0:2] != 'MZ': # MZ 로 시작하지 않을 경우
            raise ValueError
        pe_pos = struct.unpack('<L', mm[0x3c:0x3c+4])[0] # PE 시그니처 위치 알아냄(0x3c 위치로부터 4Byte에 PE 시그니처의 위치 값이 저장돼 있음)
        if mm[pe_pos:pe_pos+4] != 'PE\x00\x00': # PE 시그니처가 PE 가 아닐 경우
            raise ValueError
        pe_format['PE_Position'] = pe_pos # PE 시그니처 위치 저장
        if mm[pe_pos+0x18:pe_pos+0x18+2] != '\x0B\x01': # Optional Header의 매직넘버가 \x0B\x01 이 아닐 경우(매직넘버 위치 = PE 시그니처 위치 + 24Byte(16진수로 18))
            raise ValueError
        pe_ep = struct.unpack('<L', mm[pe_pos+0x28:pe_pos+0x28+4])[0] # Entry Point 알아냄(Entry Point 위치 = PE 시그니처 위치 + 40Byte(16진수로 28))
        pe_format['EntryPoint'] = pe_ep # Entry Point 저장
        pe_img = struct.unpack('<L', mm[pe_pos+0x34:pe_pos+0x34+4])[0] # Image Base 알아냄(Image Base 위치 = PE 시그니처 위치 + 52Byte(16진수로 34))
        pe_format['ImageBase'] = pe_img # Image Base 저장
        pe_file_align = struct.unpack('<L', mm[pe_pos+0x3c:pe_pos+0x3c+4])[0] # File Alignment 알아냄(File Alignment 위치 = PE 시그니처 위치 + 60Byte(16진수로 3c))
        pe_format['FileAlignment'] = pe_file_align # File Alignment 저장
        section_num = struct.unpack('<H', mm[pe_pos+0x6:pe_pos+0x6+2])[0] # Section 개수 알아냄(Number Of Sections 위치 = PE 시그니처 위치 + 6Byte)
        pe_format['SectionNumber'] = section_num # Section 개수 저장
        opthdr_size = struct.unpack('<H', mm[pe_pos+0x14:pe_pos+0x14+2])[0] # Optional Header 크기 알아냄(Size Of Optional Header 위치 = PE 시그니처 위치 + 20Byte(16진수로 14))
        pe_format['OptionalHeaderSize'] = opthdr_size # Optional Header 크기 저장
        section_pos = pe_pos + 0x18 + opthdr_size # 첫 번째 Section Header 의 시작 위치
        sections = [] # 모든 섹션 정보를 저장할 리스트
        for i in range(section_num): # Section 개수만큼 반복
            section = {}
            s = section_pos + (0x28 * i) # 각 Section Header 의 시작 위치(Section Header 의 크기는 40Byte(40Byte 크기의 구조체))
            section['Name'] = mm[s:s+8].replace('\x00', '') # Section 이름
            section['VirtualSize'] = struct.unpack('<L', mm[s+8:s+8+4])[0]
            section['RVA'] = struct.unpack('<L', mm[s+12:s+12+4])[0]
            section['SizeRawData'] = struct.unpack('<L', mm[s+16:s+16+4])[0]
            section['PointerRawData'] = struct.unpack('<L', mm[s+20:s+20+4])[0]
            section['Characteristics'] = struct.unpack('<L', mm[s+36:s+36+4])[0]
            sections.append(section)
            pe_format['Sections'] = sections # Section 정보 저장
            for section in sections:
                size = section['VirtualSize']
                rva = section['RVA']
                if rva <= pe_ep and pe_ep < rva + size: # Entry Point 가 속한 섹션 일 경우
                    # RVA to Offset(RAW) = Virtual Address(Entry Point) - RVA(Section 메모리 위치) + RAW(Section 파일 위치) = PointerToRawData 가 일반적인 RVA to Offset(RAW)를 구하는 공식이지만
                    # 모든 Section 의 파일에서의 위치는 File Alignment 의 배수가 돼야 하는데 그렇지 못하는 상황이 발생한다. 이때 윈도우 커널은 해당 값이 속한 File Alignment의 시작 값을 따르는데 아래의 보정된 Section 의 파일 위치가 File Alignment의 시작 값을 계산한 값이다.
                    # ex) File Alignment 값이 0x200 인데 특정 Section 의 파일 위치 값이 0x10 일 경우 해당 값은 File Alignment 의 배수가 되지 못하는데 0x0 ~ 0x200 사이의 값이므로 윈도우 커널이 섹션의 시작 값을 0x10 이 아니라 File Alignment 의 배수에 따라 0x0 으로 해석한다.
                    foff = (section['PointerRawData'] / pe_file_align) * pe_file_align # 보정된 Section 의 파일 위치 = (Section 의 파일 위치 / File Alignment) * File Alignment
                    ep_raw = pe_ep - rva + foff # RVA to Offset(RAW) = Entry Point - RVA + 보정된 Section 의 파일 위치
                    pe_format['EntryPointRaw'] = ep_raw # Entry Point 의 RAW 위치 저장
                    pe_format['EntryPoint_in_Section'] = sections.index(section) # Entry Point 가 속한 Section 저장
                    break
    except ValueError:
        return None
    return pe_format

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
        ret = {}
        pe_format = pe_parse(filehandle) # PE 파일 분석
        if pe_format is None: # PE 파일 분석 정보가 없을 경우
            return None
        fileformat['pe'] = pe_format # PE 파일 분석 정보 저장
        ret = {'ff_pe': fileformat} # ff_pe 파일 포맷 등록
        # PE 파일 뒤쪽에 추가 정보(악성코드로 많이 활용)가 있는지 검사
        pe_size = 0 # PE 파일 크기
        pe_file_align = pe_format['FileAlignment']
        for sec in pe_format['Sections']: # 각 Section 반복
            off = (sec['PointerRawData'] / pe_file_align) * pe_file_align # Section 의 시작 위치
            size = sec['SizeRawData'] # Section 의 크기
            if pe_size < off + size: # Section 의 시작 위치와 크기를 더한 값이 PE 파일의 크기보다 클 경우
                pe_size = off + size # Section 의 시작 위치와 크기를 더해서 가장 큰 값을 PE 파일의 크기로 설정
        file_size = len(filehandle) # 실제 파일 크기
        if pe_size < file_size: # 계산된 PE 파일의 크기가 실제 파일 크기보다 작을 경우 PE 파일 뒤에 추가 정보가 존재할 수 있음
            fileformat = {'Attached_Pos': pe_size}
            ret['ff_attach'] = fileformat # ff_attach 파일 포맷 등록
        return ret # PE 파일 포맷 분석 정보 반환

    # ---------------------------------------------------------------------
    # getinfo(self)
    # 플러그인 엔진의 주요 정보를 알려준다. (제작자, 버전, ...)
    # 리턴값 : 플러그인 엔진 정보
    # ---------------------------------------------------------------------
    def getinfo(self):
        info = dict()
        info['author'] = 'MINE' # 제작자
        info['version'] = '1.0' # 버전
        info['title'] = 'PE Engine' # 엔진 설명
        info['kmd_name'] = 'pe' # 엔진 파일 이름
        return info

    # ---------------------------------------------------------------------
    # uninit(self)
    # 플러그인 엔진을 종료한다.
    # 리턴값 : 0 - 성공, 0 이외의 값 - 실패
    # ---------------------------------------------------------------------
    def uninit(self):
        return 0 # 플러그인 엔진 종료 성공
