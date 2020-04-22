# -*- coding: utf-8 -*-
import numpy as np
import cv2

# https://m.blog.naver.com/samsjang/220663565072

def denseOptFlow(device_index):
    try:
        if device_index == '': # 장치를 설정 안 했을 경우
            device_index = '0' # 디폴트 장치 인덱스를 0으로 설정
        cap = cv2.VideoCapture(int(device_index)) # 장치 인덱스(카메라 지정) or 비디오 파일(비디오 파일 재생 시)
        cap.set(3, 1000) # 프레임의 가로 길이 설정(3)
        cap.set(4, 500) # 프레임의 세로 길이 설정(4)
    except:
        return
    ret, frame = cap.read() # 초기(이전) 프레임 읽음
    prev = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # 초기(이전) 프레임 흑백으로 변환
    hsv = np.zeros_like(frame)
    hsv[...,1] = 255
    while True:
        ret, frame = cap.read() # 한 프레임 읽음
        next = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # 현재 프레임 흑백으로 변환
        flow = cv2.calcOpticalFlowFarneback(prev, next, 0.0, 0.5, 3, 15, 3, 5, 1.2, 0)
        mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
        hsv[...,0] = ang*180/np.pi/2
        hsv[...,2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
        rgb = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        cv2.imshow('Movement Optical Flow', rgb) # 변환된 프레임 화면에 디스플레이
        if (cv2.waitKey(1) & 0xFF) == 27: # ESC 입력 시 종료
            break
        prev = next # 현재 프레임을 이전 프레임에 저장
    cap.release() # 객체 해제
    cv2.destroyAllWindows() # 생성한 윈도우 제거

def main():
    device_index = input('Input Device Index(Default Enter): ')
    denseOptFlow(device_index)

if __name__ == '__main__':
    main()