# -*- coding: utf-8 -*-
import numpy as np
import cv2

# https://m.blog.naver.com/samsjang/220500854338

def showWebcam(device_index, width, height): # 설정한 웹캠을 구동시켜 화면에 디스플레이하는 함수
    try:
        if device_index == '': # 장치를 설정 안 했을 경우
            device_index = '0' # 디폴트 장치 인덱스를 0으로 설정
        cap = cv2.VideoCapture(int(device_index)) # 장치 인덱스(카메라 지정) or 비디오 파일(비디오 파일 재생 시)
        print '[+] Camera settings complete'
    except:
        print '[-] Camera setting failed'
        return
    cap.set(3, width) # 프레임의 가로 길이 설정(3)
    cap.set(4, height) # 프레임의 세로 길이 설정(4)
    print '[+] Start output. Type \'esc\' if you want to exit'
    while True:
        ret, frame = cap.read() # 한 프레임 읽음
        if not ret: # 프레임을 제대로 읽지 못했을 경우
            print '[-] Failed to read frame'
            break
        color = cv2.cvtColor(frame, cv2.IMREAD_COLOR) # 컬러 프레임으로 변환
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # 흑백 프레임으로 변환
        cv2.imshow('Show Webcam', color) # 변환한 프레임을 화면에 디스플레이
        k = cv2.waitKey(1) & 0xFF # 종료 키 설정
        if k == 27: # ESC 입력 시 종료
            print '[+] End output'
            break
    cap.release() # 객체 해제
    cv2.destroyAllWindows() # 생성한 윈도우 제거

def recordWebcam(device_index, save_file): # 설정한 웹캠을 구동시키고 프레임을 저장해서 동영상 파일을 생성하는 함수
    try:
        if device_index == '': # 장치를 설정 안 했을 경우
            device_index = '0' # 디폴트 장치 인덱스를 0으로 설정
        cap = cv2.VideoCapture(int(device_index)) # 장치 인덱스(카메라 지정) or 비디오 파일(비디오 파일 재생 시)
        print '[+] Camera settings complete'
    except:
        print '[-] Camera setting failed'
        return
    fps = 20.0 # 초당 프레임
    width = int(cap.get(3)) # 프레임의 가로 길이 설정(3)
    height = int(cap.get(4)) # 프레임의 세로 길이 설정(4)
    fcc = cv2.VideoWriter_fourcc('D', 'I', 'V', 'X') # DIVX 코덱 적용(이 외에도 XVID, MJPG, X264, WMV1, WMV2 등의 코덱 적용 가능)
    out = cv2.VideoWriter(save_file, fcc, fps, (width, height)) # 전송되는 비디오 스트림을 저장해서 avi 파일로 생성
    print '[+] Start recording. Type \'esc\' if you want to exit'
    while True:
        ret, frame = cap.read() # 한 프레임 읽음
        if not ret: # 프레임을 제대로 읽지 못했을 경우
            print '[-] Failed to read frame'
            break
        cv2.imshow('Record Webcam', frame) # 변환한 프레임을 화면에 디스플레이
        out.write(frame) # avi 파일에 프레임 저장
        k = cv2.waitKey(1) & 0xFF # 종료 키 설정
        if k == 27: # ESC 입력 시 종료
            print '[+] End recording'
            break
    cap.release() # 객체 해제
    out.release() # 객체 해제
    cv2.destroyAllWindows() # 생성한 윈도우 제거

def main():
    device_index = raw_input('Input Device Index(Default Enter): ')
    save_file = raw_input('Input Save File(.avi): ')
    recordWebcam(device_index, save_file)
    # showWebcam(device_index, 500, 500)

if __name__ == '__main__':
    main()