#-*- coding: utf-8 -*-
import time, pexpect

PROMPT=['# ', '>>> ', '> ','\$ ']

def sendCommand(s, cmd):
    s.sendline(cmd)
    s.expect(PROMPT)
    print s.before

def connect(user, host, password):
    ssh_newkey='Are you sure you want to continue connecting'
    connStr='ssh '+user+'@'+host
    child=pexpect.spawn(connStr)
    ret=child.expect([pexpect.TIMEOUT, ssh_newkey, '[P|p]assword:'])
    if(ret==0): # 접속시간을 초과했을 경우
        print '[-] Error Connecting'
        time.sleep(10)
        exit(1)
    if(ret==1): # RSA 키 메세지를 받았을 경우
        child.sendline('yes')
        ret=child.expect([pexpect.TIMEOUT,'[P|p]assword:'])
        if(ret==0):
            print '[-] Error Connecting'
            time.sleep(10)
            exit(1)   
    child.sendline(password)
    child.expect(PROMPT)
    return child

def main():
    host=raw_input("Input SSH Server IP : ")
    user=raw_input("Input SSH Account : ")
    password=raw_input("Input SSH Password : ")
    s=connect(user, host, password) # connect 함수를 통해 인증
    while(True):
        account=user+"@"+host+" : "
        command=raw_input(account) # SSH 세션에 전송할 명령어 입력
        sendCommand(s, command)

if __name__ == '__main__':
    main()
'''
import time, pxssh

def sendCommand(s, cmd):
    s.sendline(cmd)
    s.prompt()
    print s.before

def connect(host, user, password):
    try:
        s=pxssh.pxssh()
        s.login(host, user, password)
        return s
    except Exception, e:
        print "[-]", e
        time.sleep(10)
        exit(0)

def main():
    host=raw_input("Input SSH Server ID : ")
    user=raw_input("Input SSH Account : ")
    password=raw_input("Input SSH Password : ")
    s=connect(host, user, password)
    while(True):
        account=user+"@"+host+" : "
        command=raw_input(account)
        sendCommand(s, command)

if __name__=='__main__':
    main()
'''