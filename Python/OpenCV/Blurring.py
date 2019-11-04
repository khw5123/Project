# -*- coding: utf-8 -*-
import numpy as np
import cv2

# https://m.blog.naver.com/samsjang/220505080672

# low-pass filter(LPF) : 노이즈를 제거하거나 이미지를 블러링 하기 위해 사용
# high-pass filter(HPF) : 이미지에서 경계를 찾기 위해 사용
# averaging filter : 이미지의 픽셀 값을 해당 픽셀의 이웃과 평균하여 값을 취하는 방법 이용

def averaging(image_file):
    img = cv2.imread(image_file)
    kernel = np.ones((5, 5), np.float32)/25 # 픽셀을 중심으로 5x5 영역 생성 후 이 영역의 모든 픽셀 값을 더하고 더한 값을 25로 나눈 값을 중심 픽셀 값으로 취함
    blur = cv2.filter2D(img, -1, kernel) # 위 커널이 적용된 Averaging Filter는 5x5 영역 내의 모든 픽셀 값들의 평균값을 취함	
    cv2.imshow('Original', img) # 원본 이미지 디스플레이
    cv2.imshow('Bluring', blur) # 블러링 이미지 디스플레이
    cv2.waitKey(0) # 키 입력할 때까지 대기
    cv2.destroyAllWindows()

def onMouse(x):
	pass	

def blurring(image_file):
    img = cv2.imread(image_file)
    cv2.namedWindow('BlurPane')
    cv2.createTrackbar('BLUR_MODE', 'BlurPane', 0, 2, onMouse)
    cv2.createTrackbar('BLUR', 'BlurPane', 0, 5, onMouse)
    mode = cv2.getTrackbarPos('BLUR_MODE', 'BlurPane')
    val = cv2.getTrackbarPos('BLUR', 'BlurPane')
    while True:
        val = val * 2 + 1
        try:
            if mode == 0:
                blur = cv2.blur(img, (val, val)) # Averaging Blur(이미지의 픽셀 값을 해당 픽셀의 이웃과 평균하여 값을 취함. 두 val 값이 달라도 됨)
            elif mode == 1:
                blur = cv2.GaussianBlur(img, (val, val), 0) # Gaussian Filter(두 val 값이 달라도 되지만 모두 양의 홀수여야 함. 가우스 노이즈를 제거하는데 효과적)
            elif mode == 2:
                blur = cv2.medianBlur(img, val) # Median Filter(val x val 크기의 박스 내에 있는 모든 픽셀들의 median 값을 취해서 중앙에 있는 픽셀에 적용함. 소금-후추 노이즈를 제거하는데 효과적)
            else:
                break
            cv2.imshow('BlurPane', blur)
        except:
            break
        if (cv2.waitKey(1) & 0xFF) == 27: # ESC 입력 시 종료
            break
        mode = cv2.getTrackbarPos('BLUR_MODE', 'BlurPane')
        val = cv2.getTrackbarPos('BLUR', 'BlurPane')
    cv2.destroyAllWindows()	

def main():
    image_file = raw_input('Input Image File : ')
    # averaging(image_file)
    blurring(image_file)

if __name__ == '__main__':
    main()