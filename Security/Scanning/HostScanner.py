import os, platform, threading, socket
from datetime import datetime

ips=[]
ping="ping -n 1 "
tn=20
activateIP=[]
windowsPort=135

def executeThread(total_ip, method):
    total_thread=total_ip/tn
    total_thread=total_thread+1
    threads=[]
    startTime=datetime.now()
    try:
        for i in xrange(total_thread):
            thread=myThread(method)
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
    activate=list(set(activateIP))
    for ip in activate:
        print "[+] ", ip, " is up"
    print "Running Time : " , runningTime

def tcpScanner():
    for ip in ips:
        sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        openPort=sock.connect_ex((ip,windowsPort))
        if(openPort==0):
            activateIP.append(ip)
        sock.close()

def pingSweeper():
    for ip in ips:
        command=ping+ip
        icmp_reply=os.popen(command)
        for line in icmp_reply.readlines():
            if(line.count("TTL")):
                activateIP.append(ip)
                break

class myThread(threading.Thread):
    def __init__(self, method):
        threading.Thread.__init__(self)
        self.identifier=method
    def run(self):
        if(self.identifier=="1"):
            pingSweeper()
        elif(self.identifier=="2"):
            tcpScanner()

def osSet():
    operatingSystem=platform.system()
    if(operatingSystem !="Windows"):
        ping="ping -c 1 "

def networkSet(network, range):
    network=network.split('.')
    startHost=int(range.split(' ')[0])
    endHost=int(range.split(' ')[1])
    for host in xrange(startHost, endHost+1):
        ips.append(network[0]+"."+network[1]+"."+network[2]+"."+str(host))
    return endHost-startHost+1

def main():
    network=raw_input("Input network-id (prefix=24, ex) 192.168.119.0 ) : ")
    range=raw_input("Input host range( ex) 1 254 ) : ")
    method=raw_input("1. Ping Sweeper 2. Tcp Scanner(Windows) : ")
    total_ip=networkSet(network, range)
    osSet()
    executeThread(total_ip, method)
    
if __name__=="__main__":
    main()