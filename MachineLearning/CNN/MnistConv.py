#-*- coding: utf-8 -*-
import os
import numpy as np
from scipy import signal

def softmax(v):
    v = np.subtract(v, np.max(v)) # 버퍼 오버플로 방지
    return np.exp(v) / np.sum(np.exp(v))

def relu(v):
    return np.maximum(0, v)

# 풀링 레이어
def pooling(activationMap, kernelStrideSize):
    row, col, filterCount = activationMap.shape # 액티베이션 맵의 행 크기, 열 크기, 필터 개수 저장
    poolingOutput = np.zeros((int(row / kernelStrideSize), int(col / kernelStrideSize), filterCount)) # 풀링 레이어 출력 데이터 초기화(커널 크기와 스트라이드가 모두 2이므로 출력 데이터의 크기는 반으로(10 x 10) 축소됨. 필터 수가 20개이므로 출력 데이터도 20개가 생성됨)
    for k in range(filterCount): # 필터 수만큼 반복
        kernel = np.ones((kernelStrideSize, kernelStrideSize)) / (2 * 2) # 커널 초기화
        image = signal.convolve2d(activationMap[:,:,k], kernel, 'valid') # 커널로 액티베이션 맵을 순환하며 합성곱 연산
        poolingOutput[:,:,k] = image[::kernelStrideSize, ::kernelStrideSize] # 스트라이드 크기로 분해해서 저장
    return poolingOutput # 2 x 2 크기의 커널과 스트라이드 2로 평균값 풀링 한 출력 데이터(10 x 10 x 20) 반환

# 합성곱 레이어
def convolution(x, W):
    filterRow, filterCol, filterCount = W.shape # 필터의 행 크기, 열 크기, 필터 개수 저장
    xRow, xCol = x.shape # 학습 데이터의 행 크기, 열 크기 저장
    featureRow, featureCol = xRow - filterRow + 1, xCol - filterCol + 1 # 피처 맵의 행 크기, 열 크기 저장
    featureMap = np.zeros((featureRow, featureCol, filterCount)) # 피처 맵 초기화
    for k in range(filterCount): # 필터 수만큼 반복
        filter = np.rot90(np.squeeze(W[:,:,k]), 2) # 필터 초기화
        featureMap[:, :, k] = signal.convolve2d(x, filter, 'valid') # 필터로 입력 데이터를 순환하며 합성곱 연산
    return featureMap # 20 x 20 x 20 크기의 피처 맵 반환(9 x 9 필터로 이미지를 순환하며 합성곱을 계산하면 최종 출력되는 피처 맵의 크기는 20 x 20이 됨. 필터 수가 20개이므로 피처 맵도 20개가 생성됨)

