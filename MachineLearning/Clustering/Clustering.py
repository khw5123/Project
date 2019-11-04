# -*- coding: utf-8 -*-
import time
import random
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from scipy.cluster.hierarchy import linkage
from scipy.cluster.hierarchy import dendrogram
from sklearn.cluster import AgglomerativeClustering

start_time1 = time.perf_counter()
start_time2 = time.process_time()

# 1. 데이터 전처리(user_product_dic, product_id_name_dic, id_product_dic, id_user_dic, user_product_vec_li)
print('\n--------------------- 1. Preprocessing ---------------------')
user_product_dic = dict() # {구매자 ID : {상품 코드1, 상품 코드2, ...}}
product_user_dic = dict() # {상품 코드 : {구매자 ID1, 구매자 ID2, ...}}
product_id_name_dic = dict() # {상품 코드 : 상품명}

fp = open('online_retail_utf.txt', 'r') # 온라인 상거래 데이터셋 오픈
for line in fp.readlines():
    line_items = line.strip().split('\t')
    user_code = line_items[6] # 구매자 ID 저장
    product_id = line_items[1] # 상품 코드 저장
    product_name = line_items[2] # 상품명 저장
    if len(user_code) == 0: # 구매자 ID가 없는 경우
        continue
    country = line_items[7] # 상품을 구매한 국가 저장
    if country != 'United Kingdom': # 영국에서 구매하지 않았을 경우
        continue
    try:
        invoice_year = time.strptime(line_items[4], '%Y-%m-%d %H:%M').tm_year # 청구일 저장
    except ValueError:
        continue
    if invoice_year != 2011: # 구매가 2011년에 발생하지 않았을 경우
        continue
    user_product_dic.setdefault(user_code, set()) # 구매자 ID를 키로, 값을 빈 집합으로 저장
    user_product_dic[user_code].add(product_id) # 상품 코드를 값으로 추가 {구매자 ID : {상품 코드1, 상품 코드2, ...}}
    product_user_dic.setdefault(product_id, set()) # 상품 코드를 키로, 값을 빈 집합으로 저장
    product_user_dic[product_id].add(user_code) # 구매자 ID를 값으로 추가 {상품 코드 : {구매자 ID1, 구매자 ID2, ...}}
    product_id_name_dic[product_id] = product_name # {상품 코드 : 상품명}
fp.close()
product_per_user_li = [len(x) for x in user_product_dic.values()] # 구매자가 구매한 상품의 가짓수로 리스트 생성
print('# Number of users : %d' % len(user_product_dic)) # 구매자 수 출력
print('# Number of products : %d' % len(product_user_dic)) # 구매한 상품 가짓수 출력
# scipy.stats.describe(a, axis=0, ddof=1, bias=True, nan_policy='propagate') : 데이터 기초 통계량을 계산하는 함수
print(stats.describe(product_per_user_li)) # min : 구매한 상품의 최소 가짓수(리스트에 있는 값의 최솟값), max : 구매한 상품의 최대 가짓수(리스트에 있는 값의 최댓값), mean : 구매한 상품의 평균 가짓수(리스트에 있는 값을 모두 더하고 리스트의 길이로 나눈 값)

# 구매한 상품 가짓수에 따른 구매자 수 시각화
plot_data_all = Counter(product_per_user_li)
plot_data_x = list(plot_data_all.keys())
plot_data_y = list(plot_data_all.values())
plt.xlabel('Number of products')
plt.ylabel('Number of users')
plt.scatter(plot_data_x, plot_data_y, marker='+')
plt.show()

