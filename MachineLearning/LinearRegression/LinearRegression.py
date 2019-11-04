# -*- coding: utf-8 -*-
import tensorflow as tf
import numpy as np
from matplotlib import pyplot as plt
from sklearn import datasets

boston = datasets.load_boston()
boston_slice = [x[5] for x in boston['data']] # 6번째 피처인 방의 평균 개수만 사용

data_x = np.array(boston_slice).reshape(-1, 1) # 피처(입력 데이터)
data_y = boston['target'].reshape(-1, 1) # 집 값(정답)

# 선형 회귀에서의 학습 함수 : y = wx + b (y : 출력 데이터, x : 입력 데이터, w : 기울기, b : 편향(절편))
n_sample = data_x.shape[0]
x = tf.placeholder(tf.float32, shape=(n_sample, 1), name='x') # 피처(입력 데이터)
y = tf.placeholder(tf.float32, shape=(n_sample, 1), name='y') # 집 값(정답)
w = tf.Variable(tf.zeros((1, 1)), name='weights') # 기울기
b = tf.Variable(tf.zeros((1, 1)), name='bias') # 편향(절편)

# 손실함수 : (출력 데이터 - (입력 데이터 x 기울기 + 편향))^2 / 샘플 수
# matmul : 곱셈, square : 제곱, reduce_mean : 평균
y_pred = tf.matmul(x, w) + b # 모델(출력 데이터)
loss = tf.reduce_mean(tf.square(y_pred - y)) # 손실함수
optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.001) # 최적화 클래스(경사 하강법, 학습률 0.001)
train_op = optimizer.minimize(loss) # 최적화 함수로 손실함수의 최솟값을 찾음
summary_op = tf.summary.scalar('loss', loss) # 시각화를 위한 함수로 손실함수의 변화 기록

def plot_graph(y, fout):
    plt.scatter(data_x.reshape(1, -1)[0], boston['target'].reshape(1, -1)[0])
    plt.plot(data_x.reshape(1, -1)[0], y.reshape(1, -1)[0])
    plt.savefig(fout)
    plt.clf()
    
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    summary_writer = tf.summary.FileWriter('D:\\MachineLearning\\Workspace\\graphs', sess.graph)
    y_pred_before = sess.run(y_pred, {x: data_x}) # 학습 전의 예측된 기울기 상태
    plot_graph(y_pred_before, 'before.png')
    # 최적화 함수를 이용해서 기울기를 100번 업데이트
    for i in range(100):
        # 위에서 정의한 loss, summary_op, train_op 연산 수행후 결과를 변수에 저장
        loss_t, summary, _ = sess.run([loss, summary_op, train_op], feed_dict={x: data_x, y: data_y})
        summary_writer.add_summary(summary, i) # 각 업데이트마다 생성된 summary_op 함수의 결과를 서머리 라이터에 기록
        if i % 10 == 0:
            print('loss = %4.4f' % loss_t.mean()) # 10회 학습 후의 평균 손실
            y_pred_after = sess.run(y_pred, {x: data_x})
    y_pred_after = sess.run(y_pred, {x: data_x})
    plot_graph(y_pred_after, 'after.png')