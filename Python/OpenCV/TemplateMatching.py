# -*- coding: utf-8 -*-
import numpy as np
import cv2
import matplotlib.pyplot as plt

# https://m.blog.naver.com/samsjang/220576634778

# 템플릿 매칭 : 이미지 내에 있는 부분 이미지(템플릿 이미지)를 찾는 기법

def templateMatching_threshold(image_file, template_image_file, threshold): # threshold 인자는 찾고자 하는 이미지의 형태가 얼마나 동일한가를 체크하는 변수임(1.0에 가까울 경우 완전히 동일할 경우만 찾음(진탐률은 높으나 탐지하지 못할 가능성이 높음), 0에 가까울 경우 동일하지 않을 경우도 찾음(오탐률은 높으나 탐지할 가능성이 높음))
    img = cv2.imread(image_file) # 원본 이미지
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # 원본 이미지 흑백으로 저장
    template = cv2.imread(template_image_file, cv2.IMREAD_GRAYSCALE) # 템플릿 이미지 흑백으로 저장
    w, h = template.shape[::-1] # 템플릿 이미지의 가로, 세로 길이 저장
    res = cv2.matchTemplate(imgray, template, cv2.TM_CCOEFF_NORMED) # 템플릿 이미지와 타겟 이미지 비교
    loc = np.where(res >= threshold) # 설정한 threshold 값 보다 matchTemplate 함수의 리턴 값이 더 클 경우 해당 위치값 저장(여러 개의 매칭 된 이미지 찾음)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2) # 매칭 된 범위 표시
    cv2.imshow('TemplateMatching', img) # 템플릿 매칭 이미지 디스플레이
    cv2.waitKey(0) # 키 입력할 때까지 대기
    cv2.destroyAllWindows()

def templateMatching(image_file, template_image_file):
    img1 = cv2.imread(image_file, cv2.IMREAD_GRAYSCALE) # 원본 이미지 흑백으로 저장
    img2 = img1.copy() # 원본 이미지 복사본 저장
    template = cv2.imread(template_image_file, cv2.IMREAD_GRAYSCALE) # 템플릿 이미지 흑백으로 저장
    w, h = template.shape[::-1] # 템플릿 이미지의 가로, 세로 길이 저장
    methods = ['cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR', 'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED'] # 템플릿 매칭 방법
    for meth in methods:
        img1 = img2.copy() # 복사본 이미지로 초기화
        method = eval(meth) # 템플릿 매칭 방법 설정
        try:
            res = cv2.matchTemplate(img1, template, method) # 템플릿 이미지와 타겟 이미지 비교(method는 비교 연산하는 방법으로 결과 값의 최대값을 취해야 할지 최소값을 취해야 할지를 결정해야 하는데 cv2.TM_SQDIFF 와 cv2.TM_SQDIFF_NORMED일 경우에는 최소값을 그 이외의 경우에는 최대값을 취함)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res) # 템플릿 매칭 성공 시 최대값, 최소값, 위치값 저장
        except:
            print '[-] Error' + str(meth)
            continue
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]: # 템플릿 매칭 방법이 cv2.TM_SQDIFF 또는 cv2.TM_SQDIFF_NORMED일 경우
            top_left = min_loc # 최소값을 좌측 상단으로 설정
        else: # 그 이외의 템플릿 매칭 방법일 경우
            top_left = max_loc # 최대값을 좌측 상단으로 설정
        # print top_left # Test
        bottom_right = (top_left[0] + w, top_left[1] + h) # 우측 하단 설정
        cv2.rectangle(img1, top_left, bottom_right, 0, 5) # 매칭 된 범위 표시
        plt.subplot(121), plt.imshow(res, cmap='gray')
        plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
        plt.subplot(122), plt.imshow(img1, cmap='gray')
        plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
        plt.suptitle(meth)
        plt.show()

def main():
    sel = raw_input('\n1. Template Matching\n2. Multiple Template Matching\n\nSelect : ')
    image_file = raw_input('Input Image File : ')
    template_image_file = raw_input('Input Template Image File : ')
    if sel == '1':
        templateMatching(image_file, template_image_file)
    elif sel == '2':
        error_value = raw_input('Input Error Value(0.0 ~ 1.0): ')
        if float(error_value) > 1.0 or float(error_value) < 0.0:
            error_value = '0.6'
        templateMatching_threshold(image_file, template_image_file, float(error_value))

if __name__ == '__main__':
    main()