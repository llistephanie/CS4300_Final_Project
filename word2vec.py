import gensim
import logging
import os
import json
import re
from gensim.test.utils import common_texts, get_tmpfile
from gensim.models import Word2Vec
from gensim.models import KeyedVectors
from itertools import islice
from gensim.parsing.preprocessing import remove_stopwords
from gensim.models.phrases import Phrases, Phraser
from spacy.lang.en.stop_words import STOP_WORDS
from nltk import tokenize

logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# pth = "./word2vec.model-yelp2"
bigram_pth = "./word2vec.model-bigrams"
# pth="/Users/shirleykabir/Desktop/cs4300sp2020-sc2524-kyh24-rdz26-sk2279-szk4/word2vec.model" # just our data

class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname), encoding="ISO-8859-1"):
                reg = re.compile(r'[a-z]+')
                # clean sentence
                sentence = line.lower().strip()
                sentence = re.sub(r'[^a-z0-9\s]', '', sentence)
                cleaned_sentence = re.sub(r'\s{2,}', ' ', sentence)
                # tokenized sentence
                # tokenized_sentence = gensim.utils.tokenize(cleaned_sentence)
                # yield tokenized_sentence

                yield re.findall(reg, remove_stopwords(cleaned_sentence))

                # parse sentence = ' '.join(phrases_model[sentence])
                # yield re.findall(reg, remove_stopwords(line.lower()))
                # clean sentence
                # cleaned_sentence = clean_sentence(sentence)
                # tokenized_sentence = tokenize(cleaned_sentence)
                # parsed_sentence = sentence_to_bi_grams(n_grams, tokenized_sentence)
                #
                # parsed_sentence = sentence_to_bi_grams(n_grams, tokenized_sentence)
                # yield phrases_model[sentence]
                # returns ['hello', 'world']

# Gets the sentences using iterator from MySentences class
sentences = MySentences('./external_data')
# print(list(sentences))
def build_phrases(sentences):
    phrases = Phrases(sentences,
                      min_count=5,
                      threshold=7)
    return Phraser(phrases)


def sentence_to_bi_grams(phrases_model, sentence):
    return ' '.join(phrases_model[sentence])


def sentences_to_bigrams(n_grams, sentences, output_file_name):
    """
    We want to create, based on our corpus, a new corpus with meaningful bi-grams concatenated together for later use
    :param n_grams:
    :param sentences:
    :param output_file_name:
    :return:
    """
    with open(output_file_name, 'w+') as out_file:
        for sentence in sentences:
            parsed_sentence = sentence_to_bi_grams(n_grams, sentence)
            out_file.write(parsed_sentence + '\n')


# generate bigram model?
phrases_model = build_phrases(sentences)
# saves bigram model
phrases_model.save('phrases_model.txt')
# loads bigram model
phrases_model= Phraser.load('phrases_model.txt')
# create new corpus
sentences_to_bigrams(phrases_model, sentences, 'new_corpus.txt')

# load the model
# bigram_model = Word2Vec.load(bigram_pth)
# save bigram model to bigram path
# bigram_model.save(bigram_pth)
# sentences = MySentences('/Users/shirleykabir/Desktop/cs4300sp2020-sc2524-kyh24-rdz26-sk2279-szk4/review_sample_cleveland.json')

# iter_listA = iter(sentences)

# next(iter_listA)

# model = gensim.models.Word2Vec(sentences)

# Loads pre-computed model
# model = Word2Vec.load(pth)

# model = Word2Vec.load(pth)
# bigram_model = Word2Vec.load(pth)
# Saves model to path
# model.save(pth)

# Prints length of vocab
# print('HELLO')
# print(len(bigram_model.wv.vocab))

# Prints vocab
# words = list(model.wv.vocab)
# print(words)

# print(model.wv.most_similar_cosmul(positive=['drink']))

# print(model.wv.most_similar('working out'))

# print(model.wv.most_similar_cosmul(positive=['affordable'], negative=['expensive']))
# print(model.wv.most_similar_cosmul(positive=['favorite', 'sweet']))
# print(model.wv.doesnt_match(['green', 'parks', 'gyms', 'food']))


# IGNORE THIS
# with open('/Users/shirleykabir/Desktop/everything.json') as json_file:
#     data = json.load(json_file)

# for k,v in data.items():
#     with open("test.txt", "a") as myfile:
#         myfile.write("".join(v))
# with open('/Users/shirleykabir/Desktop/cs4300sp2020-sc2524-kyh24-rdz26-sk2279-szk4/review_sample_cleveland.json') as f:
#     with open("review_sample_cleveland.txt", "a") as myfile:
#         for line in islice(f, 40000):
#             myfile.write(json.loads(line)['text'])
#             # yield re.findall(reg, remove_stopwords(json.loads(line)['text'])
