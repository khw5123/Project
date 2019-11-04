# -*- coding: utf-8 -*-
import os
import datetime
import random
import numpy as np
import tensorflow as tf
from collections import deque
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# https://github.com/golbin/TensorFlow-Tutorials/tree/master/12%20-%20DQN

MAX_EPISODE = 10000 # 최대 학습 횟수
OBSERVE = 100 # 학습 데이터를 어느정도 쌓은 후 설정한 반복 횟수 이후에 학습 시작
TRAIN_INTERVAL = 4 # 학습 주기
TARGET_UPDATE_INTERVAL = 1000 # 타겟 신경망 업데이트 주기
NUM_ACTION = 3 # 액션값(0: 좌, 1: 유지, 2: 우)
SCREEN_WIDTH, SCREEN_HEIGHT = 6, 10

class Game:
    def __init__(self, screen_width, screen_height, show_game=True):
        self.screen_width = screen_width # 게임판의 가로 크기
        self.screen_height = screen_height # 게임판의 세로 크기
        self.road_width = int(screen_width / 2) # 도로의 가로 크기
        self.road_left = int(self.road_width / 2 + 1) # 도로의 좌측 크기
        self.road_right = int(self.road_left + self.road_width - 1) # 도로의 우측 크기
        self.car = {"col": 0, "row": 2} # 자동차 위치
        self.block = [{"col": 0, "row": 0, "speed": 1}, {"col": 0, "row": 0, "speed": 2}] # 장애물 위치 및 속도
        self.total_reward = 0. # 한 게임의 최종 보상값
        self.current_reward = 0. # 진행중인 게임의 실시간 보상값
        self.total_game = 0 # 진행한 게임 수
        self.show_game = show_game # 게임 화면 출력 여부
        if show_game: # 게임 화면 출력 설정을 했을 경우
            self.fig, self.axis = self._prepare_display() # 게임 화면 출력 설정
    
    def _prepare_display(self): # 게임 화면 출력 설정 함수
        fig, axis = plt.subplots(figsize=(4, 6))
        fig.set_size_inches(4, 6)
        fig.canvas.mpl_connect('close_event', exit) # 화면을 닫으면 프로그램 종료
        plt.axis((0, self.screen_width, 0, self.screen_height))
        plt.tick_params(top='off', right='off', left='off', labelleft='off', bottom='off', labelbottom='off')
        plt.draw()
        plt.ion() # 게임을 진행하며 화면을 업데이트 할 수 있도록 interactive 모드로 설정
        plt.show()
        return fig, axis
    
    def _get_state(self): # 위치 상태 반환 함수
        # 게임의 상태는 screen_width x screen_height 크기로 각 위치에 대한 상태값을 가지고 있으며, 빈 공간인 경우에는 0, 사물이 있는 경우에는 1이 들어있는 1차원 배열
        state = np.zeros((self.screen_width, self.screen_height)) # 위치 상태 초기화
        state[self.car["col"], self.car["row"]] = 1 # 자동차 위치 표시
        if self.block[0]["row"] < self.screen_height: # 장애물이 있을 경우
            state[self.block[0]["col"], self.block[0]["row"]] = 1 # 장애물 위치 표시
        if self.block[1]["row"] < self.screen_height: # 장애물이 있을 경우
            state[self.block[1]["col"], self.block[1]["row"]] = 1 # 장애물 위치 표시
        return state # 위치 상태 반환
    
    def _draw_screen(self): # 게임 화면 출력 함수
        title = " Avg. Reward: %d Reward: %d Total Game: %d" % (self.total_reward / self.total_game, self.current_reward, self.total_game)
        self.axis.set_title(title, fontsize=12)
        road = patches.Rectangle((self.road_left - 1, 0), self.road_width + 1, self.screen_height, linewidth=0, facecolor="#333333")
        # 자동차, 장애물들을 1x1 크기의 정사각형으로 그리도록하며, 좌표를 기준으로 중앙에 위치시킴
        # 자동차의 경우에는 장애물과 충돌시 확인이 가능하도록 0.5만큼 아래쪽으로 이동하여 출력
        car = patches.Rectangle((self.car["col"] - 0.5, self.car["row"] - 0.5), 1, 1, linewidth=0, facecolor="#00FF00")
        block1 = patches.Rectangle((self.block[0]["col"] - 0.5, self.block[0]["row"]), 1, 1, linewidth=0, facecolor="#0000FF")
        block2 = patches.Rectangle((self.block[1]["col"] - 0.5, self.block[1]["row"]), 1, 1, linewidth=0, facecolor="#FF0000")
        self.axis.add_patch(road)
        self.axis.add_patch(car)
        self.axis.add_patch(block1)
        self.axis.add_patch(block2)
        self.fig.canvas.draw()
        plt.pause(0.0001) # 게임의 다음 단계 진행을 위해 잠시 대기

    def reset(self): # 자동차, 장애물의 위치와 보상값 초기화 함수
        self.current_reward = 0 # 보상값 초기화
        self.total_game += 1 # 진행한 게임 수 초기화
        self.car["col"] = int(self.screen_width / 2) # 자동차 위치 초기화
        self.block[0]["col"] = random.randrange(self.road_left, self.road_right + 1) # 장애물 위치 초기화
        self.block[0]["row"] = 0
        self.block[1]["col"] = random.randrange(self.road_left, self.road_right + 1) # 장애물 위치 초기화
        self.block[1]["row"] = 0
        self._update_block() # 장애물 위치 갱신
        return self._get_state() # 위치 상태 반환
    
    def _update_car(self, move): # 자동차 위치 갱신 함수
        self.car["col"] = max(self.road_left, self.car["col"] + move) # 자동차 위치를 갱신하되 자동차의 위치가 도로의 좌측을 넘지 않도록 설정
        self.car["col"] = min(self.car["col"], self.road_right) # 자동차 위치를 갱신하되 자동차의 위치가 도로의 우측을 넘지 않도록 설정
    
    def _update_block(self): # 장애물 위치 갱신 함수
        reward = 0 # 보상값 초기화
        if self.block[0]["row"] > 0: # 장애물이 화면 내에 있는 경우
            self.block[0]["row"] -= self.block[0]["speed"] # 속도에 따라 위치 변경
        else: # 장애물이 화면을 벗어난 경우
            self.block[0]["col"] = random.randrange(self.road_left, self.road_right + 1) # 장애물 재설정
            self.block[0]["row"] = self.screen_height
            reward += 1 # 보상값 증가
        if self.block[1]["row"] > 0: # 장애물이 화면 내에 있는 경우
            self.block[1]["row"] -= self.block[1]["speed"] # 속도에 따라 위치 변경
        else: # 장애물이 화면을 벗어난 경우
            self.block[1]["col"] = random.randrange(self.road_left, self.road_right + 1) # 장애물 재설정
            self.block[1]["row"] = self.screen_height
            reward += 1 # 보상값 증가
        return reward # 보상값 반환
    
    def _is_gameover(self): # 장애물과 자동차가 충돌했는지를 파악하는 함수
        if ((self.car["col"] == self.block[0]["col"] and self.car["row"] == self.block[0]["row"]) or (self.car["col"] == self.block[1]["col"] and self.car["row"] == self.block[1]["row"])): # 충돌했을 경우
            self.total_reward += self.current_reward # 보상값 추가
            return True
        else: # 충돌하지 않았을 경우
            return False
    
    def step(self, action): # 게임 진행 함수
        self._update_car(action - 1) # 자동차 위치 갱신
        escape_reward = self._update_block() # 장애물 위치 갱신 및 회피에 따른 보상값 저장
        stable_reward = 1. / self.screen_height if action == 1 else 0 # 움직임이 적을 경우에도 보상을 줘서 안정적으로 이동하는 것 처럼 보이게 함
        gameover = self._is_gameover() # 게임 종료 여부
        if gameover: # 장애물과 자동차가 충돌했을 경우.
            reward = -2 # 보상값 감소
        else: # 장애물과 자동차가 충돌하지 않았을 경우
            reward = escape_reward + stable_reward # 회피 보상값 + 안정 보상값
            self.current_reward += reward # 보상값 추가
        if self.show_game: # 게임 화면 출력 설정을 했을 경우
            self._draw_screen() # 게임 화면 출력
        return self._get_state(), reward, gameover # 위치 상태, 보상값, 게임 종료 여부 반환

