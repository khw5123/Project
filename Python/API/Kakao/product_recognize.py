# -*- coding: utf-8 -*-
import os
import requests
from io import BytesIO
from PIL import Image, ImageDraw

# https://developers.kakao.com/docs/restapi/vision#%EC%83%81%ED%92%88-%EA%B2%80%EC%B6%9C

save_file = 'result.png'

def product_recognize_url(image_url):
    try:
        res = requests.post(
            url='https://kapi.kakao.com/v1/vision/product/detect', 
            headers={'Authorization': 'KakaoAK {}'.format('b555a7f9cf72ca3e10838717c86702e3')}, 
            data={'image_url' : image_url}
        )
        product_info = res.json()
        # print(product_info)
        image_res = requests.get(image_url)
        file_jpgdata = BytesIO(image_res.content)
        image = Image.open(file_jpgdata)
        draw = ImageDraw.Draw(image)
        for obj in product_info['result']['objects']:
            x1 = int(obj['x1'] * image.width)
            y1 = int(obj['y1'] * image.height)
            x2 = int(obj['x2'] * image.width)
            y2 = int(obj['y2'] * image.height)
            draw.rectangle([(x1, y1), (x2, y2)], outline=(0, 0, 255))
            draw.text((x1, y1 + (y2 - y1)), obj['class'], fill=(0, 0, 255))
            image.save(save_file, 'png')
        print('\n[+] ' + os.getcwd() + '\\' + save_file)
        image.show()
    except Exception as e:
        print('[-]', e)

def product_recognize_file(image_file):
    try:
        res = requests.post(
            url='https://kapi.kakao.com/v1/vision/product/detect', 
            headers={'Authorization': 'KakaoAK {}'.format('b555a7f9cf72ca3e10838717c86702e3')}, 
            files={'file' : open(image_file, 'rb')}
        )
        product_info = res.json()
        # print(product_info)
        image = Image.open(image_file)
        draw = ImageDraw.Draw(image)
        for obj in product_info['result']['objects']:
            x1 = int(obj['x1'] * image.width)
            y1 = int(obj['y1'] * image.height)
            x2 = int(obj['x2'] * image.width)
            y2 = int(obj['y2'] * image.height)
            draw.rectangle([(x1, y1), (x2, y2)], outline=(0, 0, 255))
            draw.text((x1, y1 + (y2 - y1)), obj['class'], fill=(0, 0, 255))
            image.save(save_file, 'png')
        print('\n[+] ' + os.getcwd() + '\\' + save_file)
        image.show()
    except Exception as e:
        print('\n[-]', e)

def main():
    try:
        image = input('Input image file or url : ')
        if 'http' in image:
            product_recognize_url(image)
        else:
            product_recognize_file(image)
    except Exception as e:
        print('[-]', e)

if __name__ == '__main__':
    main()