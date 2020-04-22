#-*- coding: utf-8 -*-
from scapy.all import *

def scan(sourceIP, destinationIP, destinationPort, flag):
    ip=IP(src=sourceIP, dst=destinationIP) # ip 패킷 정의
    tcp=TCP(sport=34567, dport=destinationPort, flags=flag, seq=12345) # tcp 패킷 정의
    packet=ip/tcp # ip 패킷 + tcp 패킷
    p=sr1(packet, inter=1) # 패킷을 한번 전송 후 응답내용 반환
    p.show() # 전달받은 패킷을 계층구조로 출력
    if(flag=="S"): # SYN Half Open Scan 의 경우 대상 포트가 열려있을 경우 RST을 전달해 로그를 남기지 않게 한다.
        rst=TCP(sport=34567, dport=destinationPort, flags="R", seq=12347)
        rstPacket=ip/rst
        rp=sr1(rstPacket)
        rp.show()
        
def main():
    sourceIP=raw_input("Input Source IP : ")
    destinationIP=raw_input("Input Destination IP : ")
    destinationPort=raw_input("Input Destination Port : ")
    flag=raw_input("Input flag(S, F, A) : ")
    scan(sourceIP, destinationIP, int(destinationPort), flag)
    
if __name__=="__main__":
    main()