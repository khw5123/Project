# -*- coding: utf-8 -*-
import os
import time
import codecs
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import mean_squared_error
'''
import nltk
nltk.download('wordnet')
'''
user_info_file = os.getcwd() + '\\ml-100k\\u.user' # 사용자 정보 파일(사용자ID | 나이 | 성별 | 직업 | 우편번호)
item_info_file = os.getcwd() + '\\ml-100k\\u.item' # 상품(영화) 정보 파일(영화ID | 영화 제목 | 상영 개시일 | 비디오 발매일(공백) | 영화 내용 | 장르(원-핫 인코딩))
preference_info_file = os.getcwd() + '\\ml-100k\\u.data' # 선호도(별점) 정보 파일(사용자ID | 영화ID | 별점 | 데이터 생성 시간)
'''
# u.item 파일의 IMDB URL을 이용할 수 없어서 영화 내용을 가져올 수 없기 때문에 영화 내용이 있는 파일에서 직접 영화 내용을 가져와 u.item 파일의 IMDB URL을 영화 내용으로 변환하는 작업
movie_plot_file = os.getcwd() + '\\ml-100k-plot.txt' # 영화 내용 파일
fp = open(movie_plot_file, 'r') # 영화 내용 파일 오픈
movie_plot = fp.readlines() # 영화(각 라인)별로 영화 내용 저장
fp.close()
movie_plot_list = list() # 영화 내용 리스트
for line in movie_plot:
    movie_plot_list.append(line.split('|')[-1]) # 영화 내용 부분만 리스트에 추가

fp = open(item_info_file, 'r', encoding='latin-1') # 상품(영화) 정보 파일 오픈
item_info = fp.readlines() # 영화(각 라인)별로 영화 정보 저장
fp.close()
tmp_item_info_list = list() # 상품(영화) 정보 리스트
for i in range(len(item_info)):
    line = item_info[i].split('|')
    line[4] = movie_plot_list[i].strip()
    info = ''
    for l in line:
        info += l + '|'
    tmp_item_info_list.append(info[:-1]) # IMDB URL을 영화 내용으로 변경한 정보 리스트에 추가

modified_item_info_file = os.getcwd() + '\\u.item' # 수정된 상품(영화) 정보 파일
fp = open(modified_item_info_file, 'a', encoding='utf-8') # 수정된 상품(영화) 정보 파일 오픈
for line in tmp_item_info_list:
    fp.write(line) # 상품(영화) 정보 파일 수정
fp.close()
'''
start_time1 = time.perf_counter()
start_time2 = time.process_time()

# 1. 데이터 전처리
# 사용자 및 상품(영화) 정보 파일의 데이터 읽는 함수
def read_data(info_file, delimiter):
    info_list = [] # 데이터 리스트
    for line in codecs.open(info_file, 'r', encoding='latin-1'): # 사용자 및 상품(영화) 정보 파일 오픈
        line = line.strip().split(delimiter) # 구분자로 각 라인 분리
        if (len(info_list) + 1) != int(line[0]):
            print('[-] Error')
            exit(0)
        info_list.append(line[1:]) # 리스트에 데이터 추가
    print('Row in %s : %d' % (info_file, len(info_list)))
    return info_list # 데이터 리스트 반환

user_info_list = read_data(user_info_file, '|') # 사용자 정보 리스트
item_info_list = read_data(item_info_file, '|') # 상품(영화) 정보 리스트

R = np.zeros((len(user_info_list), len(item_info_list)), dtype=np.float64) # 사용자 수 X 상품(영화) 수 크기의 유틸리티 행렬

for line in codecs.open(preference_info_file, 'r', encoding='latin-1'): # 선호도(별점) 정보 파일 오픈
    user, movie, rating, date = line.strip().split('\t')
    user_index = int(user) - 1 # 사용자 인덱스
    movie_index = int(movie) - 1 # 상품(영화) 인덱스
    R[user_index][movie_index] = float(rating) # 유틸리티 행렬의 각 항에 선호도(별점) 저장

# 사용자가 상품(영화)에 준 선호도(별점)에 편차가 있는지 확인
user_mean_list = [] # 사용자의 평균 선호도(별점) 리스트
for i in range(0, R.shape[0]): # 사용자 수만큼 반복
    user_rating = [x for x in R[i] if x > 0.0] # 선호도(별점)가 0인 미지항(선호도 정보가 존재하지 않는 항)을 제외하고 저장
    user_mean_list.append(stats.describe(user_rating).mean) # 사용자의 평균 선호도(별점) 기초 통계량 추가
