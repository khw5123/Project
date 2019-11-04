# -*- coding: utf-8 -*-
import os
import random
import numpy as np
import tensorflow as tf
from collections import deque
import gym
from skimage.transform import resize
from skimage.color import rgb2gray

# https://gist.github.com/jcwleo/fffc40f69b7f14d9e2a2b8765a79b579#file-dqn_breakout-py

class DQN:
    def __init__(self, sess, height, width, state_size, output_node_count, scope):
        self.sess = sess # 세션
        self.scope = scope # 네임 스페이스명
        self.height = height # 게임판 가로 크기
        self.width = width # 게임판 세로 크기
        self.state_size = state_size # 이전 환경 기록 수
        self.output = output_node_count # 출력 노드 개수
        self.learning_rate = 0.00025 # 학습률
        self.momentum = 0.95 # 모멘텀
        self.epsilon = 0.01 # 엡실론
        self.build_network() # 신경망 생성
        self.saver = tf.train.Saver() # 학습 기록(신경망 가중치) 저장 객체
    
    def build_network(self): # 신경망 생성 메서드
        with tf.variable_scope(self.scope): # 네임 스페이스 생성
            self.X = tf.placeholder('float', [None, self.height, self.width, self.state_size]) # 환경
            self.Y = tf.placeholder('float', [None]) # 레이블
            self.A = tf.placeholder('int64', [None]) # 액션
            f1 = tf.get_variable('f1', shape=[8, 8, 4, 32], initializer=tf.contrib.layers.xavier_initializer_conv2d())
            c1 = tf.nn.relu(tf.nn.conv2d(self.X, f1, strides=[1, 4, 4, 1], padding='VALID'))
            f2 = tf.get_variable('f2', shape=[4, 4, 32, 64], initializer=tf.contrib.layers.xavier_initializer_conv2d())
            c2 = tf.nn.relu(tf.nn.conv2d(c1, f2, strides=[1, 2, 2, 1], padding='VALID'))
            f3 = tf.get_variable('f3', shape=[3, 3, 64, 64], initializer=tf.contrib.layers.xavier_initializer_conv2d())
            c3 = tf.nn.relu(tf.nn.conv2d(c2, f3, strides=[1, 1, 1, 1], padding='VALID'))
            w1 = tf.get_variable('w1', shape=[7 * 7 * 64, 512], initializer=tf.contrib.layers.xavier_initializer())
            l1 = tf.reshape(c3, [-1, w1.get_shape().as_list()[0]])
            w2 = tf.get_variable('w2', shape=[512, self.output], initializer=tf.contrib.layers.xavier_initializer())
            l2 = tf.nn.relu(tf.matmul(l1, w1))
            self.Q_pred = tf.matmul(l2, w2) # Q
        one_hot = tf.one_hot(self.A, self.output, 1.0, 0.0) # 원-핫 인코딩 벡터 생성
        Q_value = tf.reduce_sum(tf.multiply(self.Q_pred, one_hot), reduction_indices=1) # 원-핫 인코딩 적용한 Q
        error = tf.where(tf.abs(self.Y - Q_value) < 1.0, 0.5 * tf.square(self.Y - Q_value), tf.abs(self.Y - Q_value) - 0.5) # 오차를 -1 ~ 1 사이로 클립
        self.loss = tf.reduce_mean(error) # 오차 평균
        optimizer = tf.train.RMSPropOptimizer(self.learning_rate, momentum=self.momentum, epsilon=self.epsilon) # 최적화
        self.train = optimizer.minimize(self.loss) # 최적화 결과
    
    def predict(self, state_history): # 기록된 환경을 이용해서 예측한 Q를 반환하는 매서드
        return self.sess.run(self.Q_pred, feed_dict={self.X: np.reshape(np.float32(state_history / 255.0), [-1, self.height, self.width, self.state_size])}) # Q 반환
    
    def action(self, Q, epsilon): # Q와 엡실론을 이용해서 결정한 액션을 반환하는 메서드
        if epsilon > np.random.rand(1): # 엡실론이 무작위 값보다 클 경우
            action = np.random.randint(self.output) # 랜덤한 액션
        else: # 엡실론이 무작위 값보다 작을 경우
            action = np.argmax(Q) # 신경망을 이용해서 결정한 액션
        return action # 액션 반환

def get_copy_var_ops(*, src_scope_name='main', dest_scope_name='target'): # 타겟 신경망에 메인 신경망의 가중치를 복사하는 함수
    src_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope=src_scope_name)
    dest_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope=dest_scope_name)
    op_holder = [dest_var.assign(src_var.value()) for src_var, dest_var in zip(src_vars, dest_vars)]
    return op_holder

