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

logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

pth = "/Users/shirleykabir/Desktop/cs4300sp2020-sc2524-kyh24-rdz26-sk2279-szk4/word2vec.model-yelp2"
# pth="/Users/shirleykabir/Desktop/cs4300sp2020-sc2524-kyh24-rdz26-sk2279-szk4/word2vec.model" # just our data

class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname)):
                reg = re.compile(r'[a-z]+')
                yield re.findall(reg, remove_stopwords(line.lower()))
    # def __iter__(self):
    #     with open(self.dirname) as f:
    #         for line in islice(f, 40000):
    #             reg = re.compile(r'[a-z]+')
                # print(re.findall(reg, json.loads(line)['text'].lower()))
                # yield re.findall(reg, remove_stopwords(json.loads(line)['text'].lower()))

sentences = MySentences('/Users/shirleykabir/Desktop/cs4300sp2020-sc2524-kyh24-rdz26-sk2279-szk4/external_data')
# sentences = MySentences('/Users/shirleykabir/Desktop/cs4300sp2020-sc2524-kyh24-rdz26-sk2279-szk4/review_sample_cleveland.json')

# iter_listA = iter(sentences)

# next(iter_listA)

# model = gensim.models.Word2Vec(sentences)

model = Word2Vec.load(pth)

# model.save(pth)
# print(len(model.wv.vocab))

# words = list(model.wv.vocab)
# print(words)

# print(model.wv.most_similar_cosmul(positive=['drink']))

print(model.wv.most_similar('bubble'))

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
