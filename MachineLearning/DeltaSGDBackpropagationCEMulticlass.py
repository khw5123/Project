#-*- coding: utf-8 -*-
import numpy as np

def sigmoid(v):
    return 1.0 / (1.0 + np.exp(-v))

def softmax(v):
    v = np.subtract(v, np.max(v)) # 버퍼 오버플로 방지
    return np.exp(v) / np.sum(np.exp(v))

def deltaSGDBackpropagationCEMulticlass(W1, W2, X, D):
    alpha = 0.9 # 학습률
    for k in range(len(X)): # 학습 데이터 개수만큼 반복
        x = np.reshape(X[:,:,k], (25, 1)) # 학습 데이터
        d = D[k,:].T # 레이블
        v1 = np.matmul(W1, x) # 은닉층의 가중합
        y1 = sigmoid(v1) # 은닉층의 출력값
        v = np.matmul(W2, y1) # 출력층의 가중합
        y = softmax(v) # 출력층의 출력값
        e = d - y # 출력 노드의 오차
        delta = e # 출력 노드의 델타(교차 엔트로피)
        e1 = np.matmul(W2.T, delta) # 은닉 노드의 오차
        delta1 = y1 * (1 - y1) * e1 # 은닉 노드의 델타
        dW1 = alpha * delta1 * x.T # 입력층-은닉층 가중치 갱신값
        W1 = W1 + dW1 # 입력층-은닉층 가중치 갱신
        dW2 = alpha * delta * y1.T # 은닉층-출력층 가중치 갱신값
        W2 = W2 + dW2 # 은닉층-출력층 가중치 갱신
    return W1, W2 # 갱신된 가중치 반환

def learning():
    X = np.zeros((5, 5, 5)) # 학습 데이터
    X[:,:,0] = [[0,1,1,0,0], 
                [0,0,1,0,0], 
                [0,0,1,0,0], 
                [0,0,1,0,0], 
                [0,1,1,1,0]] # 숫자 1
    X[:,:,1] = [[1,1,1,1,0], 
                [0,0,0,0,1], 
                [0,1,1,1,0], 
                [1,0,0,0,0], 
                [1,1,1,1,1]] # 숫자 2
    X[:,:,2] = [[1,1,1,1,0], 
                [0,0,0,0,1], 
                [0,1,1,1,0], 
                [0,0,0,0,1], 
                [1,1,1,1,0]] # 숫자 3
    X[:,:,3] = [[0,0,0,1,0], 
                [0,0,1,1,0], 
                [0,1,0,1,0], 
                [1,1,1,1,1], 
                [0,0,0,1,0]] # 숫자 4
    X[:,:,4] = [[1,1,1,1,1], 
                [1,0,0,0,0], 
                [1,1,1,1,0], 
                [0,0,0,0,1], 
                [1,1,1,1,0]] # 숫자 5
    D = np.array([[[1,0,0,0,0]], 
                  [[0,1,0,0,0]], 
                  [[0,0,1,0,0]], 
                  [[0,0,0,1,0]], 
                  [[0,0,0,0,1]]]) # 레이블
    W1 = 2 * np.random.random((50, 25)) - 1 # 입력층-은닉층 가중치
    W2 = 2 * np.random.random((5, 50)) - 1 # 은닉층-출력층 가중치
    epoch = 10000 # 학습 횟수
    for _ in range(epoch):
        W1, W2 = deltaSGDBackpropagationCEMulticlass(W1, W2, X, D) # 학습
    return W1, W2 # 가중치 반환

def main():
    X = np.zeros((5, 5, 5)) # 입력 데이터
    X[:,:,0] = [[0,0,1,1,0], 
                [0,0,1,1,0], 
                [0,1,0,1,0], 
                [0,0,0,1,0], 
                [0,1,1,1,0]] # 숫자 1 또는 4와 비슷한 데이터
    X[:,:,1] = [[1,1,1,1,0], 
                [0,0,0,0,1], 
                [0,1,1,1,0], 
                [1,0,0,0,1], 
                [1,1,1,1,1]] # 숫자 2 또는 3과 비슷한 데이터
    X[:,:,2] = [[1,1,1,1,0], 
                [1,0,0,0,1], 
                [1,1,1,1,0], 
                [0,0,0,0,1], 
                [1,1,1,1,0]] # 숫자 3 또는 5와 비슷한 데이터
    X[:,:,3] = [[0,0,1,0,0], 
                [0,0,1,0,0], 
                [0,0,1,0,0], 
                [0,0,1,1,1], 
                [0,1,1,0,0]] # 숫자 1 또는 4와 비슷한 데이터
    X[:,:,4] = [[0,1,1,1,1], 
                [0,1,0,0,0], 
                [0,1,1,1,0], 
                [0,0,0,1,0], 
                [1,1,1,1,0]] # 숫자 5와 비슷한 데이터
    W1, W2 = learning() # 학습 후 가중치 저장
    # Test
    for k in range(len(X)): # 입력 데이터 개수만큼 반복
        x = np.reshape(X[:,:,k], (25, 1)) # 입력 데이터
        v1 = np.matmul(W1, x) # 은닉층의 가중합
        y1 = sigmoid(v1) # 은닉층의 출력값
        v = np.matmul(W2, y1) # 출력층의 가중합
        y = softmax(v) # 출력층의 출력값
        print('Label :', (k + 1), ', Output :', (list(y).index(max(y)) + 1), 'Probability :', max(y))

