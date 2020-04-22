#-*- coding: utf-8 -*-
import urllib2, urllib, webbrowser, sys, os, time
from bs4 import BeautifulSoup

count=1

def saveVideoURL(url, saveFile):
    global count
    pageSource=urllib2.urlopen(url).read()
    soup=BeautifulSoup(pageSource)
    imgTags=soup.findAll('img')
    for imgTag in imgTags:
        try:
            if(count==1):
                os.system("cls")
            if "https://i.ytimg.com/vi/" in imgTag["src"]:
                a=imgTag["src"].split("https://i.ytimg.com/vi/")
                b=a[1].split("/hqdefault")
                youtubeURL="https://www.youtube.com/watch?v="+b[0]
                #webbrowser.open(youtubeURL)
                fp=open(saveFile, "a")
                fp.write(str(count)+". "+youtubeURL+"\n")
                fp.close()
                print str(count)+". "+youtubeURL
                count+=1
            if "https://i.ytimg.com/vi/" in imgTag["data-thumb"]:
                a=imgTag["data-thumb"].split("https://i.ytimg.com/vi/")
                b=a[1].split("/hqdefault")
                youtubeURL="https://www.youtube.com/watch?v="+b[0]
                #webbrowser.open(youtubeURL)
                fp=open(saveFile, "a")
                fp.write(str(count)+". "+youtubeURL+"\n")
                fp.close()
                print str(count)+". "+youtubeURL
                count+=1
        except:
            pass
            
def makeSearchURL(keywords, filterType, page):
    searchURL=""
    if(filterType=="relevance"):
        searchURL="https://www.youtube.com/results?sp=CAA%253D&page="+page+"&search_query="+urllib.quote(keywords)
    elif(filterType=="date"):
        searchURL="https://www.youtube.com/results?sp=CAI%253D&page="+page+"&search_query="+urllib.quote(keywords)
    elif(filterType=="view"):
        searchURL="https://www.youtube.com/results?sp=CAM%253D&page="+page+"&search_query="+urllib.quote(keywords)
    return searchURL
    
def main():
    try:
        reload(sys)
        sys.setdefaultencoding('utf-8')
        search=raw_input("Input Keywords : ")
        keyword=repr(search.decode('euc-kr').encode('utf-8'))
        keyword=keyword.split("\\x")
        keywords=""
        if(keyword[0]=="'"):
            for i in range(1, len(keyword)):
                tmp=int(keyword[i].replace("'",""), 16)
                keywords+=chr(int(tmp))
        else:
            keywords=search
        print "\n[Sort Filter Options]\n1. Sorted by relevance\n2. Sorted by Uploaded Date\n3. Sorted by Views"
        select=raw_input("Input Sort Filter(1, 2, 3) : ")
        filterType=""
        if(select=="1"):
            filterType="relevance"
        elif(select=="2"):
            filterType="date"
        elif(select=="" or select=="3"):
            filterType="view"
        maxPage=raw_input("Input Maximum Page Number(If you choose default to enter) : ")
        if(maxPage==""):
            maxPage="1"
        saveFile=raw_input("Input Save File : ")
        for i in range(1, int(maxPage)+1):
            saveVideoURL(makeSearchURL(keywords, filterType, str(i)), saveFile)
        fp=open(saveFile, "a")
        fp.write("\n[+] Keywords : "+keywords+"  Filter : "+filterType+"\n[+] Visit http://mp3fiber.com")
        fp.close()
        print "\n[+] Keywords : "+search+"  Filter : "+filterType+"\n[+] Open the "+saveFile+"\n[+] Visit http://mp3fiber.com"
        time.sleep(600)
    except Exception, e: 
        if "list index out of range" in str(e):
            fp=open(saveFile, "a")
            fp.write("\n[+] Keywords : "+keywords+"  Filter : "+filterType+"\n[+] Visit http://mp3fiber.com")
            fp.close()
            print "\n[+] Keywords : "+search+"  Filter : "+filterType+"\n[+] Open the "+saveFile+"\n[+] Visit http://mp3fiber.com"
        else:
            print "[-] ", e
        time.sleep(600)
        exit(0)
            
if __name__=="__main__":
    main()
