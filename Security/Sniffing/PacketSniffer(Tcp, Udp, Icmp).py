#-*- coding: utf-8 -*-
import socket, os, struct, time
from ctypes import *

class IP(Structure):    
    _fields_=[ 
        ("ihl", c_ubyte, 4),
        ("version", c_ubyte, 4),
        ("tos", c_ubyte),
        ("len", c_ushort),
        ("id", c_ushort),
        ("offset", c_ushort),
        ("ttl", c_ubyte),
        ("protocol_num", c_ubyte),
        ("sum", c_ushort),
        ("src", c_ulong),
        ("dst", c_ulong)
    ] # IP Header (20Byte)
    
    def __new__(self, socket_buffer=None):
        return self.from_buffer_copy(socket_buffer)       
    
    def __init__(self, socket_buffer=None):
        self.protocol_map={1:"ICMP", 6:"TCP", 17:"UDP"}
        self.src_address=socket.inet_ntoa(struct.pack("<L", self.src))
        self.dst_address=socket.inet_ntoa(struct.pack("<L", self.dst))
        try:
            self.protocol=self.protocol_map[self.protocol_num]
        except:
            self.protocol=str(self.protocol_num)
        
class ICMP(Structure):
    _fields_=[
        ("type", c_ubyte),
        ("code", c_ubyte),
        ("checksum", c_ushort),
        ("unused", c_ushort),
        ("next_hop_mtu", c_ushort)
        ] # ICMP Header (8Byte)
    
    def __new__(self, socket_buffer):
        return self.from_buffer_copy(socket_buffer)
    
    def __init__(self, socket_buffer):
        pass

def hexdump(src, saveFile, length=16):
    result=[]
    digits=4 if isinstance(src, unicode) else 2
    for i in xrange(0, len(src), length):
       s=src[i:i+length]
       hexa=b' '.join(["%0*X" % (digits, ord(x))  for x in s])
       text=b''.join([x if 0x20 <= ord(x) < 0x7F else b'.'  for x in s])
       result.append( b"%04X   %-*s   %s" % (i, length*(digits + 1), hexa, text) )
    fp=open(saveFile, "a")
    fp.write(b'\n'.join(result))
    fp.close()
    print b'\n'.join(result)

def main():
    try:
        interfaceList=socket.gethostbyname_ex(socket.gethostname()) # PC 내 랜카드(인터페이스) 수에 따른 IP 리스트 얻음 
        print "\n[List]" 
        for i in range(0, len(interfaceList)+1): 
            try: 
                print str(i)+". "+interfaceList[2][i] 
            except Exception, e: 
                pass 
        select=raw_input("\nSelect Number : ") 
        ip="" # 사용할 최종적인 IP
        for i in range(0, len(interfaceList[2])): 
            if(int(select)==i): 
                ip=interfaceList[2][i] 
                break
        saveFile=raw_input("Input Save File : ")
        sniffer=socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
        sniffer.bind((ip, 0))
        sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
        try:
            while(1):
                raw_buffer=sniffer.recvfrom(65565)[0] # 하나의 패킷을 읽음
                ip_header=IP(raw_buffer[0:20]) # 패킷의 IP Header 부분(20Byte)을 IP 클래스로 전달
                if(ip_header.dst_address==ip or ip_header.src_address==ip): # 설정한 IP가 출발지 또는 목적지일 경우
                    fp=open(saveFile, "a")
                    fp.write("\n\n%s\t%s -> %s" % (ip_header.protocol, ip_header.src_address, ip_header.dst_address)+"\n")
                    fp.close()
                    print "\n\n%s\t%s -> %s" % (ip_header.protocol, ip_header.src_address, ip_header.dst_address)
                    #if(ip_header.protocol=="ICMP"): 
                        #offset=ip_header.ihl*4 # offset은 IP Header의 크기(20Byte)
                        #buf=raw_buffer[offset:offset+sizeof(ICMP)] # buf는 ICMP Header(21Byte~28Byte)
                        #icmp_header=ICMP(buf) # 패킷의 ICMP Header 부분(8Byte)을 ICMP 클래스로 전달
                        #if(icmp_header.type==8): print "ICMP Request from ", ip_header.src_address # icmp Type이 8일 경우 ICMP Request
                        #if(icmp_header.type==0): print "ICMP Reply from ", ip_header.dst_address # icmp Type이 0일 경우 ICMP Reply
                        #print "ICMP\tType : %d  Code : %d" % (icmp_header.type, icmp_header.code)
                    hexdump(raw_buffer, saveFile)
        except KeyboardInterrupt:
            sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
    except Exception, e:
        if "10013" in str(e): # 10013 에러가 날 경우 관리자 권한으로 실행해야 함을 의미
            print "[-] Please run with administrative rights"
            time.sleep(600)
            exit(0)
        print "[-] ", e 
        time.sleep(600)
        exit(0)
            
if __name__=="__main__":
    main()
