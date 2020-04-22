#-*- coding: utf-8 -*-
import json, urllib, mechanize, time
from bs4 import BeautifulSoup
        
class GoogleResult:
    def __init__(self,title, text, url):
        self.title=title
        self.text=text
        self.url=url
    def viewTitle(self):
        return self.title
    def viewText(self):
        return self.text
    def viewURL(self):
        return self.url
    
def googleSearch(gSearch):
    try:
        gSearch=urllib.quote_plus(gSearch)
        br=mechanize.Browser()
        br.set_handle_robots(False)
        response=br.open("http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q="+gSearch)
        objects=json.load(response)
        results=[]
        for result in objects['responseData']['results']:
            url=result['url']
            title=result['titleNoFormatting'].encode('utf-8')
            text=result['content'].encode('utf-8')
            gClass=GoogleResult(title,text,url)
            results.append(gClass)
        return results
    except Exception, e:
        print "[-] ", e
        time.sleep(10)
        pass
        
def main():
    try:
        while(1):
            gSearch=raw_input("Input Searches : ")
            result=googleSearch(gSearch)
            for i in range(len(result)):
                count=i+1
                print str(count)+". Ttile : "+result[i].viewTitle()
                print str(count)+". Text : "+result[i].viewText()
                print str(count)+". URL : "+result[i].viewURL()+"\n"   
    except Exception, e:
        print "[-] ", e 
        time.sleep(30)
        exit(0)

if __name__=="__main__":
    main()