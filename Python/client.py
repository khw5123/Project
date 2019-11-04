# -*- coding: utf-8 -*-
import socket
from socket import *

server_ip = '15.164.158.59' # 접속 대상 서버 IP
server_port = 2123 # 접속 대상 서버 Port

def send_data(send_file):
    try:
        sock = socket(
            AF_INET, # IPv4
            SOCK_STREAM # Stream Socket
        ) # 소켓 객체 생성
        sock.connect((
            server_ip, # 접속 서버 IP
            server_port # 접속 서버 Port
        )) # 서버 접속
        print('[+] ' + server_ip + ' connected!')
        fp = open(send_file, 'rb')
        data = fp.read(1024)
        while data:
            sock.send(data) # 데이터 송신
            data = fp.read(1024)
        fp.close()
        sock.close()
        print('[+] Transfer completed!')
    except Exception as e:
        print('[-]', e)

def main():
    send_file = input('Input send file : ')
    send_data(send_file)

if __name__ == '__main__':
    main()