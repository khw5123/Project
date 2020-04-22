# -*- coding: utf-8 -*-
import numpy as np
import cv2

# https://m.blog.naver.com/samsjang/220505815055

# Erosion 알고리즘 : 전경(foreground)이 되는 이미지의 경계 부분을 침식시켜 배경(background) 이미지로 전환(이미지가 가늘게 됨)
# Dilation 알고리즘 : 전경(foreground)이 되는 이미지의 경계 부분을 팽창시켜 배경(background) 이미지로 전환(이미지가 굵게 됨)
# Opening 기법 : Erosion 수행 후 Dilation 수행하여 본래 이미지 크기로 돌려놓는 것
# Closing 기법 : Dilation 수행 후 Erosion 수행하여 본래 이미지 크기로 돌려놓는 것

def morph(image_file_opening, image_file_closing):
    img1 = cv2.imread(image_file_opening, cv2.IMREAD_GRAYSCALE) # Opening 을 수행할 이미지를 흑백으로 저장
    img2 = cv2.imread(image_file_closing, cv2.IMREAD_GRAYSCALE) # Closing 을 수행할 이미지를 흑백으로 저장
    kernel = np.ones((5, 5), np.uint8) # 5x5 크기의 1로 채워진 매트릭스 생성
    opening = cv2.morphologyEx(img1, cv2.MORPH_OPEN, kernel) # Erosion, Dilation 알고리즘을 이용해서 노이즈 제거
    closing = cv2.morphologyEx(img2, cv2.MORPH_CLOSE, kernel) # Erosion, Dilation 알고리즘을 이용해서 노이즈 제거
    cv2.imshow('Original Opening', img1) # 원본 이미지 디스플레이
    cv2.imshow('Opening', opening) # Opening 적용한 이미지 디스플레이
    cv2.imshow('Original Closing', img2) # 원본 이미지 디스플레이
    cv2.imshow('Closing', closing) # Closing 적용한 이미지 디스플레이
    cv2.waitKey(0) # 키 입력할 때까지 대기
    cv2.destroyAllWindows()

def main():
    image_file_opening = raw_input('Input Opening Image : ')
    image_file_closing = raw_input('Input Closing Image : ')
    morph(image_file_opening, image_file_closing)

if __name__ == '__main__':
    main()