# CNN(W1 : 합성곱 레이어 필터(가중치) 행렬, W5 : 풀링 레이어(완전 연결 레이어 입력층)-완전 연결 레이어 은닉층 가중치 행렬, Wo : 완전 연결 레이어 은닉층-출력층 가중치 행렬, X : 학습 데이터, D : 학습 데이터 레이블, trainingDataCount : 학습 데이터 개수, outputNodeCount : 출력 노드 개수, filterCount : 필터 개수, kernelStrideSize : 커널 크기와 스트라이드)
def MnistConv(W1, W5, Wo, X, D, trainingDataCount, outputNodeCount, filterCount, kernelStrideSize):
    momentum1 = np.zeros_like(W1) # 합성곱 레이어의 필터 행렬(W1)과 같은 크기의 모멘텀 행렬 초기화
    momentum5 = np.zeros_like(W5) # 풀링 레이어(완전 연결 레이어 입력층)-완전 연결 레이어 은닉층 가중치 행렬(W5)과 같은 크기의 모멘텀 행렬 초기화
    momentumo = np.zeros_like(Wo) # 완전 연결 레이어 은닉층-출력층 가중치 행렬(Wo)과 같은 크기의 모멘텀 행렬 초기화
    alpha = 0.01 # 학습률
    beta = 0.95 # 모멘텀 상수
    miniBatchSize = 100 # 미니 배치 개수
    miniBatchStartIndex = np.arange(0, trainingDataCount, miniBatchSize) # 각 미니 배치의 시작 인덱스가 저장된 배열 생성(miniBatchStartIndex = [1, 101, 201, 301, ..., 7801, 7901])
    for batch in range(len(miniBatchStartIndex)): # 전체 학습 데이터의 개수가 8000개이므로 한 번의 epoch 동안 가중치는 80(8000 / 100)번 갱신됨
        dW1 = np.zeros_like(W1) # 합성곱 레이어 가중치 갱신값 초기화
        dW5 = np.zeros_like(W5) # 풀링 레이어(완전 연결 레이어 입력층)-완전 연결 레이어 은닉층 가중치 갱신값 초기화
        dWo = np.zeros_like(Wo) # 완전 연결 레이어 은닉층-출력층 가중치 갱신값 초기화
        for k in range(miniBatchStartIndex[batch], miniBatchStartIndex[batch] + miniBatchSize): # 미니 배치 개수가 100개이므로 100번 반복
            x = X[k,:,:] # 학습 데이터
            y1 = convolution(x, W1) # 합성곱 레이어(피처 맵 반환)
            y2 = relu(y1) # ReLU 활성함수 적용(액티베이션 맵 반환)
            y3 = pooling(y2, kernelStrideSize) # 풀링 레이어(풀링 레이어 출력 데이터 반환)
            y4 = np.reshape(y3, (-1, 1)) # 행렬곱을 위해 풀링 레이어 출력 데이터 모양 변경
            v1 = np.matmul(W5, y4) # 풀링 레이어(완전 연결 레이어 입력층)-완전 연결 레이어 은닉층의 가중합
            y5 = relu(v1) # ReLU 활성함수 적용
            v = np.matmul(Wo, y5) # 완전 연결 레이어 은닉층-출력층의 가중합
            y = softmax(v) # 소프트맥스 활성함수 적용(CNN 최종 출력 데이터)
            d = np.zeros((outputNodeCount, 1)) # 레이블
            d[D[k][0]][0] = 1 # 레이블 원-핫 인코딩 적용
            e = d - y # 출력 노드의 오차
            delta = e # 출력 노드의 델타(교차 엔트로피 비용함수)
            e5 = np.matmul(Wo.T, delta) # 완전 연결 레이어 은닉 노드의 오차
            delta5 = (y5 > 0) * e5 # 완전 연결 레이어 은닉 노드의 델타
            e4 = np.matmul(W5.T, delta5) # 풀링 레이어 마지막 노드의 오차
            e3 = np.reshape(e4, y3.shape) # 풀링 레이어 출력 데이터 크기로 풀링 레이어 마지막 노드의 오차 모양 변경
            e2 = np.zeros_like(y2) # 풀링 레이어 노드의 오차 초기화
            W3 = np.ones_like(y2) / (2 * 2) # 풀링 레이어 노드의 가중치 초기화
            for c in range(filterCount): # 필터의 개수만큼 반복
                e2[:,:,c] = np.kron(e3[:,:,c], np.ones((kernelStrideSize, kernelStrideSize))) * W3[:,:,c] # 풀링 레이어 노드의 오차
            delta2 = (y2 > 0) * e2 # 풀링 레이어 노드의 델타
            delta1 = np.zeros_like(W1) # 합성곱 레이어 노드의 델타 초기화
            for c in range(filterCount): # 필터의 개수만큼 반복
                delta1[:,:,c] = signal.convolve2d(x[:,:], np.rot90(delta2[:,:,c], 2), 'valid') # 합성곱 레이어 노드의 델타
            dW1 = dW1 + delta1 # 합성곱 레이어 가중치(필터) 갱신값
            dW5 = dW5 + np.matmul(delta5, y4.T) # 풀링 레이어(완전 연결 레이어 입력층)-완전 연결 레이어 은닉층 가중치 갱신값
            dWo = dWo + np.matmul(delta, y5.T) # 완전 연결 레이어 은닉층-출력층 가중치 갱신값
        # 가중치 갱신 값에 미니 배치 적용
        dW1 = dW1 / miniBatchSize
        dW5 = dW5 / miniBatchSize
        dWo = dWo / miniBatchSize
        momentum1 = alpha * dW1 + beta * momentum1 # 합성곱 레이어 모멘텀 계산
        W1 = W1 + momentum1 # 합성곱 레이어 가중치(필터) 갱신
        momentum5 = alpha * dW5 + beta * momentum5 # 풀링 레이어(완전 연결 레이어 입력층)-완전 연결 레이어 은닉층 모멘텀 계산
        W5 = W5 + momentum5 # 풀링 레이어(완전 연결 레이어 입력층)-완전 연결 레이어 은닉층 가중치 갱신
        momentumo = alpha * dWo + beta * momentumo # 완전 연결 레이어 은닉층-출력층 모멘텀 계산
        Wo = Wo + momentumo # 완전 연결 레이어 은닉층-출력층 가중치 갱신
    return W1, W5, Wo # 갱신된 가중치 반환

