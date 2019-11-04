#-*- coding: utf-8 -*-
import numpy
import scipy.special
import matplotlib.pyplot

class neuralNetwork: # 신경망 클래스(입력층, 은닉층, 출력층이 각각 1개 있는 얕은 신경망)
    def __init__(self, inputnodes, hiddennodes, outputnodes, learningrate): # 클래스 초기화(입력 노드 개수, 은닉 노드 개수, 출력 노드 개수, 학습률)
        self.inodes = inputnodes # 입력 노드 개수 저장
        self.hnodes = hiddennodes # 은닉 노드 개수 저장
        self.onodes = outputnodes # 출력 노드 개수 저장
        # 정규 분포를 이용해 중심이 0.0 이고, 표준 편차가 1/루트(노드 개수)인 가중치 배열(행렬) 생성(pow(2,3)=2^3=8)
        self.wih = numpy.random.normal(0.0, pow(self.inodes, -0.5), (self.hnodes, self.inodes)) # 입력층-은닉층의 가중치 행렬(은닉노드개수x입력노드개수)
        self.who = numpy.random.normal(0.0, pow(self.hnodes, -0.5), (self.onodes, self.hnodes)) # 은닉층-출력층의 가중치 행렬(출력노드개수x은닉노드개수)
        self.lr = learningrate # 학습률 저장
        self.activation_function = lambda x: scipy.special.expit(x) # 활성함수로 시그모이드 함수(expit()) 사용(lambda 문법 이용 - 인자 x 에 대해 expit(x) 함수의 반환값 저장)
        self.inverse_activation_function = lambda x: scipy.special.logit(x) # 시그모이드 함수의 역함수인 로지트 함수(logit())

    def train(self, inputs_list, targets_list): # 학습 함수(학습 데이터(입력) 배열(행렬), 정답 배열(행렬))
        inputs = numpy.array(inputs_list, ndmin=2).T # 1차원 배열인 입력 배열을 2차원 배열(행렬)로 변환하고, 계산의 편의를 위해 전치 행렬로 변환
        targets = numpy.array(targets_list, ndmin=2).T # 1차원 배열인 정답 배열을 2차원 배열(행렬)로 변환하고, 계산의 편의를 위해 전치 행렬로 변환
        hidden_inputs = numpy.dot(self.wih, inputs) # 입력층-은닉층의 가중치 행렬과 학습 데이터(입력) 행렬을 곱해 은닉층의 가중합 행렬 얻음
        hidden_outputs = self.activation_function(hidden_inputs) # 은닉층의 가중합 행렬을 활성함수인 시그모이드 함수에 넣어 은닉층의 출력값 행렬 얻음
        final_inputs = numpy.dot(self.who, hidden_outputs) # 은닉층-출력층의 가중치 행렬과 은닉층의 출력값 행렬을 곱해 출력층의 가중합 행렬 얻음
        final_outputs = self.activation_function(final_inputs) # 출력층의 가중합 행렬을 활성함수인 시그모이드 함수에 넣어 출력층의 출력값 행렬 얻음
        output_errors = targets - final_outputs # 정답 행렬과 출력층의 출력값 행렬을 빼서 출력층의 오차 행렬을 구함
        hidden_errors = numpy.dot(self.who.T, output_errors) # 은닉층-출력층의 가중치 행렬의 전치행렬과 출력층의 오차 행렬(출력층의 델타)을 곱해 은닉층의 오차 행렬 얻음(출력층의 델타를 출력층의 오차로 보는것으로 보아 Cross Entropy 함수로부터 유도된 학습 규칙 사용)
        self.who += self.lr * numpy.dot((output_errors * (final_outputs * (1.0 - final_outputs))), numpy.transpose(hidden_outputs)) # 학습률과 출력층의 델타(시그모이드 활성함수의 도함수(인자는 출력층의 출력값 행렬)와 출력층의 오차의 곱)와 은닉층의 출력값을 곱한 값(은닉층-출력층의 가중치 갱신값)을 더해 은닉층-출력층의 가중치 갱신
        self.wih += self.lr * numpy.dot((hidden_errors * (hidden_outputs * (1.0 - hidden_outputs))), numpy.transpose(inputs)) # 학습률과 은닉층의 델타(시그모이드 활성함수의 도함수(인자는 은닉층의 출력값 행렬)와 은닉층의 오차의 곱)와 입력층의 입력값을 곱한 값(입력층-은닉층의 가중치 갱신값)을 더해 입력층-은닉층의 가중치 갱신 

    def query(self, inputs_list): # 학습 후 갱신된 가중치로 테스트 데이터의 출력값 반환 함수(테스트 입력 데이터 배열(행렬))
        inputs = numpy.array(inputs_list, ndmin=2).T # 1차원 배열인 테스트 입력 배열을 2차원 배열(행렬)로 변환하고, 계산의 편의를 위해 전치 행렬로 변환
        hidden_inputs = numpy.dot(self.wih, inputs) # 갱신된 입력층-은닉층의 가중치 행렬과 테스트 입력 데이터 행렬을 곱해 은닉층의 가중합 행렬 얻음
        hidden_outputs = self.activation_function(hidden_inputs) # 은닉층의 가중합 행렬을 활성함수인 시그모이드 함수에 넣어 은닉층의 출력값 행렬 얻음
        final_inputs = numpy.dot(self.who, hidden_outputs) # 갱신된 은닉층-출력층의 가중치 행렬과 은닉층의 출력값 행렬을 곱해 출력층의 가중합 행렬 얻음
        final_outputs = self.activation_function(final_inputs) # 출력층의 가중합 행렬을 활성함수인 시그모이드 함수에 넣어 출력층의 출력값 행렬 얻음
        return final_outputs # 출력값 행렬 반환

    def backquery(self, targets_list): # 역질의 함수(정답 배열(행렬))
        final_outputs = numpy.array(targets_list, ndmin=2).T # 1차원 배열인 정답 배열 2차원 배열(행렬)로 변환하고, 계산의 편의를 위해 전치 행렬로 변환
        final_inputs = self.inverse_activation_function(final_outputs) # 정답 행렬을 로지트 함수(시그모이드 함수의 역함수)에 넣어 출력층의 출력값 행렬 얻음
        hidden_outputs = numpy.dot(self.who.T, final_inputs) # 갱신된 은닉층-출력층의 가중치 행렬과 출력층의 출력값 행렬을 곱해 은닉층의 가중합 행렬 얻음
        hidden_outputs -= numpy.min(hidden_outputs) # 값의 범위를 0.01~ 0.99로 설정
        hidden_outputs /= numpy.max(hidden_outputs)
        hidden_outputs *= 0.98
        hidden_outputs += 0.01
        hidden_inputs = self.inverse_activation_function(hidden_outputs) # 은닉층의 가중합 행렬을 로지트 함수에 넣어 은닉층의 출력값 행렬 얻음
        inputs = numpy.dot(self.wih.T, hidden_inputs) # 갱신된 입력층-은닉층의 가중치 행렬과 은닉층의 출력값 행렬을 곱해 입력층의 가중합 행렬 얻음
        inputs -= numpy.min(inputs) # 값의 범위를 0.01~ 0.99로 설정
        inputs /= numpy.max(inputs)
        inputs *= 0.98
        inputs += 0.01
        return inputs