class DQN:
    def __init__(self, session, width, height, n_action):
        self.session = session # 세션
        self.REPLAY_MEMORY = 10000 # 버퍼 최대 크기
        self.BATCH_SIZE = 32 # 미니배치 크기
        self.GAMMA = 0.99 # 과거 가중치를 줄이기 위한 상수
        self.n_action = n_action # 액션값(0: 좌, 1: 유지, 2: 우)
        self.width = width # 게임판의 가로 크기
        self.height = height # 게임판의 세로 크기
        self.memory = deque() # 버퍼
        self.state = None # 환경(상태)
        self.STATE_LEN = 4 # 앞의 환경까지 고려하기 위한 한 번에 볼 총 프레임 수(과거 3번 + 현재 1번)
        self.input_X = tf.placeholder(tf.float32, [None, width, height, self.STATE_LEN]) # 환경
        self.input_A = tf.placeholder(tf.int64, [None]) # 액션
        self.input_Y = tf.placeholder(tf.float32, [None]) # 레이블
        self.Q = self._build_network('main') # 메인 신경망
        self.cost, self.train_op = self._build_op() # 오차, 최적화 결과
        self.target_Q = self._build_network('target') # 타겟 신경망
    
    def _build_network(self, name): # 신경망 생성 함수
        with tf.variable_scope(name):
            model = tf.layers.conv2d(self.input_X, 32, [4, 4], padding='same', activation=tf.nn.relu) # 합성곱 레이어1
            model = tf.layers.conv2d(model, 64, [2, 2], padding='same', activation=tf.nn.relu) # 합성곱 레이어2
            model = tf.contrib.layers.flatten(model)
            model = tf.layers.dense(model, 512, activation=tf.nn.relu) # 완전 연결 레이어
            Q = tf.layers.dense(model, self.n_action, activation=None) # 출력값
        return Q # 출력값 반환
    
    def _build_op(self): # 오차 및 최적화 결과 반환 함수
        one_hot = tf.one_hot(self.input_A, self.n_action, 1.0, 0.0) # 각 액션(0: 좌, 1: 유지, 2: 우)들의 상태로 원-핫 인코딩 벡터 생성
        Q_value = tf.reduce_sum(tf.multiply(self.Q, one_hot), axis=1) # 원-핫 인코딩 적용한 Q
        cost = tf.reduce_mean(tf.square(self.input_Y - Q_value)) # 오차 평균(제곱 손실함수)
        train_op = tf.train.AdamOptimizer(1e-6).minimize(cost) # 역전파 알고리즘을 이용해서 가중치 갱신
        return cost, train_op # 오차 및 최적화 결과 반환
    
    def update_target_network(self): # 타겟 신경망이 메인 신경망과 같아지도록 복사하는 함수
        copy_op = []
        main_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope='main')
        target_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope='target')
        for main_var, target_var in zip(main_vars, target_vars):
            copy_op.append(target_var.assign(main_var.value()))
        self.session.run(copy_op)
    
    def get_action(self): # 액션 반환 함수
        Q_value = self.session.run(self.Q, feed_dict={self.input_X: [self.state]})
        action = np.argmax(Q_value[0])
        return action # 액션 반환
    
    def init_state(self, state): # 환경 초기화 함수
        state = [state for _ in range(self.STATE_LEN)] # 환경 초기화
        self.state = np.stack(state, axis=2) # 환경 저장
    
    def remember(self, state, action, reward, terminal): # 정보 저장 함수
        next_state = np.reshape(state, (self.width, self.height, 1)) # 다음 상태
        next_state = np.append(self.state[:, :, 1:], next_state, axis=2)
        self.memory.append((self.state, next_state, action, reward, terminal)) # 버퍼에 정보 추가
        if len(self.memory) > self.REPLAY_MEMORY: # 버퍼가 설정한 최대 크기를 초과했을 경우
            self.memory.popleft() # 제일 오래된 버퍼 비움
        self.state = next_state # 환경 갱신
    
    def _sample_memory(self): # 버퍼에 있는 정보 반환 함수
        sample_memory = random.sample(self.memory, self.BATCH_SIZE) # 버퍼에서 미니배치 크기만큼 랜덤한 인덱스의 정보들을 가져옴
        state = [memory[0] for memory in sample_memory]
        next_state = [memory[1] for memory in sample_memory]
        action = [memory[2] for memory in sample_memory]
        reward = [memory[3] for memory in sample_memory]
        terminal = [memory[4] for memory in sample_memory]
        return state, next_state, action, reward, terminal
    
    def train(self): # 학습 함수
        state, next_state, action, reward, terminal = self._sample_memory() # 버퍼에서 미니배치 크기만큼 랜덤한 인덱스의 정보들을 가져옴
        target_Q_value = self.session.run(self.target_Q, feed_dict={self.input_X: next_state}) # 타겟 신경망을 이용해 다음 상태의 Q 저장
        Y = [] # 레이블
        for i in range(self.BATCH_SIZE):
            if terminal[i]: # 게임 종료 상태인 경우
                Y.append(reward[i]) # 보상값만 저장
            else: # 게임 진행중인 상태일 경우
                Y.append(reward[i] + self.GAMMA * np.max(target_Q_value[i])) # 보상값과 다음 상태의 Q의 합 저장을 저장하되 다음 상태의 Q를 얻어올 때 타겟 신경망을 이용
        self.session.run(self.train_op, feed_dict={self.input_X: state, self.input_A: action, self.input_Y: Y}) # 학습

