# -*- coding: utf-8 -*-
import numpy as np
import cv2

# https://m.blog.naver.com/samsjang/220659310860

# Cam Shift : 추적 범위의 크기가 일정하다는 Mean Shift의 단점을 극복한 알고리즘

col, width, row, height = -1, -1, -1, -1 # 추적 범위 좌측 상단 x좌표, 추적 범위 폭, 추적 범위 좌측 상단 y좌표, 추적 범위 높이
frame = None # 프레임
frame2 = None # 프레임 복사본
inputmode = False # 추적 범위 설정 모드 변수
rectangle = False # 클릭 상태 여부 판단 변수
trackWindow = None # 추적 범위 구성요소(추적 범위 좌측 상단 x좌표, 추적 범위 좌측 상단 y좌표, 추적 범위 폭, 추적 범위 높이)
roi_hist = None # 히스토그램

def onMouse(event, x, y, flags, param):
    global col, width, row, height, frame, frame2, inputmode, rectangle, trackWindow, roi_hist
    if inputmode: # 범위 설정 모드일 경우
        if event == cv2.EVENT_LBUTTONDOWN: # 마우스 좌클릭일 경우
            rectangle = True # 클릭 상태 여부 판단 변수 값 설정
            col, row = x, y # 현재 클릭한 프레임의 x,y 좌표 저장
        elif event == cv2.EVENT_MOUSEMOVE: # 마우스 이동일 경우
            if rectangle: # 마우스 좌클릭 상태일 경우
                frame = frame2.copy() # 프레임 복사본 저장
                cv2.rectangle(frame, (col, row), (x, y), (0, 255, 0), 2) # 클릭한 좌표(col, row)부터 현재 마우스 좌표(x, y)까지 범위 설정
                cv2.imshow('Image Recognition', frame) # 범위 그리기
        elif event == cv2.EVENT_LBUTTONUP: # 마우스 좌클릭 해제일 경우
            inputmode = False # 범위 설정 모드 초기화
            rectangle = False # 클릭 상태 여부 판단 변수 값 초기화
            cv2.rectangle(frame, (col, row), (x, y), (0, 255, 0), 2) # 클릭한 좌표(col, row)부터 현재 마우스 좌표(x, y)까지 추적 범위 설정
            height, width = abs(row-y), abs(col-x) # 추적 범위의 높이, 폭 저장
            trackWindow = (col, row, width, height) # 추적 범위 구성요소 저장
            roi = frame[row:row+height, col:col+width] # 프레임에서 추적 범위 설정
            roi = cv2.cvtColor(roi, cv2.COLOR_RGB2HSV) # 프레임의 추적 범위를 HSV 색 공간으로 변경
            roi_hist = cv2.calcHist([roi], [0], None, [180], [0, 180]) # HSV 색 공간으로 변경한 히스토그램 계산
            cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX) # 계산된 히스토그램을 노멀라이즈(첫 번째 인자의 배열을 정규화(최소값과 최대값을 보고 비율에 맞게 값을 재조정)해서 두 번째 인자의 배열에 저장)
    return

def camShift(device_index):
    global frame, frame2, inputmode, trackWindow, roi_hist
    try:
        if device_index == '': # 장치를 설정 안 했을 경우
            device_index = '0' # 디폴트 장치 인덱스를 0으로 설정
        cap = cv2.VideoCapture(int(device_index)) # 장치 인덱스(카메라 지정) or 비디오 파일(비디오 파일 재생 시)
    except:
        return
    ret, frame = cap.read() # 한 프레임 읽음
    cv2.namedWindow('Image Recognition') # 윈도우 이름 설정
    cv2.setMouseCallback('Image Recognition', onMouse, param=(frame, frame2)) # 마우스 콜백 함수 등록
    termination = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1) # camShift 의 iteration 횟수가 10회일 때까지 알고리즘 구동 or 현재 범위의 중심과 무게중심의 차가 1pt 일 때까지 알고리즘 구동
    while True:
        ret, frame = cap.read() # 한 프레임 읽음
        if not ret: # 프레임을 제대로 읽지 못했을 경우
            break
        cv2.putText(frame, 'Press \'i\' and Select Image and Press \'i\'', (5, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 1) # 프레임에 범위 설정 모드 알림 출력 설정
        if trackWindow is not None: # 추적 범위가 있을 경우
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # 프레임 범위를 HSV 색 공간으로 변경
            dst = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1) # Histogram Backprojection
            ret, trackWindow = cv2.CamShift(dst, trackWindow, termination) # Cam Shift 알고리즘
            pts = cv2.boxPoints(ret)
            pts = np.int0(pts)
            cv2.polylines(frame, [pts], True, (0, 255, 0), 2) # 추적 범위 설정
        cv2.imshow('Image Recognition', frame) # 추적 범위 그리기
        if (cv2.waitKey(60) & 0xFF) == 27: # ESC 입력 시 종료
            break
        if (cv2.waitKey(60) & 0xFF) == ord('i'): # 범위 설정 모드 전환 키
            inputmode = True # 추적 범위 설정 모드 변수 값 설정
            frame2 = frame.copy() # 현재 프레임을 프레임 복사본에 저장
            # 추적 범위를 설정할 때까지 화면 일시정지 효과
            while inputmode: # 추적 범위를 설정 중인 경우
                cv2.imshow('Image Recognition', frame) # 같은 프레임만 출력
                cv2.waitKey(0) # 키 입력이 있을 때까지 대기
    cap.release() # 객체 해제
    cv2.destroyAllWindows() # 생성한 윈도우 제거

def main():
    device_index = input('Input Device Index(Default Enter): ')
    camShift(device_index)

if __name__ == '__main__':
    main()