# -*- coding: utf-8 -*-
import os
import random
import numpy as np
import tensorflow as tf
import gym
from collections import deque

# https://github.com/dennybritz/reinforcement-learning/blob/master/DQN

ACTIONS = [0, 1, 2, 3] # 0: noop, 1: fire, 2: left, 3: right

class StateProcessor():
    def __init__(self):
        with tf.variable_scope('state_processor'):
            self.input_state = tf.placeholder(shape=[210, 160, 3], dtype=tf.uint8) # Breakout-v0 환경(이미지)
            self.output_state = tf.image.rgb_to_grayscale(self.input_state) # 환경 흑백 변환
            self.output_state = tf.image.crop_to_bounding_box(self.output_state, 34, 0, 160, 160)
            self.output_state = tf.image.resize_images(self.output_state, [84, 84], method=tf.image.ResizeMethod.NEAREST_NEIGHBOR) # 환경 크기 변환
            self.output_state = tf.squeeze(self.output_state)
    
    def process(self, sess, state):
        return sess.run(self.output_state, {self.input_state: state}) # Breakout-v0 환경(이미지) 변환해서 반환

class Estimator():
    def __init__(self, scope, summaries_dir=None):
        self.scope = scope # 네임 스페이스명
        self.learning_rate = 0.00025 # 학습률
        self.decay = 0.99 # Discounting factor
        self.momentum = 0.0 # 모멘텀
        self.epsilon = 1e-6 # 엡실론
        with tf.variable_scope(self.scope): # 네임 스페이스 생성
            self.build_model() # 신경망 생성
            if summaries_dir: # 저장 디렉터리를 설정했을 경우
                summary_dir = os.path.join(summaries_dir, 'graph') # 텐서보드 기록 디렉터리
                if not os.path.exists(summary_dir): # 텐서보드 기록 디렉터리가 없을 경우
                    os.makedirs(summary_dir) # 텐서보드 기록 디렉터리 생성
                self.summary_writer = tf.summary.FileWriter(summary_dir) # 텐서보드 기록 객체 생성
    
    def build_model(self): # 신경망 생성 메서드
        self.X = tf.placeholder(shape=[None, 84, 84, 4], dtype=tf.uint8, name='X') # 환경(이미지)
        self.Y = tf.placeholder(shape=[None], dtype=tf.float32, name='Y') # 레이블
        self.action = tf.placeholder(shape=[None], dtype=tf.int32, name='A') # 액션(0: noop, 1: fire, 2: left, 3: right)
        conv1 = tf.contrib.layers.conv2d((tf.to_float(self.X) / 255.0), 32, 8, 4, activation_fn=tf.nn.relu) # 합성곱 레이어
        conv2 = tf.contrib.layers.conv2d(conv1, 64, 4, 2, activation_fn=tf.nn.relu)
        conv3 = tf.contrib.layers.conv2d(conv2, 64, 3, 1, activation_fn=tf.nn.relu)
        fc1 = tf.contrib.layers.fully_connected(tf.contrib.layers.flatten(conv3), 512) # 완전 연결 레이어
        self.predictions = tf.contrib.layers.fully_connected(fc1, len(ACTIONS)) # Q
        self.action_predictions = tf.gather(tf.reshape(self.predictions, [-1]), tf.range(tf.shape(self.X)[0]) * tf.shape(self.predictions)[1] + self.action) # 액션
        self.losses = tf.squared_difference(self.Y, self.action_predictions) # 오차(제곱 손실함수)
        self.loss = tf.reduce_mean(self.losses) # 오차 평균
        self.optimizer = tf.train.RMSPropOptimizer(self.learning_rate, self.decay, self.momentum, self.epsilon) # 최적화
        self.train_op = self.optimizer.minimize(self.loss, global_step=tf.contrib.framework.get_global_step()) # 최적화 결과
        self.summaries = tf.summary.merge([
            tf.summary.scalar('loss', self.loss), # 텐서보드에 기록될 오차
            tf.summary.histogram('loss_hist', self.losses), 
            tf.summary.scalar('max_q_value', tf.reduce_max(self.predictions)), # 텐서보드에 기록될 Q
            tf.summary.histogram('q_values_hist', self.predictions)
        ])
    
    def predict(self, sess, state): # 환경을 이용해서 예측한 Q를 반환하는 매서드
        return sess.run(self.predictions, {self.X: state}) # Q 반환
    
    def update(self, sess, state, action, y): # 신경망 업데이트 메서드
        summaries, global_step, _, loss = sess.run([self.summaries, tf.contrib.framework.get_global_step(), self.train_op, self.loss], feed_dict={self.X: state, self.Y: y, self.action: action}) # 신경망 업데이트
        if self.summary_writer: # 텐서보드 기록 객체가 있을 경우
            self.summary_writer.add_summary(summaries, global_step) # 텐서보드에 프레임에 따른 오차 및 Q 기록
        return loss # 오차 반환

