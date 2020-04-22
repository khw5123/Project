# -*- coding: utf-8 -*-
import os
import time
import unicodedata
from konlpy.tag import Okt
from gensim.models import Word2Vec

start_time1 = time.perf_counter()
start_time2 = time.process_time()

data_file = os.getcwd() + '\\processed_kowiki\\kowiki-latest-pages-articles.xml-01.txt' # 전처리된 위키백과 파일
save_file = os.getcwd() + '\\test_model.txt' # Word2Vec 학습 결과가 저장될 파일
corpus_list = list() # 말뭉치 리스트

okt = Okt() # KoNLPy 라이브러리의 형태소 분석 및 품사 태깅 클래스인 Okt 객체 생성
for line in open(data_file, 'r', encoding='utf-8'): # 전처리된 위키백과 파일의 한 라인씩 반복
    line = unicodedata.normalize('NFKC', line) # 깨지는 글자를 처리하기 위해 NFKC로 변환
    # 위키백과 파일에서 메타 정보는 [], {}, | 등의 특수문자로 시작하는데 word2vec 모델 학습 시 이런 정보는 필요 없으므로 제외 처리
    if line[0].isdigit(): # 해당 라인의 첫 글자가 숫자일 경우
        corpus_list.append(okt.nouns(line)) # Okt 객체의 nouns 메서드를 이용해서 해당 라인의 문장을 형태소로 분할하고 품사 정보를 부여한 뒤 품사가 명사인 단어들을 리스트 형식으로 반환. 반환된 리스트를 말뭉치 리스트에 추가
    elif ord(line[0]) >= ord('가') and ord(line[0]) <= ord('힇'): # 첫 글자가 한글일 경우(한글 유니코드 : 가 ~ 힇)
        corpus_list.append(okt.nouns(line)) # Okt 객체의 nouns 메서드를 이용해서 해당 라인의 문장을 형태소로 분할하고 품사 정보를 부여한 뒤 품사가 명사인 단어들을 리스트 형식으로 반환. 반환된 리스트를 말뭉치 리스트에 추가
    else:
        pass
print('# Number of lines in corpus : %d' % len(corpus_list)) # 말뭉치 리스트에 추가된 문장의 개수 출력

# word2vec 단어 임베딩 모델을 이용해서 학습 후 생성된 모델을 반환하는 함수
def train_word2vec(corpus_list, save_file):
    SG = 1 # 스킵-그램을 이용하여 학습
    EMBEDDING_SIZE = 200 # 단어 하나를 실수 200개로 표현
    WINDOW = 5 # 학습할 때 앞과 뒤 각 5개의 단어 이용
    MIN_COUNT = 5 # 전체 데이터에서 5번 이상 나온 단어만 사용
    WORKERS = 10 # 학습할 때 10개의 스레드 사용
    BATCH_SIZE = 10000 # 각 스레드에서 한 번의 학습에 10000개의 단어 사용
    ITER = 10 # 학습을 10번 반복
    # class gensim.models.word2vec.Word2Vec(sentences=None, size=100, alpha=0.025, window=5, min_count=5, max_vocab_size=None, sample=0.001, seed=1, workers=3, min_alpha=0.0001, sg=0, hs=0, negative=5, cbow_mean=1, hashfxn=<built-in function hash>, iter=5, null_word=0, trim_rule=None, sorted_vocab=1, batch_words=10000) : 단어 임베딩 클래스
    model = Word2Vec(corpus_list, sg=SG, size=EMBEDDING_SIZE, window=WINDOW, min_count=MIN_COUNT, workers=WORKERS, batch_words=BATCH_SIZE, iter=ITER) # word2vec 단어 임베딩 모델을 이용해서 학습
    model.init_sims(replace=True) # 메모리 정리
    # model.save(save_file) # 학습 결과 저장
    return model # 모델(학습 결과) 반환

model = train_word2vec(corpus_list, save_file) # word2vec 모델 학습 함수 호출

end_time1 = time.perf_counter()
end_time2 = time.process_time()
print('\nElapsed time : %.1f minute' % ((end_time1 - start_time1) / 60))
print('CPU process time : %.1f minute' % ((end_time2 - start_time2) / 60))

while True:
    try:
        sel = input('\n1. Single Similar\n2. Positive Negative Similar\n3. Exit\nSelect : ')
        if sel == '1':
            word = input('Input Word : ')
            for similar_word, similarity in model.most_similar(word, topn=10): # 입력받은 키워드와 가장 비슷한 임베딩을 가지는 단어 10개 출력
                print(similar_word, ' : ', similarity)
        elif sel == '2':
            positive_word = input('Input Positive Word : ')
            negative_word = input('Input Negative Word : ')
            for similar_word, similarity in model.most_similar(positive=[positive_words for positive_words in positive_word.split(' ')], negative=[negative_words for negative_words in negative_word.split(' ')], topn=10): # 설정한 키워드와 가장 비슷한 임베딩을 가지는 단어 10개 출력
                print(similar_word, ' : ', similarity)
        elif sel == '3':
            break
        else:
            print('[-] Input Error')
    except Exception as e:
        print('[-]', e)
        pass