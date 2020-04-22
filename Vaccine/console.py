#-*- coding: utf-8 -*-
import os
import sys
import urllib
import hashlib
import types
installDirectory = 'D:\\Python\\Workspace\\vaccine\\myWorkspace' # 백신 설치 디렉터리
kernelDirectory = installDirectory + os.sep + 'engine\\kavcore' # 백신 커널 디렉터리
pluginDirectory = installDirectory + os.sep + 'engine\\plugins' # 플러그인 엔진 디렉터리
sys.path.insert(0, kernelDirectory)
import Engine
from ctypes import windll, Structure, c_short, c_ushort, byref
from optparse import OptionParser
import glob
import shutil
import psutil
import email
import json
import cgi
import csv
import cgi
import HTMLParser
import xml.etree.cElementTree as ET

KAV_VERSION = '1.0' # 프로그램 버전
KAV_BUILDDATE = 'June 19 2018' # 빌드 날짜
KAV_LASTYEAR = KAV_BUILDDATE[len(KAV_BUILDDATE)-4:]

# 악성코드 치료를 지시하는 상수로 scan 콜백 함수에서 리턴 값으로 사용
K2_ACTION_IGNORE = 0
K2_ACTION_DISINFECT = 1
K2_ACTION_DELETE = 2
K2_ACTION_QUIT = 3

g_options = None # 옵션

FOREGROUND_BLACK = 0x0000
FOREGROUND_BLUE = 0x0001
FOREGROUND_GREEN = 0x0002
FOREGROUND_CYAN = 0x0003
FOREGROUND_RED = 0x0004
FOREGROUND_MAGENTA = 0x0005
FOREGROUND_YELLOW = 0x0006
FOREGROUND_GREY = 0x0007
FOREGROUND_INTENSITY = 0x0008 # 색깔 진하게

BACKGROUND_BLACK = 0x0000
BACKGROUND_BLUE = 0x0010
BACKGROUND_GREEN = 0x0020
BACKGROUND_CYAN = 0x0030
BACKGROUND_RED = 0x0040
BACKGROUND_MAGENTA = 0x0050
BACKGROUND_YELLOW = 0x00060
BACKGROUND_GREY = 0x0070
BACKGROUND_INTENSITY = 0x0080

SHORT = c_short
WORD = c_ushort

class Coord(Structure):
    _fields_ = [("X", SHORT),
                ("Y", SHORT)]

class SmallRect(Structure):
    _fields_ = [("Left", SHORT),
                ("Top", SHORT),
                ("Right", SHORT),
                ("Bottom", SHORT)]

class ConsoleScreenBufferInfo(Structure):
    _fields_ = [("dwSize", Coord),
                ("dwCursorPosition", Coord),
                ("wAttributes", WORD),
                ("srWindow", SmallRect),
                ("dwMaximumWindowSize", Coord)]

STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
STD_ERROR_HANDLE = -12

stdout_handle = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
SetConsoleTextAttribute = windll.kernel32.SetConsoleTextAttribute
GetConsoleScreenBufferInfo = windll.kernel32.GetConsoleScreenBufferInfo

def get_text_attr():
    csbi = ConsoleScreenBufferInfo()
    GetConsoleScreenBufferInfo(stdout_handle, byref(csbi))
    return csbi.wAttributes

def set_text_attr(color):
    SetConsoleTextAttribute(stdout_handle, color)

def cprint(msg, color): # 새로 정의한 출력 함수
    default_colors = get_text_attr()
    default_bg = default_colors & 0x00F0
    set_text_attr(color | default_bg)
    sys.stdout.write(msg) # 텍스트 출력
    set_text_attr(default_colors)
    sys.stdout.flush()

def print_error(msg): # 에러 출력 함수
    cprint('Error: ', FOREGROUND_RED | FOREGROUND_INTENSITY)
    print (msg)