print('\n', stats.describe(user_mean_list), '\n') # 사용자의 평균 선호도(별점) 기초 통계량 출력

item_mean_list = [] # 상품(영화)의 평균 선호도(별점) 리스트
for i in range(0, R.shape[1]): # 상품(영화) 수만큼 반복
    R_T = R.T # 상품(영화)의 평균 선호도(별점) 기초 통계량을 구하기 위해 유틸리티 행렬의 전치 행렬 저장
    movie_rating = [x for x in R_T[i] if x > 0.0] # 선호도(별점)가 0인 미지항(선호도 정보가 존재하지 않는 항)을 제외하고 저장
    item_mean_list.append(stats.describe(movie_rating).mean) # 상품(영화)의 평균 선호도(별점) 기초 통계량 추가
print('\n', stats.describe(item_mean_list), '\n') # 상품(영화)의 평균 선호도(별점) 기초 통계량 출력

# 2. 내용 기반 추천 시스템
movie_plot_list = [] # 영화 내용 리스트
movie_title_list = [] # 영화 제목 리스트

for movie_info in item_info_list:
    movie_plot_list.append(movie_info[3]) # 리스트에 영화 내용 추가
    movie_title_list.append(movie_info[0]) # 리스트에 영화 제목 추가

# class feature_extraction.text.TfidfVectorizer() : TF-IDF 클래스
vectorizer = TfidfVectorizer(min_df=3, stop_words='english') # TF-IDF 피처 객체 생성
features = vectorizer.fit_transform(movie_plot_list) # TF-IDF 피처 생성
feature_names = vectorizer.get_feature_names() # TF-IDF로 변환한 키워드 리스트
print(feature_names[:100]) # TF-IDF로 변환한 키워드 출력

# class nltk.tokenize.RegexpTokenizer() : 사용자가 정의한 정규식을 이용하여 문자열로부터 키워드를 생성하는 클래스
# class nltk.stem.WordNetLemmatizer() : 워드넷(어휘 목록)의 정보를 이용하여 입력된 단어의 원형을 찾는 클래스
# 단어의 단수/복수 형태에 관계없이 단어의 원형을 찾는 클래스
class LemmaTokenizer(object):
    def __init__(self):
        self.tokenizer = RegexpTokenizer('(?u)\w\w+') # 정규식을 이용해서 문자열로부터 키워드 추출하는 클래스 생성
        self.wnl = WordNetLemmatizer() # 단어의 원형 추출하는 클래스 생성
    def __call__(self, doc):
        return [self.wnl.lemmatize(t) for t in self.tokenizer.tokenize(doc)] # 정규식을 이용해서 문자열로부터 키워드 생성 후 단어의 원형 반환

vectorizer = TfidfVectorizer(min_df=3, tokenizer=LemmaTokenizer(), stop_words='english') # 단어 원형 클래스를 인자로 사용하여 TF-IDF 피처 객체 생성
features = vectorizer.fit_transform(movie_plot_list) # TF-IDF 피처 생성
feature_names = vectorizer.get_feature_names() # TF-IDF로 변환한 키워드 리스트
print(feature_names[:100]) # TF-IDF로 변환한 키워드 출력

# def sklearn.metrics.pairwise.cosine_similarity() : 코사인 유사도 함수
movie_similarity = cosine_similarity(features) # TF-IDF 피처를 이용해서 코사인 유사도 계산

# 코사인 유사도를 이용해서 설정한 영화와 비슷한 영화를 찾는 함수
def recommend_by_movie(movie_id):
    movie_index = movie_id - 1 # 설정한 영화의 인덱스
    # enumerate 함수로 [(인덱스, 유사도), ...] 리스트 생성 및 유사도를 기준으로 내림차순 정렬(생성된 리스트의 첫 번째 인덱스가 설정한 영화와 가장 비슷한 영화)
    similar_movies = sorted(list(enumerate(movie_similarity[movie_index])), key=lambda x: x[1], reverse=True)
    print('\nOriginal Movie : %s' % item_info_list[movie_index][0]) # 설정한 영화 제목 출력
    for i in range(1, 6): # 설정한 영화와 가장 비슷한(유사도가 가장 높은) 영화는 그 영화 자신이므로 그다음 비슷한 영화부터 출력
        movie_title = item_info_list[similar_movies[i][0]][0] # 설정한 영화와 비슷한(유사도가 높은) 영화 저장
        print('%d. Similar Movie : %s' % (i, movie_title)) # 설정한 영화와 비슷한(유사도가 높은) 영화 출력

recommend_by_movie(1)
recommend_by_movie(198)