def train(graph_directory, model_directory):
    global MAX_EPISODE, OBSERVE, TRAIN_INTERVAL, TARGET_UPDATE_INTERVAL, NUM_ACTION, SCREEN_WIDTH, SCREEN_HEIGHT
    sess = tf.Session() # 세션 생성
    game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, show_game=False) # 게임 객체 생성
    brain = DQN(sess, SCREEN_WIDTH, SCREEN_HEIGHT, NUM_ACTION) # 신경망 객체 생성
    rewards = tf.placeholder(tf.float32, [None]) # 보상값 플레이스홀더
    tf.summary.scalar('Average Reward / Episode', tf.reduce_mean(rewards)) # 평균 보상값 텐서보드 기록
    saver = tf.train.Saver() # 학습 기록 저장 객체
    sess.run(tf.global_variables_initializer()) # 세션 초기화
    writer = tf.summary.FileWriter(graph_directory, sess.graph) # 텐서보드 기록 객체
    summary_merged = tf.summary.merge_all()
    brain.update_target_network() # 타겟 신경망이 메인 신경망과 같아지도록 복사
    epsilon = 1.0 # 반복할수록 랜덤한 액션을 줄이고 신경망을 이용한 액션을 하기위한 엡실론
    time_step = 0 # 프레임 횟수
    total_reward_list = [] # 보상값 리스트
    for episode in range(MAX_EPISODE):
        terminal = False # 게임 종료 여부
        total_reward = 0 # 한 게임에서 얻은 보상값
        state = game.reset() # 게임 초기화
        brain.init_state(state) # 환경 초기화
        while not terminal:
            # 엡실론이 랜덤값보다 작은 경우에는 랜덤한 액션을 선택하고, 그 이상일 경우에는 DQN을 이용해 액션을 선택. 초반에는 거의 대부분 랜덤값을 사용하다가 점점 줄어들어 나중에는 거의 사용하지 않게됨
            if np.random.rand() < epsilon:
                action = random.randrange(NUM_ACTION) # 랜덤한 액션
            else:
                action = brain.get_action() # DQN을 이용한 액션
            # 초반에는 학습이 전혀 안되어 있기 때문에 엡실론 값을 그대로 사용하고, 일정 시간이 지난 뒤 부터 엡실론 값 감소
            if episode > OBSERVE: # 학습 횟수가 OBSERVE 보다 많을 경우
                epsilon -= 1 / 1000 # 엡실론 값 감소
            state, reward, terminal = game.step(action) # 환경 실행
            total_reward += reward # 보상값 추가
            brain.remember(state, action, reward, terminal) # 신경망에 정보 저장
            if time_step > OBSERVE and time_step % TRAIN_INTERVAL == 0:
                brain.train() # 학습
            if time_step % TARGET_UPDATE_INTERVAL == 0:
                brain.update_target_network() # 타겟 신경망이 메인 신경망과 같아지도록 복사
            time_step += 1 # 프레임 횟수 증가
        print('Episode: %d, Reward: %d' % (episode + 1, total_reward))
        total_reward_list.append(total_reward) # 리스트에 보상값 추가
        if episode % 10 == 0:
            summary = sess.run(summary_merged, feed_dict={rewards: total_reward_list}) # 텐서보드에 평균 보상값 및 프레임 횟수 기록
            writer.add_summary(summary, time_step)
            total_reward_list = [] # 보상값 리스트 초기화
        if episode % 100 == 0:
            saver.save(sess, model_directory + '\\dqn.ckpt', global_step=time_step) # 학습 기록 저장