def print_k2logo(): # 로고 출력 함수
    logo = '\nAnti-Virus (for %s) Ver %s (%s)\nCopyright (C) 2018-%s MINE. All rights reserved.\n'
    s = logo % (sys.platform.upper(), KAV_VERSION, KAV_BUILDDATE, KAV_LASTYEAR)
    cprint(s, FOREGROUND_GREEN | FOREGROUND_BLUE | FOREGROUND_INTENSITY) # 출력(두 번째 파라미터는 색깔)

# optparse 모듈의 OptionParser 클래스를 상속 받아서 새롭게 변경(파이썬에서 제공하는 optparse 모듈은 커맨드라인으로 입력되는 옵션을 체크할 수 있는데,
# 여러 옵션들을 상황에 맞게 추가하거나 수정하기 어려워서 임의로 변경해서 사용하기 위한 목적)
class OptionParsingError(RuntimeError):
    def __init__(self, msg):
        self.msg = msg

class OptionParsingExit(Exception):
    def __init__(self, status, msg):
        self.msg = msg
        self.status = status

class ModifiedOptionParser(OptionParser):
    def error(self, msg):
        raise OptionParsingError(msg)
    def exit(self, status=0, msg=None):
        raise OptionParsingExit(status, msg)

def define_options(): # 백신 옵션 정의 함수
    usage = "Usage: %prog path[s] [options]"
    parser = ModifiedOptionParser(add_help_option=False, usage=usage)
    parser.add_option("-f", "--files", action="store_true", dest="opt_files", default=True)
    parser.add_option("-r", "--arc", action="store_true", dest="opt_arc", default=False)
    parser.add_option("-I", "--list", action="store_true", dest="opt_list", default=False)
    parser.add_option("-V", "--vlist", action="store_true", dest="opt_vlist", default=False)
    parser.add_option("-p", "--prompt", action="store_true", dest="opt_prompt", default=False)
    parser.add_option("-d", "--dis", action="store_true", dest="opt_dis", default=False)
    parser.add_option("-l", "--del", action="store_true", dest="opt_del", default=False)
    parser.add_option("", "--sigtool", action="store_true", dest="opt_sigtool", default=False)
    parser.add_option("", "--update", action="store_true", dest="opt_update", default=False)
    parser.add_option("-?", "--help", action="store_true", dest="opt_help", default=False)
    return parser

def parser_options(): # 백신 옵션 분석 함수
    parser = define_options() # 백신 옵션 정의
    if len(sys.argv) < 2:
        return 'NONE_OPTION', None
    else:
        try:
            (options, args) = parser.parse_args()
            if len(args) == 0:
                return options, None
        except OptionParsingError, e: # 옵션을 잘못 사용했을 경우
            return 'ILLEGAL_OPTION', e.msg
        except OptionParsingExit, e:
            return 'ILLEGAL_OPTION', e.msg
        return options, args

def print_usage(): # 백신 사용법 출력 함수
    print '\nUsage: .exe [options] path[s]'

def print_options(): # 백신 옵션 출력 함수
    options_string = '''Options:
        -f,  --files           scan files *
        -r,  --arc             scan archives
        -I,  --list            display all files
        -V,  --vlist           display virus list
        -p,  --prompt          prompt for action
        -d,  --dis             disinfect files
        -l,  --del             delete infected files
             --sigtool         make files for malware signatures
             --update          update
        -?,  --help            this help
                               * = default option'''
    print options_string

def convert_display_filename(real_filename): # 악성코드 결과를 한 줄에 출력하기 위한 함수
    fsencoding = sys.getfilesystemencoding() or sys.getdefaultencoding()
    if isinstance(real_filename, types.UnicodeType):
        display_filename = real_filename.encode(sys.stdout.encoding, 'replace')
    else:
        display_filename = unicode(real_filename, fsencoding).encode(sys.stdout.encoding, 'replace')
    return display_filename

