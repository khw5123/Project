#-*- coding: utf-8 -*-
import re, sqlite3

def download(downloadDB):
    try:
        conn=sqlite3.connect(downloadDB) #DB로의 연결생성
        c=conn.cursor() #프롬프트 요구
        c.execute('SELECT name, source, datetime(endTime/1000000,\
                    \'unixepoch\') FROM moz_downloads;') # sqlite 데이터베이스 조회
        print "\n[Found Download Files]"
        count=1
        for row in c:
            name=str(row[0])
            source=str(row[1])
            time=str(row[2])
            print "File"+str(count)+" : "+name+"\nSource"+str(count)+" : "+source+"\At"+str(count)+" : "+time
            count+=1
    except Exception, e:
        print "[-] ", e
        pass 
    
def cookie(cookiesDB):
    try:
        conn=sqlite3.connect(cookiesDB)
        c=conn.cursor()
        c.execute('SELECT host, name, value FROM moz_cookies')
        print "\n[Found Cookies]"
        count=1
        for row in c:
            host=str(row[0])
            name=str(row[1])
            value=str(row[2])
            print "Host"+str(count)+" : "+host+"\nCookie"+str(count)+" : "+name+"\nValue"+str(count)+" : "+value
            count+=1
    except Exception, e:
        if "encrypted" in str(e): #오래된 버전의 sqlite3 라이브러리로 해당 파일을 열려고 할 때 발생하는 에러
            print "[-] Error reading your cookies database"
            print "[-] Upgrade your python-sqlite3 Library"
            return
        print "[-] ", e
        pass
    
def history(placesDB):
    try:
        conn=sqlite3.connect(placesDB)
        c=conn.cursor()
        c.execute("select url, datetime(visit_date/1000000, \
          'unixepoch') from moz_places, moz_historyvisits \
          where visit_count > 0 and moz_places.id==\
          moz_historyvisits.place_id;")
        print "\n[Found History]"
        count=1
        for row in c:
            url=str(row[0])
            date=str(row[1])
            print "URL"+str(count)+" : "+url+"\nDate"+str(count)+" : "+date
            count+=1
    except Exception, e:
        if "encrypted" in str(e): 
            print "[-] Error reading your cookies database"
            print "[-] Upgrade your python-sqlite3 Library"
            return
        print "[-] ", e
        pass

def google(placesDB):
    try:
        conn=sqlite3.connect(placesDB)
        c=conn.cursor()
        c.execute("select url, datetime(visit_date/1000000, \
          'unixepoch') from moz_places, moz_historyvisits \
          where visit_count > 0 and moz_places.id==\
          moz_historyvisits.place_id;")
        print "\n[Found Google Search]"
        count=1
        for row in c:
            url=str(row[0])
            date=str(row[1])
            if "google" in url.lower():
                if "q=" in url.lower():
                    search=url.split('q=')[-1]
                    search=search.replace('+',' ')
                    b=True
                    GoogleSearch=""
                    for ch in search:
                        if b:
                            GoogleSearch+=ch
                        if(ch=='&'):
                            b=False
                            GoogleSearch=GoogleSearch.strip('&')
                    print "Google Search"+str(count)+" : "+GoogleSearch+"\nDate"+str(count)+" : "+date
                    count+=1
    except Exception, e:
        if "encrypted" in str(e): 
            print "[-] Error reading your cookies database"
            print "[-] Upgrade your python-sqlite3 Library"
            return
        print "[-] ", e
        
def main():
    print "[downloads.sqlite, cookies.sqlite, places.sqlite]"
    while(1):
        file=raw_input("\nInput Filefox Profile : ")
        if "downloads.sqlite" in file:
            download(file)
        elif "cookies.sqlite" in file: # C:\\Users\\Mine\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\cwj5uys5.default\\places.sqlite
            cookie(file)
        elif "places.sqlite" in file: # /root/.mozilla/firefox/km2ufa9l.default/places.sqlite
            history(file)
            google(file)

if __name__=="__main__":
    main()