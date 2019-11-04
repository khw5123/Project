# -*- coding: utf-8 -*-
import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report, f1_score
import matplotlib.pyplot as plt

def read_data(csv_file):
    image_data, label = [], []
    with open(csv_file, 'r') as fp:
        for line in fp.readlines():
            image_file = line.split(';')[0]
            image_number = line.split('\\')[-1].split(';')[-1]
            image_data.append(cv2.imread(image_file, cv2.COLOR_BGR2GRAY)) # 이미지 데이터
            label.append(int(image_number)) # 레이블
    return np.array(image_data), np.array(label) # 이미지 데이터와 레이블 반환

def create_train_test_data(image_data, label): # 학습, 평가 데이터셋 분리 함수
    n_samples, image_height, image_width = image_data.shape # 이미지 데이터 수, 이미지 세로 크기, 이미지 가로 크기
    print('\nImage Count : %d\nImage Width : %dpx\nImage Height : %dpx' % (n_samples, image_width, image_height))
    X = image_data.reshape(n_samples, -1) # 가로 픽셀 강도벡터와 세로 픽셀 강도벡터를 이어서 하나의 벡터 생성
    n_features = X.shape[1] # 피처 크기(이미지 세로 크기 x 이미지 가로 크기)
    y = label # 레이블
    n_classes = len(set(y)) # 클래스(인물) 수
    print('Feature Count : %d\nClass(Person) Count : %d' % (n_features, n_classes))
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42) # 학습, 평가 데이터셋 분리
    print('Train Image Count : %d\nTest Image Count : %d\n' % (X_train.shape[0], X_test.shape[0]))
    return X_train, X_test, y_train, y_test, image_width, image_height # 학습, 평가 데이터셋 반환

def extract_features(X_train, X_test, n_eigenface, image_width, image_height): # 주성분 분석을 통한 피처 생성 함수
    pca = PCA(n_components=n_eigenface, svd_solver='randomized', whiten=True).fit(X_train) # 주성분 분석
    eigenface = pca.components_.reshape((n_eigenface, image_height, image_width)) # 주성분을 원래 이미지와 같은 차원으로 변경
    return pca.transform(X_train), pca.transform(X_test), eigenface # 학습, 평가 데이터셋 피처 반환

def train_test_classifer(X_train_pca, X_test_pca, y_train, y_test): # 모델 학습 및 성능 평가 함수
    param_grid = {'C': [1e3, 5e3, 1e4, 5e4, 1e5], 'gamma': [0.0001, 0.0005, 0.001, 0.005, 0.01, 0.1]} # {파라미터명: 파라미터값}
    clf = GridSearchCV(SVC(kernel='rbf', class_weight='balanced'), param_grid).fit(X_train_pca, y_train) # 서포트 벡터 머신으로 모델 학습 후 모델 성능 평가를 통해 가장 좋은 성능의 모델 추출
    print('[Best Model]\n', clf.best_estimator_)
    y_pred = clf.predict(X_test_pca)
    print(classification_report(y_test, y_pred))

def visualize(image, n_col=5): # 고유 얼굴 시각화 함수
    n_row = round(image.shape[0] / n_col)
    plt.figure(figsize=(1.8 * n_col, 2.4 * n_row))
    plt.subplots_adjust(bottom=0.1, left=0.01, right=0.99, top=0.90, hspace=0.35)
    for i in range(n_row * n_col):
        plt.subplot(n_row, n_col, i + 1)
        plt.imshow(image[i], cmap='gray')
        plt.xticks(())
        plt.yticks(())
    plt.show()

def visualize2(X_train, X_test, y_train, y_test): # 고유 얼굴 수에 따른 성능 변화 시각화 함수
    f1_score_list, n_eigenface_list = [], []
    for n_eigenface in range(10, 110, 10): # 고유 얼굴 수를 10 ~ 100 사이의 10의 배수로 설정하여 반복
        pca = PCA(n_components=n_eigenface, svd_solver='randomized', whiten=True).fit(X_train) # 주성분 분석
        X_train_pca, X_test_pca = pca.transform(X_train), pca.transform(X_test) # 학습, 평가 데이터셋 피처
        param_grid = {'C': [1e3, 5e3, 1e4, 5e4, 1e5], 'gamma': [0.0001, 0.0005, 0.001, 0.005, 0.01, 0.1]} # {파라미터명: 파라미터값}
        clf = GridSearchCV(SVC(kernel='rbf', class_weight='balanced'), param_grid).fit(X_train_pca, y_train) # 서포트 벡터 머신으로 모델 학습 후 모델 성능 평가를 통해 가장 좋은 성능의 모델 추출
        y_pred = clf.predict(X_test_pca)
        f1_score_list.append(f1_score(y_test, y_pred, average='weighted')) # 리스트에 f1-score 추가
        n_eigenface_list.append(n_eigenface) # 리스트에 고유 얼굴 수 추가
    plt.plot(n_eigenface_list, f1_score_list)
    plt.xlabel('n_eigenface')
    plt.ylabel('f1-score')
    plt.show()

def main():
    image_data, label = read_data(os.getcwd() + '\\faces.csv') # 이미지 데이터와 레이블 저장
    X_train, X_test, y_train, y_test, image_width, image_height = create_train_test_data(image_data, label) # 학습, 평가 데이터셋 분리
    n_eigenface = 10 # 추출할 고유 얼굴 수
    X_train_pca, X_test_pca, eigenface = extract_features(X_train, X_test, n_eigenface, image_width, image_height) # 주성분 분석 후 생성된 학습, 평가 데이터셋 피처 반환
    train_test_classifer(X_train_pca, X_test_pca, y_train, y_test) # 모델 학습 및 성능 평가
    visualize(eigenface) # 고유 얼굴 시각화
    visualize2(X_train, X_test, y_train, y_test) # 고유 얼굴 수에 따른 성능 변화 시각화

if __name__ == '__main__':
    main()