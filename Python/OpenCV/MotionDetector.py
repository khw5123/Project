# -*- coding: utf-8 -*-
import win32api
import win32con
import cv2
import numpy as np
from PIL import ImageGrab

# 하이퍼 파라미터
thresholdMin, thresholdMax = 20, 255 # 최소, 최대 임계값
dilateSize, dilateIter = 3, 3 # dilate 필터 크기, 팽창 연산 반복 횟수
rectWidthMin, rectHeightMin = 40, 40 # 움직임 탐지 박스 가로, 세로 크기의 최솟값(해당 크기 이하의 움직임 탐지 박스 미 출력)

# 동영상 파일 또는 웹캠을 대상으로 하는 움직임 탐지 함수
def videoMotionDetector(videoInput):
    global thresholdMin, thresholdMax, dilateSize, dilateIter, rectWidthMin, rectHeightMin
    if videoInput.isdigit(): # 웹캠 장치 번호일 경우
        cap = cv2.VideoCapture(int(videoInput))
    else: # 동영상 파일명일 경우
        cap = cv2.VideoCapture(videoInput)
    ret, previousFrame = cap.read() # 이전 프레임
    ret, currentFrame = cap.read() # 현재 프레임
    while ret:
        diff = cv2.absdiff(previousFrame, currentFrame) # 두 프레임 행렬 간의 요소별 절대 차이 계산
        grey = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY) # 프레임 흑백 변환
        blur = cv2.GaussianBlur(grey, (5, 5), 0) # 5 x 5 크기의 가우시안 필터를 이용해서 블러링
        ret, th = cv2.threshold(blur, thresholdMin, thresholdMax, cv2.THRESH_BINARY) # 프레임 이진화
        dilated = cv2.dilate(th, np.ones((dilateSize, dilateSize), np.uint8), iterations=dilateIter) # 팽창 연산
        img, contours, hierarchy = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # 경계 얻기
        try:
            # 부모 경계 추출(https://m.blog.naver.com/samsjang/220534805843)
            parentContours = [] # 부모 경계가 저장될 리스트
            for i in range(0, len(hierarchy[0])): # 탐지된 경계의 개수(=len(contours))만큼 반복
                if hierarchy[0][i][3] == -1: # 부모 경계일 경우
                    parentContours.append(i) # 부모 경계의 인덱스 리스트에 추가
            # 움직임 탐지 박스 설정(https://m.blog.naver.com/samsjang/220517391218)
            for i in parentContours: # 부모 경계의 개수만큼 반복
                cnt = contours[i] # 부모 경계
                x, y, w, h = cv2.boundingRect(cnt) # 경계에 외접하는 사각형(움직임 탐지 박스) 위치 및 크기 얻기
                # 설정한 크기보다 큰 움직임 탐지 박스만 출력
                if w > rectWidthMin and h > rectHeightMin:
                    # cv2.rectangle(previousFrame, (x, y), (x + w, y + h), (255, 255, 0), 2) # 움직임 탐지 박스 그리기
                    # 움직임 탐지 박스 그리기2
                    rect = cv2.minAreaRect(cnt)
                    box = cv2.boxPoints(rect)
                    cv2.drawContours(previousFrame, [np.int0(box)], 0, (255, 255, 0), 2)
                    # 무게중심 그리기(https://m.blog.naver.com/samsjang/220517848698)
                    mmt = cv2.moments(cnt) # 부모 경계의 무게중심 얻기
                    cx = int(mmt['m10'] / mmt['m00']) # 무게중심 x좌표
                    cy = int(mmt['m01'] / mmt['m00']) # 무게중심 y좌표
                    cv2.circle(previousFrame, (cx, cy), 2, (0, 255, 255), -1) # 무게중심 그리기
                    cv2.drawContours(previousFrame, cnt, -1, (255, 0, 255), 2) # 부모 경계 그리기
        except:
            pass
        cv2.imshow('Video Motion Detector', previousFrame) # 프레임 출력
        if cv2.waitKey(1) & 0xFF == 27: # ESC 입력 시 종료
            break
        previousFrame = currentFrame # 현재 프레임을 이전 프레임으로 설정
        ret, currentFrame = cap.read() # 현재 프레임 갱신
    cv2.destroyAllWindows()
    cap.release()

