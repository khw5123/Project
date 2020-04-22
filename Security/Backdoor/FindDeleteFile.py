# -*- coding: utf-8 -*-
import time, os
from _winreg import *

def findTrashCan():
    dirs=['C:\\Recycler\\','C:\\Recycled\\','C:\\$Recycle.Bin\\'] # C:\Recycler : Window XP, C:\Recycle.Bin : Window 7
    for recycleDir in dirs:
        if os.path.isdir(recycleDir):
            return recycleDir
    print "[-] Directory Not Found"
    exit(0)

def findUserName(sid):
    try:
        key=OpenKey(HKEY_LOCAL_MACHINE, "SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList\\"+sid) # 사용자 정보가 담겨있다.
        (value, type)=QueryValueEx(key, 'ProfileImagePath')
        user=value.split('\\')[-1] # 계정명 추출
        return user
    except Exception, e:
        print "[-] ", e
        pass

def findDeleteList(recycleDir):
    try:
        dirList=os.listdir(recycleDir) # C:\\$Recycle.Bin 폴더에 있는 파일이나 디렉터리 목록
        for sid in dirList:
            files=os.listdir(recycleDir+sid) # 폴더명이 SID 로 되어있다.
            user=findUserName(sid)
            print '\nUser : ', str(user)
            for file in files:
                print 'File : ', str(file)
    except Exception, e:
        print "\n[-] ", e
        pass

def main():
    recycledDir=findTrashCan()
    findDeleteList(recycledDir)
    time.sleep(30)

if __name__=='__main__':
    main()