def display_line(filename, message, message_color): # 악성 파일 출력 함수
    filename += ' '
    filename = convert_display_filename(filename)
    len_fname = len(filename)
    len_msg = len(message)
    if len_fname + 1 + len_msg < 79:
        fname = '%s' % filename
    else:
        able_size = 79 - len_msg
        able_size -= 5  # ...
        min_size = able_size / 2
        if able_size % 2 == 0:
            fname1 = filename[:min_size-1]
        else:
            fname1 = filename[:min_size]
        fname2 = filename[len_fname - min_size:]
        fname = '%s ... %s' % (fname1, fname2)
    cprint(fname + ' ', FOREGROUND_GREY)
    cprint(message + '\n', message_color)

def print_result(result): # 악성코드 검사 결과 출력 함수 
    cprint('\nResults:\n', FOREGROUND_GREEN | FOREGROUND_INTENSITY)
    cprint('Folders           :%d\n' % result['Folders'], FOREGROUND_BLUE | FOREGROUND_INTENSITY)
    cprint('Files             :%d\n' % result['Files'], FOREGROUND_CYAN | FOREGROUND_INTENSITY)
    cprint('Packed            :%d\n' % result['Packed'], FOREGROUND_YELLOW | FOREGROUND_INTENSITY)
    cprint('Infected files    :%d\n' % result['Infected_files'], FOREGROUND_RED | FOREGROUND_INTENSITY)
    cprint('Identified viruses:%d\n' % result['Identified_viruses'], FOREGROUND_MAGENTA | FOREGROUND_INTENSITY)
    cprint('I/O errors        :%d\n\n' % result['IO_errors'], FOREGROUND_GREY | FOREGROUND_INTENSITY)

def getch(): # 한 글자를 입력 받는 함수
    if os.name == 'nt':
        import msvcrt
        return msvcrt.getch()
    else:
        import tty
        import termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

def update_vaccine(): # 백신 업데이트 함수
    print ''
    try:
        url = 'http://localhost/' # 백신 업데이트(배포) 서버
        down_list = get_download_list(url) # 업데이트해야 할 파일 목록 얻음
        while len(down_list) != 0:
            filename = down_list.pop(0)
            download_file(url, filename, hook) # 파일 한개씩 업데이트(업데이트 서버에 있는 업데이트할 파일들의 위치는 'url / update.cfg 에 있는 경로를 포함한 파일명' 에 존재해야 한다. mkcfg.py 에서 파일명을 구성할 때 경로는 engine\kavcore 와 engine\plugins 로 설정했다.)
        # 업데이트 완료 메시지 출력
        cprint('\n[', FOREGROUND_GREY)
        cprint('Update complete', FOREGROUND_GREEN)
        cprint(']\n\n', FOREGROUND_GREY)
        # 업데이트 설정 파일 삭제
        os.remove('update.cfg')
    except KeyboardInterrupt:
        cprint('\n[', FOREGROUND_GREY)
        cprint('Update Stop', FOREGROUND_GREY | FOREGROUND_INTENSITY)
        cprint(']\n\n', FOREGROUND_GREY)
    except Exception ,e:
        print '[-]', e
        cprint('\n[', FOREGROUND_GREY)
        cprint('Update faild', FOREGROUND_RED | FOREGROUND_INTENSITY)
        cprint(']\n\n', FOREGROUND_GREY)

def get_download_list(url): # 업데이트 해야 할 파일의 목록을 구하는 함수
    down_list = [] # 업데이트 리스트
    pwd = os.path.abspath('') # console.py 프로그램이 실행되고 있는 디렉터리
    download_file(url, 'update.cfg', pwd) # 업데이트 설정 파일 다운로드
    fp = open('update.cfg', 'r') # 업데이트 파일 오픈
    while True:
        line = fp.readline().strip() # 파일 한줄 읽음
        if not line:
            break
        t = line.split(' ') # 파일 해시값과 파일명 구분
        if chek_need_update(pwd + os.sep + t[1], t[0]) == 1: # 업데이트 설정 파일의 해시와 로컬 파일의 해시가 다를 경우(업데이트가 필요한 파일일 경우)
            down_list.append(t[1]) # 파일명을 업데이트 목록에 추가
    fp.close()
    return down_list # 업데이트 리스트 반환

