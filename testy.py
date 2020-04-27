# import nltk 
from nltk.corpus import wordnet 
synonyms = [] 
  
for syn in wordnet.synsets("hip"): 
    for l in syn.lemmas(): 
        synonyms.append(l.name())

print(synonyms)