if __name__ == '__main__':
    main()

''' Without Numpy
#-*- coding: utf-8 -*-
import random
import math

def sigmoid(v):
    return 1 / (1 + math.exp(-v))

def softmax(v, n):
    return math.exp(v[n]) / sum([math.exp(v[i]) for i in range(len(v))])

def deltaSGDBackpropagationCEMulticlass(W, X, D, hiddenLayerCount, hiddenNodeCount, inputNodeCount, outputNodeCount):
    alpha = 0.9 # 학습률
    for i in range(len(X)): # 학습 데이터 개수만큼 반복
        for n in range(outputNodeCount): # 출력 노드의 개수만큼 반복
            hiddenY = [] # 은닉층의 출력값 초기화
            outputV = [] # 출력 노드의 가중합 초기화
            y = 0 # 출력층의 출력값 초기화
            hiddenDelta = [] # 은닉층의 델타 초기화
            weightedSum = [] # 은닉층-출력층(은닉 노드)의 순방향 신호의 가중합 초기화
            for k in range(hiddenLayerCount + 1): # 입력층-은닉층(k = 0), 은닉층-출력층(k = 1)
                v = 0 # 가중합 초기화
                if k == hiddenLayerCount: # 은닉층-출력층
                    for m in range(0,outputNodeCount): # 출력 노드의 개수만큼 반복
                        v= 0 # 가중합 초기화
                        for j in range(hiddenNodeCount): # 은닉 노드의 개수만큼 반복
                            x = hiddenY[j] # 입력값
                            weightedSum.append(W[i][j][inputNodeCount + m] * x) # 은닉층-출력층(은닉 노드)의 가중합 추가
                            v += W[i][j][inputNodeCount + m] * x # 출력층의 가중합 = 은닉층-출력층 가중치 x 입력값
                        outputV.append(v) # 출력 노드의 가중합 추가
                    y = softmax(outputV, n) # 출력층의 출력값
                else: # 입력층-은닉층
                    for l in range(hiddenNodeCount): # 은닉 노드의 개수만큼 반복
                        v = 0 # 가중합 초기화
                        for j in range(inputNodeCount): # 입력 노드의 개수만큼 반복
                            x = X[i][j] # 학습 데이터
                            v += W[i][l][j] * x # 은닉층의 가중합 = 입력층-은닉층 가중치 x 학습 데이터
                        hiddenY.append(sigmoid(v)) # 은닉층의 출력값 추가
            d = D[i][n] # 레이블
            e = d - y # 출력 노드의 오차
            outputDelta = e # 출력 노드의 델타(교차 엔트로피)
            for k in range(hiddenLayerCount): # 은닉층-출력층(k = 0)
                if k == 0: # 은닉층-출력층
                    for j in range(hiddenNodeCount): # 은닉 노드의 개수만큼 반복
                        e = W[i][j][inputNodeCount + m] * outputDelta # 은닉 노드의 오차
                        y = sigmoid(weightedSum[j]) # 은닉층-출력층(은닉 노드)의 순방향 신호의 가중합을 은닉 노드의 활성함수에 적용
                        delta = y * (1 - y) * e # 은닉 노드의 델타
                        hiddenDelta.append(delta) # 은닉 노드의 델타 추가
            for k in range(hiddenLayerCount + 1): # 은닉층-출력층(k = 0), 입력층-은닉층(k = 1)
                if k == hiddenLayerCount: # 입력층-은닉층
                    for l in range(hiddenNodeCount): # 은닉 노드의 개수만큼 반복
                        for j in range(inputNodeCount): # 입력 노드의 개수만큼 반복
                            dW = alpha * hiddenDelta[l] * X[i][j] # 입력층-은닉층 가중치 갱신값
                            W[i][l][j] += dW # # 입력층-은닉층 가중치 갱신
                else: # 은닉층-출력층
                    for j in range(hiddenNodeCount): # 은닉 노드의 개수만큼 반복
                        dW = alpha * outputDelta * hiddenY[j] # 은닉층-출력층 가중치 갱신값
                        W[i][j][inputNodeCount + m] += dW # 은닉층-출력층 가중치 갱신

def learning():
    X = [[0,1,1,0,0, 
          0,0,1,0,0, 
          0,0,1,0,0, 
          0,0,1,0,0, 
          0,1,1,1,0], # 숫자 1
         [1,1,1,1,0, 
          0,0,0,0,1, 
          0,1,1,1,0, 
          1,0,0,0,0, 
          1,1,1,1,1], # 숫자 2
         [1,1,1,1,0, 
          0,0,0,0,1, 
          0,1,1,1,0, 
          0,0,0,0,1, 
          1,1,1,1,0], # 숫자 3
         [0,0,0,1,0, 
          0,0,1,1,0, 
          0,1,0,1,0, 
          1,1,1,1,1, 
          0,0,0,1,0], # 숫자 4
         [1,1,1,1,1, 
          1,0,0,0,0, 
          1,1,1,1,0, 
          0,0,0,0,1, 
          1,1,1,1,0] # 숫자 5
         ] # 학습 데이터
    D = [[1,0,0,0,0], 
         [0,1,0,0,0], 
         [0,0,1,0,0], 
         [0,0,0,1,0], 
         [0,0,0,0,1]
         ] # 레이블
    hiddenLayerCount = 1 # 은닉층 개수
    hiddenNodeCount = 50 # 은닉 노드 개수
    inputNodeCount = len(X[0]) # 입력 노드 개수
    outputNodeCount = len(D) # 출력 노드 개수
    W = [] # 가중치(학습 데이터 개수 x 은닉 노드 개수 x (입력 노드 개수 + 출력 노드 개수))
    for i in range(len(X)): # 학습 데이터 개수만큼 반복
        W.append([])
        for j in range(hiddenNodeCount): # 은닉 노드 개수만큼 반복
            W[i].append([])
            for k in range(inputNodeCount + outputNodeCount): # 입력 노드 개수 + 출력 노드 개수만큼 반복
                W[i][j].append(2 * random.random() - 1) # 가중치 초기화
    epoch = 10000 # 학습 횟수
    for _ in range(epoch):
        deltaSGDBackpropagationCEMulticlass(W, X, D, hiddenLayerCount, hiddenNodeCount, inputNodeCount, outputNodeCount)
    return W, hiddenLayerCount, hiddenNodeCount, inputNodeCount, outputNodeCount

def main():
    X = [[0,0,1,1,0, 
          0,0,1,1,0, 
          0,1,0,1,0, 
          0,0,0,1,0, 
          0,1,1,1,0], # 숫자 1 또는 4와 비슷한 데이터
         [1,1,1,1,0, 
          0,0,0,0,1, 
          0,1,1,1,0, 
          1,0,0,0,1, 
          1,1,1,1,0], # 숫자 2 또는 3과 비슷한 데이터
         [1,1,1,1,0, 
          1,0,0,0,1, 
          1,1,1,1,0, 
          0,0,0,0,1, 
          1,1,1,1,0], # 숫자 3 또는 5와 비슷한 데이터
         [0,0,1,0,0, 
          0,0,1,0,0, 
          0,0,1,0,0, 
          0,0,1,1,1, 
          0,1,1,0,0], # 숫자 1 또는 4와 비슷한 데이터
         [0,1,1,1,1, 
          0,1,0,0,0, 
          0,1,1,1,0, 
          0,0,0,1,0, 
          1,1,1,1,0] # 숫자 5와 비슷한 데이터
         ] # 입력 데이터
    W, hiddenLayerCount, hiddenNodeCount, inputNodeCount, outputNodeCount = learning() # 학습 후 가중치 저장
    # Test
    for i in range(len(X)): # 입력 데이터 개수만큼 반복
        outputProbability = []
        for n in range(outputNodeCount): # 출력 노드의 개수만큼 반복
            hiddenY = [] # 은닉층의 출력값 초기화
            outputV = [] # 출력 노드의 가중합 초기화
            y = 0 # 출력층의 출력값 초기화
            for k in range(hiddenLayerCount + 1): # 입력층-은닉층(k = 0), 은닉층-출력층(k = 1)
                v = 0 # 가중합 초기화
                if k == hiddenLayerCount: # 은닉층-출력층
                    for m in range(0,outputNodeCount): # 출력 노드의 개수만큼 반복
                        v= 0 # 가중합 초기화
                        for j in range(hiddenNodeCount): # 은닉 노드의 개수만큼 반복
                            x = hiddenY[j] # 입력값
                            v += W[i][j][inputNodeCount + m] * x # 출력층의 가중합 = 은닉층-출력층 가중치 x 입력값
                        outputV.append(v) # 출력 노드의 가중합 추가
                    y = softmax(outputV, n) # 출력층의 출력값
                    outputProbability.append(y)
                else: # 입력층-은닉층
                    for l in range(hiddenNodeCount): # 은닉 노드의 개수만큼 반복
                        v = 0 # 가중합 초기화
                        for j in range(inputNodeCount): # 입력 노드의 개수만큼 반복
                            x = X[i][j] # 입력 데이터
                            v += W[i][l][j] * x # 은닉층의 가중합 = 입력층-은닉층 가중치 x 입력 데이터
                        hiddenY.append(sigmoid(v)) # 은닉층의 출력값 추가
        print('Label :', (i + 1), ', Output :', (list(outputProbability).index(max(outputProbability)) + 1), 'Probability :', max(outputProbability))

if __name__ == '__main__':
    main()
'''