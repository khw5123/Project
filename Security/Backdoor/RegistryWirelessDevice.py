import time
from _winreg import *

def macTypeConversions(addr):
    try:
        tmpAddr=""
        for ch in addr:
            tmpAddr+='%02x ' % ord(ch)
        tmpAddr=tmpAddr.strip(' ').replace(' ',':')[0:17]
        return tmpAddr
    except Exception, e:
        print "[-] ", e

def findWirelessMAC(fp):
    subReg="SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkList\Signatures\Unmanaged"
    regKey=OpenKey(HKEY_LOCAL_MACHINE, subReg, 0, (KEY_WOW64_64KEY+KEY_ALL_ACCESS))
    for i in range(0, 100):
        try:
            wirelessList=EnumKey(regKey, i)
            wirelessKey=OpenKey(regKey, wirelessList)
            (n, addr, t)=EnumValue(wirelessKey, 5)
            (n, name, t)=EnumValue(wirelessKey, 4)
            bssid=macTypeConversions(addr)
            ssid=str(name.encode("utf-8"))
            print 'SSID : '+ssid+" \tBSSID : "+bssid
            fp.write('SSID : '+ssid+"\tBSSID : "+bssid+"\n")
            CloseKey(wirelessKey)
        except Exception, e:
            pass
    CloseKey(regKey)

def main():
    try:
        saveFile=raw_input("Input Save File : ")
        fp=open(saveFile, "w")
        findWirelessMAC(fp)
        print "[+] Open the ", saveFile
        fp.close()
        time.sleep(30)
    except Exception, e:
        print "[-] ", e
        time.sleep(30)
        exit(0)
    
if __name__=='__main__':
    main()