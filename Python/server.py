# -*- coding: utf-8 -*-
import os
import socket
from socket import *

server_port = 2123 # 서버 오픈 Port
save_file = 'result.mp3' # 결과 파일 (보내는 프로그램의 종류에 따라 확장자 변동되므로 미부여)

def receive_data():
    try:
        sock = socket(
            AF_INET, # IPv4
            SOCK_STREAM # Stream Socket
        ) # 소켓 객체 생성
        sock.bind((
            '', # 서버 IP (공백 시 루프백 주소)
            server_port # 서버 오픈 Port
        )) # 바인딩
        print('Waiting for connection...')
        sock.listen(1) # 데이터 수신 대기 (동시 접속 허용 수)
        sock_connect, addr = sock.accept() # 클라이언트와 연결 성공 시 호출
        print('[+] ' + str(addr) + ' connected!')
        fp = open(save_file, 'wb')
        data = sock_connect.recv(1024) # 데이터 수신
        while data:
            fp.write(data)
            data = sock_connect.recv(1024) # 데이터 수신
        fp.close()
        sock_connect.close()
        sock.close()
        print('\n[+] ' + os.getcwd() + '\\' + save_file)
    except Exception as e:
        print('[-]', e)

def main():
    receive_data()

if __name__ == '__main__':
    main()