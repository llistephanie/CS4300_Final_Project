import json
import numpy as np
import re
import math
from nltk.tokenize import TreebankWordTokenizer
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import MWETokenizer
from sklearn import preprocessing
import os
import nltk
from gensim.models import Word2Vec
from nltk.corpus import wordnet
import googlemaps
from nltk import tokenize
import datetime
from time import mktime
# Full list of neighborhoods
# NOTE: if you use these as keys, you can simply update the shared data dictionary variable (data)

nlp = Word2Vec.load("./word2vec.pth")
nlp_phrases = Word2Vec.load("./word2vec-phrases.pth")
gmaps = googlemaps.Client(key='AIzaSyCnKNIOmaCU1h3MA_SnyDGjpNgIkyF6E4Y')

neighborhood_list = ['Battery Park',
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
neighborhood_name_phrases=[x.lower().replace(' ', '_') for x in neighborhood_list]

n_neighborhoods = len(neighborhood_list)
treebank_tokenizer = TreebankWordTokenizer()
neighborhood_name_to_id = {}
for neighborhood_id in range(len(neighborhood_list)):
    neighborhood = neighborhood_list[neighborhood_id]
    neighborhood_name_to_id[neighborhood] = neighborhood_id
neighborhood_id_to_name = {v: k for k, v in neighborhood_name_to_id.items()}
no_likes = False

with open("app/irsystem/controllers/data/coordinates.json", "r") as f:
    coordinates_data = json.load(f)

# place_ids=[(v['geometry']['location']['lat'], v['geometry']['location']['lng']) for k,v in coordinates_data.items()]

place_ids=[
        "New Amsterdam Pavilion Battery Park, Peter Minuit Plaza, New York, NY 10004, USA",
        "9 Av/W 23 St, New York, NY 10011, USA",
        "44 Bowery, New York, NY 10013, USA",
        "39 Centre St, New York, NY 10007, USA",
        "2237 2nd Ave, New York, NY 10029, USA",
        "144 Avenue A, New York, NY 10009, USA",
        "26 Liberty St, New York, NY 10005, USA",
        "2 E 21st St, New York, NY 10010, USA",
        "38 Gramercy Park N, New York, NY 10010, USA",
        "Christopher St Station, New York, NY 10014, USA",
        "2175 Adam Clayton Powell Jr Blvd, New York, NY 10027, USA",
        "458 W 49th St, New York, NY 10019, USA",
        "207 St Station, New York, NY 10034, USA",
        "411 3rd Ave, New York, NY 10016, USA",
        "193 Grand St, New York, NY 10013, USA",
        "465 Grand St, New York, NY 10002, USA",
        "39 Jacobus Pl, The Bronx, NY 10463, USA",
        "42 St-Bryant Park Station, New York, NY 10018, USA",
        "Broadway/W 120 St, New York, NY 10027, USA",
        "206 E 38th St, New York, NY 10016, USA",
        "411 Lafayette St # 605, New York, NY 10003, USA",
        "Mott St &, Prince St, New York, NY 10012, USA",
        "500 Main St, New York, NY 10044, USA",
        "501 Broome St, New York, NY 10013, USA",
        "252 1st Avenue, New York, NY 10009, USA",
        "1568A Broadway, New York, NY 10036, USA",
        "W Broadway/Duane St, New York, NY 10013, USA",
        "80 Catherine St, New York, NY 10038, USA",
        "235 E 78th St, New York, NY 10075, USA",
        "523 Amsterdam Ave, New York, NY 10024, USA",
        "3456 St Nicholas Ave, New York, NY 10032, USA",
        "367 Bleecker St, New York, NY 10014, USA"
    ]

data = {}
for x in neighborhood_list:
    data[x] = {}


def scoreCalculation(data_list, bar = 1.5):
    arr = np.array(data_list)
    mean = np.mean(data_list)
    std = np.std(data_list)
    if (std == 0): std = 1

    new_scores = []
    for x in (data_list):
        score = (x - mean)/std
        score = (score+bar)*100/(bar*2)
        score = min(score, 100)
        score = max(score, 0)

        if (x == 0):
            new_scores.append(0)
        else:
            new_scores.append(score)
    return new_scores

def mergeDict(original, updates, key_name):
    for k, v in updates.items():
        new_val = {key_name: v}
        original[k].update(new_val)

def loadHappinessScores():
    """
    Function adds in the attributes "description" and "safety_score" for each neighborhood.
    Description is pulled from the niche data
    Safety score ranges from (0-100)
    """
    # global data # declare global in order to update global data variable

    with open("app/irsystem/controllers/data/happiness.json", "r") as f:
        safety_data = json.load(f)

    percentages = np.array([float(v) for k, v in safety_data.items()])
    normalized = scoreCalculation(percentages,3.0)
    norm_safety_scores = {
        neighborhood_list[i]: v for i, v in enumerate(normalized)}
    mergeDict(data, norm_safety_scores, "happiness score")
    return norm_safety_scores


def calculateAgeScore(age):
    """
    Input:
        age         value (int) if user included it, None otherwise

    Output:
        age_scores  dictionary indexed by neighborhood of score (0-100) assigned to each
    """
    if age == '':
        age = 24
    else:
        age = int(age)

    with open("app/irsystem/controllers/data/niche.json", encoding="utf-8") as f:
        niche_data = json.load(f)

    age_dist = ["<10 years", "10-17 years", "18-24 years", "25-34 years",
                "35-44 years", "45-54 years", "55-64 years", "65+ years"]

    age_dist = ""
    if age < 10:
        age_dist = "<10 years"
    elif age <= 17:
        age_dist = "10-17 years"
    elif age <= 24:
        age_dist = "18-24 years"
    elif age <= 34:
        age_dist = "25-34 years"
    elif age <= 44:
        age_dist = "35-44 years"
    elif age <= 54:
        age_dist = "45-54 years"
    elif age <= 64:
        age_dist = "55-64 years"
    else:
        age_dist = "65+ years"

    percentages = np.array([int(v["age distribution"][age_dist].replace(
        '%', '')) for k, v in niche_data.items()])

    normalized = scoreCalculation(
        percentages)

    norm_age_scores = {neighborhood_list[i] : v for i, v in enumerate(normalized)}

    mergeDict(data, norm_age_scores, "age score")
    return norm_age_scores

def calculateBudget(minBudget, maxBudget, numberBeds='1BR'):
    with open("app/irsystem/controllers/data/renthop.json") as f:
        renthop_data = json.load(f)

    fit_budget = []
    top_25s = []
    bottom_25s = []
    # essentially finding percentage of homes under [min,max] range
    for k, v in renthop_data.items():

        bottom = int(v[numberBeds]["Bottom 25%"].replace('$', '').replace(',', ''))
        median = int(v[numberBeds]["Median"].replace('$', '').replace(',', ''))
        top = int(v[numberBeds]["Top 25%"].replace('$', '').replace(',', ''))

        top_25s.append(top)
        bottom_25s.append(bottom)

        my_range = set(list(range(minBudget, maxBudget)))
        n_range = set(list(range(bottom, top)))

        intersect = my_range.intersection(n_range)
        percentage_points = 50.0/(top-bottom)

        if(len(intersect) == 0):
            fit_budget.append(0)
        else:
            fit_budget.append((max(intersect)-min(intersect))
                              * percentage_points)

    fit_budget = np.array(fit_budget)

    normalized = scoreCalculation(fit_budget)

    # for text analysis
    norm_budget_scores = {
        neighborhood_list[i]: v for i, v in enumerate(normalized)}

    # data.update(norm_budget_scores)
    mergeDict(data, norm_budget_scores, "budget score")
    return norm_budget_scores

# Activities/Likes Score Code

def tokenize(multi_word_queries, text):
    """Returns a list of words that make up the text.
    Params: {text: String}
    Returns: List
    """
    lower_case = text.lower()
    tokenizer = RegexpTokenizer('not\s+very\s+[a-z]+|not\s+[a-z]+|no\s+[a-z]+|[a-z]+')
    result = tokenizer.tokenize(lower_case)
    multi_tokenizer = MWETokenizer([('working', 'out'),('coffee', 'shops'), ('average', 'prices'), ('union', 'square'), ('real', 'estate'), ('ice', 'cream'), ('whole', 'foods'), ('co', 'op'), ('wall', 'street'), ('world', 'trade'), ('high', 'school'), ('dim', 'sum'), ('empire', 'state'), ('high', 'rise'), ('walk', 'ups')])
    if len(multi_word_queries)>0:
        for tok in multi_word_queries:
            if(len(tok.split('_'))>1):
                multi_tokenizer.add_mwe(tuple(tok.split('_')))
    #add neighborhood names
    for n in neighborhood_name_phrases:
        multi_tokenizer.add_mwe(tuple(n.split('_')))

    result2 = multi_tokenizer.tokenize(result)
    return result2

def mergeMapping(original, new):
    for k,v in new.items():
        original.setdefault(k,[]).append(v)
    return original

def tokenize_niche(tokenize_method, input_niche, input_neighborhood, multi_word_queries):
    """Returns a list of words contained in a neighborhood's niche
       description.
    Params: {tokenize_method: Function (a -> b),
                 input_niche: JSON
             input_neighborhood: String}
    Returns: List
    """
    token_list = []
    n={}
    if input_neighborhood in input_niche.keys():
        reviews_list = input_niche[input_neighborhood]['reviews']
        if reviews_list is not None:
            for review in reviews_list:
                review_text = tokenize_method(multi_word_queries, review['text'])
                token_list.extend(review_text)
                tokens_post = dict.fromkeys(review_text, review['text'])
                n = mergeMapping(n, tokens_post)
    return token_list, n


def tokenize_streeteasy(tokenize_method, input_streeteasy, input_neighborhood, multi_word_queries):
    """Returns a list of words contained in a neighborhood's streeteasy data.
    Params: {tokenize_method: Function (a -> b),
             input_streeteasy: JSON
             input_neighborhood: String}
    Returns: List
    """
    token_list = []
    n={}
    if input_neighborhood in input_streeteasy.keys():
        desc = input_streeteasy[input_neighborhood]['description']
        mood = input_streeteasy[input_neighborhood]['the mood']
        more = input_streeteasy[input_neighborhood]['more']
        downside = input_streeteasy[input_neighborhood]['biggest downside']
        housing = input_streeteasy[input_neighborhood]['housing']
        best_perk = input_streeteasy[input_neighborhood]['best perk']
        if desc is not None:
            tokenized_desc = tokenize_method(multi_word_queries, desc)
            token_list.extend(tokenized_desc)
            tokens_post = dict.fromkeys(tokenized_desc, desc)
            n = mergeMapping(n, tokens_post)
        if mood is not None:
            tokenized_mood = tokenize_method(multi_word_queries, mood)
            token_list.extend(tokenized_mood)
            tokens_post = dict.fromkeys(tokenized_mood, mood)
            n = mergeMapping(n, tokens_post)
        if more is not None:
            tokenized_more = tokenize_method(multi_word_queries, more)
            token_list.extend(tokenized_more)
            tokens_post = dict.fromkeys(tokenized_more, more)
            n = mergeMapping(n, tokens_post)
        if downside is not None:
            tokenized_downside = tokenize_method(multi_word_queries, downside)
            token_list.extend(tokenized_downside)
            tokens_post = dict.fromkeys(tokenized_downside, downside)
            n = mergeMapping(n, tokens_post)
        if housing is not None:
            tokenized_housing = tokenize_method(multi_word_queries, housing)
            token_list.extend(tokenized_housing)
            tokens_post = dict.fromkeys(tokenized_housing, housing)
            n = mergeMapping(n, tokens_post)
        if best_perk is not None:
            tokenized_perk = tokenize_method(multi_word_queries, best_perk)
            token_list.extend(tokenized_perk)
            tokens_post = dict.fromkeys(tokenized_perk, best_perk)
            n = mergeMapping(n, tokens_post)
    return token_list, n


def tokenize_compass(tokenize_method, input_compass, input_neighborhood, multi_word_queries):
    """Returns a list of words contained in a neighborhood's compass data.
    Params: {tokenize_method: Function (a -> b),
             input_compass: JSON
             input_neighborhood: String}
    Returns: List
    """
    token_list = []
    n={}
    if input_neighborhood in input_compass.keys():
        tags = input_compass[input_neighborhood]['tags']
        tags_list = ' '.join(tags)
        desc = input_compass[input_neighborhood]['description']
        lifestyle = input_compass[input_neighborhood]['THE LIFESTYLE']
        market = input_compass[input_neighborhood]['THE MARKET']
        highlight = input_compass[input_neighborhood]["FALL IN LOVE"]
        expectation = input_compass[input_neighborhood]['WHAT TO EXPECT']
        if tags_list is not None:
            tokenized_tags = tokenize_method(multi_word_queries, tags_list)
            token_list.extend(tokenized_tags)
            tokens_post = dict.fromkeys(tokenized_tags, tags_list)
            n = mergeMapping(n, tokens_post)
        if desc is not None:
            tokenized_desc = tokenize_method(multi_word_queries, desc)
            token_list.extend(tokenized_desc)
            tokens_post = dict.fromkeys(tokenized_desc, desc)
            n = mergeMapping(n, tokens_post)
        if lifestyle is not None:
            tokenized_lifestyle = tokenize_method(multi_word_queries,
                lifestyle['short'] + ' ' + lifestyle['long'])
            token_list.extend(tokenized_lifestyle)
            tokens_post = dict.fromkeys(tokenized_lifestyle, lifestyle['short'] + ' ' + lifestyle['long'])
            n = mergeMapping(n, tokens_post)
        if market is not None:
            tokenized_market = tokenize_method(multi_word_queries,
                market['short'] + ' ' + market['long'])
            token_list.extend(tokenized_market)
            tokens_post = dict.fromkeys(tokenized_market, market['short'] + ' ' + market['long'])
            n = mergeMapping(n, tokens_post)
        if highlight is not None:
            tokenized_highlight = tokenize_method(multi_word_queries,
                highlight['short'] + ' ' + highlight['long'])
            token_list.extend(tokenized_highlight)
            tokens_post = dict.fromkeys(tokenized_highlight, highlight['short'] + ' ' + highlight['long'])
            n = mergeMapping(n, tokens_post)
        if expectation is not None:
            tokenized_expectation = tokenize_method(multi_word_queries,
                expectation['short'] + ' ' + expectation['long'])
            token_list.extend(tokenized_expectation)
            tokens_post = dict.fromkeys(tokenized_expectation, expectation['short'] + ' ' + expectation['long'])
            n = mergeMapping(n, tokens_post)
    return token_list, n


def tokenize_reddit(tokenize_method, input_reddit, input_neighborhood, multi_word_queries):
    """Returns a list of words contained in a neighborhood's reddit
       posts.
    Params: {tokenize_method: Function (a -> b),
                 input_reddit: JSON
             input_neighborhood: String}
    Returns: List
    """
    token_list = []
    n={}
    if input_neighborhood in input_reddit.keys():
        posts_list = input_reddit[input_neighborhood]
        if posts_list is not None:
            for post in posts_list:
                post_text = tokenize_method(multi_word_queries, post)
                token_list.extend(post_text)
                tokens_post = dict.fromkeys(post_text, post)
                n = mergeMapping(n, tokens_post)
    return token_list, n

def tokenize_goodmigrations(tokenize_method, input_goodmigrations, input_neighborhood, multi_word_queries):
    """Returns a list of words contained in a neighborhood's goodmigrations
       description.
    Params: {tokenize_method: Function (a -> b),
                 input_goodmigrations: JSON
             input_neighborhood: String}
    Returns: List
    """
    token_list = []
    n={}
    if input_neighborhood in input_goodmigrations.keys():
        desc = input_goodmigrations[input_neighborhood]['short description']
        desc2 = input_goodmigrations[input_neighborhood]['long description']
        if desc is not None:
            tokenized_desc = tokenize_method(multi_word_queries, desc)
            token_list.extend(tokenized_desc)
            tokens_post = dict.fromkeys(tokenized_desc, desc)
            n = mergeMapping(n, tokens_post)
        if desc2 is not None:
            tokenized_desc = tokenize_method(multi_word_queries, desc2)
            token_list.extend(tokenized_desc)
            tokens_post = dict.fromkeys(tokenized_desc, desc2)
            n = mergeMapping(n, tokens_post)
    return token_list, n

def tokenize_externaldata(tokenize_method, input_externaldata, input_neighborhood, multi_word_queries):
    """Returns a list of words contained in a neighborhood's external data.
    Params: {tokenize_method: Function (a -> b),
                 input_reddit: JSON
             input_neighborhood: String}
    Returns: List
    """
    token_list = []
    n={}
    if input_neighborhood in input_externaldata.keys():
        posts_list = input_externaldata[input_neighborhood]
        if posts_list is not None:
            for post in posts_list:
                post_text = tokenize_method(multi_word_queries, post)
                token_list.extend(post_text)
                tokens_post = dict.fromkeys(post_text, post)
                n = mergeMapping(n, tokens_post)
    return token_list, n

def get_neighborhood_tokens(tokenizer, data_files, tokenize_methods, input_neighborhood, multi_word_queries):
    """Returns a list of words contained in all the data describing input_neighborhood.
    Params: {tokenize_method: Function (a -> b),
             data: List,
             tokenize_data_methods: List,
             input_neighborhood: String}
    Returns: List
    """
    tokenize_niche = tokenize_methods[0]
    tokenize_streeteasy = tokenize_methods[1]
    tokenize_compass = tokenize_methods[2]
    # tokenize_reddit = tokenize_methods[3]
    tokenize_goodmigrations = tokenize_methods[4]
    tokenize_externaldata = tokenize_methods[5]
    tokens_n, mapping_n=tokenize_niche(tokenizer, data_files[0], input_neighborhood, multi_word_queries)
    tokens=tokens_n
    tokens_se, mapping_se=tokenize_streeteasy(tokenizer, data_files[1], input_neighborhood, multi_word_queries)
    tokens.extend(tokens_se)
    tokens_c, mapping_c=tokenize_compass(tokenizer, data_files[2], input_neighborhood, multi_word_queries)
    tokens.extend(tokens_c)
    # tokens_r, mapping_r=tokenize_reddit(tokenizer, data_files[3], input_neighborhood)
    # tokens.extend(tokens_r)
    tokens_gm, mapping_gm=tokenize_goodmigrations(tokenizer, data_files[4], input_neighborhood, multi_word_queries)
    tokens.extend(tokens_gm)
    tokens_ed, mapping_ed=tokenize_externaldata(tokenizer, data_files[5], input_neighborhood, multi_word_queries)
    tokens.extend(tokens_ed)
    return tokens, (mapping_n, mapping_se, mapping_c, {}, mapping_gm, mapping_ed)


def build_word_neighborhood_count(tokenizer, data, tokenize_methods, input_neighborhoods):
    """Returns a dictionary with the number of times each distinct word appears in a neighborhood
        Params: {tokenize_method: Function (a -> b),
                 data: List,
                                 tokenize_data_methods: List,
                 input_neighborhoods: String List}
        Returns: Dict
    """
    word_neighborhood_count = {}
    word_to_neighborhoods = {}
    tokenize_niche = tokenize_methods[0]
    tokenize_streeteasy = tokenize_methods[1]
    tokenize_compass = tokenize_methods[2]
    tokenize_reddit = tokenize_methods[3]
    tokenize_goodmigrations = tokenize_methods[4]
    tokenize_externaldata = tokenize_methods[5]
    # creates dictionary of unique words as keys and set of neighborhoods that the word appears in
    for neighborhood in input_neighborhoods:
        tokenized_niche = set(tokenize_niche(tokenizer, data[0], neighborhood))
        tokenized_streeteasy = set(tokenize_streeteasy(
            tokenizer, data[1], neighborhood))
        tokenized_compass = set(tokenize_compass(
            tokenizer, data[2], neighborhood))
        tokenized_reddit = set(tokenize_reddit(
            tokenizer, data[3], neighborhood))
        tokenized_goodmigrations = set(tokenize_goodmigrations(
            tokenizer, data[4], neighborhood))
        tokenized_externaldata = set(tokenize_externaldata(
            tokenizer, data[5], neighborhood))
        neighborhood_tokens = tokenized_niche.union(
            tokenized_streeteasy).union(tokenized_compass).union(tokenized_reddit).union(tokenized_goodmigrations).union(tokenized_externaldata)
        for word in neighborhood_tokens:
            if word in word_to_neighborhoods.keys():
                word_to_neighborhoods[word].add(neighborhood)
            else:
                word_to_neighborhoods[word] = set()
                word_to_neighborhoods[word].add(neighborhood)
                # sets values for word_episode_count
    for word in word_to_neighborhoods:
        word_neighborhood_count[word] = len(word_to_neighborhoods[word])
    return word_neighborhood_count


def output_good_types(input_word_counts):
    """Returns a list of good types in alphabetically sorted order
        Params: {input_word_counts: Dict}
        Returns: List
    """
    # get good types
    good_types = []
    # Iterate over all the items in dictionary and filter words that appear in more than one episode
    for (word, word_count) in input_word_counts.items():
        # Check if value is more than one then add to new dictionary
        if word_count > 1:
            good_types.append(word)
    good_types.sort()
    return good_types


def tf(word_w, neighborhood_n, input_word_matrix, types_to_i):
    """Returns the term frequency weight which is the
    ratio between the number of times an input neighborhood N says word W and
    the total number of words in a neighborhood N's descriptions.

    Params: {word_w: String,
             neighborhood_n: Integer (Index within neighborhoods_to_id),
             input_word_matrix: Numpy array}
    Returns: Float
    """
    word_idx = types_to_i[word_w]
    w_freq = input_word_matrix[neighborhood_n][word_idx]
    all_words = input_word_matrix[neighborhood_n, :]
    total_num_words = np.sum(all_words)
    return w_freq/(total_num_words + 1)


def build_inverted_index(tokenize_method, neighborhoods_to_id,
                         data, tokenize_data_methods, multi_word_queries):
    """ Builds an inverted index from the messages."""
    inv_idx = {}
    mappings={}
    for neighborhood_name, neighborhood_id in neighborhoods_to_id.items():
        tokens, mapping = get_neighborhood_tokens(
            tokenize_method, data, tokenize_data_methods, neighborhood_name, multi_word_queries)
        mappings[neighborhood_name]=mapping
        distinct_toks = set(tokens)
        for tok in distinct_toks:
            tok_count = tokens.count(tok)
            if tok not in inv_idx.keys():
                inv_idx[tok] = []
                inv_idx[tok].append((neighborhood_id, tok_count))
            else:
                term_tups = inv_idx[tok]
                term_tups.append((neighborhood_id, tok_count))
    return inv_idx, mappings


def compute_idf(inv_idx, n_neighborhoods, min_df=10, max_df_ratio=0.95):
    """ Compute term IDF values from the inverted index.
    Words that are too frequent or too infrequent get pruned.

    Arguments
    =========

    inv_idx: an inverted index as above

    n_neighborhoods: int,
        The number of neighborhoods.

    min_df: int,
        Minimum number of neighborhoods a term must occur in.
        Less frequent words get ignored.
        Documents that appear min_df number of times should be included.

    max_df_ratio: float,
        Maximum ratio of documents a term can occur in.
        More frequent words get ignored.

    Returns
    =======

    idf: dict
        For each term, the dict contains the idf value.

    """

    idf_dict = {}
    for term, list_of_postings in inv_idx.items():
        num_postings = len(list_of_postings)
        large_frac = num_postings / n_neighborhoods
        if num_postings >= min_df and large_frac <= max_df_ratio:
            idf = math.log2(n_neighborhoods / (1 + num_postings+1))+1
            idf_dict[term] = idf
    return idf_dict


def compute_neighborhood_norms(index, idf, n_neighborhoods):
    """ Precompute the euclidean norm of each document.

    Arguments
    =========

    index: the inverted index as above

    idf: dict,
        Precomputed idf values for the terms.

    n_docs: int,
        The total number of documents.

    Returns
    =======

    norms: np.array, size: n_docs
        norms[i] = the norm of document i.
    """
    norm_array = np.zeros((n_neighborhoods))
    for term, list_of_postings in index.items():
        if term in idf.keys():
            term_idf = idf[term]
            for doc_tup in list_of_postings:
                neighborhood_id = doc_tup[0]
                term_tf = doc_tup[1]
                prod = math.pow(term_tf * term_idf, 2)
                norm_array[neighborhood_id] += prod
    return np.sqrt(norm_array)


def get_new_multiword_toks(query, tokenizer, syn=True):
    new_toks = []
    for i in query:
        i=i.lower()
        related_list = []
        # phrase lookup
        if (len(i.split(' '))>1):
            phrase=i.replace(' ', '_')
            if (phrase in nlp_phrases):
                related_list = nlp_phrases.wv.most_similar(phrase)

            new_toks.append(phrase)

            for r_word, r_score in related_list:
                if r_score > 0.85: new_toks.append(r_word)

    new_toks=[x for x in new_toks if x not in neighborhood_name_phrases] # remove neighborhood names from relevant queries
    return new_toks

def compute_query_info(new_toks, query, idf, tokenizer, syn=True):
    query_norm_inner_sum = 0
    query_tf = {}
    for i in query:
        i=i.lower()
        related_list = []
        if (len(i.split(' '))<=1):
            if (i in nlp):
                related_list = nlp.wv.most_similar(i)
            if i in idf.keys():
                new_toks.append(i)

            for r_word, r_score in related_list:
                if r_word in idf.keys() and r_score > 0.85: new_toks.append(r_word)
    # print(f"new_toks {new_toks}")
    for tok in set(new_toks):
        query_tf[tok] = new_toks.count(tok)
    new_toks_checked = []

    for word in new_toks:
        if word in idf.keys():
            new_toks_checked.append(word)
            # if the word is in the original query, double the score for it
            if word in query:
                query_norm_inner_sum += 0.5 * math.pow(query_tf[word] * idf[word], 2)
            else:
                query_norm_inner_sum += math.pow(query_tf[word] * idf[word], 2)
    query_norm = math.sqrt(query_norm_inner_sum)
    return new_toks_checked, query_tf, query_norm


def cosine_sim(query, index, idf, doc_norms, tokenizer):
    """ Search the collection of documents for the given query based on cosine similarity

    Arguments
    =========
    query: Tuple,
        (x,y,z) where x = the tokens of the query we are looking for, y = dictionary (k,v) where k is a token and v is
        the term frequency of k in the query we are looking for, z = norm of the query we are looking for.

    related_words: String list,
        list of terms that are related to some words in the query and could be used in adding to the score of a neighborhood.

    index: an inverted index as above

    idf: idf values precomputed as above

    doc_norms: document norms as computed above

    tokenizer: a TreebankWordTokenizer

    Returns
    =======

    results, list of tuples (score, doc_id)
        Sorted list of results such that the first element has
        the highest score, and `doc_id` points to the document
        with the highest score.

    Note:

    """
    score_dict = {}
    query_toks = query[0]
    query_tf = query[1]
    query_norm = query[2]
    # all_toks = query_toks.extend(related_words)

    # calculate numerator
    for term in query_toks:
        if term in idf.keys():
            list_of_postings = index[term]
            q_i = query_tf[term] * idf[term]
            for posting_tup in list_of_postings:
                neighborhood_id = posting_tup[0]
                prod = q_i * posting_tup[1] * idf[term]
                if neighborhood_id not in score_dict.keys():
                    score_dict[neighborhood_id] = 0
                    score_dict[neighborhood_id] += prod
                else:
                    score_dict[neighborhood_id] += prod

    divide_dict = {k: v/(doc_norms[k] * query_norm)
                   for k, v in score_dict.items()}
    return {k: v for k, v in sorted(divide_dict.items(), key=lambda tup: tup[1], reverse=True)}

    # to_list = [(k, v) for k, v in divide_dict.items()]
    # to_list.sort(key=lambda tup: tup[1], reverse=True)
    # return to_list


def print_cossim_results(id_to_neighborhoods, query, results):
    print("#" * len(query))
    print(query)
    print("#" * len(query))
    for neighborhood_id, score in results.items():
        print("[{:.2f}] {})".format(
            score, id_to_neighborhoods[neighborhood_id]))
        print()


def calculateTextSimLikes(likes_list, merge_dict=False):
    global no_likes
    no_likes = False
    if len(likes_list) == 0:
        norm_likes_scores = {n: 0.0 for n in neighborhood_list}
        if merge_dict:
            mergeDict(data, norm_likes_scores, "likes score")
        return norm_likes_scores, {}, []

    prefix = 'app/irsystem/controllers/data/'
    query_str = likes_list
    # query_extended = query_str #+ ' ' + related_words
    likes_scores = []
    docs_with_query={}

    with open(prefix + 'niche.json', encoding="utf-8") as niche_file, \
         open(prefix + 'streeteasy.json', encoding="utf-8") as streeteasy_file, \
         open(prefix + 'compass.json', encoding="utf-8") as compass_file, \
         open(prefix + 'relevant_data.json', encoding="utf-8") as reddit_file, \
         open(prefix + 'goodmigrations.json', encoding="utf-8") as goodmigrations_file, \
         open(prefix + 'external_data.json', encoding="utf-8") as externaldata_file:

        # Loading all the data
        niche_data = json.load(niche_file)
        streeteasy_data = json.load(streeteasy_file)
        compass_data = json.load(compass_file)
        reddit_data = json.load(reddit_file)
        goodmigrations_data = json.load(goodmigrations_file)
        externaldata_data = json.load(externaldata_file)


        multi_word_tokens = get_new_multiword_toks(query_str, treebank_tokenizer)
        # Compiling data and tokenization methods
        tokenize_methods = [tokenize_niche,
                            tokenize_streeteasy,
                            tokenize_compass,
                            tokenize_reddit,
                            tokenize_goodmigrations, tokenize_externaldata]
        data_files = [niche_data, streeteasy_data,
                      compass_data, reddit_data, goodmigrations_data, externaldata_data]

        # Information retrieval
        inv_idx, mappings = build_inverted_index(
            tokenize, neighborhood_name_to_id, data_files, tokenize_methods, multi_word_tokens)
        idf = compute_idf(inv_idx, n_neighborhoods, min_df=0, max_df_ratio=1.0)

        with open("dump.json","w") as j:
            json.dump(idf, j)
        doc_norms = compute_neighborhood_norms(inv_idx, idf, n_neighborhoods)
        query_info = compute_query_info(multi_word_tokens, query_str, idf, treebank_tokenizer)
        for k,v in mappings.items():
            map_n, map_se, map_c, map_r, map_gm, map_ed=v
            rel_docs=[]
            for q in query_info[0]:
                qu=q.replace('_', '(.?)')
                rel_docs.extend([(re.sub(rf"\b{qu}\b", "<b>" + q.replace('_', re.findall(rf"\b{qu}\b", x)[0] if re.findall(rf"\b{qu}\b", x) else ' ') + "</b>" , x, flags=re.I), "niche") for x in map_n.get(q, [])])
                rel_docs.extend([(re.sub(rf"\b{qu}\b", "<b>" + q.replace('_', re.findall(rf"\b{qu}\b", x)[0] if re.findall(rf"\b{qu}\b", x) else ' ') + "</b>" , x, flags=re.I), "streeteasy")for x in map_se.get(q, [])])
                rel_docs.extend([(re.sub(rf"\b{qu}\b", "<b>" + q.replace('_', re.findall(rf"\b{qu}\b", x)[0] if re.findall(rf"\b{qu}\b", x) else ' ') + "</b>" , x, flags=re.I), "compass") for x in map_c.get(q, [])])
                rel_docs.extend([(re.sub(rf"\b{qu}\b", "<b>" + q.replace('_', re.findall(rf"\b{qu}\b", x)[0] if re.findall(rf"\b{qu}\b", x) else ' ') + "</b>" , x, flags=re.I), "reddit") for x in map_r.get(q, [])])
                rel_docs.extend([(re.sub(rf"\b{qu}\b", "<b>" + q.replace('_', re.findall(rf"\b{qu}\b", x)[0] if re.findall(rf"\b{qu}\b", x) else ' ') + "</b>" , x, flags=re.I), "goodmigrations") for x in map_gm.get(q, [])])
                rel_docs.extend([((re.sub(rf"\b{qu}\b", "<b>" + q.replace('_', re.findall(rf"\b{qu}\b", x)[0] if re.findall(rf"\b{qu}\b", x) else ' ') + "</b>" , x, flags=re.I) + "</b>"), "") for x in map_ed.get(q, [])])
            docs_with_query[k]=rel_docs

        # score, doc id use neighborhood_id_to_name
        likes_scores = cosine_sim(
            query_info, inv_idx, idf, doc_norms, treebank_tokenizer)
        if sum(likes_scores) == 0:
            no_likes = True

    # print_cossim_results(neighborhood_id_to_name, query_str, likes_scores)

    included_ids = set(likes_scores.keys())
    zero_scored_neighborhoods = list(
        set(neighborhood_id_to_name.keys()).difference(included_ids))
    for z in zero_scored_neighborhoods:
        likes_scores[z] = 0.0
    likes_scores_list = [(k, v) for k, v in likes_scores.items()]

    likes_scores = sorted(likes_scores_list, key=lambda x: x[0])
    likes_scores = np.array([l[1] for l in likes_scores])
    normalized = scoreCalculation(likes_scores, 2.0)

    norm_likes_scores = {
        neighborhood_list[i]: v for i, v in enumerate(normalized)}

    if merge_dict:
        mergeDict(data, norm_likes_scores, "likes score")
    return norm_likes_scores, docs_with_query, query_info[0]

def calculateCommuteScore(commuteType, commuteDestination, commuteDuration, commuteSubwayService):
    with open("app/irsystem/controllers/data/walkscore.json") as f:
        walkscore_data = json.load(f)
    with open("app/irsystem/controllers/data/nyc-parking-spots.json") as c:
        carscore_data = json.load(c)
    with open("app/irsystem/controllers/data/gas_stations.json") as g:
        gasscore_data = json.load(g)
    with open("app/irsystem/controllers/data/new_subway_scores.json") as s:
        subwayscore_data = json.load(s)

    # type_key = {'Walk': "walk score", 'Bike': "bike score", 'Public Transit': "transit score"}
    type_key = {'Walk': "walk score", 'Bike': "bike score"}


    all_walkscores={}
    commute_scores=np.zeros(len(neighborhood_list))
    weight = 1/len(commuteType)

    for i in range(len(commuteType)):
        #get pre-computed score for each neighborhood for walking and biking
        for cType,v in type_key.items():
            cscores = np.array([int(v['rankings'][type_key[cType]]) for k, v in walkscore_data.items()])
            all_walkscores[cType] = {neighborhood_list[i]: v for i, v in enumerate(cscores) }
            if cType==commuteType[i]:
                commute_scores = np.add(commute_scores, weight*cscores)

        #get car score for each neighborhood by combining parking lot, walk, and gas score
        car_scores = np.array([int(v['Car-Score']) for k, v in carscore_data.items()])
        walk_scores = np.array([int(v['rankings']['walk score']) for k, v in walkscore_data.items()])
        gas_scores = np.array([int(v['score']) for k, v in gasscore_data.items()])
        cscores = np.add(.5*car_scores, .5*gas_scores)
        all_walkscores['Car'] = {neighborhood_list[i]: v for i, v in enumerate(scoreCalculation(cscores))}
        if commuteType[i]=='Car':
            commute_scores = np.add(commute_scores, weight*cscores)

        #update transit score for each neighborhood based on subway scores and add transit scores to all_walkscores
        original_transit_scores = np.array([int(v['rankings']['transit score']) for k, v in walkscore_data.items()])
        all_walkscores['Public Transit'] = {neighborhood_list[i]: v for i, v in enumerate(original_transit_scores) }
        subway_scores = np.array([int(v['Score']) for k, v in subwayscore_data.items()])
        cscores = np.add(.5*original_transit_scores, .5*subway_scores)
        if commuteType[i] =='Public Transit':
            commute_scores = np.add(commute_scores, weight*cscores)
    normalized = scoreCalculation(commute_scores, 0.73)
    # print(commute_scores, normalized, "ORIG-NORM")

    all_durations=None

    if(commuteDestination):
        travel_modes={"Walk": "walking", "Bike": "bicycling", "Car": "driving", "Public Transit": "transit"}

        all_matrices={}

        all_durations={}
        ratio=np.zeros(len(neighborhood_list))

        today = datetime.date.today()
        monday=today + datetime.timedelta(days=(7 - today.weekday()))
        nineam = datetime.time(9, 0)
        monday_9am=datetime.datetime.combine(monday, nineam)

        timestamp_monday_9am=mktime(monday_9am.timetuple())

        for k,v in travel_modes.items():
            all_matrices[k] = gmaps.distance_matrix(place_ids, commuteDestination, mode=v, departure_time=timestamp_monday_9am)
            all_durations[k] = {neighborhood_list[i]: int(v['elements'][0]['duration']['value']/60) if 'duration' in v['elements'][0].keys() else None for i, v in enumerate(all_matrices[k]['rows']) }


        for i in range(len(commuteType)):
            commute_ratio=int(float(commuteDuration)+1)/(np.array([v['elements'][0]['duration']['value']/60 if 'duration' in v['elements'][0].keys() else 160.0 for v in all_matrices[commuteType[i]]['rows']])+1)
            ratio = np.add(ratio, commute_ratio*weight)
        ratio[ratio <1.0]=ratio[ratio <1.0]/5.0

        normalized=0.2*np.array(normalized)+0.8*np.array(scoreCalculation(ratio))

    if(commuteSubwayService):
        subway_service_scores = []
        selected_subway_service = commuteSubwayService.capitalize()
        selected_subway_service = re.sub(r"(?<=\d)d", ' Express', selected_subway_service)
        for k,v in subwayscore_data.items():
            # print(v['Services'][-1] == selected_subway_service, v['Services'][-1], selected_subway_service)
            if selected_subway_service in v['Services']:
                subway_service_scores.append(1)
            else:
                subway_service_scores.append(0)
        # print(subway_service_scores)
        normalized = 0.6*np.asarray(normalized) + 0.4*np.asarray(scoreCalculation(subway_service_scores, 1))
        # print(np.asarray(scoreCalculation(subway_service_scores, 1)))

    # (commute_scores-min(commute_scores)) / \
    # (max(commute_scores)-min(commute_scores))*100
    norm_commute_scores = {neighborhood_list[i]: v for i, v in enumerate(normalized)}
    # print(norm_commute_scores)
    mergeDict(data, norm_commute_scores, "commute score")

    all_scores=all_durations if commuteDestination else all_walkscores

    return norm_commute_scores, all_scores

def getScoreText(score):
    if(score>75.0):
        return "Excellent"
    elif(score>65.0):
        return "Good"
    elif(score>50.0):
        return "Fair"
    else:
        return "Poor"

def getTopNeighborhoods(query):

    with open("app/irsystem/controllers/data/neighborhoods.json", "r") as f:
        all_data = json.load(f)

    # with open("app/irsystem/controllers/data/niche.json", encoding="utf-8") as f:
    #     niche_data = json.load(f)

    with open("app/irsystem/controllers/data/goodmigrations.json", encoding="utf-8") as f:
        goodmigrations_data = json.load(f)

    with open("app/irsystem/controllers/data/renthop.json") as f:
        renthop_data = json.load(f)

    with open("app/irsystem/controllers/data/compass.json", encoding="utf-8") as f:
        compass_data = json.load(f)

    with open("app/irsystem/controllers/data/new_subway_scores.json") as f:
        subway_raw_data = json.load(f)

    with open("app/irsystem/controllers/data/neighborhood-attractions.json") as f:
        attractions_data = json.load(f)

    loadHappinessScores()
    calculateBudget(int(query['budget-min']), int(query['budget-max']), query['number-beds'])
    calculateAgeScore(query['age'])
    if(query['commute-destination']):
        if(gmaps.geocode(query['commute-destination'])==[]):
            query['commute-destination']=""

    _, durations=calculateCommuteScore(query['commute-type'], query['commute-destination'], query['commute-duration'], query['subway-service'])
    _, docs_with_query, valid_queries=calculateTextSimLikes(query['likes'], True)

    budget_likes_commute_score = 0.25
    age_score = 0.15
    safety_score = 0.1
    if len(query['likes']) == 0 or no_likes:
        budget_likes_commute_score = 0.32
        age_score = 0.22
        safety_score = 0.14

    neighborhood_scores = []
    for k, v in data.items():
        score = budget_likes_commute_score*v['budget score'] + age_score*v['age score'] + budget_likes_commute_score*v['commute score'] + safety_score*v['happiness score'] + (budget_likes_commute_score*v['likes score'] if len(query['likes']) > 0 and not(no_likes) else 0.0)

        neighborhood_scores.append(
            (k, score, v['budget score'], v['age score'], v['commute score'], v['happiness score'], v['likes score']))
    top_neighborhoods = sorted(
        neighborhood_scores, key=lambda x: x[1], reverse=True)
    best_matches = []
    for (name, score, budget, age, commute, safety, likes) in top_neighborhoods:
        subway_data_name = name.replace("'", "").replace(" ", "-").lower()
        subway_data = []
        curr_subway_services = sorted(subway_raw_data[subway_data_name]['Services'])
        for service in curr_subway_services:
            subway_service_name = re.sub(r"(?<=\d) Express", 'd', service)
            subway_data.append({"name": str(subway_service_name),
                                "img-url": "static/subways/" + subway_service_name.lower() + ".svg"})
        rent = {'median': renthop_data[name][query['number-beds']]['Median'], 'top': renthop_data[name]
                [query['number-beds']]['Top 25%'], 'bottom': renthop_data[name][query['number-beds']]['Bottom 25%']}
        rent_text = "1" if query['number-beds']=='1BR' else "2"
        n = {'name': name, 'score': round(score, 2), 'score-text': getScoreText(score), 'budget': round(budget, 2), 'age': round(age, 2), 'commute': round(commute, 2), 'safety': round(
            safety, 2), 'likes': round(likes, 2),  'image-url': all_data[name]['images'].split(',')[0], 'short description': goodmigrations_data[name]["short description"], 'long description': goodmigrations_data[name]["long description"].split("<br>"), 'rent': rent, 'budget order': int(renthop_data[name][query['number-beds']]['Median'].replace('$', '').replace(',', '')), 'div-id': name.lower().replace(' ', '-').replace("'", ''), "love": compass_data[name]['FALL IN LOVE']['short'] if (name in compass_data) else "", "subway": subway_data, "commute destination": query['commute-destination'].split(",")[0], "docs": docs_with_query[name] if len(query['likes']) > 0 else [], "rent text": rent_text, "attractions": attractions_data[name.lower().replace(' ', '-').replace("'", '')]}
        n['walk-duration']=durations['Walk'][name]
        n['bike-duration']=durations['Bike'][name]
        n['car-duration']=int(durations['Car'][name])
        n['transit-duration']=durations['Public Transit'][name]

        best_matches.append(n)
    return best_matches, valid_queries, query


def main():
    """
        Function will be loading all the data to update the global data variable
        """
    # output =  calculateTextSimLikes(["coffee shops", "boba"])


# main()
