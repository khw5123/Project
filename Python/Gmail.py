#-*- coding: utf-8 -*-
import time, smtplib
from email.mime.text import MIMEText

def sendMail(account, password, target, title, content):
    msg=MIMEText(content)
    msg['From']=account
    msg['To']=target
    msg['Subject']=content
    try:
        smtpServer=smtplib.SMTP('smtp.gmail.com', 587)
        print "[+] Connecting To Mail Server"
        smtpServer.ehlo()
        print "[+] Starting Encrypted Session"
        smtpServer.starttls()
        smtpServer.ehlo()
        print "[+] Logging Into Mail Server"
        smtpServer.login(account, password)
        print "[+] Sending Mail"
        smtpServer.sendmail(account, target, msg.as_string())
        smtpServer.close()
        print "[+] Mail Sent Successfully"
    except Exception, e:
        print "[-] Sending Mail Failed"
        print "[-] ", e
        if "Please log in via your web browser" in str(e):
            print "\n[Try]\n1. Gmail Login\n2. Open Mail\n3. Click 'Review blocked login attempts' Mail\n4. Click 'Allow access to less secure apps' Link\n5. 'Allow less secure apps: Disable' Use"
        time.sleep(600000) 
        exit(0)
        
def main():
    try:
        account=raw_input("Input Gmail Account : ")
        password=raw_input("Input Gmail Password : ")
        if "@gmail.com" not in account:
            account+="@gmail.com"
        target=raw_input("To. ")
        title=raw_input("Title : ")
        print "--------------------------------------------------------------------------"
        content=raw_input()
        print"\nFrom. "+account+"\n--------------------------------------------------------------------------"
        sendMail(account, password, target, title, content)
        time.sleep(600000)
    except Exception, e:
        print "[-] ", e 
        exit(0)
        
if __name__=="__main__":
    main()