# 군집화 노이즈 제거(1 < 구매한 상품 가짓수 <= 600 인 경우를 제외하고 노이즈로 설정)
min_product_user_li = [k for k, v in user_product_dic.items() if len(v) == 1] # 구매한 상품의 가짓수가 1인 구매자의 구매자 ID로 리스트 생성
max_product_user_li = [k for k, v in user_product_dic.items() if len(v) >= 600] # 구매한 상품의 가짓수가 600 이상인 구매자의 구매자 ID로 리스트 생성
print('# Number of users purchased one product : %d' % (len(min_product_user_li))) # 한 가지 상품만 구매한 구매자의 수 출력
print('# Number of users purchased more than 600 product : %d' % (len(max_product_user_li))) # 600개 이상의 상품을 구매한 구매자의 수 출력
user_product_dic = {k:v for k, v in user_product_dic.items() if len(v) > 1 and len(v) <= 600} # 노이즈(한 가지 상품만 구매했거나, 600개 이상의 상품을 구매한 경우)를 제거한 딕셔너리 재생성 {구매자 ID : {상품 코드1, 상품 코드2, ...}}
print('# Number of left users : %d' % (len(user_product_dic))) # 노이즈를 제거하고 남은 구매자 수 출력

id_product_dic = dict() # {상품 코드 : 상품 고유 ID(0, 1, 2, ...)}
for product_set_li in user_product_dic.values(): # product_set_li = {상품 코드1, 상품 코드2, ...}
    for x in product_set_li:
        if x not in id_product_dic: # 리스트에 상품 코드가 저장되어 있지 않을 경우
            id_product_dic.setdefault(x, len(id_product_dic)) # {상품 코드 : 상품 고유 ID(0, 1, 2, ...)}
print('# Number of left items : %d' % (len(id_product_dic))) # 노이즈를 제거하고 남은 상품 가짓수 출력

id_user_dic = dict() # {구매자 고유 인덱스 : 구매자 ID}
user_product_vec_li = [] # 구매자가 구매한 상품 목록이 저장되어 있는 리스트(2차원 배열)로 군집화의 입력으로 사용됨(행 : 구매자, 열 : 구매한 상품 목록, 구매자가 상품을 구매했을 경우 해당 위치의 값이 1로 설정되고, 구매하지 않았을 경우 0으로 설정됨(원-핫 인코딩))
all_product_count = len(id_product_dic) # 구매한 상품 가짓수로 원-핫 인코딩으로 변환할 피처의 가짓수
for user_code, product_per_user_set in user_product_dic.items(): # user_code = 구매자 ID, product_per_user_set = {상품 코드1, 상품 코드2, ...}
    user_product_vec = [0] * all_product_count # 구매한 상품 가짓수를 길이로 하는 한 명의 구매자 리스트 임시 저장(user_product_vec == user_product_vec_li 리스트의 한 행)
    id_user_dic[len(id_user_dic)] = user_code # {구매자 고유 인덱스 : 구매자 ID}
    for product_name in product_per_user_set:
        user_product_vec[id_product_dic[product_name]] = 1 # 구매자가 구매한 상품 코드를 id_product_dic 딕셔너리의 키로 설정해서 얻은 상품 고유 ID를 user_product_vec 리스트의 인덱스로 설정해서 해당 인덱스의 값을 1로 설정(구매자가 구매한 상품의 위치의 값을 1로 설정(원-핫 인코딩))
    user_product_vec_li.append(user_product_vec) # 처리된 한 명의 구매자 리스트를 user_product_vec_li 리스트의 한 행으로 추가
# print(user_product_vec_li[1])
# print(user_product_vec_li[2])

# 2. 클러스터 수 K 설정
# 2-1. 정량적 평가 - 실루엣 계수
print('\n--- 2-1. Quantitative Evaluation - Silhouette Coefficient ---')
tmp_test_data = np.array(user_product_vec_li) # 군집화 입력 데이터
cluster_max_count = 9
for k in range(2, cluster_max_count): # 클러스터 수를 2부터 cluster_max_count까지 변경하며 실루엣 계수의 평균값 확인
    km = KMeans(n_clusters=k).fit(tmp_test_data)
    # 샘플의 평균 실루엣 계수(-1 ~ 1)가 1에 가까울수록 그 샘플은 자신이 속한 클러스터와 유사하다는 의미(클러스터에 속한 샘플들이 밀접하게 모여있다는 의미)이므로 1에 가까운 적절한 클러스터의 개수를 설정해야 함(클러스터의 개수가 2일 때 가장 크고 이후에는 차이가 별로 없으므로 적절한 클러스터의 수는 2임)
    print('# Number of cluster : %d, Silhouette Coefficient : %.3f' % (k, silhouette_score(tmp_test_data, km.labels_))) # 가장 높은 평균 실루엣 계수가 0.3 정도로 1에 가깝지 않음(좋지 않은 군집화). 뚜렷이 구분되는 구매자 클러스터를 만들려면 구매한 상품(군집화 입력 데이터)만으로는 정보가 부족하다고 볼 수 있음

