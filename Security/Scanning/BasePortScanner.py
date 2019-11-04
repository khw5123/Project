import socket
import threading

def findOpenPort(target_addr,portlist):
    for port in portlist:
        sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        openPort=sock.connect_ex((target_addr,port))
        if(openPort==0):
            print "[+] ", port
        sock.close()

def main():
    target_addr=raw_input("Input Target IP : ")
    port=raw_input("Input port( ex) 21 22 80 443 ) : ")
    portlist=[]
    for port in port.split():
        portlist.append(int(port))
    t=threading.Thread(target=findOpenPort(target_addr,portlist))
    t.start()
    
if __name__=="__main__":
    main()