#-*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

def sigmoid(v):
    return 1.0 / (1.0 + np.exp(-v))

def deltaSGD(W, X, D):
    alpha = 0.9 # 학습률
    for k in range(len(X)): # 학습 데이터 개수만큼 반복
        x = X[k,:].T # 학습 데이터(1 x 3 행렬(X[k,:])을 전치 행렬로 변경(3 x 1 행렬(x)))
        d = D[k] # 레이블
        v = np.matmul(W, x) # 가중합(1 x 1 행렬) = 가중치(1 x 3 행렬) x 학습 데이터(3 x 1 행렬)
        y = sigmoid(v) # 출력값
        e = d - y # 오차
        delta = y * (1 - y) * e # 델타(시그모이드 함수(f)의 도함수 = f(1-f))
        dW = alpha * delta * x # 가중치 갱신값
        # 가중치 갱신
        W[0][0] = W[0][0] + dW[0]
        W[0][1] = W[0][1] + dW[1]
        W[0][2] = W[0][2] + dW[2]
    return W # 갱신된 가중치 반환

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
    dWavg = dWsum / len(X) # 가중치 갱신값의 평균값
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
    W1 = 2 * np.random.random((1, 3)) - 1 # SGD 가중치
    W2 = 2 * np.random.random((1, 3)) - 1 # Batch 가중치
    E1 = np.zeros(1000) # SGD 출력 오차의 제곱합의 평균값
    E2 = np.zeros(1000) # Batch 출력 오차의 제곱합의 평균값
    epoch = 1000 # 학습 횟수
    for e in range(epoch):
        es1, es2 = 0, 0 # SGD, Batch 출력 오차의 제곱합 초기화
        W1 = deltaSGD(W1, X, D) # SGD 학습
        W2 = deltaBatch(W2, X, D) # Batch 학습
        # Test
        for k in range(len(X)): # 입력 데이터 개수만큼 반복
            x = X[k,:].T # 입력 데이터
            d = D[k] # 레이블
            v1 = np.matmul(W1, x) # SGD 가중합
            y1 = sigmoid(v1) # SGD 출력값
            es1 = es1 + (d - y1)**2 # SGD 출력 오차의 제곱합
            v2 = np.matmul(W2, x) # Batch 가중합
            y2 = sigmoid(v2) # Batch 출력값
            es2 = es2 + (d - y2)**2 # Batch 출력 오차의 제곱합
        E1[e] = es1 / len(X) # SGD 출력 오차의 제곱합의 평균값
        E2[e] = es2 / len(X) # Batch 출력 오차의 제곱합의 평균값
    SGD, = plt.plot(E1, 'red')
    Batch, = plt.plot(E2, 'b:')
    plt.xlabel('Epoch')
    plt.ylabel('Average of Training Error')
    plt.legend([SGD, Batch], ['SGD', 'Batch'])
    plt.show()

if __name__ == '__main__':
    main()