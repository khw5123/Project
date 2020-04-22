import zipfile, time

def crack(zFile, dictionaryFile, saveFile):
    try:
        fp=open(dictionaryFile)
        for pw in fp.readlines():
            try:
                password=pw.strip('\n')
                print "Try : "+password
                zFile.extractall(pwd=password)
                print "\n[+] Get : "+password+"\n[+] Open Your Save File"
                fp=open(saveFile,"a")
                fp.write(password)
                fp.close()
                time.sleep(600)
                exit(0)
            except:
                pass
    except Exception, e:
        print "[-] ", e
        time.sleep(600)
        exit(0)

def main():
    try:
        zipFile=raw_input("Input Zip File : ")
        dictionaryFile=raw_input("Input Dictionary File : ")
        saveFile=raw_input("Input Save File : ")
        zFile=zipfile.ZipFile(zipFile)
        crack(zFile, dictionaryFile, saveFile)
    except Exception, e:
        print "[-] ", e
        time.sleep(600)
        exit(0)

if __name__ == '__main__':
    main()