def copy_model_parameters(sess, main_estimator, target_estimator): # 타겟 신경망에 메인 신경망의 가중치를 복사하는 함수
    main_params = [t for t in tf.trainable_variables() if t.name.startswith(main_estimator.scope)]
    main_params = sorted(main_params, key=lambda v: v.name)
    target_params = [t for t in tf.trainable_variables() if t.name.startswith(target_estimator.scope)]
    target_params = sorted(target_params, key=lambda v: v.name)
    update_ops = [target_coef.assign(main_coef) for main_coef, target_coef in zip(main_params, target_params)]
    sess.run(update_ops)

def epsilon_greedy_policy(sess, main_estimator, state, epsilon): # E-Greedy
    action = np.ones(len(ACTIONS), dtype=float) * epsilon / len(ACTIONS) # 엡실론을 이용해서 액션들의 초기값 설정
    q_values = main_estimator.predict(sess, np.expand_dims(state, 0))[0] # 메인 신경망의 Q
    best_actions = np.argmax(q_values) # 메인 신경망의 Q를 이용해서 결정한 액션
    action[best_actions] += (1.0 - epsilon) # 액션값 설정
    return action # 액션 반환

def main():
    env = gym.envs.make('Breakout-v0') # 환경 생성
    tf.reset_default_graph() # 그래프 초기화
    _ = tf.Variable(0, name='global_step', trainable=False) # 프레임 반복 횟수 텐서플로 변수
    experiment_dir = os.getcwd() + '\\experiments' # 저장 디렉터리
    if not os.path.exists(experiment_dir): # 저장 디렉터리가 없을 경우
        os.makedirs(experiment_dir) # 저장 디렉터리 생성
    checkpoint_dir = os.path.join(experiment_dir, 'model') # 학습 기록(신경망 가중치) 디렉터리
    if not os.path.exists(checkpoint_dir): # 학습 기록(신경망 가중치) 디렉터리가 없을 경우
        os.makedirs(checkpoint_dir) # 학습 기록(신경망 가중치) 디렉터리 생성
    monitor_path = os.path.join(experiment_dir, 'monitor') # 모니터링 디렉터리
    if not os.path.exists(monitor_path): # 모니터링 디렉터리가 없을 경우
        os.makedirs(monitor_path) # 모니터링 디렉터리 생성
    main_estimator = Estimator(scope='main_q', summaries_dir=experiment_dir) # 메인 신경망
    target_estimator = Estimator(scope='target_q') # 타겟 신경망
    state_processor = StateProcessor() # 환경(이미지) 처리 객체
    train_count = 10000 # 학습 횟수
    ready_count = 10000 # 학습 전 정보 수집 횟수
    target_update_interval = 10000 # 타겟 신경망 업데이트 주기
    replay_memory_size = 500000 # 버퍼 크기
    replay_memory = deque(maxlen=replay_memory_size) # 버퍼
    total_reward_memory = deque(maxlen=train_count) # 각 게임에서 얻은 보상값 버퍼
    epsilon_start = 1.0 # 초기 엡실론
    epsilon_end = 0.1 # 임계 엡실론
    epsilon_decay_step = 500000 # 엡실론 범위 수
    discount_factor = 0.99 # discount factor
    batch_size = 32 # 배치 크기
    with tf.Session() as sess: # 세션 생성
        sess.run(tf.global_variables_initializer()) # 세션 초기화
        saver = tf.train.Saver() # 학습 기록(신경망 가중치) 저장 객체
        latest_checkpoint = tf.train.latest_checkpoint(checkpoint_dir) # 저장된 학습 기록(신경망 가중치)
        if latest_checkpoint: # 저장된 학습 기록(신경망 가중치)이 있을 경우
            saver.restore(sess, latest_checkpoint) # 학습 기록(신경망 가중치) 로드
            print('[+] Loaded checkpoint {}'.format(latest_checkpoint))
        global_step = sess.run(tf.contrib.framework.get_global_step()) # 프레임 반복 횟수
        epsilons = np.linspace(epsilon_start, epsilon_end, epsilon_decay_step) # 엡실론 범위
        env = gym.wrappers.Monitor(env, directory=monitor_path, resume=True, video_callable=False)
        for episode in range(ready_count + train_count): # 정보 수집 후 학습
            state = env.reset() # 환경 초기화
            state = state_processor.process(sess, state) # 환경(이미지) 처리
            state = np.stack([state] * 4, axis=2) # 환경 기록 리스트(과거 3번(index 0 ~ 2) + 현재 1번(index 3))
            done = False # 게임 종료 여부
            loss = None # 오차
            episode_reward = 0 # 한 게임에서 얻은 보상값
            while not done:
                env.render() # 환경 렌더링
                epsilon = epsilons[min(global_step, epsilon_decay_step - 1)] # 엡실론
                action_probs = epsilon_greedy_policy(sess, main_estimator, state, epsilon) # E-Greedy
                action = np.random.choice(np.arange(len(action_probs)), p=action_probs) # 액션
                next_state, reward, done, _ = env.step(ACTIONS[action]) # 환경 실행
                next_state = state_processor.process(sess, next_state) # 다음 환경(이미지) 처리
                next_state = np.append(state[:,:,1:], np.expand_dims(next_state, 2), axis=2) # 이전 환경 + 다음 환경
                episode_reward += reward # 보상값 추가
                replay_memory.append((state, action, reward, next_state, done)) # 버퍼에 정보 저장
                if episode > ready_count: # 학습 단계일 경우
                    samples = random.sample(replay_memory, batch_size) # 버퍼에서 미니배치 크기만큼 샘플링
                    states_batch, action_batch, reward_batch, next_states_batch, done_batch = map(np.array, zip(*samples)) # 샘플링된 정보
                    q_values_next_main = main_estimator.predict(sess, next_states_batch) # 메인 신경망의 Q
                    best_actions = np.argmax(q_values_next_main, axis=1) # 메인 신경망의 Q를 이용해서 결정한 다음 환경의 액션
                    q_values_next_target = target_estimator.predict(sess, next_states_batch) # 타겟 신경망의 Q
                    targets_batch = reward_batch + np.invert(done_batch).astype(np.float32) * discount_factor * q_values_next_target[np.arange(batch_size), best_actions] # 타겟 신경망의 Q를 이용해서 구한 레이블
                    loss = main_estimator.update(sess, np.array(states_batch), action_batch, targets_batch) # 메인 신경망 업데이트
                    if global_step % target_update_interval == 0: # 타겟 신경망 업데이트 주기일 경우
                        copy_model_parameters(sess, main_estimator, target_estimator) # 타겟 신경망에 메인 신경망의 가중치 복사
                    episode_summary = tf.Summary()
                    episode_summary.value.add(simple_value=epsilon, tag='epsilon/global_step')
                    main_estimator.summary_writer.add_summary(episode_summary, global_step) # 텐서보드에 프레임에 따른 엡실론 기록
                state = next_state # 환경 업데이트
                global_step += 1 # 프레임 반복 횟수 증가
            if episode > ready_count: # 학습 단계일 경우
                total_reward_memory.append(episode_reward) # 한 게임에서 얻은 보상값 추가
                episode_summary = tf.Summary()
                episode_summary.value.add(simple_value=episode_reward, tag='reward/episode')
                episode_summary.value.add(simple_value=np.mean(total_reward_memory), tag='average_reward/episode')
                main_estimator.summary_writer.add_summary(episode_summary, episode - ready_count) # 텐서보드에 게임 반복 횟수에 따른 보상값 기록
                main_estimator.summary_writer.flush() # 텐서보드 기록 버퍼 비움
                saver.save(sess, checkpoint_dir + '\\weights.ckpt') # 학습 기록(신경망 가중치) 저장
                print('Episode: {} | Step: {} | Reward: {} | AverageReward: {:.2f} | Epsilon: {:.4f} | Loss: {:.6f}'.format(episode + 1, global_step, episode_reward, np.mean(total_reward_memory), epsilons[min(global_step, epsilon_decay_step - 1)], loss))
            else:
                print('Episode: {} | Step: {} | Reward: {} | Epsilon: {:.4f}'.format(episode + 1, global_step, episode_reward, epsilons[min(global_step, epsilon_decay_step - 1)]))
        env.monitor.close()

if __name__ == '__main__':
    main()