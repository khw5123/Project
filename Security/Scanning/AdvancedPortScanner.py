import thread, threading, time, socket, sys, shelve
from datetime import datetime

fileName="portDB.raj"
openPorts=[]

def executeThread(targetIP, startPort, endPort, timeOut):
    totalPort=endPort-startPort+1
    tn=30
    total_thread=totalPort/tn   
    if(totalPort%tn != 0):
        total_thread+=1
    if(total_thread > 300):
        tn=totalPort/300
        tn=tn+1
        total_thread=totalPort/tn
        if (totalPort%tn != 0):
            total_thread+=1
    threads=[]
    startTime=datetime.now()
    try:
        for i in range(total_thread):
            threadName="Thread"+str(i)
            thread=myThread(threadName, targetIP, startPort, endPort, timeOut)
            thread.start()
            threads.append(thread)
    except:
         print "thread error"
         exit(1)
    print "Number of Threads active:", threading.activeCount()
    for t in threads:
        t.join()
    endTime=datetime.now()
    runningTime=endTime-startTime
    ports=list(set(openPorts))
    for port in ports:
        print port
    print "Running Time : " , runningTime

def portScan(threadName, targetIP, startPort, endPort, timeOut):
    shelf=shelve.open(fileName)
    data=(shelf['desc'])
    try:
        for port in range(startPort, endPort):
            sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(timeOut)
            openPort=sock.connect_ex((targetIP,port))
            if(openPort==0):
                string="[+] "+str(port)+" : "+str(data.get(port, "Not in PortDB.raj"))
                openPorts.append(string)
            sock.close()
    except KeyboardInterrupt:
         print "You stop this "
         sys.exit()
    except socket.gaierror:
         print "Hostname could not be resolved"
         sys.exit()
    except socket.error:
         print "could not connect to server"
         sys.exit()
    shelf.close()

class myThread(threading.Thread):
    def __init__(self, threadName, targetIP, startPort, endPort, timeOut):
        threading.Thread.__init__(self)
        self.threadName=threadName
        self.targetIP=targetIP
        self.startPort=startPort
        self.endPort=endPort
        self.timeOut=timeOut
    def run(self):
            portScan(self.threadName, self.targetIP, self.startPort, self.endPort, self.timeOut)
    
def main():
    targetIP=raw_input("Input Target IP : ")   
    range=raw_input("Input port range( ex) 0 65535) : ")
    startPort=int(range.split(' ')[0])
    endPort=int(range.split(' ')[1])
    connect=raw_input("Imput Connectivity(L : Low, H : High) : ")
    if(connect=='L' or connect=='l'):
        timeOut=1.5
    elif(connect=='H' or connect=='h'):
        timeOut=0.5
    executeThread(targetIP, startPort, endPort, timeOut)
    
if __name__=="__main__":
    main()