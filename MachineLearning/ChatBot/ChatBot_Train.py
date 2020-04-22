# -*- coding: utf-8 -*-
import os
import re
import time
import math
import pickle
import tensorflow as tf
from collections import Counter

from seq2seq_model import Seq2SeqModel
from seq2seq_model import _PAD, _GO, _EOS, _UNK, PAD_ID, GO_ID, EOS_ID, UNK_ID, OP_DICT_IDS

def get_seq2seq_model(session, forward_only, dict_lengths, max_sentence_lengths, model_dir):
    model = Seq2SeqModel(
        source_vocab_size=dict_lengths[0],
        target_vocab_size=dict_lengths[1],
        buckets=[max_sentence_lengths],
        size=256,
        num_layers=2,
        max_gradient_norm=5.0,
        batch_size=128,
        learning_rate=1.0,
        learning_rate_decay_factor=0.99,
        forward_only=forward_only,
        dtype=tf.float16)
    ckpt = tf.train.get_checkpoint_state(model_dir)
    if ckpt and tf.train.checkpoint_exists(ckpt.model_checkpoint_path):
        print('[+] Loaded checkpoint {}'.format(ckpt.model_checkpoint_path))
        model.saver.restore(session, ckpt.model_checkpoint_path)
    else:
        session.run(tf.global_variables_initializer())
    return model

def train(data_set, max_sentence_lengths, dict_lengths, model_directory, model_checkpoints):
    with tf.Session() as sess:
        model = get_seq2seq_model(sess, False, dict_lengths, max_sentence_lengths, model_directory) # seq2seq 모델 객체
        step_time = 0.0 # 한 번의 반복에 걸린 학습 시간
        loss = 0.0 # 오차
        bucket = 0
        steps_per_checkpoint = 1 # 학습 기록 저장 주기
        current_step = 0 # 현재 반복 횟수
        max_steps = 20000 # 최대 반복 횟수
        while current_step < max_steps:
            start_time = time.time()
            encoder_inputs, decoder_inputs, target_weights = model.get_batch([data_set], bucket)
            _, step_loss, _ = model.step(sess, encoder_inputs, decoder_inputs, target_weights, bucket, False)
            step_time += (time.time() - start_time) / steps_per_checkpoint
            loss += step_loss / steps_per_checkpoint
            current_step += 1
            if current_step % steps_per_checkpoint == 0:
                perplexity = math.exp(float(loss)) if loss < 300 else float('inf')
                print ('global_step: {} | learning_rate: {} | step_time: {} | perplexity: {}'.format(model.global_step.eval(), model.learning_rate.eval(), step_time, perplexity))
                sess.run(model.learning_rate_decay_op)
                model.saver.save(sess, model_checkpoints, global_step=model.global_step)
                step_time, loss = 0.0, 0.0
                encoder_inputs, decoder_inputs, target_weights = model.get_batch([data_set], bucket)
                _, eval_loss, _ = model.step(sess, encoder_inputs, decoder_inputs, target_weights, bucket, True)

def prepare_sentences(sentences_l1, sentences_l2, len_l1, len_l2):
    data_set = []
    for i in range(len(sentences_l1)):
        padding_l1 = len_l1 - len(sentences_l1[i])
        pad_sentence_l1 = ([PAD_ID] * padding_l1) + sentences_l1[i]
        padding_l2 = len_l2 - len(sentences_l2[i])
        pad_sentence_l2 = [GO_ID] + sentences_l2[i] + [EOS_ID] + ([PAD_ID] * padding_l2)
        data_set.append([pad_sentence_l1, pad_sentence_l2])
    return data_set

def sentences_to_indexes(sentences, indexed_dictionary):
    indexed_sentences = []
    not_found_counter = 0
    for sent in sentences:
        idx_sent = []
        for word in sent:
            try:
                idx_sent.append(indexed_dictionary[word])
            except KeyError:
                idx_sent.append(UNK_ID)
                not_found_counter += 1
        indexed_sentences.append(idx_sent)
    # print('[sentences_to_indexes] Did not find {} words'.format(not_found_counter))
    return indexed_sentences

def create_indexed_dictionary(sentences, dict_size=10000, storage_path=None):
    count_words = Counter()
    dict_words = {}
    opt_dict_size = len(OP_DICT_IDS)
    for sen in sentences:
        for word in sen:
            count_words[word] += 1
    dict_words[_PAD] = PAD_ID
    dict_words[_GO] = GO_ID
    dict_words[_EOS] = EOS_ID
    dict_words[_UNK] = UNK_ID
    for idx, item in enumerate(count_words.most_common(dict_size)):
        dict_words[item[0]] = idx + opt_dict_size
    if storage_path:
        pickle.dump(dict_words, open(storage_path, 'wb'))
    return dict_words

