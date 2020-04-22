#-*- coding: utf-8 -*-
import time,subprocess 
from _winreg import *

def main():
    try:
        varSubKey="SYSTEM\CurrentControlSet\services\SharedAccess\Parameters\FirewallPolicy"
        varStd="\StandardProfile" # 홈,회사 네트워크
        varPub="\PublicProfile" # 공용 네트워크
        varReg=ConnectRegistry(None, HKEY_LOCAL_MACHINE)
        
        #홈,회사 네트워크 방화벽 사용해제 
        varKey=CreateKey(varReg, varSubKey+varStd)
        SetValueEx(varKey, "EnableFirewall", 0, REG_DWORD, 0)
        CloseKey(varKey)
        
        #공용 네트워크 방화벽 사용해제
        varKey=CreateKey(varReg, varSubKey+varPub)
        SetValueEx(varKey, "EnableFirewall", 0, REG_DWORD, 0)
        CloseKey(varKey)
        
        CloseKey(varReg)
        
        #변경한 레지스트리 값 적용을 위한 재부팅
        subprocess.call("shutdown -r -t 1", shell=True)
    except Exception, e:
        print "[-] ", e  
        time.sleep(30)
        exit(0)

if __name__=="__main__":
    main()