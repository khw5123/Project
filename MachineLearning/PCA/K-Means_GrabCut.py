# -*- coding: utf-8 -*-
import cv2
import numpy as np
import matplotlib.pyplot as plt

def kmeans(K, imageFile):
    img = cv2.imread(imageFile)
    res = np.float32(img.reshape((-1, 3)))
    criteria, n_init = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0), 10
    ret, label, center = cv2.kmeans(res, K, None, criteria, n_init, cv2.KMEANS_RANDOM_CENTERS)
    center = np.uint8(center)
    res = center[label.flatten()].reshape((img.shape))
    plt.imshow(cv2.cvtColor(res, cv2.COLOR_BGR2RGB))
    plt.title('K = ' + str(K))
    plt.show()

def grabcut(imageFile, startX, startY, endX, endY):
    img = cv2.imread(imageFile)
    mask = np.zeros(img.shape[:2], np.uint8)
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)
    cv2.grabCut(img, mask, (startX, startY, endX, endY), bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
    mask2 = np.where((mask==2) | (mask==0), 0, 1).astype('uint8')
    img = img * mask2[:,:,np.newaxis]
    plt.imshow(img)
    plt.colorbar()
    plt.title('GrabCut')
    plt.show()

def main():
    try:
        sel = input('[select]\n1. K-Means\n2. GrabCut\nselect : ')
        imageFile = input('Input Image File : ')
        if sel == '1':
            k = int(input('Input Cluster Count(K) : '))
            kmeans(k, imageFile)
        elif sel == '2':
            startX = int(input('Input Start X Coordinate : '))
            startY = int(input('Input Start Y Coordinate : '))
            endX = int(input('Input End X Coordinate : '))
            endY = int(input('Input End Y Coordinate : '))
            grabcut(imageFile, startX, startY, endX, endY)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()