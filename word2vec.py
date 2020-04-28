import gensim, logging, os, json
from gensim.test.utils import common_texts, get_tmpfile
from gensim.models import Word2Vec
from gensim.models import KeyedVectors

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
 
# path = get_tmpfile("word2vec.model")
pth="/Users/shirleykabir/Desktop/cs4300sp2020-sc2524-kyh24-rdz26-sk2279-szk4/word2vec.model"
# class MySentences(object):
#     def __init__(self, dirname):
#         self.dirname = dirname
 
#     def __iter__(self):
#         for fname in os.listdir(self.dirname):
#             for line in open(os.path.join(self.dirname, fname)):
#                 yield line.split()
 
# sentences = MySentences('/Users/shirleykabir/Desktop/cs4300sp2020-sc2524-kyh24-rdz26-sk2279-szk4/external_data') # a memory-friendly iterator
# model = gensim.models.Word2Vec(sentences)

model = Word2Vec.load(pth)

# print(path)
# model.save(pth)
# print(len(model.wv.vocab))


# print(model.wv.most_similar_cosmul(positive=['affordable', 'housing'], negative=['expensive']))
# print(model.wv.most_similar_cosmul(positive=['restaurants', 'foodie']))
print(model.wv.doesnt_match(['green', 'parks', 'gyms', 'food']))



# IGNORE THIS
# with open('/Users/shirleykabir/Desktop/everything.json') as json_file:
#     data = json.load(json_file)

# for k,v in data.items():
#     with open("test.txt", "a") as myfile:
#         myfile.write("".join(v))