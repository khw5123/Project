import subprocess, socket
from scapy.all import *

wireList=[]

def snifferDot11(p):
    try:
        if(p.haslayer(Dot11ProbeResp)):  
            BSSID=p.getlayer(Dot11).addr2
            SSID=p.getlayer(Dot11ProbeResp).info
            if BSSID not in wireList:
                print "SSID : ", SSID, "\tBSSID : ", BSSID
                wireList.append(BSSID)
        if p.haslayer(Dot11Beacon):
            if(p.getlayer(Dot11Beacon).info==""):
                BSSID=p.getlayer(Dot11).addr2
                if BSSID not in wireList:
                    print "BSSID of Hidden SSID : ", BSSID
                    wireList.append(BSSID)
    except Exception, e:
        print "[-] ", e
        pass

def main():
    try:
        interface=raw_input("Input Ineterface : ")
        moniterMode="airmon-ng start "+interface
        subprocess.call(moniterMode, shell=True)
        sniff(iface=interface, prn=snifferDot11)
    except Exception, e:
        print "[-] ", e
        pass
    
if __name__=="__main__":
    main()