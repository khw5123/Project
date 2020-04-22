import socket, sys

def main():
    uploadServerIP=raw_input("Input Upload Server IP : ")
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((uploadServerIP, 23456))
    print "[+] Connected ", uploadServerIP
    try:
        #sys.stdout.flush()
        uploadFile=raw_input("\nInput UPload File : ")
        fp=open(uploadFile, "rb")
        buf=fp.read()
        fp.close()
        s.send(buf)
        confirm=s.recv(100)
        print confirm
    except Exception, e:
        print "[-] ", e
    s.close()

if __name__=="__main__":
    main()