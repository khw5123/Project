# -*- coding: utf-8 -*-
import numpy as np
import cv2

# https://m.blog.naver.com/samsjang/220662493920

termination = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03)
lk_params = dict(winSize  = (15, 15), maxLevel = 2, criteria = termination)
feature_params = dict(maxCorners = 500, qualityLevel = 0.01, minDistance = 7, blockSize = 7)

class App:
    def __init__(self, video_src):
        self.track_len = 10
        self.detect_interval = 5
        self.tracks = []
        self.cap = cv2.VideoCapture(int(video_src))
        self.frame_idx = 0
        self.blackscreen = False
        self.width = int(self.cap.get(3))
        self.height = int(self.cap.get(4))

    def run(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            vis = frame.copy()
            if self.blackscreen:
                vis = np.zeros((self.height, self.width, 3), np.uint8)
            if len(self.tracks) > 0:
                img0, img1 = self.prev_gray, frame_gray
                p0 = np.float32([tr[-1] for tr in self.tracks]).reshape(-1, 1, 2)
                p1, st, err = cv2.calcOpticalFlowPyrLK(img0, img1, p0, None, **lk_params)
                p0r, st, err = cv2.calcOpticalFlowPyrLK(img1, img0, p1, None, **lk_params)
                d = abs(p0-p0r).reshape(-1, 2).max(-1)
                good = d < 1
                new_tracks = []
                for tr, (x, y), good_flag in zip(self.tracks, p1.reshape(-1, 2), good):
                    if not good_flag:
                        continue
                    tr.append((x, y))
                    if len(tr) > self.track_len:
                        del tr[0]
                    new_tracks.append(tr)
                    cv2.circle(vis, (x, y), 2, (0, 255, 0), -1)
                self.tracks = new_tracks
                cv2.polylines(vis, [np.int32(tr) for tr in self.tracks], False, (0, 255, 0))
            if self.frame_idx % self.detect_interval == 0:
                mask = np.zeros_like(frame_gray)
                mask[:] = 255
                for x, y in [np.int32(tr[-1]) for tr in self.tracks]:
                    cv2.circle(mask, (x, y), 5, 0, -1)
                p = cv2.goodFeaturesToTrack(frame_gray, mask = mask, **feature_params)
                if p is not None:
                    for x, y in np.float32(p).reshape(-1, 2):
                        self.tracks.append([(x, y)])
            self.frame_idx += 1
            self.prev_gray = frame_gray
            cv2.imshow('Optical Flow', vis)
            if (cv2.waitKey(30) & 0xFF) == 27:
                break
            if (cv2.waitKey(30) & 0xFF) == ord('b'):
                self.blackscreen = not self.blackscreen
        self.cap.release()

def main():
    device_index = input('Input Device Index(Default Enter): ')
    if device_index == '': # 장치를 설정 안 했을 경우
        device_index = '0' # 디폴트 장치 인덱스를 0으로 설정
    App(int(device_index)).run()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()