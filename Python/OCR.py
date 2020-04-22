# -*- coding: utf-8 -*-
from PIL import Image
import pytesseract

# https://m.blog.naver.com/samsjang/220694855018

languageList = ['eng', # 영어
                'kor', # 한국어
                'outputbase digits' # 숫자
                ]

def OCR(image_file, language):
    im = Image.open(image_file) # 이미지 저장
    if language == 'outputbase digits': # 숫자로 설정한 경우
        text = pytesseract.image_to_string(im, config=language) # 이미지에 있는 숫자 인식 후 저장
    else: # 숫자로 설정하지 않았을 경우
        text = pytesseract.image_to_string(im, lang=language) # 이미지에 있는 문자 인식 후 저장
    return text # 인식된 문자 반환

def main():
    global languageList
    image_file = input('Input Image File : ')
    language = input('\n[Language]\n1. English\n2. Korean\n3. Number\nSelect : ')
    text = OCR(image_file, languageList[int(language) - 1])
    print(text)

if __name__ == '__main__':
    main()