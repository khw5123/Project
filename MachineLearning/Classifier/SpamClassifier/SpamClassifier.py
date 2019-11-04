# -*- coding: utf-8 -*-
'''
import os
import numpy as np

dataset_file = os.getcwd() + '\\smsspamcollection\\SMSSpamCollection'

# 단어집 생성
vocabulary = dict() # 단어집 {단어 : 고유ID}
with open(dataset_file, 'r', encoding='utf8') as file_handle:
    for line in file_handle:
        label = line.split(' ')[0] # ham : 일반 메시지, spam : 스팸 메시지
        text = line.split(' ')[1:] # 메시지 내용
        for word in text:
            word = word.lower()
            if not word in vocabulary:
                vocabulary[word] = len(vocabulary) # 단어집 생성 {단어 : 고유ID}

# 단어 출현 빈도 처리, 피처 생성
features = list() # 단어 빈도 피처 벡터(크기 : 문서 수 X 단어집 크기)
with open(dataset_file, 'r', encoding='utf8') as file_handle:
    for line in file_handle:
        feature = np.zeros(len(vocabulary)) # 단어집 크기만큼의 빈 피처 생성
        text = line.split(' ')[1:] # 메시지 내용
        for word in text:
            word = word.lower()
            feature[vocabulary[word]] += 1 # 단어가 있는 인덱스(고유ID)의 값 1 증가
        feature /= sum(feature) # 문서에서 나온 총 단어 수로 현재 피처를 나누어 단어 빈도 피처 생성
        features.append(feature) # 단어 빈도 피처 추가

# 레이블 처리
lebels = list() # 레이블 리스트
with open(dataset_file, 'r', encoding='utf8') as file_handle:
    for line in file_handle:
        label = line.split(' ')[0] # ham : 일반 메시지, spam : 스팸 메시지
        if label == 'spam': # 레이블이 스팸 메시지일 경우
            lebels.append(1)
        else: # 레이블이 일반 메시지일 경우
            lebels.append(0)
'''
import os
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import LogisticRegression

dataset_file = os.getcwd() + '\\smsspamcollection\\SMSSpamCollection'
save_file = os.getcwd() + '\\processed.pickle'

# 1. 단어집 생성, 단어 출현 빈도 처리, 레이블 처리, 피처 생성
spam_header = 'spam\t'
no_spam_header = 'ham\t'
documents = list() # 스팸/일반 메시지 내용 리스트
labels = list() # 레이블 리스트

with open(dataset_file, 'r', encoding='utf8') as file_handle:
    for line in file_handle:
        if line.startswith(spam_header): # spam
            labels.append(1)
            documents.append(line[len(spam_header):]) # 스팸 메시지 내용 추가
        elif line.startswith(no_spam_header): # ham
            labels.append(0)
            documents.append(line[len(no_spam_header):]) # 일반 메시지 내용 추가

# class sklearn.feature_extraction.text.CountVectorizer(input=u'content', encoding=u'utf-8', decode_error=u'strict', strip_accents=None, lowercase=True, preprocessor=None, tokenizer=None, stop_words=None, token_pattern=u'(?u)\b\w\w+\b', ngram_range=(1, 1), analyzer=u'word', max_df=1.0, min_df=1, max_features=None, vocabulary=None, binary=False, dtype=<type 'numpy.int64'>) : 문서를 단어 단위로 쪼개서 각 단어가 몇 번 나왔는지 세어 단어 카운팅 피처를 만드는 클래스
vectorizer = CountVectorizer() # 단어 카운팅 피처 객체 생성
term_counts = vectorizer.fit_transform(documents) # 단어 카운팅 피처 생성
vocabulary = vectorizer.get_feature_names() # 단어집 생성

# class sklearn.feature_extraction.text.TfidfTransformer(norm=u'l2', use_idf=True, smooth_idf=True, sublinear_tf=False) : 단어 횟수 피처로 단어 빈도 피처를 만드는 클래스
tf_transformer = TfidfTransformer(use_idf=False).fit(term_counts) # 단어 빈도 피처 객체 생성(use_idf 인자 값이 True일 경우 TF-IDF 피처 생성)
features = tf_transformer.transform(term_counts) # 단어 빈도 피처 생성

with open(save_file, 'wb') as file_handle:
    pickle.dump((vocabulary, features, labels), file_handle) # 단어집, 단어 빈도 피처, 레이블을 파일에 저장

# 2. 로지스틱 회귀를 이용한 분류
with open(save_file, 'rb') as file_handle:
    vocabulary, features, labels = pickle.load(file_handle) # 단어집, 단어 빈도 피처, 레이블을 파일에서 가져옴

train_features = features[:len(labels) // 2] # 학습 데이터(문서의 처음 50%를 학습용 데이터로 사용)
train_labels = labels[:len(labels) // 2] # 학습 데이터의 레이블
test_features = features[len(labels) // 2:] # 평가 데이터(문서의 마지막 50%를 평가용 데이터로 사용)
test_labels = labels[len(labels) // 2:] # 평가 데이터의 레이블

# class sklearn.linear_model.LogisticRegression(penalty='l2', dual=False, tol=0.0001, C=1.0, fit_intercept=True, intercept_scaling=1, class_weight=None, random_state=None, solver='liblinear', max_iter=100, multi_class='ovr', verbose=0, warm_start=False, n_jobs=1) : 피처와 레이블 쌍을 이용해서 분류 모델을 학습하고 평가하는 로지스틱 회귀 모델 클래스
classifier = LogisticRegression() # 로지스틱 회귀 객체 생성
classifier.fit(train_features, train_labels) # 학습 데이터와 레이블을 이용해서 학습
print('train accurary : %4.4f' % classifier.score(train_features, train_labels)) # 학습 데이터의 정확도
print('test accurary : %4.4f\n' % classifier.score(test_features, test_labels)) # 평가 데이터의 정확도

weights = classifier.coef_[0,:] # 피처의 계수(가중치)
pairs = list() # (피처 계수의 절댓값, 해당 단어)가 저장될 리스트
for index, value in enumerate(weights):
    pairs.append((abs(value), vocabulary[index])) # 리스트에 (피처 계수의 절댓값, 해당 단어) 저장
pairs.sort(key=lambda x: x[0], reverse=True) # 피처 계수의 절댓값을 기준으로 내림차순 정렬
for pair in pairs[:20]:
    print('score %4.4f, word : %s' % pair)