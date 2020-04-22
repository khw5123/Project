#-*- coding: utf-8 -*-
import time, nmap
from datetime import datetime
    
hostList=[]  
    
def PortScan(nm,saveFile):
    fp=open(saveFile,"a")
    for host in nm.all_hosts(): # nm.scan() 함수에 저장된 호스트의 정보를 얻는다.
        print "-------------------------------", str(datetime.now()) ,"-------------------------------"
        fp.write("-------------------------------"+str(datetime.now())+"-------------------------------\n")
        print 'Host : {0} {1}'.format(host, nm[host].hostname()) # IP, 이름 출력
        fp.write('Host : {0} {1}'.format(host, nm[host].hostname()))
        print 'State : {0}'.format(nm[host].state()) # 호스트가 서비스 중이라면 up 출력
        fp.write('State : {0}'.format(nm[host].state())+"\n")
        for proto in nm[host].all_protocols(): # 스캔된 프로토콜 정보를 얻는다.
            print('Protocol : {0}'.format(proto)) # 프로토콜 종류 출력
            fp.write('Protocol : {0}'.format(proto)+"\n")
            lport=list(nm[host][proto].keys()) # 프로토콜별로 열린 포트 반환
            lport.sort()
            for port in lport: 
                print('Port : {0}\tInformation : {1}'.format(port, nm[host][proto][port])) # 열린 포트의 세부정보 출력
                fp.write('Port : {0}\tInformation : {1}'.format(port, nm[host][proto][port])+"\n")
    fp.close()
    
def main():
    try:
        sel=raw_input("1. One Host 2. Multiple Host : ")
        saveFile=raw_input("Input Save File : ")
        if(sel=="1"):
            targetHost=raw_input("Input IP : ")
            targetPorts=raw_input("Input Port Scope(Use '-' Symbol) : ")
            print "Wait..."
            nm=nmap.PortScanner()
            nm.scan(targetHost, targetPorts) # scan(IP, 포트, nmap 옵션)
            PortScan(nm, saveFile)
        elif(sel=="2"):
            targetHosts=raw_input("Input Multiple IP(Separated by space) : ")
            targetPorts=raw_input("Input Port Scope(Use '-' Symbol) : ")
            print "Wait..."
            targetHosts=targetHosts.split(' ')
            for targetHost in targetHosts:
                hostList.append(targetHost) 
            nm=nmap.PortScanner()
            for host in hostList:
                nm.scan(host, targetPorts)
                PortScan(nm, saveFile)
        print "\n[+] Open the "+saveFile
        time.sleep(60) 
    except Exception, e:
        print "\n[-] ", e 
        time.sleep(60)
        exit(0)

if __name__ =="__main__":
    main()