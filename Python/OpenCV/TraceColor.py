# -*- coding: utf-8 -*-
import numpy as np
import cv2

# https://m.blog.naver.com/samsjang/220504633218

def traceColor(device_index):
    try:
        if device_index == '': # 장치를 설정 안 했을 경우
            device_index = '0' # 디폴트 장치 인덱스를 0으로 설정
        cap = cv2.VideoCapture(int(device_index)) # 장치 인덱스(카메라 지정) or 비디오 파일(비디오 파일 재생 시)
        cap.set(3, 480) # 프레임의 가로 길이 설정(3)
        cap.set(4, 320) # 프레임의 세로 길이 설정(4)
    except:
        return
    while True:
        ret, frame = cap.read() # 한 프레임 읽음
        if not ret: # 프레임을 제대로 읽지 못했을 경우
            break
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # HSV 모드로 전환
        # 색 범위 설정
        lower_blue = np.array([110, 100, 100])
        upper_blue = np.array([130, 255, 255])
        lower_green = np.array([50, 100, 100])
        upper_green = np.array([70, 255, 255])
        lower_red = np.array([-10, 100, 100])
        upper_red = np.array([10, 255, 255])
        # HSV 이미지에서 설정한 색 범위만 추출하기 위한 설정
        mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
        mask_green = cv2.inRange(hsv, lower_green, upper_green)
        mask_red = cv2.inRange(hsv, lower_red, upper_red)
        # mask 와 원본 이미지 비트 연산
        frame_blue = cv2.bitwise_and(frame, frame, mask = mask_blue)
        frame_green = cv2.bitwise_and(frame, frame, mask = mask_green)
        frame_red = cv2.bitwise_and(frame, frame, mask = mask_red)
        cv2.imshow('Original', frame) # 프레임 디스플레이
        cv2.imshow('Blue', frame_blue) # Blue 프레임 디스플레이
        cv2.imshow('Green', frame_green) # Green 프레임 디스플레이
        cv2.imshow('Red', frame_red) # Red 프레임 디스플레이
        if (cv2.waitKey(1) & 0xFF) == 27: # ESC 입력 시 종료
            break
    cap.release() # 객체 해제
    cv2.destroyAllWindows() # 생성한 윈도우 제거

def main():
    device_index = raw_input('Input Device Index(Default Enter): ')
    traceColor(device_index)

if __name__ == '__main__':
    main()