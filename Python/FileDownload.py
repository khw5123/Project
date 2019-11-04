#-*- coding: utf-8 -*-
import socket, sys, time

def hexdump(src, length=16): # 다운로드한 파일의 바이너리를 출력하는 함수
    result=[]
    digits=4 if isinstance(src, unicode) else 2
    for i in xrange(0, len(src), length):
       s=src[i:i+length]
       hexa=b' '.join(["%0*X" % (digits, ord(x))  for x in s])
       text=b''.join([x if 0x20 <= ord(x) < 0x7F else b'.'  for x in s])
       result.append( b"%04X   %-*s   %s" % (i, length*(digits + 1), hexa, text) )
    print b'\n'.join(result)

def main():
    try:
        interfaceList=socket.gethostbyname_ex(socket.gethostname()) # PC 내 랜카드(인터페이스) 수에 따른 IP 리스트 얻음
        print "\n[List]"
        for i in range(0, len(interfaceList)+1):
            try:
                print str(i)+". "+interfaceList[2][i]
            except Exception, e:
                pass
        selectIP=raw_input("\nSelect Number : ")
        localIP="" # 사용할 최종적인 IP
        for i in range(0, len(interfaceList[2])):
            if(int(selectIP)==i):
                localIP=interfaceList[2][i]
                break
        downloadFile=raw_input("Input Save File : ") # 다운로드 받은 파일을 PC에 저장할 파일명 입력
        maxFileSize=raw_input("Input Max File Size(Byte) : ") # 다운로드할 파일의 크기보다 같거나 큰 값 입력(버퍼의 크기로 바이트 단위임) 
        connectPort=raw_input("Input Connect Port(10000~65535) : ") # 다운로드 대상 PC와 연결할 포트(둘이 같게 설정)
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM) # 소켓 생성
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # 소켓 설정
        s.bind((localIP, int(connectPort))) # 설정한 IP와 포트로 바인딩
        s.listen(10) # 연결 대기
        print "\nWait..."
        conn, addr=s.accept() # 연결 시도가 있으면 연결
        print "\nStart Download... "
        sys.stdout.flush() # 버퍼 비우기
        buf=conn.recv(int(maxFileSize)) # 다운로드 파일 바이너리 수신 후 버퍼에 저장
        fp=open(downloadFile, "wb") # 저장할 파일 열고
        fp.write(buf) # 바이너리 쓰기
        fp.close() # 파일 닫기
        hexdump(buf) # 다운로드 파일 바이너리 출력 함수
        print "[+] Download Complete!"
        conn.send("\n[+] Upload Complete!") # 완료 메시지 전송
        conn.close() # 연결 해제
        s.close() # 소켓 종료
        sys.stdout.flush() # 버퍼 비우기
        time.sleep(600)
    except Exception, e:
        print "[-] ", e
        time.sleep(600)
        conn.close()
        exit(0)
        
if __name__=="__main__":
    main()
