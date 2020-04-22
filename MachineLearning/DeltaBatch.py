#-*- coding: utf-8 -*-
import numpy as np

def sigmoid(v):
    return 1.0 / (1.0 + np.exp(-v))

def deltaBatch(W, X, D):
    alpha = 0.9 # 학습률
    dWsum = np.zeros(3) # 가중치 갱신값의 합(1 x 3 행렬)
    for k in range(len(X)): # 학습 데이터 개수만큼 반복
        x = X[k,:].T # 학습 데이터(1 x 3 행렬(X[k,:])을 전치 행렬로 변경(3 x 1 행렬(x)))
        d = D[k] # 레이블
        v = np.matmul(W, x) # 가중합(1 x 1 행렬) = 가중치(1 x 3 행렬) x 학습 데이터(3 x 1 행렬)
        y = sigmoid(v) # 출력값
        e = d - y # 오차
        delta = y * (1 - y) * e # 델타(시그모이드 함수(f)의 도함수 = f(1-f))
        dW = alpha * delta * x # 가중치 갱신값
        dWsum = dWsum + dW # 가중치 갱신값 더함
    dWavg = dWsum / len(D) # 가중치 갱신값의 평균값
    # 가중치 한 번만 갱신
    W[0][0] = W[0][0] + dWavg[0]
    W[0][1] = W[0][1] + dWavg[1]
    W[0][2] = W[0][2] + dWavg[2]
    return W # 갱신된 가중치 반환

def main():
    X = np.array([[0, 0, 1], 
                  [0, 1, 1], 
                  [1, 0, 1], 
                  [1, 1, 1]]) # 학습 데이터
    D = np.array([[0], 
                  [0], 
                  [1], 
                  [1]]) # 레이블
    W = 2 * np.random.random((1, 3)) - 1 # 가중치(1 x 3 행렬)
    epoch = 40000 # 학습 횟수
    for _ in range(epoch):
        W = deltaBatch(W, X, D) # 학습
    # Test
    for k in range(len(X)): # 입력 데이터 개수만큼 반복
        x = X[k,:].T # 입력 데이터
        v = np.matmul(W, x) # 가중합 = 가중치 x 입력 데이터
        y = sigmoid(v) # 출력값
        print('Label : %d, Output : %f' % (D[k], y))

if __name__ == '__main__':
    main()

''' Without Numpy
#-*- coding: utf-8 -*-
import random
import math

def sigmoid(v):
    return 1 / (1 + math.exp(-v))

def deltaBatch(W, X, D):
    alpha = 0.9 # 학습률
    dWsum = [0, 
             0, 
             0, 
             0] # 가중치 갱신값의 합
    for i in range(len(X)): # 학습 데이터 개수만큼 반복
        v = 0 # 가중합 초기화
        for j in range(len(X[0])):
            x = X[i][j] # 학습 데이터
            v += W[i] * x # 가중합 = 가중치 x 학습 데이터
        d = D[i] # 레이블
        y = sigmoid(v) # 출력값
        e = d - y # 오차
        delta = y * (1 - y) * e # 델타(시그모이드 함수(f)의 도함수 = f(1-f))
        dW = alpha * delta * x # 가중치 갱신값
        dWsum[i] += dW # # 가중치 갱신값 더함
    # 가중치 한 번만 갱신
    for i in range(len(D)):
        W[i] += dWsum[i] / len(D) # 가중치 갱신값의 평균값으로 가중치 갱신

def main():
    X = [[0,0,1], 
         [0,1,1], 
         [1,0,1], 
         [1,1,1]] # 학습 데이터
    D = [0, 
         0, 
         1, 
         1] # 레이블
    W = [2 * random.random() - 1, 
         2 * random.random() - 1, 
         2 * random.random() - 1, 
         2 * random.random() - 1] # 가중치
    epoch = 40000 # 학습 횟수
    for _ in range(epoch):
        deltaBatch(W, X, D) # 학습
    # Test
    for i in range(len(X)): # 입력 데이터 개수만큼 반복
        v = 0 # 가중합 초기화
        for j in range(len(X[0])):
            x = X[i][j] # 입력 데이터
            v += W[i] * x # 가중합 = 가중치 x 입력 데이터
        y = sigmoid(v) # 출력값
        print('Label : %d, Output : %f' % (D[i], y))

if __name__ == '__main__':
    main()
'''