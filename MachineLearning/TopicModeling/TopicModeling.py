# -*- coding: utf-8 -*-
import os 
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer

dataset_file = os.getcwd() + '\\smsspamcollection\\SMSSpamCollection'

spam_header = 'spam\t'
no_spam_header = 'ham\t'
documents = list() # 메시지 내용 리스트

with open(dataset_file, 'r', encoding='utf8') as file_handle:
    for line in file_handle:
        if line.startswith(spam_header): # spam
            documents.append(line[len(spam_header):]) # 스팸 메시지 내용 추가
        elif line.startswith(no_spam_header): # ham
            documents.append(line[len(no_spam_header):]) # 일반 메시지 내용 추가

vectorizer = CountVectorizer(stop_words='english', max_features=2000) # 단어 카운팅 피처 객체 생성
term_counts = vectorizer.fit_transform(documents) # 단어 카운팅 피처 생성
vocabulary = vectorizer.get_feature_names() # 단어집 생성

# class sklearn.decomposition.LatentDirichletAllocation(n_topics=10, doc_topic_prior=None, topic_word_prior=None, learning_method=None, learning_decay=0.7, learning_offset=10.0, max_iter=10, batch_size=128, evaluate_every=-1, total_samples=1000000.0, perp_tol=0.1, mean_change_tol=0.001, max_doc_update_iter=100, n_jobs=1, verbose=0, random_state=None)﻿ : 토픽 모델링 클래스
topic_model = LatentDirichletAllocation() # 토픽 모델링 객체 생성
topic_model.fit(term_counts) # 토픽 모델 학습
topics = topic_model.components_ # 학습 결과 저장

for topic_id, weights in enumerate(topics):
    print('topic %d : ' % topic_id, end='')
    pairs = list() # (피처 계수의 절댓값, 해당 단어)가 저장될 리스트
    for term_id, value in enumerate(weights):
        pairs.append((abs(value), vocabulary[term_id])) # 리스트에 (피처 계수의 절댓값, 해당 단어) 저장
    pairs.sort(key=lambda x: x[0], reverse=True) # 피처 계수의 절댓값을 기준으로 내림차순 정렬
    for pair in pairs[:10]:
        print(pair[1], end=', ')
    print()