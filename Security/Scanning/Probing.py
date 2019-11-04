#-*- coding: utf-8 -*-
import subprocess, socket
from scapy.all import *

macAddress=[]

def probeSniffer(fm):
    try:
        if fm.haslayer(Dot11ProbeReq): # 프로브 요청 프레임 수집
            ssid=fm.info
            if ssid==apName :
                if fm.addr2 not in macAddress:
                    print "New Probe Request : ", ssid
                    print "Mac Address :  ", fm.addr2
                    macAddress.append(fm.addr2)
    except Exception, e:
        print "[-] ", e
        pass
    
def main():
    try:
        global apName
        interface=raw_input("Input Ineterface : ")
        apName=raw_input("Input AP Name : ")
        moniterMode="airmon-ng start "+interface
        subprocess.call(moniterMode, shell=True)
        sniff(iface=interface,prn=probeSniffer)
    except Exception, e:
        print "[-] ", e
        pass

if __name__=="__main__":
    main()