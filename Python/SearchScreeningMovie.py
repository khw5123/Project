#-*- coding: utf-8 -*-
import mechanize, os, time
from bs4 import BeautifulSoup 

def searchMovie():
    browser=mechanize.Browser()
    browser.set_handle_robots(False)
    browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    url="http://movie.naver.com/movie/running/current.nhn?view=list&tab=normal&order=reserve"
    u=browser.open(url)
    source=u.read()
    b_object=BeautifulSoup(source)
    i=1
    os.system("cls")
    print "\n[Screening Movie(Order by Reservation)]"
    for content in b_object.find_all("img"):
        if("자동완성" in str(content) or "NAVER" in str(content) or "영화" in str(content) or "맨위로" in str(content)):
            continue
        print str(i), ". ", content.get('alt')
        i+=1
        
def main():
    searchMovie()
    time.sleep(600)
    
if __name__=="__main__":
    main()
