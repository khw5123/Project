#-*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

def sigmoid(v):
    return 1.0 / (1.0 + np.exp(-v))

def deltaSGDBackpropagationCE(W1, W2, X, D):
    alpha = 0.9 # 학습률
    for k in range(len(X)): # 학습 데이터 개수만큼 반복
        x = X[k,:].T # 학습 데이터
        d = D[k] # 레이블
        v1 = np.matmul(W1, x) # 은닉층의 가중합
        y1 = sigmoid(v1) # 은닉층의 출력값
        v = np.matmul(W2, y1) # 출력층의 가중합
        y = sigmoid(v) # 출력층의 출력값
        e = d - y # 출력 노드의 오차
        delta = e # 출력 노드의 델타(교차 엔트로피)
        e1 = np.matmul(W2.T, delta) # 은닉 노드의 오차
        delta1 = y1 * (1 - y1) * e1 # 은닉 노드의 델타
        dW1 = (alpha * delta1).reshape(4, 1) * x.reshape(1, 3) # 입력층-은닉층 가중치 갱신값
        W1 = W1 + dW1 # 입력층-은닉층 가중치 갱신
        dW2 = alpha * delta * y1 # 은닉층-출력층 가중치 갱신값
        W2 = W2 + dW2 # 은닉층-출력층 가중치 갱신
    return W1, W2 # 갱신된 가중치 반환

def deltaSGDBackpropagation(W1, W2, X, D):
    alpha = 0.9 # 학습률
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
        W1 = W1 + dW1 # 입력층-은닉층 가중치 갱신
        dW2 = alpha * delta * y1 # 은닉층-출력층 가중치 갱신값
        W2 = W2 + dW2 # 은닉층-출력층 가중치 갱신
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
    W11 = 2 * np.random.random((4, 3)) - 1 # 입력층-은닉층 가중치(교차 엔트로피)
    W12 = 2 * np.random.random((1, 4)) - 1 # 은닉층-출력층 가중치(교차 엔트로피)
    W21 = np.array(W11) # 입력층-은닉층 가중치
    W22 = np.array(W12) # 은닉층-출력층 가중치
    E1 = np.zeros(1000) # 출력 오차의 제곱합의 평균값(교차 엔트로피)
    E2 = np.zeros(1000) # 출력 오차의 제곱합의 평균값
    epoch = 1000 # 학습 횟수
    for e in range(epoch):
        es1, es2 = 0, 0 # 출력 오차의 제곱합 초기화
        W11, W12 = deltaSGDBackpropagationCE(W11, W12, X, D) # 학습(교차 엔트로피)
        W21, W22 = deltaSGDBackpropagation(W21, W22, X, D) # 학습
        for k in range(len(X)): # 입력 데이터 개수만큼 반복
            x = X[k,:].T # 입력 데이터
            d = D[k] # 레이블
            v1 = np.matmul(W11, x) # 은닉층의 가중합(교차 엔트로피)
            y1 = sigmoid(v1) # 은닉층의 출력값(교차 엔트로피)
            v = np.matmul(W12, y1) # 출력층의 가중합(교차 엔트로피)
            y = sigmoid(v) # 출력층의 출력값(교차 엔트로피)
            es1 = es1 + (d - y)**2 # 출력 오차의 제곱합(교차 엔트로피)
            v1 = np.matmul(W21, x) # 은닉층의 가중합
            y1 = sigmoid(v1) # 은닉층의 출력값
            v = np.matmul(W22, y1) # 출력층의 가중합
            y = sigmoid(v) # 출력층의 출력값
            es2 = es2 + (d - y)**2 # 출력 오차의 제곱합
        E1[e] = es1 / len(D) # 출력 오차의 제곱합의 평균값(교차 엔트로피)
        E2[e] = es2 / len(D) # 출력 오차의 제곱합의 평균값
    CE, = plt.plot(E1, 'red')
    SSE, = plt.plot(E2, 'b:')
    plt.xlabel('Epoch')
    plt.ylabel('Average of Training error')
    plt.legend([CE, SSE], ['Cross Entropy', 'Sum of Squared Error'])
    plt.show()

if __name__ == '__main__':
    main()