#-*- coding: utf-8 -*-
import win32file, win32con, os, threading, time
from datetime import datetime

dirs_to_monitor=[]
FILE_CREATED=1
FILE_DELETED=2
FILE_MODIFIED=3
FILE_RENAMED_FROM=4
FILE_RENAMED_TO=5

def log(message, saveFile):
    fp=open(saveFile, "a")
    fp.write("%s\n" % message.encode('utf-8'))
    fp.close()
  
def start_monitor(path_to_watch, saveFile):
    FILE_LIST_DIRECTORY=0x0001
    h_directory=win32file.CreateFile(path_to_watch, FILE_LIST_DIRECTORY, win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE, None, win32con.OPEN_EXISTING, win32con.FILE_FLAG_BACKUP_SEMANTICS, None) # 모니터링할 디렉터리의 핸들을 가져온다.
    while(1):
        try:
            results=win32file.ReadDirectoryChangesW(h_directory, 1024, True, win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES | win32con.FILE_NOTIFY_CHANGE_DIR_NAME | win32con.FILE_NOTIFY_CHANGE_FILE_NAME | win32con.FILE_NOTIFY_CHANGE_LAST_WRITE | win32con.FILE_NOTIFY_CHANGE_SECURITY | win32con.FILE_NOTIFY_CHANGE_SIZE, None, None) # 디렉토리에 변경이 발생하면 알림을 받기위한 함수
            for action, file_name in results:
                full_filename=os.path.join(path_to_watch, file_name)
                if(action==FILE_CREATED):
                    print "[%s] Created : %s" % (str(datetime.now()), full_filename)
                    log("[%s] Created : %s" % (str(datetime.now()), full_filename), saveFile)
                elif(action==FILE_DELETED):
                    print "[%s] Deleted : %s" % (str(datetime.now()), full_filename)
                    log("[%s] Deleted : %s" % (str(datetime.now()), full_filename), saveFile)
                elif(action==FILE_MODIFIED):
                    if(full_filename==saveFile):
                        break
                    print "[%s] Modified : %s" % (str(datetime.now()), full_filename)
                    log("[%s] Modified : %s" % (str(datetime.now()), full_filename), saveFile)
                elif(action==FILE_RENAMED_FROM):
                    print "[%s] Renamed from : %s" % (str(datetime.now()), full_filename)
                    log("[%s] Renamed from : %s" % (str(datetime.now()), full_filename), saveFile)
                elif(action==FILE_RENAMED_TO):
                    print "[%s] Renamed to : %s" % (str(datetime.now()), full_filename)
                    log("[%s] Renamed to : %s" % (str(datetime.now()), full_filename), saveFile)
                else:
                    print "[%s] Unknown : %s" % (str(datetime.now()), full_filename)
                    log("[%s] Unknown : %s" % (str(datetime.now()), full_filename), saveFile)
        except:
            pass

def main():
    try:
        while(1):
            dirList=raw_input("Input the directory to be monitored('q' to exit input) : ")
            if(dirList=="q"):
                break
            dirs_to_monitor.append(dirList)
        saveFile=raw_input("Input Save File : ")
        for path in dirs_to_monitor:
            monitor_thread=threading.Thread(target=start_monitor, args=(path, saveFile))
            monitor_thread.start()
    except Exception, e:
        print "[-] ", e
        time.sleep(600)
        exit(0)

if __name__=="__main__":
    main()
