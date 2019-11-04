import ftplib, time

def anonymousLogin(host):
    try:
        ftp=ftplib.FTP(host)
        ftp.login("anonymous", "")
        ftp.quit()
        return True
    except Exception, e:
        print "\n[-] ", e
        return False

def main():
    try:
        host=raw_input("Input FTP Server IP : ")
        if(anonymousLogin(host)):
            print "[+] "+host+" FTP Anonymous Login Succeeded"
        else:
            print "[-] "+host+" FTP Anonymous Login Failed"
        time.sleep(600)
    except Exception, e:
        print "[-] ", e
        time.sleep(600)
        exit(0)
    
if __name__=="__main__":
    main()
