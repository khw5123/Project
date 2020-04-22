#-*- coding: utf-8 -*-
import time
from _winreg import *

def findUser(fp):
    try:
        varSubKey="SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList"  # 서브 레지스트리 목록 지정
        varReg=ConnectRegistry(None, HKEY_LOCAL_MACHINE) # 루트 레지스트리 핸들 객체 얻음
        varKey=OpenKey(varReg, varSubKey) # 레지스트리 핸들 객체 얻음
        count=1
        for i in range(1024):
            keyname=EnumKey(varKey, i) # 지정한 레지스트리에 포함된 하위 키 목록 조회
            varSubKey2="%s\\%s" % (varSubKey, keyname) # 하위 키까지의 서브 레지스트리 목록
            varKey2=OpenKey(varReg, varSubKey2) # 최종적인 레지스트리 핸들 객체 얻음
            for j in range(1024):
                try:
                    n,v,t=EnumValue(varKey2, j) # 레지스트리에 등록된 이름, 데이터형, 데이터 조회
                    if("ProfileImagePath" in n and "Users" in v):
                        account=v.split('\\')
                        print "[+] Account "+str(count)+" : "+account[-1] #계정 이름 정보가 담긴 데이터 출력
                        fp.write("[+] Account "+str(count)+" : "+account[-1]+"\n")
                        count+=1
                except Exception, e:
                    pass
            CloseKey(varKey2)
        CloseKey(varKey)
        CloseKey(varReg)   
    except Exception, e:
        pass  

def findURL(fp):
    try:
        urlSubKey="Software\Microsoft\Internet Explorer\TypedURLs"
        urlReg=ConnectRegistry(None, HKEY_CURRENT_USER)
        urlKey=OpenKey(urlReg, urlSubKey)
        for i in range(1024):
            try:
                a,b,c=EnumValue(urlKey, i)
                count=i+1
                print "[+] Access URL "+str(count)+" : "+b
                fp.write("[+] Access URL "+str(count)+" : "+b+"\n")
            except Exception, e:
                pass
        CloseKey(urlKey)
        CloseKey(urlReg)
    except Exception, e:
        pass

def main():
    try:
        saveFile=raw_input("Input Save File : ")
        fp=open(saveFile, "w")
        findUser(fp)
        findURL(fp)
        fp.close()
        print "\n[+] Open the "+saveFile
        time.sleep(30)
    except Exception, e:
        print "[-] ", e
        time.sleep(30)
        exit(0)
    
if __name__=="__main__":
    main()