# 윈도우를 대상으로 하는 움직임 탐지 함수
def windowsMotionDetector():
    global thresholdMin, thresholdMax, dilateSize, dilateIter, rectWidthMin, rectHeightMin
    screenWidth = win32api.GetSystemMetrics(win32con.SM_CXSCREEN) # 윈도우 가로 크기
    screenHeight = win32api.GetSystemMetrics(win32con.SM_CYSCREEN) # 윈도우 세로 크기
    screenFrame = ImageGrab.grab(bbox=(0, 0, screenWidth, screenHeight)) # 윈도우 프레임
    previousFrame = np.array(screenFrame) # 이전 프레임
    currentFrame = np.array(screenFrame) # 현재 프레임
    while True:
        diff = cv2.absdiff(previousFrame, currentFrame) # 두 프레임 행렬 간의 요소별 절대 차이 계산
        grey = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY) # 프레임 흑백 변환
        blur = cv2.GaussianBlur(grey, (5, 5), 0) # 5 x 5 크기의 가우시안 필터를 이용해서 블러링
        ret, th = cv2.threshold(blur, thresholdMin, thresholdMax, cv2.THRESH_BINARY) # 프레임 이진화
        dilated = cv2.dilate(th, np.ones((dilateSize, dilateSize), np.uint8), iterations=dilateIter) # 팽창 연산
        img, contours, hierarchy = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # 경계 얻기
        try:
            # 부모 경계 추출(https://m.blog.naver.com/samsjang/220534805843)
            parentContours = [] # 부모 경계가 저장될 리스트
            for i in range(0, len(contours)): # 탐지된 경계의 개수(=len(hierarchy[0]))만큼 반복
                if hierarchy[0][i][3] == -1: # 부모 경계일 경우
                    parentContours.append(i) # 부모 경계의 인덱스 리스트에 추가
            # 움직임 탐지 박스 설정(https://m.blog.naver.com/samsjang/220517391218)
            for i in parentContours: # 부모 경계의 개수만큼 반복
                cnt = contours[i] # 부모 경계
                x, y, w, h = cv2.boundingRect(cnt) # 경계에 외접하는 사각형(움직임 탐지 박스) 위치 및 크기 얻기
                # 설정한 크기보다 큰 움직임 탐지 박스만 출력
                if w > rectWidthMin and h > rectHeightMin:
                    cv2.rectangle(previousFrame, (x, y), (x + w, y + h), (255, 255, 0), 2) # 움직임 탐지 박스 그리기
                    ''' 움직임 탐지 박스 그리기2
                    rect = cv2.minAreaRect(cnt)
                    box = cv2.boxPoints(rect)
                    cv2.drawContours(previousFrame, [np.int0(box)], 0, (255, 255, 0), 2) '''
                    # 무게중심 그리기(https://m.blog.naver.com/samsjang/220517848698)
                    mmt = cv2.moments(cnt) # 부모 경계의 무게중심 얻기
                    cx = int(mmt['m10'] / mmt['m00']) # 무게중심 x좌표
                    cy = int(mmt['m01'] / mmt['m00']) # 무게중심 y좌표
                    cv2.circle(previousFrame, (cx, cy), 2, (0, 255, 255), -1) # 무게중심 그리기
                    # cv2.drawContours(previousFrame, cnt, -1, (255, 0, 255), 2) # 부모 경계 그리기
        except:
            pass
        cv2.imshow('Windows Motion Detector', previousFrame) # 프레임 출력
        if cv2.waitKey(1) & 0xFF == 27: # ESC 입력 시 종료
            break
        previousFrame = currentFrame # 현재 프레임을 이전 프레임으로 설정
        currentFrame = np.array(ImageGrab.grab(bbox=(0, 0, screenWidth, screenHeight))) # 현재 프레임 갱신
    cv2.destroyAllWindows()

def main():
    global thresholdMin, thresholdMax, dilateSize, dilateIter, rectWidthMin, rectHeightMin
    sel = input('[Select]\n1. Video Motion Detector\n2. Windows Motion Detector\nselect : ')
    if sel == '1':
        videoInput = input('Input Video File or Webcam Device Number : ')
        hyperSel = input('Input Whether or Not to Set Hyper Parameters(y/n) : ')
        if hyperSel.lower() == 'n' or hyperSel.lower() == 'no':
            videoMotionDetector(videoInput)
        elif hyperSel.lower() == 'y' or hyperSel.lower() == 'yes':
            thresholdMin = int(input('Input Minimum Threshold : '))
            thresholdMax = int(input('Input Maximum Threshold : '))
            dilateSize = int(input('Input Dilate Filter Size : '))
            dilateIter = int(input('Input Iteration of Dilate Operation : '))
            rectWidthMin = int(input('Input Motion Detect Box Minimum Width : '))
            rectHeightMin = int(input('Input Motion Detect Box Minimum Height : '))
            videoMotionDetector(videoInput)
        else:
            print('[-] Input Error')
    elif sel == '2':
        hyperSel = input('Input Whether or Not to Set Hyper Parameters(y/n) : ')
        if hyperSel.lower() == 'n' or hyperSel.lower() == 'no':
            windowsMotionDetector()
        elif hyperSel.lower() == 'y' or hyperSel.lower() == 'yes':
            thresholdMin = int(input('Input Minimum Threshold : '))
            thresholdMax = int(input('Input Maximum Threshold : '))
            dilateSize = int(input('Input Dilate Filter Size : '))
            dilateIter = int(input('Input Iteration of Dilate Operation : '))
            rectWidthMin = int(input('Input Motion Detect Box Minimum Width : '))
            rectHeightMin = int(input('Input Motion Detect Box Minimum Height : '))
            windowsMotionDetector()
        else:
            print('[-] Input Error')
    else:
        print('[-] Input Error')

if __name__ == '__main__':
    main()