from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import numpy as np
import json
# %matplotlib inline
import matplotlib.pyplot as plt

# with open("/Users/shirleykabir/Desktop/cs4300sp2020-sc2524-kyh24-rdz26-sk2279-szk4/app/irsystem/controllers/data/niche.json") as f:
#     niche = json.load(f)

# with open("/Users/shirleykabir/Desktop/cs4300sp2020-sc2524-kyh24-rdz26-sk2279-szk4/app/irsystem/controllers/data/relevant_data.json") as f:
#     reddit = json.load(f)

# with open("/Users/shirleykabir/Desktop/cs4300sp2020-sc2524-kyh24-rdz26-sk2279-szk4/app/irsystem/controllers/data/compass.json") as f:
#     compass = json.load(f)

# with open("/Users/shirleykabir/Desktop/cs4300sp2020-sc2524-kyh24-rdz26-sk2279-szk4/app/irsystem/controllers/data/goodmigrations.json") as f:
#     goodmigrations = json.load(f)

# with open("/Users/shirleykabir/Desktop/cs4300sp2020-sc2524-kyh24-rdz26-sk2279-szk4/app/irsystem/controllers/data/streeteasy.json") as f:
#     streeteasy = json.load(f)

# data={}

# for k,v in niche.items():
#     data[k.lower()]=[v['description']]
#     reviews=[x['text'] for x in v['reviews']]
#     data[k.lower()].extend(reviews)

# for k,v in reddit.items():
#     data[k.lower()].extend(v)

# for k,v in compass.items():
#     data[k.lower()].extend(v['tags'])
#     rel=[v['description'], v['WHAT TO EXPECT']['short'], v['WHAT TO EXPECT']['long'], v['THE LIFESTYLE']['short'], v['THE LIFESTYLE']['long'], v['WHAT NOT TO EXPECT']['short'], v['WHAT NOT TO EXPECT']['long'], v['THE MARKET']['short'], v['THE MARKET']['long'], v['FALL IN LOVE']['short'], v['FALL IN LOVE']['long']]
#     data[k.lower()].extend(rel)

# for k,v in goodmigrations.items():
#     data[k.lower()].extend([v['short description'],v['long description']])

# for k,v in streeteasy.items():
#     data[k.lower()].extend([v['location'],v['description'],v['the mood'],v['heart of the neighborhood'],v['neighborhood quirk'],v['best perk'],v['biggest downside'],v['housing'],v['more']])

# with open("everything.txt", 'w', encoding='utf-8') as f:
#     json.dump(data, f, ensure_ascii=False, indent=4)

# def mergeDict(original, updates, key_name):
#     for k, v in updates.items():
#         new_val = {key_name: v}
#         original[k].update(new_val)



with open("everything.json") as f:
    data = json.load(f)

print("Loaded {} streeteasy, reddit, niche, compass, and goodmigrations data".format(len(data)))
print("Dictionary with the following keys...")
print(data.keys())
# print("The index of \"{}\" is {}".format(data[7]['movie_name'], movie_id_to_index[data[7]['movie_id']]))

count_vec = CountVectorizer(stop_words='english', max_df=0.8, min_df=10,
                            max_features=1000, binary = True)

# print([t for t in list(data.values())[0]])
term_doc_matrix = count_vec.fit_transform([t for (k,v) in data.items() for t in v])
# term_doc_matrix = count_vec.fit_transform([t for t in list(data.values())[0]])
print(term_doc_matrix.shape)

# word index
features = count_vec.get_feature_names()
print(features[:100])

term_doc_matrix = term_doc_matrix.toarray()

term_doc_matrix[:1].tolist()

cooccurence_matrix = np.dot(term_doc_matrix.T, term_doc_matrix)

def find_most_similar_words(word, similarity_matrix, topk=10):
    if word not in features:
        print(word, 'is OOV.')
        return None
    idx = features.index(word)
    sorted_words = np.argsort(similarity_matrix[idx])[::-1]
    print('Most similar {} words to "{}" are:'.format(topk, word))
    for i in range(topk):
        j = sorted_words[i]
        print(features[j], similarity_matrix[idx, j])

# find_most_similar_words('park', similarity_matrix = cooccurence_matrix)

pa = np.sum(term_doc_matrix,0)

pa.shape

PMI_part = cooccurence_matrix / pa

PMI = PMI_part.T / pa

find_most_similar_words('families',PMI, 10)

