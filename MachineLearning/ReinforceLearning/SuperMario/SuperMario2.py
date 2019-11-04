# -*- coding: utf-8 -*-
import random
import numpy as np
import tensorflow as tf
from collections import deque
from nes_py.wrappers import BinarySpaceToDiscreteSpaceEnv
import gym_super_mario_bros

# https://github.com/wonseokjung/ai_supermario
# http://jinman190.blogspot.com/2017/10/rl.html
# https://github.com/chris-chris/mario-rl-tutorial (https://brunch.co.kr/@kakao-it/144, https://brunch.co.kr/@kakao-it/161)

movements = [
    ['NOOP'], 
    ['A'], # Jump
    ['B'], # Attack
    ['right'], 
    ['right', 'A'], 
    ['right', 'B'], 
    ['right', 'A', 'B'], 
    ['left'], 
    ['left', 'A'], 
    ['left', 'B'], 
    ['left', 'A', 'B'], 
    ['down'], 
    ['up']
]

env = gym_super_mario_bros.make('SuperMarioBros-4-2-v0')
env = BinarySpaceToDiscreteSpaceEnv(env, movements)
env._max_episode_steps = 10001 # 환경 최대 반복 횟수 설정

input_size = env.observation_space.shape[0] * env.observation_space.shape[1] * 3 # 입력 노드 개수(env.observation_space.shape[0])
output_size = len(movements) # 출력 노드 개수(env.action_space.n)
dis = 0.9 # 과거 가중치를 줄이기 위한 상수
max_replay_buffer = 50000 # 버퍼 최대 크기

class DQN:
    def __init__(self, session, input_size, output_size, name='main'):
        self.session = session # 세션
        self.input_size = input_size # 입력 노드 개수
        self.output_size = output_size # 출력 노드 개수
        self.net_name = name # 신경망 이름
        self.neural_network() # 신경망 생성
    
    def neural_network(self, hidden_size=10, learning_rate=1e-1): # 신경망 생성 및 학습 함수(은닉 노드 개수, 학습률)
        with tf.variable_scope(self.net_name):
            self.X = tf.placeholder(shape=[None, self.input_size], dtype=tf.float32, name='input_x') # 입력 노드
            '''
            W1 = tf.get_variable('W1', shape=[self.input_size, hidden_size], initializer=tf.contrib.layers.xavier_initializer()) # 입력층-은닉층 가중치
            V1 = tf.nn.tanh(tf.matmul(self.X, W1)) # 은닉층 가중합
            W2 = tf.get_variable('W2', shape=[hidden_size, self.output_size], initializer=tf.contrib.layers.xavier_initializer()) # 은닉층-출력층 가중치
            self.Y = tf.matmul(V1, W2) # 출력층 가중합(출력값)
            '''
            W1 = tf.get_variable('W1', shape=[self.input_size, hidden_size], initializer=tf.contrib.layers.xavier_initializer()) # 입력층-은닉층1 가중치
            V1 = tf.nn.tanh(tf.matmul(self.X, W1)) # 은닉층1 가중합
            W2 = tf.get_variable('W2', shape=[hidden_size, hidden_size], initializer=tf.contrib.layers.xavier_initializer()) # 은닉층1-은닉층2 가중치
            V2 = tf.nn.tanh(tf.matmul(V1, W2)) # 은닉층2 가중합
            W3 = tf.get_variable('W3', shape=[hidden_size, hidden_size], initializer=tf.contrib.layers.xavier_initializer()) # 은닉층2-은닉층3 가중치
            V3 = tf.nn.tanh(tf.matmul(V2, W3)) # 은닉층3 가중합
            W4 = tf.get_variable('W4', shape=[hidden_size, self.output_size], initializer=tf.contrib.layers.xavier_initializer()) # 은닉층3-출력층 가중치
            self.Y = tf.matmul(V3, W4) # 출력층 가중합(출력값)
        self.D = tf.placeholder(shape=[None, self.output_size], dtype=tf.float32) # 레이블
        self.loss = tf.reduce_mean(tf.square(self.Y - self.D)) # 오차 평균(제곱 손실함수)
        self.train = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(self.loss) # 역전파 알고리즘으로 오차를 최소화 하는 방향으로 학습
    
    def predict(self, state): # 환경을 입력받아 Q를 반환하는 함수
        x = np.reshape(state, [1, self.input_size])
        return self.session.run(self.Y, feed_dict={self.X: x})
    
    def update(self, x_stack, y_stack): # 학습 함수
        return self.session.run([self.loss, self.train], feed_dict={self.X: x_stack, self.D: y_stack})