def play(save_directory):
    global MAX_EPISODE, NUM_ACTION, SCREEN_WIDTH, SCREEN_HEIGHT
    sess = tf.Session() # 세션 생성
    game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, show_game=True) # 게임 객체 생성
    brain = DQN(sess, SCREEN_WIDTH, SCREEN_HEIGHT, NUM_ACTION) # 신경망 객체 생성
    saver = tf.train.Saver() # 학습 기록 저장 객체
    ckpt = tf.train.get_checkpoint_state(save_directory + '\\model') # 기록 가져옴
    saver.restore(sess, ckpt.model_checkpoint_path) # 기록 로드
    for episode in range(MAX_EPISODE):
        terminal = False # 게임 종료 여부
        total_reward = 0 # 한 게임에서 얻은 보상값
        state = game.reset() # 게임 초기화
        brain.init_state(state) # 환경 초기화
        while not terminal:
            action = brain.get_action() # DQN을 이용한 액션
            state, reward, terminal = game.step(action) # 환경 실행
            total_reward += reward # 보상값 추가
            brain.remember(state, action, reward, terminal) # 신경망에 정보 저장
        print('Episode: %d, Reward: %d' % (episode + 1, total_reward))

def main():
    sel = input('\n[select]\n1. Train\n2. Play\nSelect : ')
    if sel == '1':
        save_directory = os.getcwd() + '\\' + datetime.datetime.today().strftime('%Y-%m-%d_%H_%M_%S')
        graph_directory = save_directory + '\\graph'
        model_directory = save_directory + '\\model'
        os.mkdir(save_directory)
        os.mkdir(graph_directory)
        os.mkdir(model_directory)
        train(graph_directory, model_directory)
    elif sel == '2':
        save_directory = input('Input Save Directory : ')
        play(save_directory)

if __name__ == '__main__':
    main()