def download_file(url, filename, fnhook=None): # 업데이트 파일을 다운로드하는 함수
    rurl = url
    rurl += filename.replace('\\', '/') # 업데이트 설정 파일에 있는 목록을 URL 주소로 변환
    pwd = os.path.abspath('') + os.sep + filename # 저장해야 할 파일의 전체 경로 구함
    if fnhook is not None:
        cprint(filename + ' ', FOREGROUND_GREY)
    urllib.urlretrieve(rurl, pwd) # 파일 다운로드
    if fnhook is not None:
        cprint(' update\n', FOREGROUND_GREEN)

def chek_need_update(file, hash): # 업데이트 설정 파일의 해시와 로컬 파일의 해시를 비교하는 함수
    try:
        # 로컬 파일의 해시를 구해서 비교
        fp = open(file, 'rb')
        data = fp.read()
        fp.close()
        s = hashlib.sha1()
        s.update(data)
        if s.hexdigest() == hash: # 업데이트 설정 파일의 해시과 로컬 파일의 해시가 같을 경우
            return 0 # 업데이트 대상 파일이 아님을 반환
    except IOError:
        pass
    return 1 # 업데이트 대상 파일임을 반환

# 업데이트 진행율 표시
def hook(blocknumber, blocksize, totalsize):
    cprint('.', FOREGROUND_GREY)

def listvirus_callback(plugin_name, vnames): # EngineInstance 클래스의 listvirus 콜백 함수
    for vname in vnames:
        print '%-50s [%s.kmd]' % (vname, plugin_name)

def scan_callback(ret_value): # EngineInstance 클래스의 scan 콜백 함수
    fs = ret_value['file_struct']
    if len(fs.get_additional_filename()) != 0:
        disp_name = '%s (%s)' % (fs.get_master_filename(), fs.get_additional_filename())
    else:
        disp_name = '%s' % (fs.get_master_filename())
    if ret_value['result']:
        state = 'infected'
        vname = ret_value['virus_name']
        message = '%s : %s' % (state, vname)
        message_color = FOREGROUND_RED | FOREGROUND_INTENSITY
    else:
        message = 'ok'
        message_color = FOREGROUND_GREY | FOREGROUND_INTENSITY
    display_line(disp_name, message, message_color)
    if g_options.opt_prompt: # 프롬프트 옵션이 설정됐을 경우
        while True and ret_value['result']: # 악성코드가 발견됐을 경우
            cprint('Disinfect/Delete/Ignore/Quit? (d/l/i/q) : ', FOREGROUND_CYAN | FOREGROUND_INTENSITY)
            ch = getch().lower()
            print ch
            if ch == 'd':
                return K2_ACTION_DISINFECT # 악성코드 치료
            elif ch == 'l':
                return K2_ACTION_DELETE # 악성코드 삭제
            elif ch == 'i':
                return K2_ACTION_IGNORE # 악성코드 치료 무시
            elif ch == 'q':
                return K2_ACTION_QUIT # 악성코드 검사 종료
    elif g_options.opt_dis: # 프롬프트 옵션이 치료 옵션일 경우
        return K2_ACTION_DISINFECT
    elif g_options.opt_del: # 프롬프트 옵션이 삭제 옵션일 경우
        return K2_ACTION_DELETE
    return K2_ACTION_IGNORE # 악성코드 치료 무시(디폴트)

def disinfect_callback(ret_value, action_type): # EngineInstance 클래스의 disinfect 콜백 함수
    fs = ret_value['file_struct']
    message = ''
    if len(fs.get_additional_filename()) != 0:
        disp_name = '%s (%s)' % (fs.get_master_filename(), fs.get_additional_filename())
    else:
        disp_name = '%s' % (fs.get_master_filename())
    if fs.is_modify(): # 악성코드 치료로 인해 파일이 수정됐을 경우
        if action_type == K2_ACTION_DISINFECT: # 악성코드 치료 옵션일 경우
            message = 'disinfected'
        elif action_type == K2_ACTION_DELETE: # 악성코드 삭제 옵션일 경우
            message = 'deleted'
        message_color = FOREGROUND_GREEN | FOREGROUND_INTENSITY
    else: # 파일이 수정되지 않았을 경우
        if action_type == K2_ACTION_DISINFECT: # 악성코드 치료 옵션일 경우
            message = 'disinfection failed'
        elif action_type == K2_ACTION_DELETE: # 악성코드 삭제 옵션일 경우
            message = 'deletion failed'
        message_color = FOREGROUND_RED | FOREGROUND_INTENSITY
    display_line(disp_name, message, message_color)

