# -*- coding: utf-8 -*-
import numpy as np
import cv2

# https://m.blog.naver.com/samsjang/220507996391

# Canny Edge Detection 알고리즘 : 경계 찾기 알고리즘
# 1단계 : 5x5 Gaussian Filter를 적용해 이미지의 노이즈 제거
# 2단계 : 노이즈가 제거된 이미지를 Sobel 커널을 수평, 수직 방향으로 적용해서 각 방향의 gradient 획득
# 3단계 : edge(경계)에 기여하지 않은 픽셀을 제거하기 위해 이미지 전체를 스캔하면서 gradient 방향으로 스캔 구역에서 gradient의 최대값을 가진 픽셀을 찾음
# 4단계 : 3단계에서 찾은 픽셀들이 실제 edge(경계)인지 판단(문턱값(minVal, maxVal)을 설정하고, maxVal 보다 높은 부분은 edge이고, minVal 보다 낮은 부분은 edge 가 아니라고 판단. 두 값의 중간에 있는 부분은 픽셀들의 연결 구조를 보고 edge 인지 아닌지 판단)

def canny(image_file, minVal, maxVal):
    img = cv2.imread(image_file, cv2.IMREAD_GRAYSCALE) # 원본 이미지 흑백으로 저장
    edge1 = cv2.Canny(img, minVal, maxVal) # Canny Edge Detection 함수(img, minimum thresholding value, maximum thresholding value)
    cv2.imshow('Original', img) # 원본 이미지 디스플레이
    cv2.imshow('Canny Edge', edge1) # Canny Edge Detection 알고리즘 적용된 이미지 디스플레이
    cv2.waitKey(0) # 키 입력할 때까지 대기
    cv2.destroyAllWindows()

def main():
    image_file = raw_input('Input Image File : ')
    minVal = raw_input('Input Minimum Thresholding Value : ')
    maxVal = raw_input('Input Maximum Thresholding Value : ')
    canny(image_file, int(minVal), int(maxVal))

if __name__ == '__main__':
	main()