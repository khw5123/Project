#-*- coding: utf-8 -*-
import socket, subprocess
from scapy.all import *

apList=[]

def info(fm):
    try:
        if(fm.haslayer(Dot11)): # 802.1 트래픽을 뜻하는 Dot11 트래픽만 통과시킨다.
            if((fm.type == 0) & (fm.subtype==8)): # 프레임 타입이 0(관리 프레임)이고, 프레임 서브타입이 8(비콘 프레임)인 트래픽만 통과시킨다.
                if fm.addr2 not in apList:
                    apList.append(fm.addr2)
                    print "SSID : ", fm.info, "\t\tBSSID : ", fm.addr2, "\t\tChannel : ", ord(fm[Dot11Elt:3].info)
    except Exception, e:
        print "[-] ", e
        pass
    
def main():
    try:
        interface=raw_input("Input Interface Name : ")
        moniterMode="airmon-ng start "+interface
        subprocess.call(moniterMode, shell=True)
        sniff(iface=interface, prn=info)
    except Exception, e:
        print "[-] ", e
        pass
    
if __name__=="__main__":
    main()
'''
#-*- coding: utf-8 -*-
import socket, sys, os, signal    # AP Sniffer

sniff=socket.socket(socket.AF_PACKET, socket.SOCK_RAW, 3) # 세번째 파라미터의 3은 프로토콜번호중 ETH_P_ALL 이다.
sniff.bind(("ra0", 0x0003))
ap_list=[]
while(1):
    fm1=sniff.recvfrom(1000)
    fm=fm1[0] # 프레임의 첫 부분의 값을 저장
    if(fm[26]=="\x80"): # 프레임의 서브타입이 비콘 프레임을 의미하는 8비트일 경우
        if fm[36:42] not in ap_list: 
            ap_list.append(fm[36:42]) # BSSID
            a=ord(fm[63]) # SSID의 길이
            print "SSID :", fm[64:64+a], "\nBSSID : ", fm[36:42].encode("hex"), "\nChannel : ", ord(fm[64+a+12])
'''