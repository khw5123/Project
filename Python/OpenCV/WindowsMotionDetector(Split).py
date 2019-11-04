#-*- coding: utf-8 -*-
import win32api
import win32con
from threading import Thread
import cv2
import numpy as np
from PIL import ImageGrab

def diffImage(i):
    diff0 = cv2.absdiff(i[0], i[1])
    diff1 = cv2.absdiff(i[1], i[2])
    return cv2.bitwise_and(diff0, diff1)

def getGrayCameraImage(screen):
    return cv2.cvtColor(screen, cv2.COLOR_RGB2GRAY)

def updateCameraImage(screen, i):
    i[0] = i[1]
    i[1] = i[2]
    i[2] = getGrayCameraImage(screen)

def windowsMotionDetectThread(startPosX, startPosY, endPosX, endPosY):
    thresh, minCount = 60, 500
    firstScreen = ImageGrab.grab(bbox=(startPosX, startPosY, endPosX, endPosY))
    screen = np.array(firstScreen)
    i = [None, None, None]
    for n in range(3):
        i[n] = getGrayCameraImage(screen)
    while True:
        currentScreen = ImageGrab.grab(bbox=(startPosX, startPosY, endPosX, endPosY))
        screen = np.array(currentScreen)
        diff = diffImage(i)
        ret, thrimg = cv2.threshold(diff, thresh, 1, cv2.THRESH_BINARY)
        count = cv2.countNonZero(thrimg)
        if count > minCount:
            nz = np.nonzero(thrimg)
            cv2.rectangle(screen, (min(nz[1]),min(nz[0])), (max(nz[1]),max(nz[0])), (0,0,255), 2)
        cv2.imshow(str(startPosX) + ',' + str(startPosY), screen)
        updateCameraImage(screen, i)
        if cv2.waitKey(10) == 27:
            break

def windowsMotionDetect(split=2):
    split_width_screen = int(win32api.GetSystemMetrics(win32con.SM_CXSCREEN) / split)
    split_height_screen = int(win32api.GetSystemMetrics(win32con.SM_CYSCREEN) / split)
    coordinates = list()
    for x in range(split):
        coordinates.append(list())
        for y in range(split):
            coordinates[x].append(list())
            for _ in range(4):
                coordinates[x][y].append(None)
    for x in range(split):
        for y in range(split):
            width = y * split_width_screen
            coordinates[x][y][0] = width
            coordinates[x][y][2] = width + split_width_screen
    for x in range(split):
        height = x * split_height_screen
        for y in range(split):
            coordinates[x][y][1] = height
            coordinates[x][y][3] = height + split_height_screen
    for x in range(split):
        for y in range(split):
            Thread(target=windowsMotionDetectThread, args=(coordinates[x][y][0], coordinates[x][y][1], coordinates[x][y][2], coordinates[x][y][3],)).start()

def main():
    windowsMotionDetect(2)

if __name__ == '__main__':
    main()