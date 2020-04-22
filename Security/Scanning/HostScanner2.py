import os, platform, socket, time
from datetime import datetime

ipList=[]
ping="ping -n 1 "
tn=20
activateIP=[]
windowsPort=135
clear="cls"

def scan(totalIP, select):
    try:
        print "Scanning..."
        startTime=datetime.now()
        if(select=="1"):
            pingSweeper()
        elif(select=="2"):
            tcpScanner()
        endTime=datetime.now()
        runningTime=endTime-startTime
        activate=list(set(activateIP))
        os.system(clear)
        print "\n["+str(ipList[0])+" ~ "+str(ipList[-1])+"]"
        for ip in activate:
            print "[+] "+ip+" is up"
        print "\nRunning Time : "+str(runningTime)
    except Exception, e:
         print "[-] ", e
         time.sleep(600)
         exit(0)

def pingSweeper():
    for ip in ipList:
        try:
            print "Try : "+str(ip)
            command=ping+ip
            icmp_reply=os.popen(command)
            for line in icmp_reply.readlines():
                if(line.count("TTL")):
                    activateIP.append(ip)
                    break
        except Exception, e:
            pass   

def tcpScanner():
    for ip in ipList:
        try:
            print "Try : "+str(ip)
            sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(1)
            openPort=sock.connect_ex((ip, windowsPort))
            if(openPort==0):
                activateIP.append(ip)
            sock.close()
        except Exception, e:
            pass         

def osSet():
    operatingSystem=platform.system()
    if(operatingSystem != "Windows"):
        ping="ping -c 1 "
        clear="clear"

def networkSet(network, hostRange):
    network=network.split(".")
    startHost=int(hostRange.split(" ")[0])
    endHost=int(hostRange.split(" ")[1])
    for host in xrange(startHost, endHost+1):
        ipList.append(network[0]+"."+network[1]+"."+network[2]+"."+str(host))
    return endHost-startHost+1

def main():
    try:
        network=raw_input("Input Network-ID ( ex) 192.168.119.0(prefix=24)) : ")
        hostRange=raw_input("Input Host Range( ex) 1 254 ) : ")
        select=raw_input("1. Ping Sweeper 2. Windows Tcp Scanner : ")
        totalIP=networkSet(network, hostRange)
        osSet()
        scan(totalIP, select)
        time.sleep(600)
    except Exception, e:
        print "[-] ", e
        time.sleep(600)
        exit(0)
        
if __name__=="__main__":
    main()