def update_callback(ret_file_info): # EngineInstance 클래스의 update 콜백 함수
    if ret_file_info.is_modify(): # 수정되었을 경우 결과 출력
        disp_name = ret_file_info.get_filename()
        message = 'updated'
        message_color = FOREGROUND_GREEN | FOREGROUND_INTENSITY
        display_line(disp_name, message, message_color)

def main():
    global g_options
    print_k2logo() # 로고 출력
    
    options, args = parser_options() # 옵션 분석
    g_options = options # 글로벌 옵션 설정
    if options == 'NONE_OPTION': # 옵션이 없을 경우
        print_usage() # 프로그램 사용법 출력
        print_options() # 옵션 출력
        return 0
    elif options == 'ILLEGAL_OPTION': # 정의되지 않은 옵션을 사용한 경우
        print_usage() # 프로그램 사용법 출력
        print 'Error: %s' % args # 에러 메시지 출력
        return 0
    if options.opt_help or not args: # 도움말 옵션을 사용했거나 인자값이 없을 경우
        if options.opt_update: # 업데이트 옵션이 있는 경우
            update_vaccine() # 업데이트 후
            return 0 # 종료
        print_usage()
        print_options()
        return 0
    if options.opt_update: # 업데이트 옵션이 있는 경우
        update_vaccine() # 업데이트
   
    k2 = Engine.Engine(debug=True) # 백신 커널 클래스 생성
    if not k2.set_plugins(pluginDirectory): # 플러그인 엔진 로딩 준비
        print_error('KICOM Anti-Virus Engine set_plugins')
        return 0
    
    kav = k2.create_instance() # 플러그인 엔진의 KavMain 인스턴스 생성
    if not kav:
        print_error('KICOM Anti-Virus Engine create_instance')
        return 0
    
    if not kav.init(): # 플러그인 엔진 초기화
        print_error('KICOM Anti-Virus Engine init')        
        return 0
    
    info = kav.get_version() # 플러그인 엔진 버전 확인
    msg = '\nLast updated %s UTC\n\n' % info.ctime()
    cprint(msg, FOREGROUND_YELLOW | FOREGROUND_INTENSITY)
    
    msg = 'Signature nubmer: %d\n\n' % kav.get_signum() # 진단/치료 가능한 악성코드 수 출력
    cprint(msg, FOREGROUND_MAGENTA | FOREGROUND_INTENSITY)
    
    kav.set_options(options) # 옵션 설정
    
    if options.opt_vlist is True:
        kav.listvirus(listvirus_callback) # 콜백 함수를 이용해 치료 가능한 악성코드 목록 확인
    else:
        if args: # 악성코드를 검사하기 위해 여러 폴더나 파일을 입력 받을 수 있음
            kav.set_result() # 악성코드 검사 결과 초기화
            for scan_path in args: # 반복문을 통해 입력받은 폴더나 파일 검사
                scan_path = os.path.abspath(scan_path)
                if os.path.exists(scan_path): # 폴더나 파일이 존재할 경우
                    kav.scan(scan_path, scan_callback, disinfect_callback, update_callback) # 악성코드 검사
                else: # 폴더나 파일이 존재하지 않을 경우
                    print_error('Invalid path: \'%s\'' % scan_path)
            ret = kav.get_result() # 악성코드 검사 결과 저장
            print_result(ret) # 악성코드 검사 결과 출력
    
    kav.uninit() # 플러그인 엔진 종료

if __name__ == '__main__':
    main()
