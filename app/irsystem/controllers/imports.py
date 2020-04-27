import spacy
from nltk.stem.porter import PorterStemmer

nlp = spacy.load("en_vectors_web_lg")
stemmer = PorterStemmer()