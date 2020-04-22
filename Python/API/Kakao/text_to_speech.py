# -*- coding: utf-8 -*-
import os
import urllib

# https://developers.kakao.com/docs/restapi/speech
# curl -v -X POST "https://kakaoi-newtone-openapi.kakao.com/v1/synthesize" -H "Content-Type: application/xml" -H "Authorization: KakaoAK b555a7f9cf72ca3e10838717c86702e3" -d "<speak><voice>Test</voice></speak>" > test.mp3

dialogic_style = [
    'WOMAN_READ_CALM', # 여성 차분한 낭독체
    'MAN_READ_CALM', # 남성 차분한 낭독체
    'WOMAN_DIALOG_BRIGHT', # 여성 밝은 대화체
    'MAN_DIALOG_BRIGHT' # 남성 밝은 대화체
]
speech_speed = [
    'SS_READ_SPEECH', # 기본 속도
    'SS_ALT_FAST_1', # 빠르게
    'SS_ALT_SLOW_1' # 느리게
]
save_file = 'message.wav' # 생성될 음성 파일

def text_to_speech(message, dialogic, speed):
    try:
        req = urllib.request.Request(
            url = 'https://kakaoi-newtone-openapi.kakao.com/v1/synthesize', # 요청 URL
            data = ('<speak><voice name="' + dialogic + '" speechStyle="' + speed + '">' + message + '</voice></speak>').encode('utf-8'), # HTTP REQUEST BODY
            headers = {
                'Content-Type': 'application/xml', 
                'Authorization': 'KakaoAK b555a7f9cf72ca3e10838717c86702e3' # 카카오 REST API 키
            } # HTTP REQUEST HEADER
        )
        res = urllib.request.urlopen(req) # Send HTTP REQUEST
        fp = open(save_file, 'wb') # 음성 파일 생성
        fp.write(res.read())
        fp.close()
        print('\n[+] ' + os.getcwd() + '\\' + save_file)
    except Exception as e:
        print('\n[-]', e)

def main():
    try:
        message = input('Input message : ') # 메시지
        dialogic = dialogic_style[1] # 낭독체
        speed = speech_speed[2] # 낭독 속도
        text_to_speech(message, dialogic, speed)
    except Exception as e:
        print('\n[-]', e)

if __name__ == '__main__':
    main()