# -*- coding: utf-8 -*-
import requests

# https://developers.kakao.com/docs/restapi/translation

language = {
    '한국어': 'kr', 
    '영어': 'en', 
    '일본어': 'jp', 
    '중국어':	'cn', 
    '베트남어': 'vi', 
    '인도네시아어': 'id', 
    '아랍어':	'ar', 
    '뱅갈어':	'bn', 
    '독일어':	'de', 
    '스페인어': 'es', 
    '프랑스어': 'fr', 
    '힌디어': 'hi', 
    '이탈리아어':	'it', 
    '말레이시아어': 'ms', 
    '네덜란드어':	'nl', 
    '포르투갈어': 'pt', 
    '러시아어': 'ru', 
    '태국어': 'th', 
    '터키어': 'tr'
}

def translage(message, src_lang, dst_lang):
    try:
        res = requests.get(
            url='https://kapi.kakao.com/v1/translation/translate', 
            headers={'Authorization': 'KakaoAK b555a7f9cf72ca3e10838717c86702e3'}, 
            params=(
                ('src_lang', language[src_lang]), 
                ('target_lang', language[dst_lang]), 
                ('query', message)
            )
        )
        print(res.json()['translated_text'])
    except Exception as e:
        print('\n[-]', e)

def main():
    try:
        src_lang = input('Input src language : ') # 번역 대상 언어
        dst_lang = input('Input dst language : ') # 번역하고 싶은 언어
        message = input('Input message : ') # 메시지
        translage(message, src_lang, dst_lang)
    except Exception as e:
        print('\n[-]', e)

if __name__ == '__main__':
    main()