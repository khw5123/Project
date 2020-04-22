# -*- coding: utf-8 -*-
import os
import operator
from nltk.tag import StanfordPOSTagger
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
'''
import nltk
nltk.download('punkt')
'''
# https://nlp.stanford.edu/software/tagger.shtml#Download
STANFORD_POS_MODEL_PATH = os.getcwd() + '\\stanford-postagger-full-2018-10-16\\models\\english-bidirectional-distsim.tagger'
STANFORD_POS_JAR_PATH = os.getcwd() + '\\stanford-postagger-full-2018-10-16\\stanford-postagger-3.9.2.jar'
# https://nlp.stanford.edu/software/CRF-NER.shtml#Download
STANFORD_NER_CLASSIFER_PATH = os.getcwd() + '\\stanford-ner-2018-10-16\\classifiers\\english.muc.7class.distsim.crf.ser.gz'
STANFORD_NER_JAR_PATH = os.getcwd() + '\\stanford-ner-2018-10-16\\stanford-ner-3.9.2.jar'

pos_tagger = StanfordPOSTagger(STANFORD_POS_MODEL_PATH, STANFORD_POS_JAR_PATH) # POS 객체 생성
ner_tagger = StanfordNERTagger(STANFORD_NER_CLASSIFER_PATH, STANFORD_NER_JAR_PATH) # NER 객체 생성

# https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
part_of_speech_dict = {'CC':'Coordinating conjunction (등위접속사)', 'CD':'Cardinal number (숫자)', 'DT':'Determiner (한정사)', 'EX':'Existential there (유도부사)', 'FW':'Foreign word (외래어)', 'IN':'Preposition or subordinating conjunction (전치사 or 종속절접속사)', 'JJ':'Adjective (형용사)', 'JJR':'Adjective, comparative (비교급형용사)', 'JJS':'Adjective, superlative (최상급형용사)',
                       'LS':'List item marker', 'MD':'Modal (법조동사)', 'NN':'Noun, singular or mass (단수명사)', 'NNS':'Noun, plural (복수명사)', 'NNP':'Proper noun, singular (단수고유명사)', 'NNPS':'Proper noun, plural (복수고유명사)', 'PDT':'Predeterminer (전치한정사)', 'POS':'Possessive ending', 'PRP':'Personal pronoun (인칭대명사)',
                       'PRP$':'Possessive pronoun (소유대명사)', 'RB':'Adverb (부사)', 'RBR':'Adverb, comparative (비교급부사)', 'RBS':'Adverb, superlative (최상급부사)', 'RP':'Particle', 'SYM':'Symbol', 'TO':'to', 'UH':'Interjection (감탄사)', 'VB':'Verb, base form (동사기본형)',
                       'VBD':'Verb, past tense (동사과거형)', 'VBG':'Verb, gerund or present participle (동명사 or 현재분사)', 'VBN':'Verb, past participle (과거분사)', 'VBP':'Verb, non-3rd person singular present (Non-3인칭단수동사)', 'VBZ':'Verb, 3rd person singular present (3인칭단수동사)', 'WDT':'Wh-determiner (복합관계한정사)', 'WP':'Wh-pronoun (복합관계대명사)', 'WP$':'Possessive wh-pronoun (복합관계소유대명사)', 'WRB':'Wh-adverb (복합관계부사)'}
part_of_speech_list = sorted(part_of_speech_dict.items(), key=operator.itemgetter(0))
print('======================================================================')
for abbreviation, part_of_speech in part_of_speech_list:
    print(abbreviation, ':', part_of_speech)
print('======================================================================')

text = 'One day in November 2016, the two authors of this book, Seungyuon and Youngjoo, had a coffee at Red Rock cafe, which is very popular place in Mountain View.' # 테스트 문장
tokens = word_tokenize(text) # 문장 내 단어들(토큰)
print('\nToken :', tokens)
print('\nPOS Tagging :', pos_tagger.tag(tokens)) # 품사 태깅
print('\nNER Tagging :', ner_tagger.tag(tokens)) # 고유명사 추출