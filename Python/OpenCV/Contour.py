# -*- coding: utf-8 -*-
import numpy as np
import cv2

# https://m.blog.naver.com/samsjang/220516697251

# Image Contour : 동일한 색(동일한 색상 강도)을 가진 부분의 가장자리 경계를 연결한 선

def contour(image_file):
    img = cv2.imread(image_file)
    img2 = img.copy() # 원본 이미지 복사본 저장(원본 이미지 변경됨)
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # 이미지 흑백으로 변환
    # opencv에서 contour 찾기는 검은색 배경에서 흰색 대상을 찾는 것임. 따라서 경계를 찾고자 하는 대상은 흰색으로, 배경은 검은색으로 변경해야 됨
    ret, thr = cv2.threshold(imgray, 210, 255, 0) # thresholding
    _, contours, _ = cv2.findContours(thr, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # Suzuki85 알고리즘을 사용해 이미지에서 경계를 찾음
    # _, contours, _ = cv2.findContours(thr, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE) # CHAIN_APPROX_NONE의 경우 경계를 구성하는 모든 점을 저장하는 반면에 CHAIN_APPROX_SIMPLE은 경계의 수평, 수직, 대각선 방향의 점은 모두 버리고 끝 점만 남겨둠(성능의 차이가 있고(CHAIN_APPROX_NONE이 더 많은 메모리 사용), CHAIN_APPROX_SIMPLE을 사용할 경우 경계가 안 그려질 수 있음)
    cv2.drawContours(img, contours, -1, (0, 0, 255), 1) # 찾은 경계를 그리는 함수(대상 이미지, 이미지에 그릴 contour, 이미지에 실제로 그릴 contour 인덱스(음수일 경우 모든 contour를 그림), contour 선의 RGB, contour 선의 두께)
    cv2.imshow('Original', img2) # 원본 이미지 디스플레이
    # cv2.imshow('Threshold', thr) # thresholding 이미지 디스플레이
    cv2.imshow('Contour', img) # Contour 이미지 디스플레이
    cv2.waitKey(0) # 키 입력할 때까지 대기
    cv2.destroyAllWindows()

def main():
    image_file = input('Input Image File : ')
    contour(image_file)

if __name__ == '__main__':
    main()