# -*- coding: utf-8 -*-
import random
import cv2

def createTracker(trackerType):
    if trackerType == '1':
        tracker = cv2.TrackerBoosting_create()
    elif trackerType == '2':
        tracker = cv2.TrackerMIL_create()
    elif trackerType == '3':
        tracker = cv2.TrackerKCF_create()
    elif trackerType == '4':
        tracker = cv2.TrackerTLD_create()
    elif trackerType == '5':
        tracker = cv2.TrackerMedianFlow_create()
    elif trackerType == '6':
        tracker = cv2.TrackerGOTURN_create()
    elif trackerType == '7':
        tracker = cv2.TrackerMOSSE_create()
    else:
        tracker = cv2.TrackerCSRT_create()
    return tracker

def objectMultiTracker(videoInput, trackerType):
    try:
        if videoInput.isdigit(): # 웹캠 장치 번호일 경우
            cap = cv2.VideoCapture(int(videoInput))
        else: # 동영상 파일명일 경우
            cap = cv2.VideoCapture(videoInput)
        ret, frame = cap.read() # 처음 프레임
        objectBox = [] # 추적할 오브젝트 박스의 위치 및 크기가 저장될 리스트
        print('\nSet the range and press ENTER. When all is done, press ESC.')
        while True:
            box = cv2.selectROI('MultiTracker', frame) # 범위 설정
            if box[0] == 0 and box[1] == 0 and box[2] == 0 and box[3] == 0: # 범위를 설정하지 않았을 경우
                break
            objectBox.append(box) # 선택한 영역(추적할 오브젝트 박스)의 위치 및 크기 리스트에 추가
        multiTracker = cv2.MultiTracker_create() # MultiTracker 객체 생성
        for box in objectBox: # 설정한 범위 수만큼 반복
            multiTracker.add(createTracker(trackerType), frame, box) # MultiTracker 객체 초기화
        while True:
            ret, frame = cap.read() # 현재 프레임
            if not ret: # 프레임을 제대로 읽지 못했을 경우
                break
            ret, boxes = multiTracker.update(frame) # 추적할 오브젝트 박스 위치 갱신
            for i, newbox in enumerate(boxes):
                p1 = (int(newbox[0]), int(newbox[1]))
                p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
                cv2.rectangle(frame, p1, p2, [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)], 2, 1) # 추적할 오브젝트 박스 그리기
            cv2.imshow('MultiTracker', frame) # 프레임 출력
            if cv2.waitKey(1) & 0xFF == 27: # ESC 입력 시 종료
                break
    except Exception as e:
        print('[-]', e)
    finally:
        cv2.destroyAllWindows()
        cap.release()

def main():
    try:
        videoInput = input('Input Video File or Webcam Device Number : ')
        trackerType = input('[Select Tracker Type]\n1. BOOSTING\n2. MIL\n3. KCF\n4. TLD\n5. MEDIANFLOW\n6. GOTURN\n7. MOSSE\n8. CSRT(Default)\nSelect : ')
        objectMultiTracker(videoInput, trackerType)
    except Exception as e:
        print('[-]', e)

if __name__ == '__main__':
    main()