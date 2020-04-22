#-*- coding: utf-8 -*-
import wmi, win32security, win32api, win32con, time, os
from datetime import datetime

saveFile="C:\\Intel Architecture\\Exception\\"+str(datetime.today().year)+"-"+str(datetime.today().month)+"-"+str(datetime.today().day)+"-"+str(datetime.today().hour)+"-"+str(datetime.today().minute)+"-"+str(datetime.today().second)+".csv"

def get_process_privileges(pid):
    try:
        hproc=win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION, False, pid) # 타겟 프로세스의 핸들 얻음
        htok=win32security.OpenProcessToken(hproc, win32con.TOKEN_QUERY) # 타겟 프로세스의 토큰 오픈
        privs=win32security.GetTokenInformation(htok, win32security.TokenPrivileges) # 타겟 프로세스의 토큰 정보 요청(활성화된 권한 목록 추출)
        priv_list=""
        for i in privs:
            if(i[1]==3):
                priv_list+="%s|" % win32security.LookupPrivilegeName(None, i[0])
    except:
        priv_list="N/A"
    return priv_list

def main():
    try:
        os.system("mkdir \"C:\\Intel Architecture\"")
        os.system("mkdir \"C:\\Intel Architecture\\Exception\"")
        fp=open(saveFile, "wb")
        fp.write("Time,User,Excutable,CommandLine,PID,Parent PID,Privileges\r\n")
        fp.close()
        c=wmi.WMI() # WMI 클래스의 인스턴스 생성
        process_watcher=c.Win32_process.watch_for("creation") # 프로세스 생성, 소멸 등의 이벤트를 모니터링할 수 있음
        #process_watcher=c.Win32_process.watch_for("operation") # 프로세스에서 발생하는 이벤트를 모두 모니터링할 수 있음
        while True:
            try:
                new_process=process_watcher() # process_watcher 함수에서 새 프로세스 이벤트를 리턴
                proc_owner=new_process.GetOwner() # GetOwner 함수에서 프로세스를 생성한 사용자 리턴
                proc_owner="%s\\%s" % (proc_owner[0], proc_owner[2])
                create_date=new_process.CreationDate
                executable=new_process.ExecutablePath
                cmdline=new_process.CommandLine
                pid=new_process.ProcessId
                parent_pid=new_process.ParentProcessId
                privileges=get_process_privileges(pid)
                process_log_message="%s,%s,%s,%s,%s,%s,%s\r\n" % (create_date, proc_owner, executable, cmdline, pid, parent_pid, privileges)
                #print process_log_message
                fp=open(saveFile, "ab")
                fp.write(process_log_message+"\r\n")
                fp.close()
            except:
                pass
    except Exception, e:
        exit(0)
        
if __name__=="__main__":
    main()
