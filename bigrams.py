import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

tokenizer = RegexpTokenizer(r'\w+')
# tokenizer.tokenize('Eighty-seven miles to go, yet.  Onward!')

# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('averaged_perceptron_tagger')

file_content = open(
    "/Users/shirleykabir/Desktop/cs4300sp2020-sc2524-kyh24-rdz26-sk2279-szk4/external_data/original.txt").read()
tokens = [t.lower() for t in tokenizer.tokenize(file_content)]

bigrams = nltk.collocations.BigramAssocMeasures()
trigrams = nltk.collocations.TrigramAssocMeasures()
bigramFinder = nltk.collocations.BigramCollocationFinder.from_words(tokens)

# trigramFinder = nltk.collocations.TrigramCollocationFinder.from_words(tokens)

# bigrams
bigram_freq = bigramFinder.ngram_fd.items()
bigramFreqTable = pd.DataFrame(list(bigram_freq), columns=[
                               'bigram', 'freq']).sort_values(by='freq', ascending=False)
# trigrams

# print(bigramFreqTable.head(20).to_string())

# get english stopwords
en_stopwords = set(stopwords.words('english'))
neighborhood_list = ['New York', 
                     'New York City'
                     'Battery Park',
                     'Chelsea',
                     'Chinatown',
                     'Civic Center',
                     'East Harlem',
                     'East Village',
                     'Financial District',
                     'Flatiron',
                     'Gramercy',
                     'Greenwich Village',
                     'Harlem',
                     "Hell's Kitchen",
                     'Inwood',
                     'Kips Bay',
                     'Little Italy',
                     'Lower East Side',
                     'Marble Hill',
                     'Midtown',
                     'Morningside Heights',
                     'Murray Hill',
                     'NoHo',
                     'Nolita',
                     'Roosevelt Island',
                     'SoHo',
                     'Stuyvesant Town',
                     'Theater District',
                     'TriBeCa',
                     'Two Bridges',
                     'Upper East Side',
                     'Upper West Side',
                     'Washington Heights',
                     'West Village']

names = (" ".join(neighborhood_list)).split(' ')
names=[n.lower() for n in names]

# function to filter for ADJ/NN bigrams

def rightTypes(ngram):
    if '-pron-' in ngram or 't' in ngram:
        return False
    for word in ngram:
        if word in en_stopwords or word.isspace() or word in names:
            return False
    acceptable_types = ('JJ', 'JJR', 'JJS', 'NN', 'NNS', 'NNP', 'NNPS')
    second_type = ('NN', 'NNS', 'NNP', 'NNPS')
    tags = nltk.pos_tag(ngram)
    if tags[0][1] in acceptable_types and tags[1][1] in second_type:
        return True
    else:
        return False

# filter bigrams
filtered_bi = bigramFreqTable[bigramFreqTable.bigram.map(
    lambda x: rightTypes(x))]

print(filtered_bi.head(100).to_string())