#-*- coding: utf-8 -*-
import os
import numpy as np
import scipy
import matplotlib.pyplot as plt

class NeuralNetwork:
    def __init__(self, learningRate, inputNodeCount, hiddenNodeCount, outputNodeCount):
        self.learningRate = learningRate # 학습률 저장
        self.inputNodeCount = inputNodeCount # 입력 노드 개수 저장
        self.hiddenNodeCount = hiddenNodeCount # 은닉 노드 개수 저장
        self.outputNodeCount = outputNodeCount # 출력 노드 개수 저장
        self.weightInputHidden = np.random.normal(0.0, pow(self.inputNodeCount, -0.5), (self.hiddenNodeCount, self.inputNodeCount)) # 입력층-은닉층의 가중치(은닉 노드 개수 x 입력 노드 개수)
        self.weightHiddenOutput = np.random.normal(0.0, pow(self.hiddenNodeCount, -0.5), (self.outputNodeCount, self.hiddenNodeCount)) # 은닉층-출력층의 가중치(출력 노드 개수 x 은닉 노드 개수)
        self.sigmoid = lambda x: scipy.special.expit(x) # 시그모이드 활성함수
    
    def train(self, trainData, label): # 학습 함수
        trainData = np.array(trainData, ndmin=2).T # 1차원 학습 데이터 배열을 2차원 배열로 변경 후 전치 행렬로 변환
        label = np.array(label, ndmin=2).T # 1차원 레이블 배열을 2차원 배열로 변경 후 전치 행렬로 변환
        weightedSumHidden = np.dot(self.weightInputHidden, trainData) # 은닉층의 가중합
        hiddenOutputValue = self.sigmoid(weightedSumHidden) # 은닉층의 출력값
        weightedSumOutput = np.dot(self.weightHiddenOutput, hiddenOutputValue) # 출력층의 가중합
        outputValue = self.sigmoid(weightedSumOutput) # 출력층의 출력값
        outputError = label - outputValue # 출력 노드의 오차
        outputDelta = outputError # 출력 노드의 델타(교차 엔트로피)
        hiddenError = np.dot(self.weightHiddenOutput.T, outputDelta) # 은닉 노드의 오차
        hiddenDalta = hiddenOutputValue * (1.0 - hiddenOutputValue) * hiddenError # 은닉 노드의 델타
        self.weightInputHidden += self.learningRate * np.dot(hiddenDalta, np.transpose(trainData)) # 입력층-은닉층 가중치 갱신
        self.weightHiddenOutput += self.learningRate * np.dot(outputDelta, np.transpose(hiddenOutputValue)) # 은닉층-출력층 가중치 갱신
    
    def query(self, testData): # 평가 함수
        testData = np.array(testData, ndmin=2).T # 1차원 평가 데이터 배열을 2차원 배열로 변경 후 전치 행렬로 변환
        weightedSumHidden = np.dot(self.weightInputHidden, testData) # 은닉층의 가중합
        hiddenOutputValue = self.sigmoid(weightedSumHidden) # 은닉층의 출력값
        weightedSumOutput = np.dot(self.weightHiddenOutput, hiddenOutputValue) # 출력층의 가중합
        outputValue = self.sigmoid(weightedSumOutput) # 출력층의 출력값
        return outputValue # 출력값 반환

def learning():
    inputNodeCount = 784 # 입력 노드 개수(28 x 28)
    hiddenNodeCount = 200 # 은닉 노드 개수
    outputNodeCount = 10 # 출력 노드 개수(0 ~ 9)
    learningRate = 0.1 # 학습률(너무 작으면 경사 하강의 속도를 제한하고, 너무 크면 경사 하강 과정에서 오버슈팅이 일어나서 성능이 떨어짐)
    obj = NeuralNetwork(learningRate, inputNodeCount, hiddenNodeCount, outputNodeCount) # 신경망 객체 생성
    with open(os.getcwd() + '\\mnist_dataset\\mnist_train_5000.csv', 'r') as fp:
        trainData = fp.readlines() # 학습 데이터
    epoch = 10 # 학습 횟수
    for _ in range(epoch):
        for data in trainData:
            inputData = (np.asfarray(data.split(',')[1:]) / 255.0 * 0.99) + 0.01 # 레이블을 제외한 값들을 색상(RGB) 값의 범위(0 ~ 255)로 변경 후 0.01 ~ 1.0 사이의 값으로 변환
            label = np.zeros(outputNodeCount) + 0.01 # 레이블 배열 초기화
            label[int(data.split(',')[0])] = 0.99 # 레이블이 있는 0번째 인덱스의 값을 인덱스로 하는 레이블 배열의 값에 0.99를 더해서 레이블 값을 1로 변경
            obj.train(inputData, label) # 학습
            rotationInputData1 = scipy.ndimage.interpolation.rotate(inputData.reshape(28, 28), 10, cval=0.01, order=1, reshape=False) # 학습 데이터를 10도 회전
            obj.train(rotationInputData1.reshape(784), label) # 학습
            rotationInputData2 = scipy.ndimage.interpolation.rotate(inputData.reshape(28, 28), -10, cval=0.01, order=1, reshape=False) # 학습 데이터를 -10도 회전
            obj.train(rotationInputData2.reshape(784), label) # 학습
    return obj # 신경망 객체 반환

