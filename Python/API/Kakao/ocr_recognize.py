# -*- coding: utf-8 -*-
import cv2
import json
import requests

# https://developers.kakao.com/docs/restapi/vision#OCR

def ocr_recognize(image_file):
    try:
        image = cv2.imread(image_file)
        jpeg_image = cv2.imencode('.jpg', image)[1]
        data = jpeg_image.tobytes()
        res = requests.post(
            url='https://kapi.kakao.com/v1/vision/text/detect', 
            headers={'Authorization': 'KakaoAK {}'.format('b555a7f9cf72ca3e10838717c86702e3')}, 
            files={'file': data}
        )
        boxes = res.json()['result']['boxes']
        res = requests.post(
            url='https://kapi.kakao.com/v1/vision/text/recognize', 
            headers={'Authorization': 'KakaoAK {}'.format('b555a7f9cf72ca3e10838717c86702e3')}, 
            files={'file': data}, 
            data={'boxes': json.dumps(boxes)}
        )
        print(res.json()['result']['recognition_words'][::-1])
    except Exception as e:
        print('\n[-]', e)

def main():
    try:
        image_file = input('Input image file : ') # 이미지 파일
        ocr_recognize(image_file)
    except Exception as e:
        print('\n[-]', e)

if __name__ == '__main__':
    main()