def init_state(height, width, state_history, state, state_size): # 기록된 환경 초기화 함수
    for i in range(state_size):
        state_history[:,:,i] = np.uint8(resize(rgb2gray(state), (height, width), mode='reflect') * 255) # 이미지 흑백 변환 후 크기 변경하고 255 곱한 환경으로 저장

def replay_train(mainDQN, targetDQN, replay_memory_minibatch, state_size, discount_factor): # 메인 신경망 학습 함수
    state_stack, action_stack, reward_stack, next_state_stack, done_stack = [], [], [], [], []
    for state, action, reward, done in replay_memory_minibatch:
        state_stack.append(state[:,:,:state_size])
        action_stack.append(action)
        reward_stack.append(reward)
        next_state_stack.append(state[:,:,1:])
        done_stack.append(done)
    done_stack = np.array(done_stack) + 0 # 불리언 값을 숫자(0, 1)로 변환
    Q = targetDQN.predict(np.array(next_state_stack)) # 타겟 신경망을 이용해서 예측한 Q
    y = reward_stack + (1 - done_stack) * discount_factor * np.max(Q, axis=1) # 레이블
    mainDQN.sess.run(mainDQN.train, feed_dict={mainDQN.X: np.float32(np.array(state_stack) / 255.0), mainDQN.Y: y, mainDQN.A: action_stack}) # 메인 신경망 학습