def decoding(imageFile): # 28 x 28 크기의 이미지 파일의 색상 값을 0 ~ 255 범위로 변경 후 0.01 ~ 1.0 사이의 값으로 변환하는 함수
    imgArray = scipy.misc.imread(imageFile, flatten=True) # 이미지 파일로부터 데이터 로드 후 실수값으로 변환해서 저장
    imgData  = 255.0 - imgArray.reshape(784) # MNIST 데이터는 흑백이 반대로 구성되어 있어서 255에서 해당 이미지 픽셀의 색상 값을 빼주는 것임
    return ((imgData / 255.0) * 0.99) + 0.01 # 색상(RGB) 값의 범위(0 ~ 255)로 변경 후 0.01 ~ 1.0 사이의 값으로 변환해서 반환

def main():
    obj = learning() # 학습
    imageFile = [os.getcwd() + '\\mnist_image\\test0.png', 
                 os.getcwd() + '\\mnist_image\\test1.png', 
                 os.getcwd() + '\\mnist_image\\test2.png', 
                 os.getcwd() + '\\mnist_image\\test3.png', 
                 os.getcwd() + '\\mnist_image\\test4.png', 
                 os.getcwd() + '\\mnist_image\\test5.png', 
                 os.getcwd() + '\\mnist_image\\test6.png', 
                 os.getcwd() + '\\mnist_image\\test7.png', 
                 os.getcwd() + '\\mnist_image\\test8.png', 
                 os.getcwd() + '\\mnist_image\\test9.png'] # 테스트할 이미지 파일(28 x 28 크기의 png 파일)
    label = [0, 
             1, 
             2, 
             3, 
             4, 
             5, 
             6, 
             7, 
             8, 
             9] # 레이블
    accuracy = 0.0 # 정확도
    for i in range(len(label)):
        testData = decoding(imageFile[i]) # 평가 데이터(28 x 28 크기의 이미지 파일의 색상 값을 0 ~ 255 범위로 변경 후 0.01 ~ 1.0 사이의 값으로 변환)
        outputData = obj.query(testData) # 출력값
        if np.argmax(outputData) == label[i]: # 출력값이 레이블과 같을 경우(이미지를 제대로 인식했을 경우)
            accuracy += 1.0
            print('[+] Label : %d, Output : %d, Probability : %f' % (label[i], np.argmax(outputData), outputData[np.argmax(outputData)]))
        else: # 출력값이 정답과 다를 경우(이미지를 제대로 인식하지 못했을 경우)
            print('[-] Label : %d, Output : %d, Probability : %f' % (label[i], np.argmax(outputData), outputData[np.argmax(outputData)]))
        plt.imshow(testData.reshape(28, 28), cmap='Greys', interpolation='None')
        plt.show()
    accuracyRatio = (accuracy / len(label)) * 100
    print('\nAccuracy : ' + str(accuracyRatio) + '%')

if __name__ == '__main__':
    main()

