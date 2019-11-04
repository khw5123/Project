# -*- coding: utf-8 -*-
import win32api
import win32con
import cv2
import numpy as np
from PIL import ImageGrab

thresholdMin, thresholdMax = 20, 255 # 최소, 최대 임계값

def videoMotionDetector(videoInput, version):
    if videoInput.isdigit(): # 웹캠 장치 번호일 경우
        cap = cv2.VideoCapture(int(videoInput))
    else: # 동영상 파일명일 경우
        cap = cv2.VideoCapture(videoInput)
    mog = cv2.createBackgroundSubtractorMOG2() # 배경 추출 객체
    while True:
        ret, frame = cap.read() # 현재 프레임
        if not ret: # 프레임을 제대로 읽지 못했을 경우
            break
        if version == '1':
            foreground = mog.apply(frame) # 전경 추출
            cv2.imshow('Video Motion Detector(Foreground Extraction)', foreground) # 프레임 출력
        elif version == '2':
            foreground = mog.apply(frame) # 전경 추출
            edge = cv2.Canny(foreground, thresholdMin, thresholdMax) # 경계 추출
            cv2.imshow('Video Motion Detector(Edge Extraction)', edge) # 프레임 출력
        elif version == '3':
            foreground = mog.apply(frame) # 전경 추출
            edge = cv2.Canny(foreground, thresholdMin, thresholdMax) # 경계 추출
            grey = cv2.cvtColor(edge, cv2.COLOR_GRAY2RGB) # 경계 흑백 변환
            grey[np.where((grey == [255, 255, 255]).all(axis=2))] = [0, 0, 255] # 경계 색 변경
            combine = cv2.add(frame, grey) # 현재 프레임에 경계 추가
            cv2.imshow('Video Motion Detector(Edge Extraction(Color))', combine) # 프레임 출력
        '''
        elif version == '4':
            foreground = mog.apply(frame) # 전경 추출
            pts = np.array(list(map(list, zip(np.nonzero(foreground)[1], np.nonzero(foreground)[0]))), np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(frame, [pts], True, (0, 0, 255)) # 다각형 그리기
            cv2.imshow('Video Motion Detector(Polygone Area Extraction)', frame) # 프레임 출력
        '''
        if cv2.waitKey(1) & 0xFF == 27:
            break	
    cv2.destroyAllWindows()
    cap.release()

def windowsMotionDetector(version):
    global thresholdMin, thresholdMax
    screenWidth = win32api.GetSystemMetrics(win32con.SM_CXSCREEN) # 윈도우 가로 크기
    screenHeight = win32api.GetSystemMetrics(win32con.SM_CYSCREEN) # 윈도우 세로 크기
    mog = cv2.createBackgroundSubtractorMOG2() # 배경 추출 객체
    while True:
        currentScreen = ImageGrab.grab(bbox=(0, 0, screenWidth, screenHeight)) # 윈도우 프레임
        screen = np.array(currentScreen) # 현재 프레임
        if version == '1':
            foreground = mog.apply(screen) # 전경 추출
            cv2.imshow('Windows Motion Detector(Foreground Extraction)', foreground) # 프레임 출력
        elif version == '2':
            foreground = mog.apply(screen) # 전경 추출
            edge = cv2.Canny(foreground, thresholdMin, thresholdMax) # 경계 추출
            cv2.imshow('Windows Motion Detector(Edge Extraction)', edge) # 프레임 출력
        elif version == '3':
            foreground = mog.apply(screen) # 전경 추출
            edge = cv2.Canny(foreground, thresholdMin, thresholdMax) # 경계 추출
            grey = cv2.cvtColor(edge, cv2.COLOR_GRAY2RGB) # 경계 흑백 변환
            grey[np.where((grey == [255, 255, 255]).all(axis=2))] = [0, 0, 255] # 경계 색 변경
            combine = cv2.add(screen, grey) # 현재 프레임에 경계 추가
            cv2.imshow('Windows Motion Detector(Edge Extraction(Color))', combine) # 프레임 출력
        '''
        elif version == '4':
            foreground = mog.apply(screen) # 전경 추출
            pts = np.array(list(map(list, zip(np.nonzero(foreground)[1], np.nonzero(foreground)[0]))), np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(screen, [pts], True, (0, 0, 255)) # 다각형 그리기
            cv2.imshow('Windows Motion Detector(Polygone Area Extraction)', screen) # 프레임 출력
        '''
        if cv2.waitKey(1) & 0xFF == 27:
            break	
    cv2.destroyAllWindows()

def main():
    global thresholdMin, thresholdMax
    sel = input('[Select]\n1. Video Motion Detector\n2. Windows Motion Detector\nselect : ')
    version = input('[Version]\n1. Foreground Extraction\n2. Edge Extraction\n3. Edge Extraction(Color)\nselect : ')
    if version == '1' or version == '2' or version == '3':
        if sel == '1':
            videoInput = input('Input Video File or Webcam Device Number : ')
            hyperSel = input('Input Whether or Not to Set Hyper Parameters(y/n) : ')
            if hyperSel.lower() == 'n' or hyperSel.lower() == 'no':
                videoMotionDetector(videoInput, version)
            elif hyperSel.lower() == 'y' or hyperSel.lower() == 'yes':
                thresholdMin = int(input('Input Minimum Threshold : '))
                thresholdMax = int(input('Input Maximum Threshold : '))
                videoMotionDetector(videoInput, version)
            else:
                print('[-] Input Error')
        elif sel == '2':
            hyperSel = input('Input Whether or Not to Set Hyper Parameters(y/n) : ')
            if hyperSel.lower() == 'n' or hyperSel.lower() == 'no':
                windowsMotionDetector(version)
            elif hyperSel.lower() == 'y' or hyperSel.lower() == 'yes':
                thresholdMin = int(input('Input Minimum Threshold : '))
                thresholdMax = int(input('Input Maximum Threshold : '))
                windowsMotionDetector(version)
            else:
                print('[-] Input Error')
        else:
            print('[-] Input Error')
    else:
        print('[-] Input Error')

if __name__ == '__main__':
    main()