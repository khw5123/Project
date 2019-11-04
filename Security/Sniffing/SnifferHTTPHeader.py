import socket
from scapy.all import *

def sniffer(pkt):
    try:
        raw=pkt.sprintf('%Raw.load%')
        if "GET " in raw:
            if "Cookie: " in raw:
                print "----------------------------------------------------------------"
                print raw
        if "HTTP/1.1 " in raw:
            if "Set-Cookie: " in raw:
                print "----------------------------------------------------------------"
                print raw
    except Exception, e:
        pass
    
def main():
    try:
        interface=raw_input("Input Interface : ")
        conf.iface=interface
        sniff(filter='tcp port 80', prn=sniffer, store=0)
    except Exception, e:
        print "[-] ", e
        exit(0)
        
if __name__=='__main__':
    main()
'''
import socket
from scapy.all import *

def sniffer(pkt):
    raw=pkt.sprintf('%Raw.load%')
    print "----------------------------------------------------------------"
    print str(raw)

def main():
    try:
        interface=raw_input("Input Interface : ")
        conf.iface=interface
        sniff(filter='tcp', prn=sniffer, store=0)
    except Exception, e:
        print "[-] ", e
        exit(0)
        
if __name__=='__main__':
    main()
'''