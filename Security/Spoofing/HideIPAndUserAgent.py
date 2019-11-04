#-*- coding: utf-8 -*-
import mechanize, cookielib, time, random

class anonBrowser(mechanize.Browser):
    def __init__(self, url):
        mechanize.Browser.__init__(self)   
        self.url=url
        self.proxies=["112.26.205.66:81",
                            "176.10.41.143:1080",
                            "190.120.123.2:1080",
                            "111.56.13.152:80"
                            ] #http://rmccurdy.com/scripts/proxy/good.txt
        self.uAgents=['Galaxy/1.0 [en] (Mac OS X 10.5.6; U; en)',
                            'Mozilla/4.0 (compatible; IBrowse 2.3; AmigaOS4.0)',
                            'HotJava/1.0.1/JRE1.1.x',
                            '(Windows NT 6.2; WOW64) KHTML/4.11 Gecko/20130308 Firefox/33.0 (PaleMoon/25.1)'
                            ] #http://www.useragentstring.com/pages/useragentstring.php
        self.cookies=cookielib.LWPCookieJar()
        self.set_cookiejar(self.cookies)
        self.hideIP()
        self.hideUserAgent()
        self.set_handle_robots(False)
        self.openURL()
        
    def addProxy(self, proxy):
        self.proxies.append(proxy)
        
    def addUserAgent(self, uAgent):
        self.uAgents.append(uAgent)
        
    def hideIP(self):
        try:
            idx=random.randrange(0, len(self.proxies))
            self.set_proxies({'http' : self.proxies[idx]})
            #print "\nProxy Used : "+self.proxies[idx]
        except Exception, e:
            print "[-] ", e 
            
    def hideUserAgent(self):
        try:
            idx=random.randrange(0, len(self.uAgents))
            self.addheaders=[('User-agent', self.uAgents[idx])]    
            #print "Useg-agent Used : "+self.uAgents[idx]
        except Exception, e:
            print "[-] ", e  
            
    def openURL(self):
        try:   
            self.open(self.url)
        except Exception, e:
            print "[-] ", e
            time.sleep(30)
            exit(0)
            
    def viewPageSource(self): 
        try:   
            if(self.url != "None"):
                source=self.open(self.url)
                return source.read()
        except Exception, e:
            print "[-]", e
            time.sleep(30)
            exit(0) 

def main():
    try:
        url=raw_input("Input URL : ")
        sourceSaveFile=raw_input("Input Page Source Save File : ")
        a=anonBrowser(url)
        fp=open(sourceSaveFile,"w")
        fp.write(a.viewPageSource())
        fp.close()
        print "[+] Open the "+sourceSaveFile
        time.sleep(30)
    except Exception, e:
        print "[-] ", e
        time.sleep(30)
        exit(0)
    
if __name__=="__main__":
    main() 