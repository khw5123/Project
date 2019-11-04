import urllib2, time, os
from urlparse import urlsplit
from os.path import basename
from bs4 import BeautifulSoup

def findImgTags(url):
    pageSource=urllib2.urlopen(url).read()
    soup=BeautifulSoup(pageSource)
    imgTags=soup.findAll("img")
    return imgTags

def download(imgTag):
    try:
        imgFile=imgTag["src"]
        binaryData=urllib2.urlopen(imgFile).read()
        imgFileName=basename(urlsplit(imgFile)[2])
        fp=open(imgFileName, "wb")
        fp.write(binaryData)
        fp.close()
        print "[+] "+imgFileName
    except Exception, e:
        pass
        
def main():
    try:
        url=raw_input("Input URL : ")
        imgTags=findImgTags(url)
        os.system("cls")
        for imgTag in imgTags:
            download(imgTag)
        print "\n[+] Open the Current Directory"
        time.sleep(600)
    except Exception, e:
        print "[-] ", e
        time.sleep(600)
        exit(0)
    
if __name__ == "__main__":
    main()
