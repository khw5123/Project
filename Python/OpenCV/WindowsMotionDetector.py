#-*- coding: utf-8 -*-
import win32api
import win32con
import cv2
import numpy as np
from PIL import ImageGrab
from threading import Thread

box = list() # 움직임 탐지 박스 시작, 끝 위치가 저장될 리스트
threadExit = False # 스레드 종료 변수
thresholdMin, thresholdMax, nonZeroMin = 60, 1, 500 # 최소, 최대 임계값, 0이 아닌 요소 개수의 최솟값

# 프레임 행렬 간의 요소별 절대 차이를 계산하는 함수
def diffFrame(i):
    diff0 = cv2.absdiff(i[0], i[1])
    diff1 = cv2.absdiff(i[1], i[2])
    return cv2.bitwise_and(diff0, diff1)

# 프레임 갱신하는 함수
def updateFrame(frame, i):
    i[0] = i[1]
    i[1] = i[2]
    i[2] = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

# 윈도우를 대상으로 하는 움직임 탐지 스레드
def windowsMotionDetectorThread(startPosX, startPosY, endPosX, endPosY, screenIndex):
    global box, threadExit, thresholdMin, thresholdMax, nonZeroMin
    firstFrame = ImageGrab.grab(bbox=(startPosX, startPosY, endPosX, endPosY)) # 처음 윈도우 프레임
    frame = np.array(firstFrame) # 처음 프레임
    i = [None, None, None] # 프레임 갱신을 위한 리스트
    for n in range(len(i)):
        i[n] = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY) # 프레임 흑백 변환
    while True:
        currentFrame = ImageGrab.grab(bbox=(startPosX, startPosY, endPosX, endPosY)) # 현재 윈도우 프레임
        frame = np.array(currentFrame) # 현재 프레임
        diff = diffFrame(i) # 프레임 행렬 간의 요소별 절대 차이 계산
        ret, th = cv2.threshold(diff, thresholdMin, thresholdMax, cv2.THRESH_BINARY) # 프레임 이진화
        nonZero = cv2.countNonZero(th) # 0이 아닌 요소 개수 저장
        # 움직임이 발생했을 경우
        if nonZero > nonZeroMin:
            nz = np.nonzero(th) # 0이 아닌 요소 저장
            # 움직임 탐지 박스의 시작, 끝 위치 저장
            box[screenIndex][0] = startPosX + min(nz[1])
            box[screenIndex][1] = startPosY + min(nz[0])
            box[screenIndex][2] = startPosX + max(nz[1])
            box[screenIndex][3] = startPosY + max(nz[0])
        else:
            box[screenIndex][0] = None
            box[screenIndex][1] = None
            box[screenIndex][2] = None
            box[screenIndex][3] = None
        updateFrame(frame, i) # 프레임 갱신
        # 스레드 종료 변수가 설정됐을 경우
        if threadExit == True:
            break

# 윈도우를 대상으로 하는 움직임 탐지 함수
def windowsMotionDetector(split):
    global box, threadExit
    screenWidth = win32api.GetSystemMetrics(win32con.SM_CXSCREEN) # 윈도우 가로 크기
    screenHeight = win32api.GetSystemMetrics(win32con.SM_CYSCREEN) # 윈도우 세로 크기
    splitScreenWidth = int(screenWidth / split) # 분할된 윈도우 가로 크기
    splitScreenHeight = int(screenHeight / split) # 분할된 윈도우 세로 크기
    coordinates = list() # 분할된 윈도우 시작, 끝 좌표가 저장될 리스트
    screenIndex = 0 # 분할된 윈도우 인덱스
    # 윈도우 분할 및 좌표 저장
    for x in range(split):
        coordinates.append(list())
        for y in range(split):
            coordinates[x].append(list())
            for _ in range(4):
                coordinates[x][y].append(None)
    for x in range(split):
        for y in range(split):
            width = y * splitScreenWidth
            coordinates[x][y][0] = width
            coordinates[x][y][2] = width + splitScreenWidth
    for x in range(split):
        height = x * splitScreenHeight
        for y in range(split):
            coordinates[x][y][1] = height
            coordinates[x][y][3] = height + splitScreenHeight
    for i in range(split**2):
        box.append(list())
        for _ in range(4):
            box[i].append(None)
    # 윈도우를 대상으로 하는 움직임 탐지 스레드 생성 및 실행
    for x in range(split):
        for y in range(split):
            Thread(target=windowsMotionDetectorThread, args=(coordinates[x][y][0], coordinates[x][y][1], coordinates[x][y][2], coordinates[x][y][3], screenIndex)).start()
            screenIndex += 1
    while True:
        currentFrame = ImageGrab.grab(bbox=(0, 0, screenWidth, screenHeight)) # 현재 윈도우 프레임
        frame = np.array(currentFrame) # 현재 프레임
        for i in range(split**2): # 분할된 윈도우 개수만큼 반복
            # 움직임이 발생해서 움직임 탐지 박스 리스트에 위치 값이 있을 경우
            if box[i][0] != None and box[i][1] != None and box[i][2] != None and box[i][3] != None:
                cv2.rectangle(frame, (box[i][0], box[i][1]), (box[i][2], box[i][3]), (0, 0, 255), 2) # 움직임 탐지 박스 그리기
        cv2.imshow('Windows Motion Detector', frame) # 프레임 출력
        if cv2.waitKey(10) == 27: # ESC 입력 시 종료
            threadExit = True # 스레드 종료 변수 설정
            break

def main():
    try:
        split = int(input('Input Number of Screen Split(N x N) : '))
        if split < 1 or split > 3:
            split = 3
        windowsMotionDetector(split)
    except Exception as e:
        print('[-]', e)

if __name__ == '__main__':
    main()