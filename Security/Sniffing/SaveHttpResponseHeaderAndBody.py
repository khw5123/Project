import urllib, time

def header(url, saveFile):
    http_r=urllib.urlopen(url)
    if http_r.code==200:
        fp=open(saveFile, "a")
        fp.write("[Header Response Header]\n"+str(http_r.headers))
        fp.close()
        print "[HTTP Response Header]\n"+str(http_r.headers)
        
def body(url, saveFile):
    http_r=urllib.urlopen(url)
    if http_r.code==200:
        fp=open(saveFile, "a")
        fp.write("\n[HTTP Response Body]\n"+str(http_r.read()))
        fp.close()
        print "\n[HTTP Response Body]\n"+str(http_r.read())

def main():
    try:
        url=raw_input("Input URL : ")
        saveFile=raw_input("Input Save File : ")
        header(url, saveFile)
        body(url, saveFile)
        print "\n[+] Open the "+saveFile
        time.sleep(600)
    except Exception, e:
        print "[-] ", e
        time.sleep(600)
        exit(0)
    
if __name__=="__main__":
    main()
