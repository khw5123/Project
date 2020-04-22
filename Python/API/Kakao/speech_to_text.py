# -*- coding: utf-8 -*-
import urllib

# https://developers.kakao.com/docs/restapi/speech
# curl -v -X POST "https://kakaoi-newtone-openapi.kakao.com/v1/recognize" -H "Transfer-Encoding: chunked" -H "Content-Type: application/octet-stream" -H "X-DSS-Service: DICTATION" -H "Authorization: KakaoAK b555a7f9cf72ca3e10838717c86702e3" --data-binary @test.mp3

def speech_to_text(speech_file):
    try:
        req = urllib.request.Request(
            url = 'https://kakaoi-newtone-openapi.kakao.com/v1/recognize', # 요청 URL
            data = open(speech_file, 'rb').read(), # HTTP REQUEST BODY
            headers = {
                'Transfer-Encoding': 'chunked', 
                'Content-Type': 'application/octet-stream', 
                'X-DSS-Service': 'DICTATION', 
                'Authorization': 'KakaoAK b555a7f9cf72ca3e10838717c86702e3' # 카카오 REST API 키
            } # HTTP REQUEST HEADER
        )
        res = urllib.request.urlopen(req).read().decode('utf-8') # Send HTTP REQUEST
        print(res)
    except Exception as e:
        print('[-]', e)

def main():
    try:
        speech_file = input('Input speech file : ') # 음성 파일
        speech_to_text(speech_file)
    except Exception as e:
        print('[-]', e)

if __name__ == '__main__':
    main()