# Baked Code
def loadMnistData(imagefile, labelfile):
    import gzip
    from struct import unpack
    images = gzip.open(imagefile, 'rb')
    labels = gzip.open(labelfile, 'rb')
    images.read(4)
    number_of_images = images.read(4)
    number_of_images = unpack('>I', number_of_images)[0]
    rows = images.read(4)
    rows = unpack('>I', rows)[0]
    cols = images.read(4)
    cols = unpack('>I', cols)[0]
    labels.read(4)
    N = labels.read(4)
    N = unpack('>I', N)[0]
    if number_of_images != N:
        raise Exception('number of labels did not match the number of images')
    x = np.zeros((N, rows, cols), dtype=np.float32)
    y = np.zeros((N, 1), dtype=np.uint8)
    for i in range(N):
        for row in range(rows):
            for col in range(cols):
                tmp_pixel = images.read(1)
                tmp_pixel = unpack('>B', tmp_pixel)[0]
                x[i][row][col] = tmp_pixel
        tmp_label = labels.read(1)
        y[i] = unpack('>B', tmp_label)[0]
    return (x, y)

def main():
    images, labels = loadMnistData(os.getcwd() + '\\MNIST\\t10k-images-idx3-ubyte.gz', os.getcwd() + '\\MNIST\\t10k-labels-idx1-ubyte.gz') # MNIST 데이터 로드
    images = np.divide(images, 255)
    filterWidth, filterHeight, filterCount = 9, 9, 20 # 필터 가로 크기, 필터 세로 크기, 필터 수(깊이)
    kernelStrideSize = 2 # 커널 크기와 스트라이드
    hiddenNodeCount, outputNodeCount = 100, 10 # 은닉 노드 개수, 출력 노드 개수
    trainingDataCount, testDataCount = 8000, 2000 # 학습 데이터 개수, 평가 데이터 개수
    W1 = 1e-2 * np.random.randn(filterWidth, filterHeight, filterCount) # 합성곱 레이어 필터(가중치) 행렬(9(가로) x 9(세로) x 20(커널 수, 깊이))
    W5 = np.random.uniform(-1, 1, (hiddenNodeCount, 2000)) * np.sqrt(6) / np.sqrt(360 + 2000) # 풀링 레이어(완전 연결 레이어 입력층)-완전 연결 레이어 은닉층 가중치 행렬(100(은닉 노드 개수) x 2000(2 x 2 크기의 커널과 스트라이드 2로 평균값 풀링 한 출력 데이터(10 x 10 x 20)))
    Wo = np.random.uniform(-1, 1, (outputNodeCount, hiddenNodeCount)) * np.sqrt(6) / np.sqrt(10 + 100) # 완전 연결 레이어 은닉층-출력층 가중치 행렬(10(출력 노드 개수) x 100(은닉 노드 개수))
    X = images[0:trainingDataCount,:,:] # 8000개의 학습 데이터
    D = labels[0:trainingDataCount] # 학습 데이터 레이블
    epoch = 3 # 학습 횟수
    for _ in range(epoch):
        W1, W5, Wo = MnistConv(W1, W5, Wo, X, D, trainingDataCount, outputNodeCount, filterCount, kernelStrideSize) # 학습
    X = images[trainingDataCount:trainingDataCount + testDataCount,:,:] # 2000개의 평가 데이터
    D = labels[trainingDataCount:trainingDataCount + testDataCount] # 평가 데이터 레이블
    accuracy = 0.0 # 정확도
    for k in range(testDataCount): # 평가 데이터 개수만큼 반복
        x = X[k,:,:] # 평가 데이터
        y1 = convolution(x, W1) # 합성곱 레이어(피처 맵 반환)
        y2 = relu(y1) # ReLU 활성함수 적용(액티베이션 맵 반환)
        y3 = pooling(y2, kernelStrideSize) # 풀링 레이어(풀링 레이어 출력 데이터 반환)
        y4 = np.reshape(y3, (-1, 1)) # 행렬곱을 위해 풀링 레이어 출력 데이터 모양 변경
        v5 = np.matmul(W5, y4) # 풀링 레이어(완전 연결 레이어 입력층)-완전 연결 레이어 은닉층의 가중합
        y5 = relu(v5) # ReLU 활성함수 적용
        v = np.matmul(Wo, y5) # 완전 연결 레이어 은닉층-출력층의 가중합
        y = softmax(v) # 소프트맥스 활성함수 적용(CNN 최종 출력 데이터)
        if np.argmax(y) == D[k][0]: # 출력값이 레이블과 같을 경우(이미지를 제대로 인식했을 경우)
            accuracy += 1.0
            print('Label : %d, Output : %f' % (D[k][0], y[np.argmax(y)]))
    accuracyRatio = (accuracy / testDataCount) * 100
    print('\nAccuracy : ' + str(accuracyRatio) + '%')

if __name__ == '__main__':
    main()