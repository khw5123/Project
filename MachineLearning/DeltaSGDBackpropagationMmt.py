#-*- coding: utf-8 -*-
import numpy as np

def sigmoid(v):
    return 1.0 / (1.0 + np.exp(-v))

def deltaSGDBackpropagationMmt(W1, W2, X, D):
    alpha = 0.9 # 학습률
    beta = 0.9 # 모멘텀 상수
    mmt1 = np.zeros_like(W1) # 입력층-은닉층 모멘텀
    mmt2 = np.zeros_like(W2) # 은닉층-출력층 모멘텀
    for k in range(len(X)): # 학습 데이터 개수만큼 반복
        x = X[k,:].T # 학습 데이터
        d = D[k] # 레이블
        v1 = np.matmul(W1, x) # 은닉층의 가중합
        y1 = sigmoid(v1) # 은닉층의 출력값
        v = np.matmul(W2, y1) # 출력층의 가중합
        y = sigmoid(v) # 출력층의 출력값
        e = d - y # 출력 노드의 오차
        delta = y * (1 - y) * e # 출력 노드의 델타
        e1 = np.matmul(W2.T, delta) # 은닉 노드의 오차
        delta1 = y1 * (1 - y1) * e1 # 은닉 노드의 델타
        dW1 = (alpha * delta1).reshape(4, 1) * x.reshape(1, 3) # 입력층-은닉층 가중치 갱신값
        mmt1 = dW1 + beta * mmt1 # 입력층-은닉층 모멘텀 계산
        W1 = W1 + mmt1 # 모멘텀을 이용한 입력층-은닉층 가중치 갱신
        dW2 = alpha * delta * y1 # 은닉층-출력층 가중치 갱신값
        mmt2 = dW2 + beta * mmt2 # 은닉층-출력층 모멘텀 계산
        W2 = W2 + mmt2 # 모멘텀을 이용한 은닉층-출력층 가중치 갱신
    return W1, W2 # 갱신된 가중치 반환

def main():
    X = np.array([[0, 0, 1], 
                  [0, 1, 1], 
                  [1, 0, 1], 
                  [1, 1, 1]]) # 학습 데이터
    D = np.array([[0], 
                  [1], 
                  [1], 
                  [0]]) # 레이블
    W1 = 2 * np.random.random((4, 3)) - 1 # 입력층-은닉층 가중치
    W2 = 2 * np.random.random((1, 4)) - 1 # 은닉층-출력층 가중치
    epoch = 10000 # 학습 횟수
    for _ in range(epoch):
        W1, W2 = deltaSGDBackpropagationMmt(W1, W2, X, D) # 학습
    # Test
    for k in range(len(X)): # 입력 데이터 개수만큼 반복
        x = X[k ,:].T # 입력 데이터
        v1 = np.matmul(W1, x) # 은닉층의 가중합
        y1 = sigmoid(v1) # 은닉층의 출력값
        v = np.matmul(W2, y1) # 출력층의 가중합
        y = sigmoid(v) # 출력층의 출력값
        print('Label : %d, Output : %f' % (D[k], y))

if __name__ == '__main__':
    main()