# 3. 협업 필터링 기반 추천 시스템
# def sklearn.metrics.mean_squared_error() : 평균 제곱 편차 함수
# 교대 최소제곱법을 이용한 특이값 분해 함수(R : 유틸리티 행렬 or 학습데이터 행렬, n_iter : 미지 행렬 X, Y의 갱신 횟수, lambda_ : 정규화 파라미터, k : 요인 행렬 크기, test : 평가데이터 행렬)
def singular_value_decomposition_using_alternating_least_squares(R, n_iter, lambda_, k, test=False):
    m, n = R.shape # 사용자 수 X 상품(영화) 수
    X = 5 * np.random.rand(m, k) # 선호도(별점(0 ~ 5))를 원소로 갖는 사용자 수 X 요인 행렬 크기 크기의 미지 행렬
    Y = 5 * np.random.rand(k, n) # 선호도(별점(0 ~ 5))를 원소로 갖는 요인 행렬 크기 X 상품(영화) 수 크기의 미지 행렬
    errors = [] # 오차(작을수록 예측값이 실제값과 비슷함)
    if 'numpy' in str(type(test)): # 학습-평가 데이터를 이용한 경우
        print('\n[Singular Value Decomposition(SVD) Using Alternating Least Squares(ALS) Train-Test]')
    else: # 학습-평가 데이터를 이용하지 않은 경우
        print('\n[Singular Value Decomposition(SVD) Using Alternating Least Squares(ALS)]')
    for i in range(0, n_iter): # 설정한 갱신 횟수만큼 반복
        # def np.linalg.solve(a, b) : 선형 방정식(aX = b) 계산 함수
        X = np.linalg.solve(np.dot(Y, Y.T) + lambda_ * np.eye(k), np.dot(Y, R.T)).T # L2 정규화 손실함수를 x에 대해서 미분한 값(행렬)
        Y = np.linalg.solve(np.dot(X.T, X) + lambda_ * np.eye(k), np.dot(X.T, R)) # L2 정규화 손실함수를 y에 대해서 미분한 값(행렬)
        if 'numpy' in str(type(test)): # 학습-평가 데이터를 이용한 경우
            train_data = np.dot(X, Y)[test.nonzero()].flatten() # 미지항(선호도 정보가 존재하지 않는 항)을 제외한 학습데이터 행렬
            test_data = test[test.nonzero()].flatten() # 미지항(선호도 정보가 존재하지 않는 항)을 제외한 평가데이터 행렬
            errors.append(mean_squared_error(test_data, train_data)) # 두 행렬의 평균 제곱 편차 계산 후 오차 추가
        else: # 학습-평가 데이터를 이용하지 않은 경우
            errors.append(mean_squared_error(R, np.dot(X, Y))) # 두 행렬의 평균 제곱 편차 계산 후 오차 추가
        print('Error of %dst iteration : %f' % (i + 1, errors[i])) # 갱신에 따른 오차 출력
    R_hat = np.dot(X, Y) # 근사 행렬(XY) 저장
    print('The final Error : %f' % errors[-1]) # 최종 오차 출력
    return R_hat, errors # 근사 행렬 및 오차 반환

R_hat, errors = singular_value_decomposition_using_alternating_least_squares(R, 20, 0.1, 100)

# 가중치 교대 최소제곱법을 이용한 특이값 분해 함수(R : 유틸리티 행렬, W : 가중치 행렬, n_iter : 미지 행렬 X, Y의 갱신 횟수, lambda_ : 정규화 파라미터, k : 요인 행렬 크기)
def singular_value_decomposition_using_weighted_alternating_least_squares(R, W, n_iter, lambda_, k):
    m, n = R.shape # 사용자 수 X 상품(영화) 수
    X = 5 * np.random.rand(m, k) # 선호도(별점(0 ~ 5))를 원소로 갖는 사용자 수 X 요인 행렬 크기 크기의 미지 행렬
    Y = 5 * np.random.rand(k, n) # 선호도(별점(0 ~ 5))를 원소로 갖는 요인 행렬 크기 X 상품(영화) 수 크기의 미지 행렬
    weighted_errors = [] # 오차(작을수록 예측값이 실제값과 비슷함)
    print('\n[Singular Value Decomposition(SVD) Using Weighted Alternating Least Squares(WALS)]')
    for j in range(n_iter): # 설정한 갱신 횟수만큼 반복
        for u, Wu in enumerate(W):
            X[u,:] = np.linalg.solve(np.dot(Y, np.dot(np.diag(Wu), Y.T)) + lambda_ * np.eye(k), np.dot(Y, np.dot(np.diag(Wu), R[u,:].T))).T # 가중치 행렬이 적용된 L2 정규화 손실함수를 x에 대해서 미분한 값(행렬)
        for i, Wi in enumerate(W.T):
            Y[:,i] = np.linalg.solve(np.dot(X.T, np.dot(np.diag(Wi), X)) + lambda_ * np.eye(k), np.dot(X.T, np.dot(np.diag(Wi), R[:,i]))) # 가중치 행렬이 적용된 L2 정규화 손실함수를 y에 대해서 미분한 값(행렬)
        weighted_errors.append(mean_squared_error(R, np.dot(X, Y), sample_weight=W)) # 두 행렬의 평균 제곱 편차 계산 후 오차 추가
        print('Error of %dst iteration : %f' % (j + 1, weighted_errors[j])) # 갱신에 따른 오차 출력
    R_hat = np.dot(X, Y) # 근사 행렬(XY) 저장
    print('The final Error : %f' % weighted_errors[-1]) # 최종 오차 출력
    return R_hat, weighted_errors # 근사 행렬 및 오차 반환

