# -*- coding: utf-8 -*-
import os
import random
import datetime
import tempfile
import numpy as np
import tensorflow as tf
import gym
from collections import deque

class DQN:
    def __init__(self, input_node_count, output_node_count, learning_rate, global_step, save_directory, name):
        self.input_node_count = input_node_count # 입력 노드 크기
        self.output_node_count = output_node_count # 출력 노드 크기
        self.learning_rate = learning_rate # 학습률
        self.global_step = global_step # 반복 횟수
        self.name = name # 신경망 이름
        with tf.variable_scope(name):
            self.build_network() # 신경망 생성
            if save_directory: # 텐서보드 로그 디렉터리를 설정했을 경우
                self.graph_directory = os.path.join(save_directory, 'graph') # 텐서보드 로그 디렉터리 생성
                if not os.path.exists(self.graph_directory): # 경로가 존재하지 않을 경우
                    os.makedirs(self.graph_directory) # 경로 생성
                self.summaries = tf.summary.merge([
                    tf.summary.scalar('loss', self.loss), # 텐서보드에 오차 기록
                    tf.summary.scalar('max_q_value', tf.reduce_max(self.Q_pred)), # 텐서보드에 예측한 Q의 최댓값 기록
                    tf.summary.scalar('mean_q_value', tf.reduce_mean(self.Q_pred)) # 텐서보드에 예측한 Q의 평균값 기록
                ])
                self.rewards = tf.placeholder(tf.float32, [None]) # 보상값 플레이스홀더
                self.reward_summary = tf.summary.merge([tf.summary.scalar('average_reward', tf.reduce_mean(self.rewards))]) # 평균 보상값 텐서보드 기록
                self.writer = tf.summary.FileWriter(self.graph_directory) # 텐서보드 기록 객체
            else: # 텐서보드 로그 디렉터리를 설정하지 않았을 경우
                self.writer = None
    
    def neural_network(self): # 신경망 메서드
        first_hidden_node_count, second_hidden_node_count, = 32, 32 # 은닉 노드 개수
        first_layer = tf.contrib.layers.fully_connected(self.X, first_hidden_node_count, activation_fn=tf.nn.relu) # 완전 연결 레이어 1
        second_layer = tf.contrib.layers.fully_connected(first_layer, second_hidden_node_count, activation_fn=tf.nn.relu) # 완전 연결 레이어 2
        return tf.contrib.layers.fully_connected(second_layer, self.output_node_count, activation_fn=None) # 출력값
    
    def build_network(self): # 신경망 생성 메서드
        self.X = tf.placeholder(shape=[None, self.input_node_count], dtype=tf.float32, name='X') # 환경
        self.Y = tf.placeholder(shape=[None, self.output_node_count], dtype=tf.float32, name='Y') # 레이블
        self.Q_pred = self.neural_network() # Q
        self.loss = tf.reduce_mean(tf.squared_difference(self.Y, self.Q_pred)) # 오차 평균(제곱 손실함수)
        self.train_op = tf.contrib.layers.optimize_loss(self.loss, global_step=tf.train.get_global_step(), learning_rate=self.learning_rate, optimizer='Adam') # 최적화
    
    def predict(self, sess, state): # 환경을 이용해서 예측한 Q를 반환하는 매서드
        return sess.run(self.Q_pred, feed_dict={self.X: state}) # Q 반환
    
    def fit(self, sess, state, y, epoch): # 신경망 학습 메서드
        for _ in range(epoch):
            summaries, train_op, loss, Q_pred, self.global_step = sess.run([self.summaries, self.train_op, self.loss, self.Q_pred, tf.train.get_global_step()], feed_dict={self.X: state, self.Y: y}) # 신경망 학습
        if self.writer: # 텐서보드 기록 객체가 있을 경우
            self.writer.add_summary(summaries, self.global_step) # 텐서보드에 기록

