# -*- coding: utf-8 -*-
import os
from PIL import Image
import numpy as np
import cv2

FACE_XML = 'haarcascade_frontalface_default.xml'
image_dir = 'image\\'
train_dir = 'train\\'
TRAIN_YML = train_dir + 'trainer.yml'

def save_face(face_name):
    cam = cv2.VideoCapture(0)
    cam.set(3, 640)
    cam.set(4, 480)
    face_detector = cv2.CascadeClassifier(FACE_XML)
    os.system('mkdir ' + image_dir \
              + str(max(list(map(int, os.listdir(image_dir)))) + 1))
    print('\nLook the camera and wait...')
    count = 0
    while(True):
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)
            count += 1
            cv2.imwrite(image_dir + '\\' \
                        + str(max(list(map(int, os.listdir(image_dir))))) \
                        + '\\' + str(face_name) + '.' + str(count) \
                        + '.jpg', gray[y:y+h,x:x+w])
            cv2.imshow('Save face image', img)
        if (cv2.waitKey(100) & 0xff) == 27:
            break
        if count >= 30:
             break
    print('\n[+] Face images saved.')
    cam.release()
    cv2.destroyAllWindows()
    return str(max(list(map(int, os.listdir(image_dir)))))

def train_face(id_):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_detector = cv2.CascadeClassifier(FACE_XML)
    face_samples, ids = list(), list()
    for i in range(int(id_) + 1):
        path = image_dir + str(i) + '\\'
        images = [os.path.join(path, f) for f in os.listdir(path)]
        for image in images:
            PIL_img = Image.open(image).convert('L')
            img_numpy = np.array(PIL_img, 'uint8')
            faces = face_detector.detectMultiScale(img_numpy)
            for (x,y,w,h) in faces:
                face_samples.append(img_numpy[y:y+h,x:x+w])
                ids.append(i)
    recognizer.train(face_samples, np.array(ids))
    recognizer.write(TRAIN_YML)
    print('\n[+] Faces trained.')

def show_face():
    cam = cv2.VideoCapture(0)
    cam.set(3, 640)
    cam.set(4, 480)
    minW, minH = 0.1 * cam.get(3), 0.1 * cam.get(4)
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(TRAIN_YML)
    face_detector = cv2.CascadeClassifier(FACE_XML)
    font = cv2.FONT_HERSHEY_SIMPLEX
    names = [os.listdir(image_dir + '\\' + str(i))[0].split('.')[0] \
             for i in range(len(os.listdir(image_dir)))]
    while True:
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(
            gray, 
            scaleFactor = 1.2, 
            minNeighbors = 5, 
            minSize = (int(minW), int(minH))
        )
        for (x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
            id_, confidence = recognizer.predict(gray[y:y+h,x:x+w])
            print(id_, confidence)
            if confidence < 100:
                name = names[id_]
                confidence = '  {0}%'.format(round(100 - confidence))
            else:
                name = 'unknown'
                confidence = '  {0}%'.format(round(100 - confidence))
            cv2.putText(img, str(name), (x+5,y-5), font, 1, (255,255,255), 2)
            cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)
        cv2.imshow('Detect face', img)
        if (cv2.waitKey(10) & 0xff) == 27:
            break
    cam.release()
    cv2.destroyAllWindows()

def main():
    try:
        select = input('\n[Menu]\n1. Train faces\n2. Detect Faces\nSelect : ')
        if select == '1':
            face_name = input('\nInput face name : ')
            new_id = save_face(face_name)
            train_face(new_id)
            show_face()
        elif select == '2':
            show_face()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()