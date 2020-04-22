from scapy.all import *

def sequenceDifference(targetIP):
    curSeq=0
    preSeq=0
    seqDiff=0
    while(1):
        preSeq=curSeq
        tcpPacket=IP(src="123.123.123.123" , dst=targetIP)/TCP(sport=12345, dport=80)
        p=sr1(tcpPacket, verbose=0)
        curSeq=p.getlayer(TCP).seq
        seqDiff=curSeq-preSeq
        print "Previous Sequence Number : ", preSeq
        print "Current Sequence Number : ", str(curSeq)
        print "[+] Sequence Number Difference : ", str(seqDiff)

def main():
    ip=raw_input("Input Server IP : ")
    sequenceDifference(ip)

if __name__ == '__main__':
    main()