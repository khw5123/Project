# -*- coding: utf-8 -*-
import numpy as np
import cv2

# https://m.blog.naver.com/samsjang/220699662173
# http://www.bogotobogo.com/python/OpenCV_Python/python_opencv3_Image_Object_Detection_Face_Detection_Haar_Cascade_Classifiers.php
# http://darkpgmr.tistory.com/70

# Haar cascade classifier(Haar feature 기반 다단계 분류) : 다수의 객체 이미지(postive 이미지)와 객체가 아닌 이미지(negative 이미지)를 cascade 함수로 학습시켜 객체를 검출하는 머신러닝 기반 객체 검출 기법
# OpenCV 는 Haar-Cascade 트레이너(이미지 학습)와 검출기(이미지 판별)를 모두 제공

def faceRecognition(face_xml_file, eye_xml_file, device_index): # 정면 얼굴 학습 데이터 xml 파일, 사람 눈 학습 데이터 xml 파일
    eye_detect = False # 얼굴 검출 모드 활성화 여부
    face_cascade = cv2.CascadeClassifier(face_xml_file) # 정면 얼굴 Haar-Cascade 학습 데이터를 읽어 CascadeClassifier 객체 생성
    eye_cascade = cv2.CascadeClassifier(eye_xml_file) # 눈 Haar-Cascade 학습 데이터를 읽어 CascadeClassifier 객체 생성
    info = '' # 얼굴 검출 모드 활성/비활성 알림 문자열
    try:
        if device_index == '': # 장치를 설정 안 했을 경우
            device_index = '0' # 디폴트 장치 인덱스를 0으로 설정
        cap = cv2.VideoCapture(int(device_index)) # 장치 인덱스(카메라 지정) or 비디오 파일(비디오 파일 재생 시)
    except:
        return
    while True:
        ret, frame = cap.read() # 한 프레임 읽음
        if not ret: # 프레임을 제대로 읽지 못했을 경우
            break
        if eye_detect: # 얼굴 검출 모드 활성화 상태인 경우
            info = 'Eye Detection On(Press \'i\')' # 얼굴 검출 모드 활성화 알림 문자열
        else: # 얼굴 검출 모드 비활성화 상태인 경우
            info = 'Eye Detection Off(Press \'i\')' # 얼굴 검출 모드 비활성화 알림 문자열
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # 프레임 흑백으로 변환
        # 이미지를 입력하여 얼굴 검출.(한 번에 여러 객체 검출 가능) 얼굴이 검출되면 위치를 리스트로 반환(검출된 얼굴의 좌측 상단 x좌표, 검출된 얼굴의 좌측 상단 y좌표, 검출된 얼굴의 가로 길이, 검출된 얼굴의 세로 길이)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5) # 인자 : image, scaleFactor(각 이미지 크기에서 이미지 크기를 얼마나 줄일 것인지 지정), minNeighbors(검출 범위를 유지해야 하는 이웃 수를 지정. 값이 높을수록 탐지는 적지만 정확도는 높아짐), flags, minSize(가능한 최소 오브젝트 크기), maxSize(가능한 최대 오브젝트 크기)
        cv2.putText(frame, info, (5, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 1) # 프레임에 얼굴 검출 모드 활성/비활성 알림 출력 설정
        for (x, y, w, h) in faces: # 검출된 얼굴 수만큼 반복
            cv2.rectangle(frame, (x,y), (x+w, y+h), (255, 0, 0), 2) # 프레임에 검출된 얼굴 범위 설정
            cv2.putText(frame, 'Detected Face', (x-5, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2) # 검출된 얼굴 범위 위에 출력될 문자열 설정
            if eye_detect: # 얼굴 검출 모드 활성화 상태인 경우
                roi_gray = gray[y:y+h, x:x+w] # 얼굴 범위 흑백으로 저장
                eyes = eye_cascade.detectMultiScale(roi_gray) # 이미지를 입력하여 눈 검출
                for (ex, ey, ew, eh) in eyes: # 검출된 눈 개수만큼 반복
                    roi_color = frame[y:y+h, x:x+w] # 프레임에서 얼굴 범위 저장
                    cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2) # 프레임에 검출된 눈 범위 설정
        cv2.imshow('Face Recognition', frame) # 프레임 그리기
        if cv2.waitKey(30) == ord('i'): # 얼굴 검출 모드 전환 키
            eye_detect = not eye_detect
        if cv2.waitKey(30) == 27: # ESC 입력 시 종료
            break
    cap.release() # 객체 해제
    cv2.destroyAllWindows() # 생성한 윈도우 제거

def main():
    face_xml_file = input('Input Face XML File : ')
    eye_xml_file = input('Input Eye XML File : ')
    device_index = input('Input Device Index(Default Enter): ')
    faceRecognition(face_xml_file, eye_xml_file, device_index)

if __name__ == '__main__':
    main()