def main():
    env = gym.make('Breakout-v4') # 환경 생성
    tf.reset_default_graph() # 그래프 초기화
    experiment_dir = os.getcwd() + '\\experiment' # 저장 디렉터리
    if not os.path.exists(experiment_dir): # 저장 디렉터리가 없을 경우
        os.makedirs(experiment_dir) # 저장 디렉터리 생성
    model_directory = os.path.join(experiment_dir, 'model') # 학습 기록(신경망 가중치) 디렉터리
    if not os.path.exists(model_directory): # 학습 기록(신경망 가중치) 디렉터리가 없을 경우
        os.makedirs(model_directory) # 학습 기록(신경망 가중치) 디렉터리 생성
    graph_directory = os.path.join(experiment_dir, 'graph') # 텐서보드 기록 디렉터리
    if not os.path.exists(graph_directory): # 텐서보드 기록 디렉터리가 없을 경우
        os.makedirs(graph_directory) # 텐서보드 기록 디렉터리 생성
    height, width = 84, 84 # 게임판 세로, 가로 크기
    output_node_count = env.action_space.n # 출력 노드 개수
    state_size = 4 # 이전 환경 기록 수
    discount_factor = 0.99 # 과거의 보상을 줄이기 위한 상수
    minibatch_size = 32 # 미니배치 크기
    replay_memory_size = 400000 # 버퍼 크기
    replay_memory = deque(maxlen=replay_memory_size) # 버퍼
    total_reward_memory = deque() # 각 게임에서 얻은 보상값 버퍼
    Q_memory = deque() # 각 학습 주기에서 얻은 Q 버퍼
    train_interval = 10000 # 학습 주기
    target_update_interval = 10000 # 타겟 신경망 업데이트 주기
    epsilon = 1.0 # 반복할수록 랜덤한 액션을 줄이고 신경망을 이용해서 결정한 액션을 하기위한 엡실론
    epsilon_start = 1.0 # 초기 엡실론
    epsilon_end = 0.1 # 임계 엡실론
    decay = 1000000 # 엡실론 감소 상수
    epoch = 0 # 학습 주기 도달 횟수
    epoch_complete = False # 학습 주기 도달 유무
    episode = 0 # 게임 반복 횟수
    global_step = 0 # 프레임 반복 횟수
    with tf.Session() as sess: # 세션 생성
        writer = tf.summary.FileWriter(graph_directory, sess.graph) # 텐서보드 기록 객체
        mainDQN = DQN(sess, height, width, state_size, output_node_count, scope='main') # 메인 신경망
        targetDQN = DQN(sess, height, width, state_size, output_node_count, scope='target') # 타겟 신경망
        latest_checkpoint = tf.train.latest_checkpoint(model_directory) # 저장된 학습 기록(신경망 가중치)
        if latest_checkpoint: # 저장된 학습 기록(신경망 가중치)이 있을 경우
            mainDQN.saver.restore(sess, latest_checkpoint) # 학습 기록(신경망 가중치) 로드
            print('[+] Loaded checkpoint {}'.format(latest_checkpoint))
        sess.run(tf.global_variables_initializer()) # 세션 초기화
        sess.run(get_copy_var_ops(src_scope_name='main', dest_scope_name='target')) # 타겟 신경망에 메인 신경망의 가중치 복사
        while epoch <= 200:
            state = env.reset() # 환경 초기화
            state_history = np.zeros([height, width, state_size + 1], dtype=np.uint8) # 환경 기록 리스트(과거 4번(index 0 ~ 3) + 현재 1번(index 4))
            init_state(height, width, state_history, state, state_size) # 기록된 환경 초기화
            episode_reward = 0 # 한 게임에서 얻은 보상값
            done = False # 게임 종료 여부
            episode += 1 # 게임 반복 횟수 증가
            while not done:
                env.render() # 환경 렌더링
                global_step += 1 # 프레임 횟수 증가
                if epsilon > epsilon_end and global_step > train_interval: # 프레임 횟수가 학습 주기를 넘겼고, 현재 엡실론이 임계 엡실론보다 클 경우
                    epsilon -= (epsilon_start - epsilon_end) / decay # 현재 엡실론 감소
                Q = mainDQN.predict(state_history[:,:,:state_size]) # 기록된 환경을 이용해서 예측한 Q
                Q_memory.append(np.max(Q)) # Q 버퍼에 추가
                action = mainDQN.action(Q, epsilon) # Q와 엡실론을 이용해서 액션 결정
                next_state, reward, done, _ = env.step(action) # 환경 실행
                reward = np.clip(reward, -1, 1) # 보상값을 -1 ~ 1 사이로 클립(-1보다 작은 보상값은 -1로, 1보다 큰 보상값은 1로 변경)
                state_history[:,:,state_size] = np.uint8(resize(rgb2gray(next_state), (height, width), mode='reflect') * 255) # 다음 환경을 환경 기록 리스트(index 4)에 추가
                replay_memory.append((np.copy(state_history[:,:,:]), action, reward, done)) # 버퍼에 정보 저장
                state_history[:,:,:state_size] = state_history[:,:,1:] # 다음 환경이 저장될 공간(index 4)과 겹치지 않게 하기 위해 이전 환경 중 가장 오래된 환경(index 0)을 제거하고 이전 환경 재배치(index 1 ~ 4 -> index 0 ~ 3)
                episode_reward += reward # 보상 추가
                if global_step > train_interval: # 프레임 반복 횟수가 학습 주기를 넘겼을 경우
                    replay_memory_minibatch = random.sample(replay_memory, minibatch_size) # 버퍼에서 미니배치 크기만큼 샘플링
                    replay_train(mainDQN, targetDQN, replay_memory_minibatch, state_size, discount_factor) # 메인 신경망 학습
                    if global_step % target_update_interval == 0: # 타겟 신경망 업데이트 주기일 경우
                        sess.run(get_copy_var_ops(src_scope_name='main', dest_scope_name='target')) # 타겟 신경망에 메인 신경망의 가중치 복사
                if global_step % train_interval == 0: # 프레임 반복 횟수가 학습 주기에 도달했을 경우
                    epoch_complete = True # 학습 주기 도달 유무 변경
            total_reward_memory.append(episode_reward) # 한 게임에서 얻은 보상값 추가
            episode_summary = tf.Summary()
            episode_summary.value.add(simple_value=episode_reward, tag='reward/episode')
            episode_summary.value.add(simple_value=np.mean(total_reward_memory), tag='average_reward/episode')
            writer.add_summary(episode_summary, episode) # 텐서보드에 게임 반복 횟수에 따른 보상값 기록
            episode_summary2 = tf.Summary()
            episode_summary2.value.add(simple_value=epsilon, tag='epsilon/global_step')
            episode_summary2.value.add(simple_value=np.mean(Q_memory), tag='average_max_q_value/global_step')
            writer.add_summary(episode_summary2, global_step) # 텐서보드에 프레임 반복 횟수에 따른 엡실론 및 Q 기록
            writer.flush() # 텐서보드 기록 버퍼 비움
            if epoch_complete: # 프레임 반복 횟수가 학습 주기에 도달했을 경우
                epoch += 1 # 학습 주기 도달 횟수 증가
                epoch_complete = False # 학습 주기 도달 유무 변경
                Q_memory = deque() # 각 학습 주기에서 얻은 Q 버퍼 초기화
                mainDQN.saver.save(mainDQN.sess, model_directory + '\\weights.ckpt') # 학습 기록 저장
            print('Episode: {} | Step: {} | Reward: {} | AverageReward: {:.2f} | AverageMaxQ: {:.6f} | Epsilon: {:.6f}'.format(episode, global_step, episode_reward, np.mean(total_reward_memory), np.mean(Q_memory), epsilon))

if __name__ == '__main__':
    main()