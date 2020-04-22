# -*- coding: utf-8 -*-
import numpy as np
import cv2

# https://m.blog.naver.com/samsjang/220664036092

def backgroundSubtractor(device_index):
    try:
        if device_index == '': # 장치를 설정 안 했을 경우
            device_index = '0' # 디폴트 장치 인덱스를 0으로 설정
        cap = cv2.VideoCapture(int(device_index)) # 장치 인덱스(카메라 지정) or 비디오 파일(비디오 파일 재생 시)
        cap.set(3, 1000) # 프레임의 가로 길이 설정(3)
        cap.set(4, 500) # 프레임의 세로 길이 설정(4)
    except:
        return
    mog = cv2.createBackgroundSubtractorMOG2() # 배경 제거 함수 설정
    while True:
        ret, frame = cap.read() # 한 프레임 읽음
        fgmask = mog.apply(frame) # 프레임에 배경 제거 기법 적용
        cv2.imshow('Background Subtraction', fgmask) # 프레임 화면에 디스플레이
        if (cv2.waitKey(1) & 0xFF) == 27: # ESC 입력 시 종료
            break	
    cap.release() # 객체 해제
    cv2.destroyAllWindows() # 생성한 윈도우 제거

def main():
    device_index = input('Input Device Index(Default Enter): ')
    backgroundSubtractor(device_index)

if __name__ == '__main__':
    main()