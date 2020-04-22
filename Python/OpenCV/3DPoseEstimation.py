# -*- coding: utf-8 -*-
import numpy as np
import cv2

# https://m.blog.naver.com/samsjang/220664805818

def drawCube(img, corners, imgpts):
	imgpts = np.int32(imgpts).reshape(-1, 2)
	cv2.drawContours(img, [imgpts[:4]], -1, (255, 0, 0), -3)
	
	for i, j in zip(range(4), range(4, 8)):
		cv2.line(img, tuple(imgpts[i]), tuple(imgpts[j]), (0, 255, 0), 2)

	cv2.drawContours(img, [imgpts[4:]], -1, (0, 255, 0), 2)
	
	return img
	
def poseEstimation():
	with np.load('calib.npz') as X:
		ret, mtx, dist, _, _ = [X[i] for i in ('ret', 'mtx', 'rvecs', 'tvecs')]
	
	termination = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
	objp = np.zeros((7*10, 3), np.float32)
	objp[:, :2] = np.mgrid[0:7, 0:10].T.reshape(-1, 2)
	axis = np.floast32([[0,0,0], [0,3,0], [3,3,0], [3,0,0], [0,0,-3], [0,3,-3], [3,3,-3], [3,0,-3]])
	
	objpoints = []
	imgpoints = []
	
	cap = cv2.VideoCapture(0)
	
	while True:
		ret, frame = cap.read()
		
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		ret, corners = cv2.findChessboardCorners(gray, (7, 10), None)
		
		if ret:
			cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), termination)
			_, rvecs, tvecs, inliers = cv2.solvePnPRansac(objp, corners, mtx, dist)
			imgpts, jac = cv2.projectPoints(axis, rvecs, tvecs, mtx, dist)
			frame = drawCube(frame, corners, imgpts)
			
		cv2.imshow('frame', frame)
		k = cv2.waitKey(1) & 0xFF
		if k == 27:
			break
			
	cap.release()
	cv2.destroyAllWindows()	

def saveCamCalibration():
	termination = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
	
	objp = np.zeros((7*10, 3), np.float32)
	objp[:, :2] = np.mgrid[0:7, 0:10].T.reshape(-1, 2)
	
	objpoints = []
	imgpoints = []
	
	cap = cv2.VideoCapture(0)
	count = 0
	while True:
		ret, frame = cap.read()

		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		ret, corners = cv2.findChessboardCorners(gray, (3, 3), None)
		
		if ret:
			objpoints.append(objp)
			cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), termination)
			imgpoints.append(corners)
			
			cv2.drawChessboardCorners(frame, (7, 10), corners, ret)
			count += 1
			print '%d' % count
			
		cv2.imshow('img', frame)
		
		k = cv2.waitKey(0)
		if k == 27:
			break
		
		if count > 15:
			break
		
	cv2.destroyAllWindows()	
	ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
	
	np.savez('calib.npz', ret=ret, mtx=mtx, dist=dist, rvecs=rvecs, tvecs=tvecs)
	
saveCamCalibration()
# poseEstimation()