# 2-2. 정량적 평가 - 엘보 방법
print('\n-------- 2-2. Quantitative Evaluation - Elbow Method --------')
ssw_dic = dict() # {클러스터 수 : 급내제곱합의 평균값}
tmp_test_data = np.array(user_product_vec_li) # 군집화 입력 데이터
cluster_max_count = 8
for k in range(1, cluster_max_count): # 클러스터 수를 1부터 cluster_max_count까지 변경하며 급내제곱합의 평균값 저장
    km = KMeans(n_clusters=k).fit(tmp_test_data)
    ssw_dic[k] = km.inertia_ # 클러스터 수가 k 일 때의 급내제곱합의 평균값 저장
# 클러스터 수 K에 따른 급내제곱합의 변화 시각화
plot_data_x = list(ssw_dic.keys()) # X축 : 클러스터 수 K
plot_data_y = list(ssw_dic.values()) # Y축 : 급내제곱합의 평균값
plt.xlabel('# Number of cluusters')
plt.ylabel('within ss')
plt.plot(plot_data_x, plot_data_y, linestyle='-', marker='o')
plt.show() # 급내제곱합의 기울기(변화율)가 클수록 그 샘플은 자신이 속한 클러스터와 유사하다는 의미(클러스터에 속한 샘플들이 밀접하게 모여있다는 의미)이므로 급내제곱합의 변화율(기울기)에 따라 적절한 클러스터의 개수를 설정해야 함(클러스터의 개수가 1 ~ 2 사이에서 기울기가 가장 크고 이후에는 차이가 별로 없으므로 적절한 클러스터의 수는 2임)

# 2-3. 정성적 평가 - 같은 클러스터에 속한 구매자가 구매한 상품의 경향 확인
print('\n---------------- 2-3. Qualitative evaluation ----------------')
# 각 클러스터에 속한 구매자가 구매한 상품의 상품명에 나타나는 단어 중 자주 나타나는 단어 20개와 그 빈도수를 출력하는 함수
def analyze_clusters_keywords(labels, product_id_name_dic, user_product_dic, id_user_dic): # 파라미터 : KMeans 클래스의 fit 함수 결과로 얻은 lables_ 값, {상품 코드 : 상품명}, {구매자 ID : {상품 코드1, 상품 코드2, ...}}, {구매자 고유 인덱스 : 구매자 ID}
    print('{Cluster ID: Number of users} : ', end='')
    print(Counter(labels)) # 각 클러스터의 ID와 클러스터에 들어 있는 구매자 수 출력
    cluster_item = dict() # {클러스터 ID : [상품명1, 상품명2, ...]}
    for i in range(0, len(labels)):
        cluster_item.setdefault(labels[i], []) # 클러스터 ID를 키로, 값을 공백 리스트로 저장
        for x in user_product_dic[id_user_dic[i]]: # x = 상품 코드
            cluster_item[labels[i]].extend([product_id_name_dic[x]]) # 상품명을 값으로 추가 {클러스터 ID : [상품명1, 상품명2, ...]}
    for cluster_id, product_name in cluster_item.items():
        bigram = []
        product_name_keyword = (' ').join(product_name).replace(' OF ', ' ').split() # 상품명 리스트를 하나의 문자열로 만들고, 스톱워드(의미 없는 단어)를 공백으로 바꾼 뒤 스페이스나 탭으로 분해해서 저장
        for i in range(0, len(product_name_keyword) - 1):
            bigram.append(' '.join(product_name_keyword[i : i + 2]))
        print('Cluster ID :', cluster_id) # 클러스터 ID 출력
        print(Counter(bigram).most_common(20)) # 각 클러스터에 속한 구매자가 구매한 상품의 상품명에 나타나는 단어 중 자주 나타나는 단어 20개를 빈도순으로 출력