'''
#-*- coding: utf-8 -*-
import os
import numpy as np
import scipy.misc
import matplotlib.pyplot as plt

def softmax(v):
    v = np.subtract(v, np.max(v)) # 버퍼 오버플로 방지
    return np.exp(v) / np.sum(np.exp(v))

def relu(v):
    return np.maximum(0, v)

class NeuralNetwork:
    def __init__(self, learningRate, inputNodeCount, hiddenNodeCount, outputNodeCount):
        self.learningRate = learningRate # 학습률 저장
        self.inputNodeCount = inputNodeCount # 입력 노드 개수 저장
        self.hiddenNodeCount = hiddenNodeCount # 은닉 노드 개수 저장
        self.outputNodeCount = outputNodeCount # 출력 노드 개수 저장
        self.weightInputHidden = np.random.normal(0.0, pow(self.inputNodeCount, -0.5), (self.hiddenNodeCount, self.inputNodeCount)) # 입력층-은닉층의 가중치(은닉 노드 개수 x 입력 노드 개수)
        self.weightHiddenOutput = np.random.normal(0.0, pow(self.hiddenNodeCount, -0.5), (self.outputNodeCount, self.hiddenNodeCount)) # 은닉층-출력층의 가중치(출력 노드 개수 x 은닉 노드 개수)
        self.relu = lambda x: relu(x) # ReLU 활성함수(은닉층)
        self.softmax = lambda x: softmax(x) # 소프트맥스 활성함수(출력층)
    
    def train(self, trainData, label): # 학습 함수
        trainData = np.array(trainData, ndmin=2).T # 1차원 학습 데이터 배열을 2차원 배열로 변경 후 전치 행렬로 변환
        label = np.array(label, ndmin=2).T # 1차원 레이블 배열을 2차원 배열로 변경 후 전치 행렬로 변환
        weightedSumHidden = np.dot(self.weightInputHidden, trainData) # 은닉층의 가중합
        hiddenOutputValue = self.relu(weightedSumHidden) # 은닉층의 출력값
        weightedSumOutput = np.dot(self.weightHiddenOutput, hiddenOutputValue) # 출력층의 가중합
        outputValue = self.softmax(weightedSumOutput) # 출력층의 출력값
        outputError = label - outputValue # 출력 노드의 오차
        outputDelta = outputError # 출력 노드의 델타(교차 엔트로피)
        hiddenError = np.dot(self.weightHiddenOutput.T, outputDelta) # 은닉 노드의 오차
        hiddenDalta = (weightedSumHidden > 0) * hiddenError # 은닉 노드의 델타
        self.weightInputHidden += self.learningRate * np.dot(hiddenDalta, np.transpose(trainData)) # 입력층-은닉층 가중치 갱신
        self.weightHiddenOutput += self.learningRate * np.dot(outputDelta, np.transpose(hiddenOutputValue)) # 은닉층-출력층 가중치 갱신
    
    def query(self, testData): # 평가 함수
        testData = np.array(testData, ndmin=2).T # 1차원 평가 데이터 배열을 2차원 배열로 변경 후 전치 행렬로 변환
        weightedSumHidden = np.dot(self.weightInputHidden, testData) # 은닉층의 가중합
        hiddenOutputValue = self.relu(weightedSumHidden) # 은닉층의 출력값
        weightedSumOutput = np.dot(self.weightHiddenOutput, hiddenOutputValue) # 출력층의 가중합
        outputValue = self.softmax(weightedSumOutput) # 출력층의 출력값
        return outputValue # 출력값 반환

def learning():
    inputNodeCount = 784 # 입력 노드 개수(28 x 28)
    hiddenNodeCount = 200 # 은닉 노드 개수
    outputNodeCount = 10 # 출력 노드 개수(0 ~ 9)
    learningRate = 0.1 # 학습률(너무 작으면 경사 하강의 속도를 제한하고, 너무 크면 경사 하강 과정에서 오버슈팅이 일어나서 성능이 떨어짐)
    obj = NeuralNetwork(learningRate, inputNodeCount, hiddenNodeCount, outputNodeCount) # 신경망 객체 생성
    with open(os.getcwd() + '\\mnist_dataset\\mnist_train_5000.csv', 'r') as fp:
        trainData = fp.readlines() # 학습 데이터
    epoch = 10 # 학습 횟수
    for _ in range(epoch):
        for data in trainData:
            inputData = (np.asfarray(data.split(',')[1:]) / 255.0 * 0.99) + 0.01 # 레이블을 제외한 값들을 색상(RGB) 값의 범위(0 ~ 255)로 변경 후 0.01 ~ 1.0 사이의 값으로 변환
            label = np.zeros(outputNodeCount) + 0.01 # 레이블 배열 초기화
            label[int(data.split(',')[0])] = 0.99 # 레이블이 있는 0번째 인덱스의 값을 인덱스로 하는 레이블 배열의 값에 0.99를 더해서 레이블 값을 1로 변경
            obj.train(inputData, label) # 학습
    return obj # 신경망 객체 반환

def decoding(imageFile): # 28 x 28 크기의 이미지 파일의 색상 값을 0 ~ 255 범위로 변경 후 0.01 ~ 1.0 사이의 값으로 변환하는 함수
    imgArray = scipy.misc.imread(imageFile, flatten=True) # 이미지 파일로부터 데이터 로드 후 실수값으로 변환해서 저장
    imgData  = 255.0 - imgArray.reshape(784) # MNIST 데이터는 흑백이 반대로 구성되어 있어서 255에서 해당 이미지 픽셀의 색상 값을 빼주는 것임
    return ((imgData / 255.0) * 0.99) + 0.01 # 색상(RGB) 값의 범위(0 ~ 255)로 변경 후 0.01 ~ 1.0 사이의 값으로 변환해서 반환

def main():
    obj = learning() # 학습
    imageFile = [os.getcwd() + '\\mnist_image\\test0.png', 
                 os.getcwd() + '\\mnist_image\\test1.png', 
                 os.getcwd() + '\\mnist_image\\test2.png', 
                 os.getcwd() + '\\mnist_image\\test3.png', 
                 os.getcwd() + '\\mnist_image\\test4.png', 
                 os.getcwd() + '\\mnist_image\\test5.png', 
                 os.getcwd() + '\\mnist_image\\test6.png', 
                 os.getcwd() + '\\mnist_image\\test7.png', 
                 os.getcwd() + '\\mnist_image\\test8.png', 
                 os.getcwd() + '\\mnist_image\\test9.png'] # 테스트할 이미지 파일(28 x 28 크기의 png 파일)
    label = [0, 
             1, 
             2, 
             3, 
             4, 
             5, 
             6, 
             7, 
             8, 
             9] # 레이블
    accuracy = 0.0 # 정확도
    for i in range(len(label)):
        testData = decoding(imageFile[i]) # 평가 데이터(28 x 28 크기의 이미지 파일의 색상 값을 0 ~ 255 범위로 변경 후 0.01 ~ 1.0 사이의 값으로 변환)
        outputData = obj.query(testData) # 출력값
        if np.argmax(outputData) == label[i]: # 출력값이 레이블과 같을 경우(이미지를 제대로 인식했을 경우)
            accuracy += 1.0
            print('[+] Label : %d, Output : %d, Probability : %f' % (label[i], np.argmax(outputData), outputData[np.argmax(outputData)]))
        else: # 출력값이 정답과 다를 경우(이미지를 제대로 인식하지 못했을 경우)
            print('[-] Label : %d, Output : %d, Probability : %f' % (label[i], np.argmax(outputData), outputData[np.argmax(outputData)]))
        plt.imshow(testData.reshape(28, 28), cmap='Greys', interpolation='None')
        plt.show()
    accuracyRatio = (accuracy / len(label)) * 100
    print('\nAccuracy : ' + str(accuracyRatio) + '%')

if __name__ == '__main__':
    main()
'''