def replay_train(mainDQN, targetDQN, replay_buffer_minibatch): # 학습 함수
    global dis
    x_stack = np.empty(0).reshape(0, mainDQN.input_size)
    y_stack = np.empty(0).reshape(0, mainDQN.output_size)
    for state, action, reward, next_state, done in replay_buffer_minibatch:
        Q = mainDQN.predict(state) # Q(효율적인 액션을 선택하기위한 지표)
        if done: # 막대기가 넘어진 상태일 경우
            Q[0, action] = reward # reward만 저장
        else: # 진행중인 상태일 경우
            Q[0, action] = reward + dis * np.max(targetDQN.predict(next_state)) # reward와 다음 상태의 Q의 합 저장을 저장하되 다음 상태의 Q를 얻어올 때 타겟 신경망을 이용
        x_stack = np.vstack([x_stack, state.reshape(-1, mainDQN.input_size)]) # 환경 스택에 쌓음
        y_stack = np.vstack([y_stack, Q]) # Q 스택에 쌓음
    return mainDQN.update(x_stack, y_stack) # 메인 신경망 학습

def get_copy_var_ops(*, dest_scope_name='target', src_scope_name='main'): # 타겟 신경망이 메인 신경망과 같아지도록 복사하는 함수
    op_holder = []
    src_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope=src_scope_name)
    dest_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope=dest_scope_name)
    for src_var, dest_var in zip(src_vars, dest_vars):
        op_holder.append(dest_var.assign(src_var.value()))
    return op_holder

def play(mainDQN):
    global env
    state = env.reset() # 환경 초기화
    reward_sum = 0 # reward 합계
    while True:
        env.render() # 환경 렌더링
        action = np.argmax(mainDQN.predict(state)) # 신경망을 이용한 액션
        state, reward, done, _ = env.step(action) # 환경 실행
        reward_sum += reward
        if done:
            print('Total score : {}'.format(reward_sum))
            break

def main():
    global env, input_size, output_size, max_replay_buffer
    epoch = 5000 # 반복 횟수
    replay_buffer = deque() # 버퍼
    with tf.Session() as sess: # 세션 생성
        mainDQN = DQN(sess, input_size, output_size, name='main') # 메인 신경망 생성 및 학습
        targetDQN = DQN(sess, input_size, output_size, name='target') # 타겟 신경망 생성 및 학습
        tf.global_variables_initializer().run() # 세션 초기화
        copy_ops = get_copy_var_ops(dest_scope_name='target', src_scope_name='main')
        sess.run(copy_ops) # 타겟 신경망이 메인 신경망과 같아지도록 복사
        for episode in range(epoch):
            e = 1.0 / ((episode / 10) + 1) # 반복할수록 랜덤한 액션을 줄이고 신경망을 이용한 액션을 하기위한 변수
            done = False # 막대기 넘어짐 여부
            reward = 0
            step_count = 0 # 반복 횟수
            state = env.reset() # 환경 초기화
            while not done:
                env.render()
                if np.random.rand(1) < e:
                    action = env.action_space.sample() # 랜덤한 액션
                else:
                    action = np.argmax(mainDQN.predict(state)) # 신경망을 이용한 액션
                next_state, reward, done, _ = env.step(action) # 환경 실행
                if done: # 막대기가 넘어졌을 경우
                    reward -= 100 # reward 감소
                if action == 3 or action == 4 or action == 5 or action == 6: # 오른쪽(깃발 방향)으로 이동했을 경우
                    reward += 0.1
                if action == 7 or action == 8 or action == 9 or action == 10: # 왼쪽(깃발 반대 방향)으로 이동했을 경우
                    reward -= 0.1
                if step_count % 30 == 0:
                    reward -= 1
                replay_buffer.append((state, action, reward, next_state, done)) # 버퍼에 추가
                if len(replay_buffer) > max_replay_buffer: # 버퍼가 설정한 최대 크기를 초과했을 경우
                    replay_buffer.popleft() # 제일 오래된 버퍼 비움
                state = next_state # 환경 갱신
                step_count += 1 # 반복 횟수 갱신
                if step_count > 1000: # 특정 반복 횟수를 초과했을 경우
                    break
                print('Step: {} | Reward: {} | Epsilon: {}'.format(step_count, reward, e), end='\r')
            print('Episode: {} | Step: {} | Reward: {}'.format(episode, step_count, reward))
            if episode % 10 == 0 and episode != 0: # 10번 반복했을 경우
                for _ in range(50):
                    replay_buffer_minibatch = random.sample(replay_buffer, 10) # 버퍼에서 미니배치 크기만큼 랜덤한 인덱스의 값들을 가져옴
                    loss, _ = replay_train(mainDQN, targetDQN, replay_buffer_minibatch) # 학습
                print('Loss :', loss)
                sess.run(copy_ops) # 타겟 신경망이 메인 신경망과 같아지도록 복사
        play(mainDQN) # Test

if __name__ == '__main__':
    main()