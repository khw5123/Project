# -*- coding: utf-8 -*-
import time
from bluetooth import *

serviceList=[]
deviceNameList=[]
deviceMacList=[]

def findOpenPort(mac, port):
    sock=BluetoothSocket(RFCOMM)
    try:
        sock.connect((mac, port))
        sock.close()
        return True
    except:
        return False

def findService(mac, saveFile):
    services=find_service(address=mac)
    for service in services:    
        name=service["name"]
        proto=service["protocol"]
        port=str(service["port"])
        portOpen=findOpenPort(mac, int(port))
        if name not in serviceList:
            serviceList.append(name)
            if portOpen:
                print "[+] Service Name : "+str(name)+"  Protocol : "+str(proto)+"  Port : "+port+" Open"
                fp=open(saveFile, "a")
                fp.write("[+] Service Name : "+str(name)+"  Protocol : "+str(proto)+"  Port : "+port+" Open\n")
                fp.close()
            else:
                fp=open(saveFile, "a")
                fp.write("[-] Service Name : "+str(name)+"  Protocol : "+str(proto)+"  Port : "+port+" Close\n")
                fp.close()
                print "[-] Service Name : "+str(name)+"  Protocol : "+str(proto)+"  Port : "+port+" Close"           

def findDevice(saveFile):
    try:
        foundDevs=discover_devices(lookup_names=True)
        for (mac, name) in foundDevs:
            if mac not in deviceMacList:
                fp=open(saveFile, "a")
                fp.write("[+] Bluetooth Device : "+str(name)+"\tMAC Address : "+str(mac)+"\n")
                fp.close()
                print "[+] Bluetooth Device : "+str(name)+"\tMAC Address : "+str(mac)
                deviceMacList.append(mac)
                deviceNameList.append(str(name))
    except Exception, e:
        #print "[-] ", e
        return

def main():
    try:
        searchTime=raw_input("Input Search Time : ")
        saveFile=raw_input("Input Save File : ")
        waitTime=int(searchTime)/4.5
        if(waitTime<20):
            waitTime=20/4.5
        count=0
        print "\nLooking for bluetooth device...\n"
        while(waitTime > count):
            findDevice(saveFile)
            time.sleep(2)
            count+=2
        print ""
        for i in range(0, len(deviceMacList)):
            print str(i)+". "+deviceNameList[i]
        select=raw_input("Select the number you want to see the service : ")
        fp=open(saveFile, "a")
        fp.write("\n[Service of "+deviceNameList[int(select)]+"("+deviceMacList[int(select)]+")]\n")
        fp.close()
        findService(deviceMacList[int(select)], saveFile)
        print "\n[+] Open the "+saveFile
        time.sleep(600)
    except Exception, e:
        print "[-] ", e
        time.sleep(600)
        exit(0)
    
if __name__=="__main__":
    main()
