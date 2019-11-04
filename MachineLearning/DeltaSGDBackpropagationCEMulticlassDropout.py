#-*- coding: utf-8 -*-
import numpy as np

def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))

def softmax(v):
    v = np.subtract(v, np.max(v)) # 버퍼 오버플로 방지
    return np.exp(v) / np.sum(np.exp(v))

def dropout(y, ratio):
    dropRatio = np.zeros_like(y) # 드롭아웃 비율값(값을 모두 0으로 초기화)
    notDropSize = round(y.size * (1 - ratio)) # 드롭아웃 하지 않을 크기(은닉 노드의 개수 x 드롭아웃 하지 않을 비율)
    notDropIndex = np.random.choice(y.size, int(notDropSize), replace=False) # 드롭아웃 하지 않을 은닉 노드들의 인덱스
    dropRatio[notDropIndex] = 1.0 / (1.0 - ratio) # 드롭아웃된 은닉 노드들로 인한 출력값을 보상해주기 위한 비율값(드롭아웃 되면 해당 계층의 출력값의 크기가 많이 줄어들어서 이러한 출력값의 감소를 보상하기 위해 드롭아웃되지 않는 노드의 출력값을 비율에 맞춰 임의로 키워준 것임)
    return y * dropRatio # 은닉층의 출력값 x 드롭아웃 비율값 반환

def deltaSGDBackpropagationCEMulticlassDropout(W1, W2, W3, W4, X, D):
    alpha = 0.01 # 학습률
    for k in range(len(X)): # 학습 데이터 개수만큼 반복
        x = np.reshape(X[:,:,k], (25, 1)) # 학습 데이터
        d = D[k,:].T # 레이블
        v1 = np.matmul(W1, x) # 은닉층1의 가중합
        y1 = sigmoid(v1) # 은닉층1의 출력값
        y1 = dropout(y1, 0.2) # 은닉층1의 출력값 드롭아웃 적용
        v2 = np.matmul(W2, y1) # 은닉층2의 가중합
        y2 = sigmoid(v2) # 은닉층2의 출력값
        y2 = dropout(y2, 0.2) # 은닉층2의 출력값 드롭아웃 적용
        v3 = np.matmul(W3, y2) # 은닉층3의 가중합
        y3 = sigmoid(v3) # 은닉층3의 출력값
        y3 = dropout(y3, 0.2) # 은닉층3의 출력값 드롭아웃 적용
        v = np.matmul(W4, y3) # 출력층의 가중합
        y = softmax(v) # 출력층의 출력값
        e = d - y # 출력 노드의 오차
        delta = e # 출력 노드의 델타(교차 엔트로피)
        e3 = np.matmul(W4.T, delta) # 은닉층3의 오차
        delta3 = y3 * (1 - y3) * e3 # 은닉층3의 델타
        e2 = np.matmul(W3.T, delta3) # 은닉층2의 오차
        delta2 = y2 * (1 - y2) * e2 # 은닉층2의 델타
        e1 = np.matmul(W2.T, delta2) # 은닉층1의 오차
        delta1 = y1 * (1 - y1) * e1 # 은닉층1의 델타
        dW1 = alpha * delta1 * x.T # 입력층-은닉층1 가중치 갱신값
        W1 = W1 + dW1 # 입력층-은닉층1 가중치 갱신
        dW2 = alpha * delta2 * y1.T # 은닉층1-은닉층2 가중치 갱신값
        W2 = W2 + dW2 # 은닉층1-은닉층2 가중치 갱신
        dW3 = alpha * delta3 * y2.T # 은닉층2-은닉층3 가중치 갱신값
        W3 = W3 + dW3 # 은닉층2-은닉층3 가중치 갱신
        dW4 = alpha * delta * y3.T # 은닉층3-출력층 가중치 갱신값
        W4 = W4 + dW4 # 은닉층3-출력층 가중치 갱신
    return W1, W2, W3, W4 # 갱신된 가중치 반환

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
    W1 = 2 * np.random.random((20, 25)) - 1 # 입력층-은닉층1 가중치
    W2 = 2 * np.random.random((20, 20)) - 1 # 은닉층1-은닉층2 가중치
    W3 = 2 * np.random.random((20, 20)) - 1 # 은닉층2-은닉층3 가중치
    W4 = 2 * np.random.random((5, 20)) - 1 # 은닉층3-출력층 가중치
    epoch = 10000 # 학습 횟수
    for _ in range(epoch):
        W1, W2, W3, W4 = deltaSGDBackpropagationCEMulticlassDropout(W1, W2, W3, W4, X, D) # 학습
    return W1, W2, W3, W4 # 가중치 반환

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
    W1, W2, W3, W4 = learning() # 학습 후 가중치 저장
    # Test
    for k in range(len(X)): # 입력 데이터 개수만큼 반복
        x = np.reshape(X[:,:,k], (25, 1)) # 입력 데이터
        v1 = np.matmul(W1, x) # 은닉층1의 가중합
        y1 = sigmoid(v1) # 은닉층1의 출력값
        y1 = dropout(y1, 0.2) # 은닉층1의 출력값 드롭아웃 적용
        v2 = np.matmul(W2, y1) # 은닉층2의 가중합
        y2 = sigmoid(v2) # 은닉층2의 출력값
        y2 = dropout(y2, 0.2) # 은닉층2의 출력값 드롭아웃 적용
        v3 = np.matmul(W3, y2) # 은닉층3의 가중합
        y3 = sigmoid(v3) # 은닉층3의 출력값
        y3 = dropout(y3, 0.2) # 은닉층3의 출력값 드롭아웃 적용
        v = np.matmul(W4, y3) # 출력층의 가중합
        y = softmax(v) # 출력층의 출력값
        print('Label :', (k + 1), ', Output :', (list(y).index(max(y)) + 1), 'Probability :', max(y))

if __name__ == '__main__':
    main()