def filter_sentence_length(sentences_l1, sentences_l2, min_len=0, max_len=20):
    filtered_sentences_l1, filtered_sentences_l2 = [], []
    for i in range(len(sentences_l1)):
        if min_len <= len(sentences_l1[i]) <= max_len and min_len <= len(sentences_l2[i]) <= max_len:
            filtered_sentences_l1.append(sentences_l1[i])
            filtered_sentences_l2.append(sentences_l2[i])
    return filtered_sentences_l1, filtered_sentences_l2

def clean_sentence(sentence):
    regex_splitter = re.compile("([!?.,:;$\"')( ])")
    clean_words = [re.split(regex_splitter, word.lower()) for word in sentence]
    return [w for words in clean_words for w in words if words if w]

def get_tokenized_sequencial_sentences(list_of_lines, line_text):
    for line in list_of_lines:
        for i in range(len(line) - 1):
            yield (line_text[line[i]].split(' '), line_text[line[i + 1]].split(' '))

def read_data(file_conversations, file_lines):
    with open(file_conversations, 'r', encoding='ISO-8859-1') as fp:
        conversations_chunks = [line.split(' +++$+++ ') for line in fp]
    conversations = [re.sub('[\[\]\']', '', el[3].strip()).split(', ') for el in conversations_chunks]
    with open(file_lines, 'r', encoding='ISO-8859-1') as fp:
        lines_chunks = [line.split(' +++$+++ ') for line in fp]
    lines = {line[0]: line[-1].strip() for line in lines_chunks}
    return tuple(zip(*list(get_tokenized_sequencial_sentences(conversations, lines))))

def build_dataset(file_conversations, file_lines, file_dict_l1, file_dict_l2, train_sentence_count=30000, train_sentence_length=20):
    sen_l1, sen_l2 = read_data(file_conversations, file_lines) # 가는 말, 오는 말
    clean_sen_l1 = [clean_sentence(s) for s in sen_l1][:train_sentence_count] # 소문자 변환 및 문장 분리
    clean_sen_l2 = [clean_sentence(s) for s in sen_l2][:train_sentence_count]
    filt_clean_sen_l1, filt_clean_sen_l2 = filter_sentence_length(clean_sen_l1, clean_sen_l2, max_len=train_sentence_length) # 문장 길이 제한
    if not os.path.exists(file_dict_l2):
        dict_l1 = create_indexed_dictionary(filt_clean_sen_l1, dict_size=10000, storage_path=file_dict_l1) # 문장 빈도순으로 인덱싱
        dict_l2 = create_indexed_dictionary(filt_clean_sen_l2, dict_size=10000, storage_path=file_dict_l2)
    else:
        dict_l1 = pickle.load(open(file_dict_l1, 'rb'))
        dict_l2 = pickle.load(open(file_dict_l2, 'rb'))
    dict_l1_length = len(dict_l1)
    dict_l2_length = len(dict_l2)
    idx_sentences_l1 = sentences_to_indexes(filt_clean_sen_l1, dict_l1) # 문장 인덱스로 구성된 리스트
    idx_sentences_l2 = sentences_to_indexes(filt_clean_sen_l2, dict_l2)
    max_length_l1 = max([len(sentence) for sentence in idx_sentences_l1])
    max_length_l2 = max([len(sentence) for sentence in idx_sentences_l2])
    data_set = prepare_sentences(idx_sentences_l1, idx_sentences_l2, max_length_l1, max_length_l2) # 문장 형식 구성    
    return (filt_clean_sen_l1, filt_clean_sen_l2), data_set, (max_length_l1, max_length_l2), (dict_l1_length, dict_l2_length)

def main():
    file_conversations = os.getcwd() + '\\cornell_movie_dialogs_corpus\\movie_conversations.txt'
    file_lines = os.getcwd() + '\\cornell_movie_dialogs_corpus\\movie_lines.txt'
    file_dict_l1 = os.getcwd() + '\\l1_dict.p'
    file_dict_l2 = os.getcwd() + '\\l2_dict.p'
    model_directory = os.path.join(os.getcwd(), 'model')
    if not os.path.exists(model_directory):
        os.makedirs(model_directory)
    model_checkpoints = model_directory + '\\chatbot.ckpt'
    _, data_set, max_sentence_lengths, dict_lengths = build_dataset(file_conversations, file_lines, file_dict_l1, file_dict_l2, train_sentence_count=30000, train_sentence_length=10)
    train(data_set, max_sentence_lengths, dict_lengths, model_directory, model_checkpoints)

if __name__ == '__main__':
    main()