import sys
from socket import *

maxSize=50000

def hexdump(src, length=16):
    result=[]
    digits=4 if isinstance(src, unicode) else 2
    for i in xrange(0, len(src), length):
       s=src[i:i+length]
       hexa=b' '.join(["%0*X" % (digits, ord(x))  for x in s])
       text=b''.join([x if 0x20 <= ord(x) < 0x7F else b'.'  for x in s])
       result.append( b"%04X   %-*s   %s" % (i, length*(digits + 1), hexa, text) )
    print b'\n'.join(result)

def main():
    uploadServerIP=raw_input("Input Upload Server(yourself) IP : ")
    s=socket(AF_INET, SOCK_STREAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind((uploadServerIP, 23456))
    s.listen(10)
    conn, addr=s.accept()
    print "[+] Connected ", addr
    try:
        #sys.stdout.flush()
        buf=conn.recv(maxSize)
        downloadFile=raw_input("\nInput Download File : ")
        fp=open(downloadFile, "wb")
        fp.write(buf)
        fp.close()
        hexdump(buf)
        print "[+] Download Successed"
        conn.send("[+] Upload Successed")
    except Exception, e:
        print "[-] ", e
    conn.close()

if __name__=="__main__":
    main()