'''
#-*- coding: utf-8 -*-
import os
import numpy as np
import scipy.special
import matplotlib.pyplot as plt

class NeuralNetwork:
    def __init__(self, learningRate, inputNodeCount, hiddenNodeCount, outputNodeCount):
        self.learningRate = learningRate # 학습률 저장
        self.inputNodeCount = inputNodeCount # 입력 노드 개수 저장
        self.hiddenNodeCount = hiddenNodeCount # 은닉 노드 개수 저장
        self.outputNodeCount = outputNodeCount # 출력 노드 개수 저장
        self.weightInputHidden = np.random.normal(0.0, pow(self.inputNodeCount, -0.5), (self.hiddenNodeCount, self.inputNodeCount)) # 입력층-은닉층의 가중치(은닉 노드 개수 x 입력 노드 개수)
        self.weightHiddenOutput = np.random.normal(0.0, pow(self.hiddenNodeCount, -0.5), (self.outputNodeCount, self.hiddenNodeCount)) # 은닉층-출력층의 가중치(출력 노드 개수 x 은닉 노드 개수)
        self.sigmoid = lambda x: scipy.special.expit(x) # 시그모이드 활성함수
    
    def train(self, trainData, label): # 학습 함수
        trainData = np.array(trainData, ndmin=2).T # 1차원 학습 데이터 배열을 2차원 배열로 변경 후 전치 행렬로 변환
        label = np.array(label, ndmin=2).T # 1차원 레이블 배열을 2차원 배열로 변경 후 전치 행렬로 변환
        weightedSumHidden = np.dot(self.weightInputHidden, trainData) # 은닉층의 가중합
        hiddenOutputValue = self.sigmoid(weightedSumHidden) # 은닉층의 출력값
        weightedSumOutput = np.dot(self.weightHiddenOutput, hiddenOutputValue) # 출력층의 가중합
        outputValue = self.sigmoid(weightedSumOutput) # 출력층의 출력값
        outputError = label - outputValue # 출력 노드의 오차
        outputDelta = outputError # 출력 노드의 델타(교차 엔트로피)
        hiddenError = np.dot(self.weightHiddenOutput.T, outputDelta) # 은닉 노드의 오차
        hiddenDalta = hiddenOutputValue * (1.0 - hiddenOutputValue) * hiddenError # 은닉 노드의 델타
        self.weightInputHidden += self.learningRate * np.dot(hiddenDalta, np.transpose(trainData)) # 입력층-은닉층 가중치 갱신
        self.weightHiddenOutput += self.learningRate * np.dot(outputDelta, np.transpose(hiddenOutputValue)) # 은닉층-출력층 가중치 갱신
    
    def query(self, testData): # 평가 함수
        testData = np.array(testData, ndmin=2).T # 1차원 평가 데이터 배열을 2차원 배열로 변경 후 전치 행렬로 변환
        weightedSumHidden = np.dot(self.weightInputHidden, testData) # 은닉층의 가중합
        hiddenOutputValue = self.sigmoid(weightedSumHidden) # 은닉층의 출력값
        weightedSumOutput = np.dot(self.weightHiddenOutput, hiddenOutputValue) # 출력층의 가중합
        outputValue = self.sigmoid(weightedSumOutput) # 출력층의 출력값
        return outputValue # 출력값 반환

def learning():
    inputNodeCount = 784 # 입력 노드 개수(28 x 28)
    hiddenNodeCount = 200 # 은닉 노드 개수
    outputNodeCount = 10 # 출력 노드 개수(0 ~ 9)
    learningRate = 0.1 # 학습률(너무 작으면 경사 하강의 속도를 제한하고, 너무 크면 경사 하강 과정에서 오버슈팅이 일어나서 성능이 떨어짐)
    obj = NeuralNetwork(learningRate, inputNodeCount, hiddenNodeCount, outputNodeCount) # 신경망 객체 생성
    with open(os.getcwd() + '\\mnist_dataset\\mnist_train_5000.csv', 'r') as fp:
        trainData = fp.readlines() # 학습 데이터
    epoch = 5 # 학습 횟수
    for _ in range(epoch):
        for data in trainData:
            inputData = (np.asfarray(data.split(',')[1:]) / 255.0 * 0.99) + 0.01 # 레이블을 제외한 값들을 색상(RGB) 값의 범위(0 ~ 255)로 변경 후 0.01 ~ 1.0 사이의 값으로 변환
            label = np.zeros(outputNodeCount) + 0.01 # 레이블 배열 초기화
            label[int(data.split(',')[0])] = 0.99 # 레이블이 있는 0번째 인덱스의 값을 인덱스로 하는 레이블 배열의 값에 0.99를 더해서 레이블 값을 1로 변경
            obj.train(inputData, label) # 학습
    return obj # 신경망 객체 반환

def main():
    obj = learning() # 학습
    with open(os.getcwd() + '\\mnist_dataset\\mnist_test_10.csv', 'r') as fp:
        testData = fp.readlines() # 평가 데이터
    accuracy = 0.0 # 정확도
    for data in testData:
        label = int(data.split(',')[0]) # 레이블
        inputData = ((np.asfarray(data.split(',')[1:]) / 255.0) * 0.99) + 0.01 # 레이블을 제외한 값들을 색상(RGB) 값의 범위(0 ~ 255)로 변경 후 0.01 ~ 1.0 사이의 값으로 변환
        outputData = obj.query(inputData) # 출력값
        if np.argmax(outputData) == label: # 출력값이 레이블과 같을 경우(이미지를 제대로 인식했을 경우)
            accuracy += 1.0
            print('[+] Label : %d, Output : %d, Probability : %f' % (label, np.argmax(outputData), outputData[np.argmax(outputData)]))
        else: # 출력값이 레이블과 다를 경우(이미지를 제대로 인식하지 못했을 경우)
            print('[-] Label : %d, Output : %d, Probability : %f' % (label, np.argmax(outputData), outputData[np.argmax(outputData)]))
        image = np.asfarray(data.split(',')[1:]).reshape((28, 28))
        plt.imshow(image, cmap='Greys', interpolation='None')
        plt.show()        
    accuracyRatio = (accuracy / len(testData)) * 100
    print('\nAccuracy : ' + str(accuracyRatio) + '%')

if __name__ == '__main__':
    main()
'''