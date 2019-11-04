#-*- coding: utf-8 -*-
import urllib2, time, threading
from urlparse import urlsplit
from os.path import basename
from bs4 import BeautifulSoup
from PIL import Image
from PIL.ExifTags import TAGS

srcList=["src", "data-src"]
mainURL="" # 이미지 파일이 있는 URL
inURL="" # 이미지 파일에 있는 경로
downDirectory="" # 다운로드할 디렉터리
startNumber=
endNumber=
sem=threading.Semaphore(10)

def findImgTags(url):
    pageSource=urllib2.urlopen(url).read()
    soup=BeautifulSoup(pageSource)
    imgTags=soup.findAll('img')
    return imgTags

def download(imgTag):
    sem.acquire()
    for srcName in srcList: 
        try:
            imgFile=imgTag[srcName]
            if inURL in imgFile:
                binaryData=urllib2.urlopen(imgFile).read()
                imgFileName=basename(urlsplit(imgFile)[2])
                imgFileName=downDirectory+imgFileName
                fp=open(imgFileName, 'wb')
                fp.write(binaryData)
                fp.close()
                print "[+] "+imgFileName
                sem.release()
                return
        except Exception, e:
            sem.release()
            pass
    sem.release()

def main():
    try:
        threads=[]
        for index in range(startNumber, endNumber):
            try:
                url=mainURL+str(index)
                imgTags=findImgTags(url)
                for imgTag in imgTags:
                    th=threading.Thread(target=download, args=(imgTag,))
                    th.start()
                    threads.append(th)
                    if(len(threads) > 300):
                        for th in threads: 
                            th.join()
                        threads=[]
            except Exception, e:
                pass  
        for th in threads:
            th.join()
    except Exception, e:
        exit(0)
        
if __name__ == '__main__':
    main()
