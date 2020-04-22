import ftplib, time

def show(ftp, directory):
    try:
        dirList=ftp.nlst(directory)
        for file in dirList:
            if "." in file:
                print "/", file
            else:
                show(ftp, file)
    except Exception, e:
        print "[-] ", e
        time.sleep(30)
        exit(0)

def main():
    host=raw_input("Input FTP Server IP : ")
    user=raw_input("Input FTP Account : ")
    password=raw_input("Input FTP password : ")
    ftp=ftplib.FTP(host)
    ftp.login(user, password)
    show(ftp, "")

if __name__=="__main__":
    main()