'''' Without Numpy
#-*- coding: utf-8 -*-
import random
import math

def sigmoid(v):
    return 1 / (1 + math.exp(-v))

def deltaSGDBackpropagationMmt(W, X, D, hiddenLayerCount, hiddenNodeCount, M):
    alpha = 0.9 # 학습률
    beta = 0.9 # 모멘텀 상수
    for i in range(len(X)): # 학습 데이터 개수만큼 반복
        hiddenY = [] # 은닉층의 출력값 초기화
        y = 0 # 출력층의 출력값 초기화
        hiddenDelta = [] # 은닉층의 델타 초기화
        weightedSum = [] # 은닉층-출력층(은닉 노드)의 순방향 신호의 가중합 초기화
        for k in range(hiddenLayerCount + 1): # 입력층-은닉층(k = 0), 은닉층-출력층(k = 1)
            v = 0 # 가중합 초기화
            if k == hiddenLayerCount: # 은닉층-출력층
                for j in range(hiddenNodeCount): # 은닉 노드의 개수만큼 반복
                    x = hiddenY[j] # 입력값
                    weightedSum.append(W[i][j][-1] * x) # 은닉층-출력층(은닉 노드)의 가중합 추가
                    v += W[i][j][-1] * x # 출력층의 가중합 = 은닉층-출력층 가중치 x 입력값
                y = sigmoid(v) # 출력층의 출력값
            else: # 입력층-은닉층
                for l in range(hiddenNodeCount): # 은닉 노드의 개수만큼 반복
                    v = 0 # 가중합 초기화
                    for j in range(len(X[0])): # 입력 노드의 개수만큼 반복
                        x = X[i][j] # 학습 데이터
                        v += W[i][l][j] * x # 은닉층의 가중합 = 입력층-은닉층 가중치 x 학습 데이터
                    hiddenY.append(sigmoid(v)) # 은닉층의 출력값 추가
        d = D[i] # 레이블
        e = d - y # 출력 노드의 오차
        outputDelta = y * (1 - y) * e # 출력 노드의 델타
        for k in range(hiddenLayerCount): # 은닉층-출력층(k = 0)
            if k == 0: # 은닉층-출력층
                for j in range(hiddenNodeCount): # 은닉 노드의 개수만큼 반복
                    e = W[i][j][-1] * outputDelta # 은닉 노드의 오차
                    y = sigmoid(weightedSum[j]) # 은닉층-출력층(은닉 노드)의 순방향 신호의 가중합을 은닉 노드의 활성함수에 적용
                    delta = y * (1 - y) * e # 은닉 노드의 델타
                    hiddenDelta.append(delta) # 은닉 노드의 델타 추가
        for k in range(hiddenLayerCount + 1): # 은닉층-출력층(k = 0), 입력층-은닉층(k = 1)
            if k == hiddenLayerCount: # 입력층-은닉층
                for l in range(hiddenNodeCount): # 은닉 노드의 개수만큼 반복
                    for j in range(len(X[0])): # 입력 노드의 개수만큼 반복
                        dW = alpha * hiddenDelta[l] * X[i][j] # 입력층-은닉층 가중치 갱신값
                        m = dW + beta * M[i] # 입력층-은닉층 모멘텀 계산
                        M[i] = m # 입력층-은닉층 모멘텀 갱신
                        W[i][l][j] += (dW + M[i]) # 모멘텀을 이용한 입력층-은닉층 가중치 갱신
            else: # 은닉층-출력층
                for j in range(hiddenNodeCount): # 은닉 노드의 개수만큼 반복
                    dW = alpha * outputDelta * hiddenY[j] # 은닉층-출력층 가중치 갱신값
                    m = dW + beta * M[i] # 은닉층-출력층 모멘텀 계산
                    M[i] = m # 은닉층-출력층 모멘텀 갱신
                    W[i][j][-1] += (dW + M[i]) # 모멘텀을 이용한 은닉층-출력층 가중치 갱신

def main():
    X = [[0, 0, 1], 
         [0, 1, 1], 
         [1, 0, 1], 
         [1, 1, 1]] # 학습 데이터
    D = [0, 
         1, 
         1, 
         0] # 레이블
    w = 2 * random.random() - 1 # 가중치 초기화값
    W = [[[w, w, w, w], # 입력층-은닉층 가중치
          [w, w, w, w], # 입력층-은닉층 가중치
          [w, w, w, w], # 입력층-은닉층 가중치
          [w, w, w, w]], # 은닉층-출력층 가중치
         [[w, w, w, w], # 입력층-은닉층 가중치
          [w, w, w, w], # 입력층-은닉층 가중치
          [w, w, w, w], # 입력층-은닉층 가중치
          [w, w, w, w]], # 은닉층-출력층 가중치
         [[w, w, w, w], # 입력층-은닉층 가중치
          [w, w, w, w], # 입력층-은닉층 가중치
          [w, w, w, w], # 입력층-은닉층 가중치
          [w, w, w, w]], # 은닉층-출력층 가중치
         [[w, w, w, w], # 입력층-은닉층 가중치
          [w, w, w, w], # 입력층-은닉층 가중치
          [w, w, w, w], # 입력층-은닉층 가중치
          [w, w, w, w]]] # 은닉층-출력층 가중치
    M = [0, # 입력층-은닉층 모멘텀
         0, # 입력층-은닉층 모멘텀
         0, # 입력층-은닉층 모멘텀
         0] # 은닉층-출력층 모멘텀
    hiddenLayerCount = 1 # 은닉층 개수
    hiddenNodeCount = len(W[0][0]) # 은닉 노드 개수
    epoch = 10000 # 학습 횟수
    for _ in range(epoch):
        deltaSGDBackpropagationMmt(W, X, D, hiddenLayerCount, hiddenNodeCount, M) # 학습
    # Test
    for i in range(len(X)): # 입력 데이터 개수만큼 반복
        hiddenY = [] # 은닉층 출력값 초기화
        for k in range(hiddenLayerCount + 1): # 입력층-은닉층(k = 0), 은닉층-출력층(k = 1)
            v = 0 # 가중합 초기화
            if k == hiddenLayerCount: # 은닉층-출력층
                for j in range(hiddenNodeCount): # 은닉 노드의 개수만큼 반복
                    x = hiddenY[j] # 입력값
                    v += W[i][j][-1] * x # 출력층의 가중합 = 은닉층-출력층 가중치 x 입력값
                y = sigmoid(v) # 출력층의 출력값
                print('Label : %d, Output : %f' % (D[i], y))
            else: # 입력층-은닉층
                for l in range(hiddenNodeCount): # 은닉 노드의 개수만큼 반복
                    v = 0 # 가중합 초기화
                    for j in range(len(X[0])): # 입력 노드의 개수만큼 반복
                        x = X[i][j] # 입력 데이터
                        v += W[i][l][j] * x # 은닉층의 가중합 = 입력층-은닉층 가중치 x 입력 데이터
                    hiddenY.append(sigmoid(v)) # 은닉층의 출력값 추가

if __name__ == '__main__':
    main()
'''