class Memory:
    def __init__(self, memory_size=5000):
        self.memory = deque(maxlen=memory_size) # 버퍼
    
    def __len__(self):
        return len(self.memory) # 버퍼 크기 반환
    
    def add_memory(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # 버퍼에 정보 추가
    
    def get_memory(self):
        return list(self.memory) # 버퍼 반환

class Agent:
    def __init__(self, input_node_count, output_node_count, save_directory=None):
        self.input_node_count = input_node_count # 입력 노드 크기
        self.output_node_count = output_node_count # 출력 노드 크기
        self.epsilon = 1.0 # 반복할수록 랜덤한 액션을 줄이고 신경망을 이용해서 결정한 액션을 하기위한 엡실론
        self.epsilon_min = 0.01 # 임계 엡실론
        self.epsilon_decay = 0.9994 # 엡실론 감소 상수
        self.discounted_reward = 0.99  # 과거의 보상을 줄이기 위한 상수
        self.learning_rate = 0.0001 # 학습률
        self.epoch = 1  # 신경망 학습 반복 횟수
        self.batch_size = 32 # 미니배치 크기
        self.memory = Memory(memory_size=250000) # 버퍼
        self.global_step = tf.Variable(0, name='global_step', trainable=False) # 반복 횟수
        self.main_model = DQN(self.input_node_count, self.output_node_count, self.learning_rate, self.global_step, save_directory, name='main') # 메인 신경망
        self.target_model = DQN(self.input_node_count, self.output_node_count, self.learning_rate, self.global_step, save_directory, name='target') # 타겟 신경망
        self.saver = tf.train.Saver() # 학습 기록(신경망 가중치) 저장 객체
        self.sess = tf.Session() # 세션 생성
        self.sess.run(tf.global_variables_initializer()) # 세션 초기화
    
    def update_epsilon(self): # 엡실론 업데이트 메서드
        if self.epsilon > self.epsilon_min: # 엡실론이 임계치보다 클 경우
            self.epsilon *= self.epsilon_decay # 엡실론 감소
    
    def save_weights(self, model_directory):
        self.saver.save(self.sess, model_directory + '\\weights.ckpt') # 학습 기록(신경망 가중치) 저장
    
    def load_weights(self, model_directory):
        self.saver.restore(self.sess, model_directory + '\\weights.ckpt') # 학습 기록(신경망 가중치) 로드
    
    def update_target_model(self): # 타겟 신경망에 메인 신경망의 가중치를 복사하는 메서드
        main_model_params = [t for t in tf.trainable_variables() if t.name.startswith(self.main_model.name)]
        target_model_params = [t for t in tf.trainable_variables() if t.name.startswith(self.target_model.name)]
        main_model_params = sorted(main_model_params, key=lambda x: x.name)
        target_model_params = sorted(target_model_params, key=lambda x: x.name)
        operations = [target_coef.assign(main_coef) for main_coef, target_coef in zip(main_model_params, target_model_params)]
        self.sess.run(operations)
    
    def get_action(self, state): # Q와 엡실론을 이용해서 결정한 액션을 반환하는 메서드
        if self.epsilon >= np.random.rand(): # 엡실론이 무작위 값보다 클 경우
            return np.random.choice(self.output_node_count) # 랜덤한 액션
        else: # 엡실론이 무작위 값보다 작을 경우
            return np.argmax(self.main_model.predict(self.sess, state)[0]) # 신경망을 이용해서 결정한 액션
    
    def replay_train(self): # 메인 신경망 학습 메서드
        replay_memory_minibatch = np.array(random.sample(self.memory.get_memory(), self.batch_size)) # 버퍼에서 미니배치 크기만큼 랜덤한 인덱스의 정보들을 가져옴
        state = np.vstack(replay_memory_minibatch[:, 0]) # 환경
        action = np.array(replay_memory_minibatch[:, 1], dtype=int) # 액션
        reward = np.copy(replay_memory_minibatch[:, 2]) # 보상
        next_state = np.vstack(replay_memory_minibatch[:, 3]) # 다음 상태
        done = np.where(replay_memory_minibatch[:, 4] == False) # 게임 종료 여부
        Q_main = self.main_model.predict(self.sess, next_state) # 메인 신경망의 Q
        Q_target = self.target_model.predict(self.sess, next_state) # 타겟 신경망의 Q
        if len(done[0]) > 0: # 게임이 진행중인 경우
            reward[done] += np.multiply(self.discounted_reward, Q_target[done, np.argmax(Q_main[done, :][0], axis=1)][0]) # 레이블
        expected_reward = self.main_model.predict(self.sess, state)
        expected_reward[range(self.batch_size), action] = reward
        self.main_model.fit(self.sess, state, expected_reward, self.epoch) # 메인 신경망 학습

class Environment:
    def __init__(self, game, save_directory):
        np.set_printoptions(precision=2)
        self.env = gym.make(game) # 환경 생성
        self.env = gym.wrappers.Monitor(self.env, tempfile.mkdtemp(), force=True, video_callable=False)
        self.input_node_count = self.env.observation_space.shape[0] # 입력 노드 개수
        self.output_node_count = self.env.action_space.n # 출력 노드 개수
        self.save_directory = save_directory # 저장 디렉터리
        self.model_directory = save_directory + '\\model' # 학습 기록(신경망 가중치) 디렉터리
        self.total_reward_memory = deque(maxlen=100) # 각 게임에서 얻은 보상값 버퍼
        self.episode_reward_memory = deque() # 한 게임에서 얻은 보상값 버퍼
    
    def test(self): # 평가 메서드
        self.agent = Agent(self.input_node_count, self.output_node_count) # 에이전트 생성
        self.learn(epsilon=0.0, episodes=0, play=True) # 평가
    
    def train(self, epsilon=1.0, episodes=2500): # 학습 메서드
        os.mkdir(self.save_directory) # 저장 디렉터리 생성
        os.mkdir(self.model_directory) # 학습 기록(신경망 가중치) 디렉터리 생성
        self.agent = Agent(self.input_node_count, self.output_node_count, self.save_directory) # 에이전트 생성
        self.learn(epsilon=epsilon, episodes=episodes, play=False) # 학습
    
    def learn(self, epsilon, episodes, play):
        if play == True: # 평가일 경우
            self.agent.load_weights(self.model_directory) # 학습 기록(신경망 가중치) 로드
        episode = -1 # 게임 반복 횟수
        self.agent.epsilon = epsilon # 반복할수록 랜덤한 액션을 줄이고 신경망을 이용해서 결정한 액션을 하기위한 엡실론
        while episode <= episodes:
            if episodes == 0: # 평가일 경우
                episode = -1 # 무한 반복을 위해 게임 반복 횟수 초기화
            episode += 1 # 게임 반복 횟수 증가
            episode_reward = 0 # 한 게임에서 얻은 보상값
            done = False # 게임 종료 여부
            state = self.env.reset() # 환경 초기화
            state = np.reshape(state, [1, self.input_node_count])
            while not done:
                if play == True: # 평가일 경우
                    self.env.render() # 환경 렌더링
                action = self.agent.get_action(state) # 액션
                next_state, reward, done, _ = self.env.step(action) # 환경 실행
                next_state = np.reshape(next_state, [1, self.input_node_count]) # 다음 상태
                episode_reward += reward # 보상 추가
                if play == False: # 학습일 경우
                    self.agent.memory.add_memory(state, action, reward, next_state, done) # 버퍼에 정보 추가
                state = next_state # 환경 업데이트
                if play == False: # 학습일 경우
                    if len(self.agent.memory) > self.agent.batch_size: # 버퍼의 크기가 미니배치 크기보다 클 경우
                        self.agent.replay_train() # 메인 신경망 학습
            if play == False: # 학습일 경우
                self.agent.update_target_model() # 타겟 신경망에 메인 신경망의 가중치를 복사
            self.agent.update_epsilon() # 엡실론 업데이트
            self.total_reward_memory.append(episode_reward) # 한 게임에서 얻은 보상값 추가
            self.episode_reward_memory.append(episode_reward) # 한 게임에서 얻은 보상값 추가
            print('Episode: %d | Reward: %.2f | Average_Reward: %.2f | epsilon %.2f' % (episode, episode_reward, np.average(self.total_reward_memory), self.agent.epsilon))
            if play == False: # 학습일 경우
                summary = self.agent.sess.run(self.agent.main_model.reward_summary, feed_dict={self.agent.main_model.rewards: self.episode_reward_memory}) # 텐서보드에 평균 보상값 및 게임 반복 횟수 기록
                self.agent.main_model.writer.add_summary(summary, episode)
                self.episode_reward_memory = deque() # 한 게임에서 얻은 보상값 버퍼 초기화
                if episode % 100 == 0:
                    self.agent.save_weights(self.model_directory) # 학습 기록(신경망 가중치) 저장
        self.env.close()
        if play == False: # 학습일 경우
            self.agent.save_weights(self.model_directory) # 학습 기록(신경망 가중치) 저장

def main():
    sel = input('\n[select]\n1. Train\n2. Play\nSelect : ')
    if sel == '1':
        save_directory = os.getcwd() + '\\' + datetime.datetime.today().strftime('%Y-%m-%d_%H_%M_%S')
        obj = Environment('LunarLander-v2', save_directory)
        obj.train(epsilon=1.0, episodes=5000)
    elif sel == '2':
        save_directory = input('Input Save Directory : ')
        obj = Environment('LunarLander-v2', save_directory)
        obj.test()

if __name__ == '__main__':
    main()