tmp_test_data = np.array(user_product_vec_li) # 군집화 입력 데이터
km = KMeans(n_clusters=2, n_init=10, max_iter=20).fit(tmp_test_data) # 입력 데이터를 군집화하여 2개의 클러스터 생성 후 결과 저장
analyze_clusters_keywords(km.labels_, product_id_name_dic, user_product_dic, id_user_dic) # 함수 실행

# 각 클러스터에 속한 구매자가 구매한 상품 가짓수의 기초 통계량을 출력하는 함수
def analyze_clusters_product_count(labels, user_product_dic, id_user_dic): # 파라미터 : KMeans 클래스의 fit 함수 결과로 얻은 lables_ 값, {구매자 ID : {상품 코드1, 상품 코드2, ...}}, {구매자 고유 인덱스 : 구매자 ID}
    print('\n{Cluster ID: Number of users} : ', end='')
    print(Counter(labels)) # 각 클러스터의 ID와 클러스터에 들어 있는 구매자 수 출력
    product_len_dic = dict() # {클러스터 ID : 구매한 상품 가짓수}
    for i in range(0, len(labels)):
        product_len_dic.setdefault(labels[i], []) # 클러스터 ID를 키로, 값을 공백 리스트로 저장
        product_len_dic[labels[i]].append(len(user_product_dic[id_user_dic[i]])) # 구매자가 구매한 상품 가짓수를 값으로 추가 {클러스터 ID : 구매한 상품 가짓수}
    for cluster_id, product_count in product_len_dic.items():
        print('Cluster ID :', cluster_id) # 클러스터 ID 출력
        print(stats.describe(product_count)) # 각 클러스터에 속한 구매자가 구매한 상품 가짓수의 기초 통계량 출력
tmp_test_data = np.array(user_product_vec_li) # 군집화 입력 데이터
km = KMeans(n_clusters=2, n_init=10, max_iter=20).fit(tmp_test_data) # 입력 데이터를 군집화하여 2개의 클러스터 생성 후 결과 저장
analyze_clusters_product_count(km.labels_, user_product_dic, id_user_dic) # 함수 실행

# 3. K-평균 군집화
print('\n------------------- 3. K-Means Clustering -------------------')
random.shuffle(user_product_vec_li) # 학습용 데이터와 평가용 데이터로 나누기 위해 입력 데이터(원-핫 인코딩 적용된 리스트) 셔플
train_data = user_product_vec_li[:2500] # 학습용 데이터에 구매자 2500명 저장
test_data = user_product_vec_li[2500:] # 평가용 데이터에 나머지 구매자 저장
print('# Number of train data : %d' % len(train_data)) # 학습용 데이터 개수 출력
print('# Number of test data : %d' % len(test_data)) # 평가용 데이터 개수 출력
# sklearn.cluster.KMeans(n_clusters=8, init='k-means++', n_init=10, max_iter=300, tol=0.0001, precompute_distances='auto', verbose=0, random_state=None, copy_x=True, n_jobs=1) : K-평균 군집화 클래스
km_predict = KMeans(n_clusters=2, init='k-means++', n_init=10, max_iter=20).fit(train_data) # 학습 데이터를 군집화하여 2개의 클러스터 생성 후 결과 저장
# sklearn.cluster.KMeans.predict(X) : 새로운 샘플이 학습 데이터를 이용하여 생성된 클러스터 중 어디에 속하는지 예측하는 함수로, 인자 X(2차원 배열의 새로운 데이터) 안의 샘플이 속하는 클러스터 ID를 리스트로 반환함
km_predict_result = km_predict.predict(test_data) # 평가 데이터가 생성된 2개의 클러스터 중 어디에 속하는지를 리스트로 저장
print(km_predict_result) # 결과 출력