W = R > 0.0 # 미지항(선호도 정보가 존재하지 않는 항)이 아닐 경우 해당 항에 True 값이, 미지항일 경우 False 값이 저장됨
W[W == True] = 1 # 미지항이 아닐 경우 해당 항에 1 저장
W[W == False] = 0 # 미지항일 경우 해당 항에 0 저장
W = W.astype(np.float64, copy=False) # 유틸리티 행렬 R에 대한 가중치 행렬
R_hat, weighted_errors = singular_value_decomposition_using_weighted_alternating_least_squares(R, W, 5, 0.1, 100)

# 경사하강법을 이용한 특이값 분해 함수(R : 유틸리티 행렬, n_iter : 미지 행렬 X, Y의 갱신 횟수, lambda_ : 정규화 파라미터, learning_rate : 학습률, k : 요인 행렬 크기)
def singular_value_decomposition_using_gradient_descent(R, n_iter, lambda_, learning_rate, k):
    m, n = R.shape # 사용자 수 X 상품(영화) 수
    X = 5 * np.random.rand(m, k) # 선호도(별점(0 ~ 5))를 원소로 갖는 사용자 수 X 요인 행렬 크기 크기의 미지 행렬
    Y = 5 * np.random.rand(k, n) # 선호도(별점(0 ~ 5))를 원소로 갖는 요인 행렬 크기 X 상품(영화) 수 크기의 미지 행렬
    errors = [] # 오차(작을수록 예측값이 실제값과 비슷함)
    print('\n[Singular Value Decomposition(SVD) Using Gradient Descent(GD)]')
    for j in range(0, n_iter): # 설정한 갱신 횟수만큼 반복
        for u in range(m):
            for i in range(n):
                X[u,:] += learning_rate * ((R[u, i] - np.dot(X[u,:], Y[:,i])) * Y[:,i].T - lambda_ * X[u,:]) # L2 정규화 손실함수를 x에 대해서 미분한 식을 경사하강법에 적용한 값(행렬)
                Y[:,i] += learning_rate * ((R[u, i] - np.dot(X[u,:], Y[:,i])) * X[u,:].T - lambda_ * Y[:,i]) # L2 정규화 손실함수를 y에 대해서 미분한 식을 경사하강법에 적용한 값(행렬)
        errors.append(mean_squared_error(R, np.dot(X, Y))) # 두 행렬의 평균 제곱 편차 계산 후 오차 추가
        print('Error of %dst iteration : %f' % (j + 1, errors[j])) # 갱신에 따른 오차 출력
    R_hat = np.dot(X, Y) # 근사 행렬(XY) 저장
    print('The final Error : %f' % errors[-1]) # 최종 오차 출력
    return R_hat, errors # 근사 행렬 및 오차 반환

R_hat, errors = singular_value_decomposition_using_gradient_descent(R, 5, 1, 0.001, 100)

# 오차 평가를 위해 유틸리티 행렬을 학습데이터 행렬과 평가데이터 행렬로 나누는 함수
def train_test_split(R, n_test):
    train = R.copy() # 학습데이터 행렬(기존 유틸리티 행렬 복사)
    test = np.zeros(R.shape) # 평가데이터 행렬(유틸리티 행렬 크기의 영행렬)
    for user in range(R.shape[0]): # 유틸리티 행렬의 행 크기(사용자 수)만큼 반복
        test_index = np.random.choice(R[user,:].nonzero()[0], size=n_test, replace=False) # 유틸리티 행렬의 각 행에 있는 미지항이 아닌 항을 임의로 선택해서 인덱스 저장
        train[user, test_index] = 0 # 학습데이터 행렬의 해당 인덱스의 선호도를 0으로 설정
        test[user, test_index] = R[user, test_index] # 평가데이터 행렬의 해당 인덱스에 유틸리티 행렬의 실제 선호도 저장
    return train, test # 학습, 평가데이터 행렬 반환

