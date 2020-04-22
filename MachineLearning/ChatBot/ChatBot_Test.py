# -*- coding: utf-8 -*-
import os
import pickle
import numpy as np
import tensorflow as tf

import ChatBot_Train
from seq2seq_model import EOS_ID

def prepare_sentence(sentence, dict_l1, max_length):
    sents = [sentence.split(' ')]
    clean_sen_l1 = [ChatBot_Train.clean_sentence(s) for s in sents]
    idx_sentences_l1 = ChatBot_Train.sentences_to_indexes(clean_sen_l1, dict_l1)
    data_set = ChatBot_Train.prepare_sentences(idx_sentences_l1, [[]], max_length, max_length)
    sentences = (clean_sen_l1, [[]])
    return sentences, data_set

def decode(sentences, data_set, dict_lengths, max_sentence_lengths, inv_dict_l2, model_directory):
    with tf.Session() as sess:
        model = ChatBot_Train.get_seq2seq_model(sess, True, dict_lengths, max_sentence_lengths, model_directory)
        model.batch_size = 1
        bucket = 0
        encoder_inputs, decoder_inputs, target_weights = model.get_batch({bucket: [(data_set[0][0], [])]}, bucket)
        _, _, output_logits = model.step(sess, encoder_inputs, decoder_inputs, target_weights, bucket, True)
        outputs = [int(np.argmax(logit, axis=1)) for logit in output_logits]
        if EOS_ID in outputs:
            outputs = outputs[1:outputs.index(EOS_ID)]
        return ' '.join(sentences[0][0]), ' '.join([tf.compat.as_str(inv_dict_l2[output]) for output in outputs])

def main():
    file_dict_l1 = os.getcwd() + '\\l1_dict.p'
    file_dict_l2 = os.getcwd() + '\\l2_dict.p'
    model_directory = os.path.join(os.getcwd(), 'model')
    dict_l1 = pickle.load(open(file_dict_l1, 'rb'))
    dict_l1_length = len(dict_l1)
    dict_l2 = pickle.load(open(file_dict_l2, 'rb'))
    dict_l2_length = len(dict_l2)
    inv_dict_l2 = {v: k for k, v in dict_l2.items()}
    max_lengths = 10
    while True:
        sentence = input('\nInput : ')
        sentences, data_set = prepare_sentence(sentence, dict_l1, max_lengths)
        dict_lengths = (dict_l1_length, dict_l2_length)
        max_sentence_lengths = (max_lengths, max_lengths)
        input_sentence, output_sentence = decode(sentences, data_set, dict_lengths, max_sentence_lengths, inv_dict_l2, model_directory)
        tf.reset_default_graph() # 그래프 초기화
        os.system('cls')
        print('\nInput :', input_sentence, '\nOutput :', output_sentence)

if __name__ == '__main__':
    main()