# 4. 계층적 군집화 - 집괴적 군집화
print('\n--------- 4. Hierarchical Clustering - Agglomerative ---------')
# 4-1. 싸이파이의 집괴적 군집화 클래스를 이용
# scipy.cluster.hierarchy.linkage(y, method='single', metric='euclidean') : 집괴적 군집화 클래스
row_clusters = linkage(test_data, method='complete', metric='euclidean') # 유사도(거리) 측정 방법으로 완전 연결법, 거리 함수로 유클리디안 함수를 사용해서 집괴적 군집화
tmp_label = [] # 구매자 ID가 저장될 리스트
for i in range(0, len(id_user_dic)):
    tmp_label.append(id_user_dic[i]) # 구매자 ID 추가
# 샘플들이 군집화를 이루는 양상을 시각화(계통 트리(덴드로그램))
plt.figure(figsize=(100, 20))
# scipy.cluster.hierarchy.dendrogram(Z, p=30, truncate_mode=None, color_threshold=None, get_leaves=True, oridentation='top', labels=None, count_sort=False, distance_sort=False, show_leaf_counts=True, no_plot=False, no_labels=False, leaf_font_size=None, leaf_rotation=None, leaf_label_func=None, show_contracted=False, link_color_func=None, ax=None, above_threshold_color='b') : scipy.cluster.hierarchy.linkage 클래스 객체를 이용하여 샘플들이 군집화를 이루는 양상을 시각화하는 함수
row_denr = dendrogram(row_clusters, labels=tmp_label) # X축 : 구매자 ID, Y축 : 유사도(거리) 계산법을 완전 연결 방법으로 하여 측정한 클러스터 간의 유클리드 거리
plt.tight_layout()
plt.xlabel('User ID')
plt.ylabel('Euclidean Distance')
plt.show() # 계통 트리(덴드로그램)를 적절한 유클리드 거리에서 가로로 끊으면 유사도에 따른 여러 그룹으로 나눠짐

# 데이터의 일부만 이용하여 집괴적 군집화
user_count = 100 # 일부 구매자 수
small_test_data = np.array(random.sample(user_product_vec_li, user_count)) # 구매자의 일부만 이용하여 입력 데이터 생성
small_row_clusters = linkage(small_test_data, method='complete', metric='euclidean') # 유사도(거리) 측정 방법으로 완전 연결법, 거리 함수로 유클리디안 함수를 사용해서 집괴적 군집화
# 샘플들이 군집화를 이루는 양상을 시각화(계통 트리(덴드로그램))
plt.figure(figsize=(25, 10))
row_denr = dendrogram(small_row_clusters, labels=list(range(len(small_test_data))), leaf_font_size=20) # X축 : 구매자 ID, Y축 : 유사도(거리) 계산법을 완전 연결 방법으로 하여 측정한 클러스터 간의 유클리드 거리
plt.tight_layout()
plt.xlabel('User ID')
plt.ylabel('Euclidean Distance')
plt.show() # 계통 트리(덴드로그램)를 적절한 유클리드 거리에서 가로로 끊으면 유사도에 따른 여러 그룹으로 나눠짐

# 4-2. 사이킷런의 집괴적 군집화 클래스를 이용
tmp_test_data = np.array(user_product_vec_li) # 군집화 입력 데이터
# class sklearn.cluster.AgglomerativeClustering(n_clusters=2, affinity='euclidean', memory=Memory(cachedir=None), connectivity=None, n_components=None, compute_full_tree='auto', linkage='ward', pooling_func=<function mean>) : 집괴적 군집화 클래스
ward = AgglomerativeClustering(n_clusters=2, affinity='euclidean', linkage='ward').fit(tmp_test_data) # 클러스터 수 및 유사도(거리) 계산법을 설정하여 집괴적 군집화
analyze_clusters_keywords(ward.labels_, product_id_name_dic, user_product_dic, id_user_dic) # 함수 실행

end_time1 = time.perf_counter()
end_time2 = time.process_time()
print('\nElapsed time : %.1f minute' % ((end_time1 - start_time1) / 60))
print('CPU process time : %.1f minute' % ((end_time2 - start_time2) / 60))