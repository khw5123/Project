#-*- coding: utf-8 -*-
import utils, sys
from pydbg import *
from pydbg.defines import *

isProcess=False
# beforeValue 변수와 afterValue 변수의 크기(길이)가 같지 않으면(변경 전 값과 변경 후 값의 길이가 같지 않으면) 버퍼를 메모리에 쓸 때 버퍼의 맨 뒤쪽이 잘리거나(변경 후 값의 길이가 클 경우), 버퍼의 맨 뒤쪽에 쓰레기값이 들어옴(변경 전 값의 길이가 클 경우)
beforeValue="" # 변경 전 값
afterValue="" # 변경 후 값

def falsification(dbg, args): # 후킹 작업을 하는 콜백 함수로 디버그 이벤트가 발생할 때 호출됨
    try:
        global beforeValue, afterValue
        buffer=dbg.read_process_memory(args[1], args[2]) # 메모리 주소를 읽어 값을 반환
        #print str(args[1])+"\n" # 버퍼의 시작 주소
        #print str(args[2])+"\n" # 버퍼의 크기
        print buffer
        if beforeValue in buffer: # 버퍼에 해당 값이 있을 경우
            buffer=buffer.replace(beforeValue, afterValue) # 값 변조
            dbg.write_process_memory(args[1], buffer) # 변조된 버퍼 메모리에 쓰기
            #print buffer+"\n" # 버퍼 출력
            print "[+] "+beforeValue+" -> "+afterValue
        return DBG_CONTINUE # 디버깅 계속 진행
    except Exception, e:
        print "[-] ", e
        return DBG_CONTINUE

def main():
    try:
        global isProcess, beforeValue, afterValue
        targetProcess=raw_input("Input Process Name( ex) notepad++.exe): ") # 타겟 프로세스명
        beforeValue=raw_input("Input Before Value : ") # 현재 설정된 값
        afterValue=raw_input("Input After Value : ") # 바꾸고 싶은 값
        funcName=raw_input("Input Win32 API Function Name( ex) WriteFile) : ") # 후킹하고자 하는 함수
        dllName=raw_input("Input Dll Name( ex) kernel32.dll) : ") # 해당 함수를 로딩한 dll
        dbg=pydbg()
        for(pid, name) in dbg.enumerate_processes(): # 현재 실행중인 모든 프로세스를 탐색
            if(name==targetProcess): # 현재 실행중인 프로세스 중에 타겟 프로세스가 있을 경우
                isProcess=True
                hooks=utils.hook_container() # 모든 후킹 객체를 담을 공간 확보
                dbg.attach(pid) # 해당 프로세스의 핸들을 얻어 클래스 내부에 저장
                print "[+] Saves a process handle in self.h_process of pid[%d]" % pid
                hookAddress=dbg.func_resolve_debuggee(dllName, funcName) # 핸들을 이용해 Win32 API 함수 주소를 찾아 반환     
                if(hookAddress): # 해당 함수 주소 반환에 성공했을 경우
                    hooks.add(dbg, hookAddress, 5, falsification, None) # 해당 함수에 중단점 설정 후 콜백함수 등록
                    print "[+] sets a breakpoint at the designated address : 0x%08x" % hookAddress
                    break
                else:
                    print "[-] couldn't resolve hook address"
                    exit(0)
        if(isProcess): # 타겟 프로세스가 실행중인 경우
            dbg.run() # 디버그 이벤트가 발생하면 콜백함수 호출
        else: # 타겟 프로세스가 종료된 경우
            print "[-] There in no process [%s]" % targetProcess
            exit(0)
    except Exception, e:
        print "[-] ", e 
        exit(0)
        
if __name__=="__main__":
    main()