iteration = 20 # 반복(갱신) 횟수
train, test = train_test_split(R, 10) # 학습, 평가데이터 행렬 저장
R_hat, train_errors = singular_value_decomposition_using_alternating_least_squares(train, iteration, 0.1, 100, train)
R_hat, test_errors = singular_value_decomposition_using_alternating_least_squares(train, iteration, 0.1, 100, test)
R_hat, modified_train_errors = singular_value_decomposition_using_alternating_least_squares(train, iteration, 50, 100, train)
R_hat, modified_test_errors = singular_value_decomposition_using_alternating_least_squares(train, iteration, 50, 100, test)

# 반복 횟수에 따른 학습, 평가데이터 오차 변화 플롯
plt.xlim(0, iteration)
plt.ylim(0, iteration)
plt.xlabel('Iteration')
plt.ylabel('Mean Squared Error')
plt.xticks(range(iteration), range(iteration))
train_plot, = plt.plot(range(iteration), train_errors, label='train_error')
test_plot, = plt.plot(range(iteration), test_errors, '--', label='test_error')
modified_train_plot, = plt.plot(range(iteration), modified_train_errors, label='modified_train_error')
modified_test_plot, = plt.plot(range(iteration), modified_test_errors, '--', label='modified_test_error')
plt.legend(handles=[train_plot, test_plot, modified_train_plot, modified_test_plot])
plt.show()

# 근사 행렬의 예측 선호도(별점)를 유틸리티 행렬의 실제 선호도(별점) 범위(0 ~ 5)로 설정하기 위한 작업
R_hat -= np.min(R_hat) # 근사 행렬의 가장 작은 값을 0으로 만들기 위해 근사 행렬의 전체 항의 값에서 가장 작은 값을 뺌
R_hat *= float(5) / np.max(R_hat) # 근사 행렬의 가장 큰 값을 5로 만들기 위해 근사 행렬의 전체 항의 값에서 가장 큰 값으로 5를 나눈 값을 곱함

# 근사 행렬을 이용해서 설정한 사용자가 본 영화와 비슷한 영화를 찾는 함수
def recommend_by_user(user_id):
    user_index = user_id - 1 # 설정한 사용자의 인덱스
    # enumerate 함수로 [(인덱스, 예측 선호도), ...] 리스트 생성 및 예측 선호도를 기준으로 내림차순 정렬(생성된 리스트의 첫 번째 인덱스가 설정한 사용자가 본 영화와 가장 비슷한 영화)
    user_seen_movies = sorted(list(enumerate(R_hat[user_index])), key=lambda x : x[1], reverse=True)
    print('\nJob : %s, Sex : %s, Age : %s' % (user_info_list[user_index][2], user_info_list[user_index][1], user_info_list[user_index][0])) # 설정한 사용자의 직업, 성별, 나이 출력
    recommend_count = 0
    for movie_info in user_seen_movies: # 설정한 사용자가 본 영화와 가장 비슷한 영화(본 영화 포함) 순으로 반복
        if W[user_id][movie_info[0]] == 0: # 설정한 사용자가 본 영화와 비슷한 영화 중 보지 않은 영화일 경우
            movie_title = item_info_list[int(movie_info[0] + 1)][0] # 설정한 사용자가 본 영화와 비슷한 영화 중 보지 않은 영화 제목 저장
            movie_score = movie_info[1] # 설정한 사용자가 본 영화와 비슷한 영화 중 보지 않은 영화 별점(예측 선호도) 저장
            print('%dst recommendation : %s(%.3f)' % (recommend_count + 1, movie_title, movie_score)) # 설정한 사용자가 본 영화와 비슷한 영화 중 보지 않은 영화 제목 및 별점(예측 선호도) 출력
            recommend_count += 1
            if recommend_count == 5: # 추천한 영화가 5개일 경우
                break

recommend_by_user(1)
recommend_by_user(100)

end_time1 = time.perf_counter()
end_time2 = time.process_time()
print('\nElapsed time : %.1f minute' % ((end_time1 - start_time1) / 60))
print('CPU process time : %.1f minute' % ((end_time2 - start_time2) / 60))