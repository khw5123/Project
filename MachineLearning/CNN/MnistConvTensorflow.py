# -*- coding: utf-8 -*-
import numpy as np
from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf
import matplotlib.pyplot as plt

# 필터(가중치) 초기화 함수(shape : 필터 텐서([필터 가로 크기, 필터 세로 크기, 입력 채널 수, 출력 채널 수]))
def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1) # 절단정규분포(표준편차의 절댓값이 2 이상인 값을 버리는 분포)를 이용해서 필터(가중치)의 초기값 설정
    return tf.Variable(initial, name='weights')

# 편향 초기화 함수(shape : 편향 텐서)
def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape) # 편향의 초기값 설정
    return tf.Variable(initial, name='bias')

# 합성곱 계산 함수(x : 입력 데이터, W : 필터(가중치) 텐서)
def conv2d_(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME', name='conv') # 입력 데이터와 필터의 합성곱 반환

# 최댓값 풀링 함수(x : 입력 데이터, kernel_size : 커널 크기, stride : 스트라이드)
def max_pool_(x, kernel_size, stride):
    return tf.nn.max_pool(x, ksize=[1, kernel_size, kernel_size, 1], strides=[1, stride, stride, 1], padding='SAME', name='pool') # 2 x 2 커널을 2(스트라이드) 씩 이동해서 각 커널 안의 최댓값을 뽑아 새로운 텐서 생성(커널 크기와 스트라이드가 2이므로 출력 데이터의 가로, 세로 크기는 입력 데이터의 절반이 됨)

def main():
    mnist = input_data.read_data_sets('MNIST', one_hot=True) # MNIST 데이터셋 다운 및 로드
    input_data_width, input_data_height, input_data_channel = 28, 28, 1 # 입력 데이터 가로 크기, 입력 데이터 세로 크기, 입력 데이터 채널 수
    filter_width, filter_height, first_filter_count, second_filter_count = 5, 5, 32, 64 # 필터 가로 크기, 필터 세로 크기, 필터 수(깊이)
    kernel_size, stride = 2, 2 # 커널 크기, 스트라이드
    hiddenNodeCount, label_count = 1024, 10 # 은닉층 개수, 레이블(0 ~ 9) 개수
    x = tf.placeholder(tf.float32, [None, input_data_width * input_data_height], name='x') # 입력 데이터
    y = tf.placeholder(tf.float32, [None, label_count]) # 레이블
    print('\nInput Data Size : %d x %d x %d' % (input_data_width, input_data_height, input_data_channel))
    print('First Filter Size : %d x %d x %d' % (filter_width, filter_height, first_filter_count))
    print('Second Filter Size : %d x %d x %d' % (filter_width, filter_height, second_filter_count))
    # 첫 번째 합성곱 레이어
    with tf.name_scope('first_conv'):
        # 5(가로) x 5(세로) x 32(필터 수, 깊이) 크기의 필터를 이용하여 28(가로) x 28(세로) x 1(채널 수) 크기의 입력 데이터를 28(가로) x 28(세로) x 32(피처 수, 깊이) 크기의 출력 텐서(액티베이션 맵)로 변환
        W_conv1 = weight_variable([filter_width, filter_height, input_data_channel, first_filter_count]) # 필터 텐서([가로(5), 세로(5), 입력 채널 수(1), 출력 채널 수(32)])
        b_conv1 = bias_variable([first_filter_count]) # 편향 텐서
        x_image = tf.reshape(x, [-1, input_data_width, input_data_height, input_data_channel]) # 입력 데이터의 개수는 유지하고(-1), 28 x 28 x 1 크기의 텐서로 변환
        h_conv1 = tf.nn.relu(conv2d_(x_image, W_conv1) + b_conv1, name='act') # 피처 맵(합성곱(입력 데이터(28 x 28 x 1), 필터(5 x 5 x 32)) + 편향)에 ReLU 활성함수 적용해서 액티베이션 맵(28 x 28 x 32) 생성
    print('First Convolution Layer Output Tenser Size :', h_conv1.shape)
    # 첫 번째 풀링 레이어
    with tf.name_scope('first_pool'):
        h_pool1 = max_pool_(h_conv1, kernel_size, stride) # 첫 번째 합성곱 레이어의 출력 데이터(액티베이션 맵)를 이용해서 최댓값 풀링
    print('First Pooling Layer Output Tenser Size :', h_pool1.shape)
    # 두 번째 합성곱 레이어
    with tf.name_scope('second_conv'):
        # 5(가로) x 5(세로) x 64(필터 수, 깊이) 크기의 필터를 이용하여 14(가로) x 14(세로) x 32(채널 수) 크기의 입력 데이터(첫 번째 풀링 레이어 출력 텐서)를 14(가로) x 14(세로) x 64(피처 수, 깊이) 크기의 출력 텐서(액티베이션 맵)로 변환
        W_conv2 = weight_variable([filter_width, filter_height, int(list(h_pool1.shape)[-1]), second_filter_count]) # 필터 텐서([가로(5), 세로(5), 입력 채널 수(32), 출력 채널 수(64)])
        b_conv2 = bias_variable([second_filter_count]) # 편향 텐서
        h_conv2 = tf.nn.relu(conv2d_(h_pool1, W_conv2) + b_conv2, name='act') # 피처 맵(합성곱(첫 번째 풀링 레이어 출력 텐서(14 x 14 x 32), 필터(5 x 5 x 64)) + 편향)에 ReLU 활성함수 적용해서 액티베이션 맵(14 x 14 x 64) 생성
    print('Second Convolution Layer Output Tenser Size :', h_conv2.shape)
    # 두 번째 풀링 레이어
    with tf.name_scope('second_pool'):
        h_pool2 = max_pool_(h_conv2, kernel_size, stride) # 두 번째 합성곱 레이어의 출력 데이터(액티베이션 맵)를 이용해서 최댓값 풀링
    print('Second Pooling Layer Output Tenser Size :', h_pool2.shape)
    # 첫 번째 완전 연결 레이어
    with tf.name_scope('first_fc'):
        # 7(가로) x 7(세로) x 64(채널 수) 크기의 입력 데이터(두 번째 풀링 레이어 출력 텐서)를 1 x 1024(은닉 노드 개수) 크기의 1차원 텐서로 변환
        W_fc1 = weight_variable([int(list(h_pool2.shape)[-3]) * int(list(h_pool2.shape)[-2]) * int(list(h_pool2.shape)[-1]), hiddenNodeCount]) # 가중치 텐서([두 번째 풀링 레이어 출력 텐서(3차원) 원소 개수(7 * 7 * 64), 은닉 노드 개수(1024)])
        b_fc1 = bias_variable([hiddenNodeCount]) # 편향 텐서
        h_pool2_flat = tf.reshape(h_pool2, [-1, int(list(h_pool2.shape)[-3]) * int(list(h_pool2.shape)[-2]) * int(list(h_pool2.shape)[-1])]) # 입력 데이터의 개수는 유지하고(-1), 1 x (7 * 7 * 64) 크기의 1차원 텐서로 변환
        h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1, name='act') # '변환된 1차원 텐서와 가중치 텐서의 행렬곱 + 편향'에 ReLU 활성함수를 적용해서 1차원 텐서(1 x 1024) 생성
    print('First Fully Connected Layer Output Tenser Size :', h_fc1.shape)
    # 드롭아웃
    with tf.name_scope('drop_out'):
        keep_prob = tf.placeholder(tf.float32) # 플레이스홀더
        h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob) # 첫 번째 완전 연결 레이어 출력 텐서에 드롭아웃 적용
    # 두 번째 완전 연결 레이어
    with tf.name_scope('second_fc'):
        # 1 x 1024(은닉 노드 개수) 크기의 입력 데이터(첫 번째 완전 연결 레이어 출력 텐서)를 1 x 10(레이블(0 ~ 9) 개수) 크기의 텐서로 변환
        W_fc2 = weight_variable([int(list(h_fc1_drop.shape)[-1]), label_count]) # 가중치 텐서([은닉 노드 개수(1024), 레이블 개수(10)])
        b_fc2 = bias_variable([label_count]) # 편향 텐서
    y_conv = tf.matmul(h_fc1_drop, W_fc2) + b_fc2 # CNN 최종 출력 데이터(첫 번째 완전 연결 레이어 출력 텐서에 드롭아웃 적용한 텐서와 가중치 텐서의 행렬곱 + 편향)
    print('Second Fully Connected Layer Output Tenser Size :', y_conv.shape)
    error = tf.nn.softmax_cross_entropy_with_logits(logits=y_conv, labels=y) # 최종 출력 데이터를 레이블과 비교하기 위해 소프트맥스 활성함수를 이용하여 텐서를 각 숫자(0 ~ 9)에 속할 확률로 변경 후 해당 확률과 레이블을 비교하고, 교차 엔트로피 비용함수를 이용하여 오차 계산
    cross_entropy = tf.reduce_mean(error, name='cross_entropy') # 오차 평균
    train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy) # 오차를 줄이기 위해 역전파 알고리즘을 이용해서 가중치 갱신
    correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y, 1)) # 최종 출력 데이터와 레이블에서 가장 큰 값을 가지는 인덱스 반환(값(확률)이 1에 제일 가까운(가장 큰) 값을 가지는 인덱스(숫자(0 ~ 9))로 분류). 최종 출력 데이터와 레이블의 인덱스가 같으면(true 반환) 올바른 예측이고, 다르면(false 반환) 잘못된 예측
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32)) # 정확도(올바르게 예측한 데이터 수 / 전체 데이터 수)
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        # labels = sess.run(y_conv, feed_dict={x: mnist.test.images, y: mnist.test.labels, keep_prob: 1.0})
        fig = plt.figure()
        for i in range(0, 10):
            subplot = fig.add_subplot(2, 5, i + 1)
            subplot.set_xticks([])
            subplot.set_yticks([])
            # subplot.set_title('%d' % np.argmax(labels[i]))
            subplot.imshow(mnist.test.images[i].reshape((28, 28)), cmap=plt.cm.gray_r)
        plt.show()
        writer = tf.summary.FileWriter('graphs', sess.graph) # 텐서 보드 기록
        batch_size = 100 # 배치 크기
        max_iter = 5 # 반복 횟수
        for i in range(max_iter):
            batch = mnist.train.next_batch(batch_size) # 배치 크기만큼 학습 데이터 로드
            if i % batch_size == 0:
                train_accuracy = accuracy.eval(feed_dict={x: batch[0], y: batch[1], keep_prob: 1.0})
                print('Step %d Training Accuracy : %g' % (i, train_accuracy))
            train_step.run(feed_dict={x: batch[0], y: batch[1], keep_prob: 0.5})
        print('\nTest Accuracy : %g' % accuracy.eval(feed_dict={x: mnist.test.images, y: mnist.test.labels, keep_prob: 1.0}))
        writer.close()

if __name__ == '__main__':
    main()