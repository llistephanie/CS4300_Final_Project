# # import nltk 
# from nltk.corpus import wordnet 
# synonyms = [] 
  
# for syn in wordnet.synsets("boujee"): 
#     for l in syn.lemmas(): 
#         synonyms.append(l.name())

# print(synonyms)

# Python program to print the similar 
# words using Enchant module 
  
# Importing the Enchant module 
import enchant 
  
# Using 'en_US' dictionary 
d = enchant.Dict("en_US") 
  
# Taking input from user 
word = input("Enter word: ") 
  
d.check(word) 
  
# Will suggest similar words 
# form given dictionary 
print(d.suggest(word)) 