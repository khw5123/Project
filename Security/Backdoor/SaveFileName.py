import os, threading, time

threads=10

def saveFileName(driveORdirectory, extension, saveFile):
    for r,d,f in os.walk(driveORdirectory):
        for file in f:    
            path="%s\\%s" % (r, file)
            if(extension!=""):
                if "."+extension in path:
                    fp=open(saveFile, "a")
                    fp.write(path+"\n")
                    fp.close()
                    print path
            else:
                fp=open(saveFile, "a")
                fp.write(path+"\n")
                fp.close()
                print path
          
def main():
    try:
        print "1. Specific Directory\n2. All Drive"
        sel=raw_input("Select : ")
        print "\n1. Specific File Name Extension\n2. All File"
        sel2=raw_input("Select : ")
        extension=""
        if(sel2=="1"):
            extension=raw_input("Input File Name Extension( ex) exe) : ")
        saveFile=raw_input("Input Save File : ")
        if(sel=="1"):
            directory=raw_input("Input Directory : ")
            print "Wait..."
            os.chdir(directory)
            for i in range(threads): 
                t=threading.Thread(target=saveFileName(directory, extension, saveFile))
                t.start()
        elif(sel=="2"):
            drives=raw_input("Input Drives( ex) c:\ d:\ f:\ ) : ")
            print "Wait..."
            for drive in drives.split(' '):
                os.chdir(drive)
                for i in range(threads): 
                    t=threading.Thread(target=saveFileName(drive, extension, saveFile))
                    t.start()
        print "\n[+] Open The ", saveFile    
        time.sleep(600)
    except Exception, e:
        print "[-] ", e 
        time.sleep(600)
        exit(0)
    
if __name__=="__main__":
    main()
