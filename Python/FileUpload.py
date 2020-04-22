#-*- coding: utf-8 -*-
import socket, os, sys, time

def main():
    try:
        uploadFile=raw_input("Input Upload File : ") # 업로드할 파일 입력
        print "\n["+uploadFile+"] Size : "+str(os.path.getsize(uploadFile))+"Byte\n" # 업로드할 파일 크기 출력(바이트 단위)
        targetIP=raw_input("Input Target IP : ") # 업로드 대상 PC의 IP 입력
        connectPort=raw_input("Input Connect Port(10000~65535) : ") # 다운로드 대상 PC와 연결할 포트(둘이 같게 설정)
        while(1): # 주기적으로 연결 시도
            try:
                s=socket.socket(socket.AF_INET, socket.SOCK_STREAM) # 소켓 생성
                s.connect((targetIP, int(connectPort))) # 연결 시도
                break
            except Exception, e: # 업로드 대상 PC와 연결하지 못했을 경우
                print "Try Connect..."
                time.sleep(5) # 잠시 대기
                pass
        print "Start Upload..."
        sys.stdout.flush() # 버퍼 비우기
        fp=open(uploadFile, "rb") # 업로드 파일 열기
        buf=fp.read() # 파일의 바이너리 버퍼에 저장
        fp.close() # 파일 닫기
        s.send(buf) # 바이너리 전송
        confirm=s.recv(100) # 완료 메시지 수신
        print confirm
        s.close() # 소켓 종료
        sys.stdout.flush() # 버퍼 비우기
        time.sleep(600)
    except Exception, e:
        print "[-] ", e
        time.sleep(600)
        s.close()
        exit(0)
        
if __name__=="__main__":
    main()
