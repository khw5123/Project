# -*- coding: utf-8 -*-
import os
import requests
from PIL import Image, ImageDraw

# https://developers.kakao.com/docs/restapi/vision#%EC%96%BC%EA%B5%B4-%EA%B2%80%EC%B6%9C

save_file = 'result.png'

def face_recognize(image_file):
    try:
        res = requests.post(
            url='https://kapi.kakao.com/v1/vision/face/detect', 
            headers={'Authorization': 'KakaoAK {}'.format('b555a7f9cf72ca3e10838717c86702e3')}, 
            files={'file' : open(image_file, 'rb')}
        )
        face_info = res.json()
        # print(face_info)
        image = Image.open(image_file)
        draw = ImageDraw.Draw(image)
        for face in face_info['result']['faces']:
            x = int(face['x'] * image.width)
            w = int(face['w'] * image.width)
            y = int(face['y'] * image.height)
            h = int(face['h'] * image.height)
            draw.rectangle(((x, y), (x + w, y + h)), outline='black')
            draw.text((x, y + h), 'Deteced', fill='black')
            image.save(save_file, 'png')
        print('\n[+] ' + os.getcwd() + '\\' + save_file)
        image.show()
    except Exception as e:
        print('\n[-]', e)

def main():
    try:
        image_file = input('Input face image file : ') # 얼굴 이미지 파일
        face_recognize(image_file)
    except Exception as e:
        print('\n[-]', e)

if __name__ == '__main__':
    main()