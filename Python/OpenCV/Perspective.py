# -*- coding: utf-8 -*-
import numpy as np
import cv2

# https://m.blog.naver.com/samsjang/220504966397

def perspective(image_file):
    img = cv2.imread(image_file)
    h, w = img.shape[:2]
    pts1 = np.float32([[0, 0], [300, 0], [0, 300], [300, 300]]) # 변환 전 좌표
    pts2 = np.float32([[56, 65], [368, 0], [28, 387], [150, 390]]) # 변환 후 좌표
    M = cv2.getPerspectiveTransform(pts1, pts2) # 원근감을 주는 변환 매트릭스를 구하는 함수(4개의 좌표로 된 인자 필요)
    img2 = cv2.warpPerspective(img, M, (w, h)) # 변환 매트릭스를 이용해서 원근감을 주는 함수
    cv2.imshow('Original', img) # 원본 이미지 디스플레이
    cv2.imshow('Perspective-Transform', img2) # 원근 이미지 디스플레이
    cv2.waitKey(0) # 키 입력할 때까지 대기
    cv2.destroyAllWindows()

def transform(image_file):
    img = cv2.imread(image_file)
    h, w = img.shape[:2]
    pts1 = np.float32([[50, 50], [200, 50], [20, 200]]) # 변환 전 좌표
    pts2 = np.float32([[10, 100], [200, 50], [100, 250]]) # 변환 후 좌표
    M = cv2.getAffineTransform(pts1, pts2) # 좌표 (50, 50), (200, 50), (20, 200) 을 각각 (10, 100), (200, 50), (100, 250)으로 변환한 매트릭스 저장	
    img2 = cv2.warpAffine(img, M, (w, h)) # 변환 매트릭스를 이용해서 원근감을 주는 함수
    cv2.imshow('Original', img) # 원본 이미지 디스플레이
    cv2.imshow('Affine-Transform', img2) # 원근 이미지 디스플레이
    cv2.waitKey(0) # 키 입력할 때까지 대기
    cv2.destroyAllWindows()

def main():
    image_file = raw_input('Input Image File : ')
    transform(image_file)
    perspective(image_file)

if __name__ == '__main__':
    main()