def learning():
    input_nodes = 784 # 입력 노드의 개수(28x28 픽셀)
    hidden_nodes = 200 # 은닉 노드의 개수(은닉 노드의 개수가 너무 작을 경우 성능이 떨어짐)
    output_nodes = 10 # 출력 노드의 개수(0~9 숫자)
    learning_rate = 0.1 # 학습률(너무 작으면 경사 하강의 속도를 제한하고, 너무 크면 경사 하강 과정에서 오버슈팅이 일어나서 성능이 떨어짐)
    n = neuralNetwork(input_nodes,hidden_nodes,output_nodes, learning_rate) # 신경망 클래스 
    # print n.query([1.0, 0.5, -1.5])
    training_data_file = open("D:\\DeepLearning\\makeyourownneuralnetwork-master\\mnist_dataset\\mnist_train_5000.csv", 'r') # 각 행의 0번째 인덱스의 값이 정답이고, 1~784 인덱스의 값들이 픽셀(28x28)을 구성하는 색(RGB)의 값들임
    training_data_list = training_data_file.readlines() # csv 파일의 내용 저장(각 행이 정답과 픽셀로 이루어진 1차원 배열임)
    training_data_file.close()
    epochs = 5 # 너무 많이 학습하면 신경망이 학습 데이터에 과적합(오버피팅)되어 성능이 떨어짐
    for e in range(epochs): # 신경망 epoch 만큼 학습
        for record in training_data_list: # csv 파일 내용의 행 개수만큼 반복
            all_values = record.split(',') # 각 행의 값들을 , 로 구분
            inputs = (numpy.asfarray(all_values[1:]) / 255.0 * 0.99) + 0.01 # 각 행의 0번째 인덱스(정답)를 제외한 값들을 실수 형태로 변환 후, 0~255 사이에 속하는 입력 색상(RGB)의 값의 범위를 0.01~1.0 사이에 속하게 변환(0의 경우 가중치를 없애므로 하한선은 0.01)
            targets = numpy.zeros(output_nodes) + 0.01 # 정답 배열 생성 후 값을 모두 0.01로 설정(0의 경우 가중치를 없애므로 하한선은 0.01)
            targets[int(all_values[0])] = 0.99 # 정답이 있는 각 행의 0번째 인덱스 값(int(all_values[0]))을 인덱스로하는 정답 배열(targets[int(all_values[0])])의 값에 0.99를 더해 최종적으로 정답 값을 1로 변경
            n.train(inputs, targets) # 학습 데이터와 정답으로 학습
    return n, output_nodes

def main():
    n, output_nodes = learning() # 학습
    label = [0,1,2,3,4,5,6,7,8,9] # 정답
    for i in range(0, len(label)):
        targets = numpy.zeros(output_nodes) + 0.01 # 정답 배열 생성 및 값(0.01) 초기화
        targets[i] = 0.99 # 정답 배열의 정답 인덱스에 정답값(0.99) 설정
        image_data = n.backquery(targets) # 역질의
        print "정답 : "+str(label[i])
        matplotlib.pyplot.imshow(image_data.reshape(28,28), cmap='Greys', interpolation='None')
        matplotlib.pyplot.show() # 이미지 출력

if __name__=="__main__":
    main()
