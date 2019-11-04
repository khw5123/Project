import socket, struct, binascii

def sniffer():
    s=socket.socket(socket.PF_PACKET, socket.SOCK_RAW, 8) #Using PF_PACKET and Raw Socket, 0x0800 : EETH_P_IP Protocol
    while True:
        pkt=s.recvfrom(2048)
        print pkt[0]
        
        ethernetHeader=pkt[0][0:14] # 1~6Byte : Destination Mac Address, 7~12Byte : Source Mac Address, 13~14Byte : Type or Length
        eth=struct.unpack("!6s6s2s", ethernetHeader) #s : string, ! : Network Byte
        print "--------------------Ethernet Frame--------------------"
        print "Desination Mac Address : ", binascii.hexlify(eth[0])
        print "Source Mac Address : ", binascii.hexlify(eth[1])
    
        # IPv4 Header Length : 20Byte
        ipHeader=pkt[0][14:34] # 23Byte : TTL, 27~30Byte : Source IP Address, 31~34Byte : Destination IP Address 
        iphdr=struct.unpack("!8sB3s4s4s", ipHeader) # B : integer(1Byte)
        print "---------------------------IP----------------------------"
        print "TTL : ", iphdr[1]
        print "Source IP Address : ", socket.inet_ntoa(iphdr[3])
        print "Destination IP Address : ", socket.inet_ntoa(iphdr[4])
        
        # TCP Header Length : 20Byte
        tcpHeader=pkt[0][34:54] # 34~35Byte : Source Port, 36~37Byte : Destination Port, 47Byte : TCP Flag
        #tcphdr=struct.unpack("!HH16s",tcpHeader)
        tcphdr = struct.unpack("!HH9ss6s", tcpHeader) # H : integer(2Byte)
        print "--------------------------TCP---------------------------"
        print "Source Port : ", tcphdr[0]
        print "Destination Port : ", tcphdr[1]
        print "TCP Flag : ", binascii.hexlify(tcphdr[3])
        
        print pkt[0][54:]
    
def main():
    sniffer()
    
if __name__=="__main__":
    main()