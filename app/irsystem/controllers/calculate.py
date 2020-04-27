import json
import numpy as np
import re
import math
from nltk.tokenize import TreebankWordTokenizer
from sklearn import preprocessing
import os
import nltk
import en_core_web_sm

# import nltk 
from nltk.corpus import wordnet 

#from imports import * # created to make testing quicker

# from nltk.stem.porter import PorterStemmer
import googlemaps
from datetime import datetime
# nltk.download('wordnet')
# from nltk.corpus import wordnet as wn

# Full list of neighborhoods
# NOTE: if you use these as keys, you can simply update the shared data dictionary variable (data)

gmaps = googlemaps.Client(key='AIzaSyDkJTfA9iboEc6Wc1y-FEPrH3-wIBfonDE')

#import en_core_web_md
from nltk.stem.porter import PorterStemmer
nlp = en_core_web_sm.load()#en_vectors_web_lg.load()#spacy.load("en_vectors_web_lg")
stemmer = PorterStemmer()

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

n_neighborhoods = len(neighborhood_list)
treebank_tokenizer = TreebankWordTokenizer()
neighborhood_name_to_id = {}
for neighborhood_id in range(len(neighborhood_list)):
    neighborhood = neighborhood_list[neighborhood_id]
    neighborhood_name_to_id[neighborhood] = neighborhood_id
neighborhood_id_to_name = {v: k for k, v in neighborhood_name_to_id.items()}

with open("app/irsystem/controllers/data/coordinates.json", "r") as f:
    coordinates_data = json.load(f)

place_ids=[(v['geometry']['location']['lat'], v['geometry']['location']['lng']) for k,v in coordinates_data.items()]


relevant_keywords = {"Coffee Shops": ["coffee", "tea", "shops", "cafe", "cafes", "shop", "bakeries", "bookstores"],
                     "Working Out": ["gym", "gyms", "yoga", "run", "skating", "basketball", "volleyball", "running", "exercise"],
                     "Watching Movies": ["film", "theatre", "movies", "movie"],
                     "Nightlife": ["nightlife", "bars", "clubs", "rooftops", "party", "cocktail", "drinking", "partiers"],
                     "Music": ["music", "entertainment", "jazz", "performance", "performances", "concert", "talent"],
                     "Theater": ["theatre", "entertainment", "theaters", "broadway", "performances", "off-Broadway", "dance", "drama", "talent", "shows"],
                     "Restaurants": ["restaurants", "restaurant", "foodie", "foodies", "food", "eat", "eateries", "culinary", "cuisine", "bistros", "dining", "meal", "farmer's", "market", "eats", "snack"],
                     "Shopping": ["shopping", "shopper", "boutiques", "shopper's", "commercial", "fashion-forward", "fashion", "retailers", "commerce", "stores", "markets"],
                     "Art": ["art", "artsy", "architecture", "buildings", "artists", "gallery", "galleries", "artistic", "photographers", "sculptors", "painters", "trendy", "bohemian", "creative", "museum", "museums", "picturesque", "creative"],
                     "Outdoors": ["outdoors", "parks", "park", "recreation", "waterfront", "spaces", "outdoor", "tree", "flowers", "garden", "gardens", "picnics", "green", "nature", "greenspace", "open", "bike", "water", "biking", "kayaking", "boating", "piers", "pier"],
                     "Expensive": ["expensive", "pricey", "luxury", "affluent", "posh", "expensive"],
                     "Affordable": ["affordable", "inexpensive", "below-market", "diverse budgets", "cheap"],
                     "Quiet": ["quiet", "escape", "peaceful", "serene", "calm", "laid-back", "tranquil", "mellow", "low key", "low-key", "early", "secluded", "simplicity", "empty", "uncluttered", "simple", "slower", "relaxed", "grace"],
                     "Loud": ["loud", "lively", "fast-paced", "congested", "energetic", "traffic", "hustle", "noise", "vibrant", "packed", "tight"],
                     "Young": ["young", "students", "younger"],
                     "Modern": ["modern", "high-rises", "skyscrapers", "lofts", "skyline", "industrial", "posh",
                                "elevator", "doorman"],
                     "Rustic": ["old", "rustic", "pre-war", "historic", "brownstones", "historical", "walk-ups", "old-world",
                                "character"],
                     "Trendy": ["trendy", "popular", "upcoming"],
                     "College": ["college", "university", "student"]}

"""
Shared data containing all the scores and information for each neighborhood.
Scores will be a value from
Includes the following components:
    - description (of the neighborhood)
    - commute scores
    - safety/happiness score
    - budget
    - hobbies/interests
"""
data = {}
for x in neighborhood_list:
    data[x] = {}


def scoreCalculation(data_list):
    arr = np.array(data_list)
    mean = np.mean(data_list)
    std = np.std(data_list)
    if (std == 0): std = 1
    # max_score = 1.5
    # min_score = -1.5
    new_scores = []
    for x in (data_list):
        score = (x - mean)/std
        score = (score+1.5)*100/3

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

def loadCrimeScores():
    """
    Function adds in the attributes "description" and "safety_score" for each neighborhood.
    Description is pulled from the niche data
    Safety score ranges from (0-100)
    """
    # global data # declare global in order to update global data variable

    with open("app/irsystem/controllers/data/safety.json", "r") as f:
        safety_data = json.load(f)

    percentages = np.array([float(v) for k, v in safety_data.items()])
    normalized = scoreCalculation(
        percentages)  # (percentages-min(percentages)) / \
    # (max(percentages)-min(percentages))*100
    norm_safety_scores = {
        neighborhood_list[i]: v for i, v in enumerate(normalized)}
    mergeDict(data, norm_safety_scores, "safety score")
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

    # for k,v in niche_data.items():
    if not age:
        return None

    percentages = np.array([int(v["age distribution"][age_dist].replace(
        '%', '')) for k, v in niche_data.items()])

    normalized = scoreCalculation(
        percentages)  # (percentages-min(percentages)) / \
    # (max(percentages)-min(percentages))*100

    norm_age_scores = {neighborhood_list[i] : v for i, v in enumerate(normalized)}

    # data.update(norm_age_scores)
    mergeDict(data, norm_age_scores, "age score")
    return norm_age_scores


def calculateBudget(minBudget, maxBudget):
    with open("app/irsystem/controllers/data/renthop.json") as f:
        renthop_data = json.load(f)

    fit_budget = []
    top_25s = []
    bottom_25s = []
    # essentially finding percentage of homes under [min,max] range
    for k, v in renthop_data.items():

        bottom = int(v.get("Studio", v.get("1BR"))[
                     "Bottom 25%"].replace('$', '').replace(',', ''))
        median = int(v.get("Studio", v.get("1BR"))[
                     "Median"].replace('$', '').replace(',', ''))
        top = int(v.get("Studio", v.get("1BR"))[
                  "Top 25%"].replace('$', '').replace(',', ''))
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

    # keywords={}
    if maxBudget >= np.mean(np.array(top_25s)):
        expensive_scores = np.array(
            list(calculateTextSimLikes(['Expensive']).values()))
        fit_budget = fit_budget+expensive_scores

    if minBudget <= np.mean(np.array(bottom_25s)):
        affordable_scores = np.array(
            list(calculateTextSimLikes(['Affordable']).values()))
        fit_budget = fit_budget+affordable_scores

    normalized = scoreCalculation(
        fit_budget)  # (fit_budget-min(fit_budget)) / \
    # (max(fit_budget)-min(fit_budget))*100

    # for text analysis
    norm_budget_scores = {
        neighborhood_list[i]: v for i, v in enumerate(normalized)}

    # data.update(norm_budget_scores)
    mergeDict(data, norm_budget_scores, "budget score")
    return norm_budget_scores

# Activities/Likes Score Code


def tokenize(text):
    """Returns a list of words that make up the text.
    Params: {text: String}
    Returns: List
    """
    lower_case = text.lower()
    reg = re.compile(r'[a-z]+')
    result = re.findall(reg, lower_case)
    return result


def tokenize_niche(tokenize_method, input_niche, input_neighborhood):
    """Returns a list of words contained in a neighborhood's niche
       description.
    Params: {tokenize_method: Function (a -> b),
                 input_niche: JSON
             input_neighborhood: String}
    Returns: List
    """
    token_list = []
    if input_neighborhood in input_niche.keys():
        # desc = input_niche[input_neighborhood]['description']
        reviews_list = input_niche[input_neighborhood]['reviews']
        # if desc is not None:
        #     tokenized_desc = tokenize_method(desc)
        #     token_list.extend(tokenized_desc)
        if reviews_list is not None:
            for review in reviews_list:
                review_text = tokenize_method(review['text'])
                token_list.extend(review_text)
    return token_list


def tokenize_streeteasy(tokenize_method, input_streeteasy, input_neighborhood):
    """Returns a list of words contained in a neighborhood's streeteasy data.
    Params: {tokenize_method: Function (a -> b),
             input_streeteasy: JSON
             input_neighborhood: String}
    Returns: List
    """
    token_list = []
    if input_neighborhood in input_streeteasy.keys():
        desc = input_streeteasy[input_neighborhood]['description']
        mood = input_streeteasy[input_neighborhood]['the mood']
        more = input_streeteasy[input_neighborhood]['more']
        downside = input_streeteasy[input_neighborhood]['biggest downside']
        housing = input_streeteasy[input_neighborhood]['housing']
        best_perk = input_streeteasy[input_neighborhood]['best perk']
        if desc is not None:
            tokenized_desc = tokenize_method(desc)
            token_list.extend(tokenized_desc)
        if mood is not None:
            tokenized_mood = tokenize_method(mood)
            token_list.extend(tokenized_mood)
        if more is not None:
            tokenized_more = tokenize_method(more)
            token_list.extend(tokenized_more)
        if downside is not None:
            tokenized_downside = tokenize_method(downside)
            token_list.extend(tokenized_downside)
        if housing is not None:
            tokenized_housing = tokenize_method(housing)
            token_list.extend(tokenized_housing)
        if best_perk is not None:
            tokenized_perk = tokenize_method(best_perk)
            token_list.extend(tokenized_perk)
    return token_list


def tokenize_compass(tokenize_method, input_compass, input_neighborhood):
    """Returns a list of words contained in a neighborhood's compass data.
    Params: {tokenize_method: Function (a -> b),
             input_compass: JSON
             input_neighborhood: String}
    Returns: List
    """
    token_list = []
    if input_neighborhood in input_compass.keys():
        tags = input_compass[input_neighborhood]['tags']
        tags_list = ' '.join(tags)
        desc = input_compass[input_neighborhood]['description']
        lifestyle = input_compass[input_neighborhood]['THE LIFESTYLE']
        market = input_compass[input_neighborhood]['THE MARKET']
        highlight = input_compass[input_neighborhood]["FALL IN LOVE"]
        expectation = input_compass[input_neighborhood]['WHAT TO EXPECT']
        if tags_list is not None:
            tokenized_tags = tokenize_method(tags_list)
            token_list.extend(tokenized_tags)
        if desc is not None:
            tokenized_desc = tokenize_method(desc)
            token_list.extend(tokenized_desc)
        if lifestyle is not None:
            tokenized_lifestyle = tokenize_method(
                lifestyle['short'] + ' ' + lifestyle['long'])
            token_list.extend(tokenized_lifestyle)
        if market is not None:
            tokenized_market = tokenize_method(
                market['short'] + ' ' + market['long'])
            token_list.extend(tokenized_market)
        if highlight is not None:
            tokenized_highlight = tokenize_method(
                highlight['short'] + ' ' + highlight['long'])
            token_list.extend(tokenized_highlight)
        if expectation is not None:
            tokenized_expectation = tokenize_method(
                expectation['short'] + ' ' + expectation['long'])
            token_list.extend(tokenized_expectation)
    return token_list


def tokenize_reddit(tokenize_method, input_reddit, input_neighborhood):
    """Returns a list of words contained in a neighborhood's niche
       description.
    Params: {tokenize_method: Function (a -> b),
                 input_reddit: JSON
             input_neighborhood: String}
    Returns: List
    """
    token_list = []
    if input_neighborhood in input_reddit.keys():
        posts_list = input_reddit[input_neighborhood]
        if posts_list is not None:
            for post in posts_list:
                post_text = tokenize_method(post)
                token_list.extend(post_text)
    return token_list


def tokenize_goodmigrations(tokenize_method, input_goodmigrations, input_neighborhood):
    """Returns a list of words contained in a neighborhood's niche
       description.
    Params: {tokenize_method: Function (a -> b),
                 input_goodmigrations: JSON
             input_neighborhood: String}
    Returns: List
    """
    token_list = []
    if input_neighborhood in input_goodmigrations.keys():
        desc = input_goodmigrations[input_neighborhood]['short description']
        desc2 = input_goodmigrations[input_neighborhood]['long description']
        if desc is not None:
            tokenized_desc = tokenize_method(desc)
            token_list.extend(tokenized_desc)
        if desc2 is not None:
            tokenized_desc = tokenize_method(desc2)
            token_list.extend(tokenized_desc)
    return token_list


def get_neighborhood_tokens(tokenizer, data_files, tokenize_methods, input_neighborhood):
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
    tokens = tokenize_niche(tokenizer, data_files[0], input_neighborhood)
    tokens.extend(tokenize_streeteasy(
        tokenizer, data_files[1], input_neighborhood))
    tokens.extend(tokenize_compass(
        tokenizer, data_files[2], input_neighborhood))
    return tokens


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
    # creates dictionary of unique words as keys and set of neighborhoods that the word appears in
    for neighborhood in input_neighborhoods:
        tokenized_niche = set(tokenize_niche(tokenizer, data[0], neighborhood))
        tokenized_streeteasy = set(tokenize_streeteasy(
            tokenizer, data[1], neighborhood))
        tokenized_compass = set(tokenize_compass(
            tokenizer, data[2], neighborhood))
        neighborhood_tokens = tokenized_niche.union(
            tokenized_streeteasy).union(tokenized_compass)
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
                         data, tokenize_data_methods):
    """ Builds an inverted index from the messages."""
    inv_idx = {}
    for neighborhood_name, neighborhood_id in neighborhoods_to_id.items():
        tokens = get_neighborhood_tokens(
            tokenize_method, data, tokenize_data_methods, neighborhood_name)
        
        distinct_toks = set(tokens)
        for tok in distinct_toks:
            tok_count = tokens.count(tok)
            if tok not in inv_idx.keys():
                inv_idx[tok] = []
                inv_idx[tok].append((neighborhood_id, tok_count))
            else:
                term_tups = inv_idx[tok]
                term_tups.append((neighborhood_id, tok_count))
    # print(inv_idx['coffee'])
    # [(0, 1), (1, 2), (2, 1), (3, 1), (4, 1), (5, 2), (6, 2), (7, 1), (8, 1), (9, 1), (10, 1), (11, 2), (12, 3), (13, 1), (14, 1), (15, 2), (16, 1), (17, 3), (18, 2), (19, 1), (20, 2), (21, 1), (22, 1), (23, 2), (24, 1), (25, 1), (26, 2), (27, 1), (28, 4), (29, 4), (30, 1), (31, 1)]
    return inv_idx


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
            idf = math.log2(n_neighborhoods / (1 + num_postings))
            idf_dict[term] = idf
        else:
            if term=='coffee':
                print(large_frac)
                print('yeaahhh boiii')
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


def compute_query_info(query, idf, tokenizer, syn=True):
    toks = treebank_tokenizer.tokenize(query.lower())
    # get norm of query
    query_norm_inner_sum = 0

    # Replaces tokens when it cannot be found with similar words from the corpus
    # if the word is misspelled it will not be replaced
    # For example: if toks = ["asdf","dolphins"] after the loop toks = ["asdf","turtle"]
    # since turtle was the closest word it could fine. "asdf" is simply misspelled
    # uses a combination of the stem words to find the best output tokens
    query_tf = {}
    # term frequencies in query
    for tok in set(toks):
        query_tf[tok] = toks.count(tok)
    for i in range(len(toks)):
        word = toks[i]
        stem_word = stemmer.stem(word)

        w_vec =  nlp(word)
        stem_vec = nlp(stem_word)
        if (np.sum(w_vec.vector)==0) or word in idf.keys():
            continue
        elif stem_word in idf.keys():
            toks[i] = stem_word
        else:
            if syn:
                for syn in wordnet.synsets(word): 
                    for l in syn.lemmas(): 
                        if l.name() in idf:
                            print(l.name())
                            toks[i] = l.name()
                    # synonyms.append(l.name())

            # max_similarity_score = 0
            # track_word = ""
            # for k in idf.keys():
            #     k_vec = nlp(k)
            #     stem_k = nlp(stemmer.stem(k))
            #     if np.sum(k_vec.vector) == 0 and np.sum(stem_k.vector) ==0:
            #         continue # key not found in the library
            #     elif(np.sum(k_vec.vector) == 0): # if original word isn't found use stem
            #         k_vec = stem_k
            #     score = w_vec.similarity(k_vec)
            #     if (score > max_similarity_score) and score > 0.6: 
            #         max_similarity_score = score
            #         track_word = k
            # if (max_similarity_score > 0): toks[i] = track_word

    query_tf = {}
    # term frequencies in query
    for tok in set(toks):
        query_tf[tok] = toks.count(tok)

    for word in toks:
        if word in idf.keys():
            query_norm_inner_sum += math.pow(query_tf[word] * idf[word], 2)
    query_norm = math.sqrt(query_norm_inner_sum)
    return toks, query_tf, query_norm


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


def get_related_words(likes):
    related_tokens_list = []
    for like in likes:
        if like in relevant_keywords.keys():
            related_tokens_list.extend(relevant_keywords[like])
    return related_tokens_list


def calculateTextSimLikes(likes_list, merge_dict=False):
    if len(likes_list) == 0:
        norm_likes_scores = {n: 0.0 for n in neighborhood_list}

        if merge_dict:
            mergeDict(data, norm_likes_scores, "likes score")
        return norm_likes_scores

    prefix = 'app/irsystem/controllers/data/'
    query_str = ' '.join(likes_list)
    #related_words = ' '.join(get_related_words(likes_list))
    #related_words = " ".join(likes_list)
    query_extended = query_str #+ ' ' + related_words
    likes_scores = []

    with open(prefix + 'niche.json', encoding="utf-8") as niche_file, \
         open(prefix + 'streeteasy.json', encoding="utf-8") as streeteasy_file, \
         open(prefix + 'compass.json', encoding="utf-8") as compass_file, \
         open(prefix + 'relevant_data.json', encoding="utf-8") as reddit_file, \
         open(prefix + 'goodmigrations.json', encoding="utf-8") as goodmigrations_file:

        # Loading all the data
        niche_data = json.load(niche_file)
        streeteasy_data = json.load(streeteasy_file)
        compass_data = json.load(compass_file)
        reddit_data = json.load(reddit_file)
        goodmigrations_data = json.load(goodmigrations_file)

        # Compiling data and tokenization methods
        tokenize_methods = [tokenize_niche,
                            tokenize_streeteasy, 
                            tokenize_compass, 
                            tokenize_reddit, 
                            tokenize_goodmigrations]
        data_files = [niche_data, streeteasy_data,
                      compass_data, reddit_data, goodmigrations_data]

        # Information retrieval
        inv_idx = build_inverted_index(
            tokenize, neighborhood_name_to_id, data_files, tokenize_methods)
        idf = compute_idf(inv_idx, n_neighborhoods, min_df=0, max_df_ratio=0.95)
        # print('coffee' in idf)

        doc_norms = compute_neighborhood_norms(inv_idx, idf, n_neighborhoods)
        query_info = compute_query_info(query_extended, idf, treebank_tokenizer)
        print(f"query_info {query_info}")

        # score, doc id use neighborhood_id_to_name
        likes_scores = cosine_sim(
            query_info, inv_idx, idf, doc_norms, treebank_tokenizer)

    print_cossim_results(neighborhood_id_to_name, query_str, likes_scores)

    included_ids = set(likes_scores.keys())
    zero_scored_neighborhoods = list(
        set(neighborhood_id_to_name.keys()).difference(included_ids))
    for z in zero_scored_neighborhoods:
        likes_scores[z] = 0.0
    likes_scores_list = [(k, v) for k, v in likes_scores.items()]

    likes_scores = sorted(likes_scores_list, key=lambda x: x[0])
    likes_scores = np.array([l[1] for l in likes_scores])
    normalized = scoreCalculation(likes_scores)

    norm_likes_scores = {
        neighborhood_list[i]: v for i, v in enumerate(normalized)}

    if merge_dict:
        mergeDict(data, norm_likes_scores, "likes score")
    return norm_likes_scores

def calculateCommuteScore(commuteType, commuteDestination, commuteDuration):
    with open("app/irsystem/controllers/data/walkscore.json") as f:
        walkscore_data = json.load(f)
    with open("app/irsystem/controllers/data/nyc-parking-spots.json") as c:
        carscore_data = json.load(c)

    type_key = {'walk': "walk score", 'bike': "bike score", 'public transit': "transit score"}

    if commuteType.lower() in ['walk', 'bike', 'public transit']:
        commute_scores = np.array(
            [int(v['rankings'][type_key[commuteType.lower()]]) for k, v in walkscore_data.items()])
    else:
        car_scores = np.array(
            [int(v['Car-Score']) for k, v in carscore_data.items()])
        walk_scores = np.array(
            [int(v['rankings']['walk score']) for k, v in walkscore_data.items()])
        commute_scores = np.add(.2 * car_scores, .8*walk_scores)
    
    normalized = scoreCalculation(commute_scores)  

    durations=None
    
    if(commuteDestination):
        geocode_result = gmaps.geocode(commuteDestination)[0]

        travel_modes={"Walk": "walking", "Bike": "bicycling", "Car": "driving", "Public Transit": "transit"} 
        
        matrix = gmaps.distance_matrix(place_ids, (geocode_result['geometry']['location']['lat'], geocode_result['geometry']['location']['lng']), mode=travel_modes[commuteType])

        durations = {neighborhood_list[i]: int(v['elements'][0]['duration']['value']/60) for i, v in enumerate(matrix['rows'])}

        ratio=15.0/(np.array([v['elements'][0]['duration']['value']/60 for v in matrix['rows']])+1e-1)

        ratio[ratio <1.0]=ratio[ratio <1.0]/5.0

        normalized=0.2*np.array(normalized)+0.8*np.array(scoreCalculation(ratio))

    # (commute_scores-min(commute_scores)) / \
    # (max(commute_scores)-min(commute_scores))*100
    norm_commute_scores = {neighborhood_list[i]: v for i, v in enumerate(normalized)}
    mergeDict(data, norm_commute_scores, "commute score")

    # print(durations)

    return norm_commute_scores, durations

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

    loadCrimeScores()
    calculateBudget(int(query['budget-min']), int(query['budget-max']))
    calculateAgeScore(query['age'])
    _, durations=calculateCommuteScore(query['commute-type'], query['commute-destination'], query['commute-duration'])
    calculateTextSimLikes(query['likes'], True)

    totalOtherScores = 5 if len(query['likes']) > 0 else 4
    # safetyPercentage = 0.2 if len(query['likes']) > 0 else 0.25
    # safetyWeight = safetyPercentage * (int(query['safety'])/5.0)
    otherWeights = 1.0/totalOtherScores

    neighborhood_scores = []
    for k, v in data.items():
        score = otherWeights*v['budget score'] + otherWeights*v['age score'] + otherWeights*v['commute score'] + \
            otherWeights*v['safety score'] + \
            (otherWeights*v['likes score'] if len(query['likes']) > 0 else 0.0)

        neighborhood_scores.append((k, score, v['budget score'], v['age score'], v['commute score'], v['safety score'], v['likes score']))
    
    # for k, v in neighborhood_scores.items():
    #     print(k + " " + str(v))
    top_neighborhoods = sorted(neighborhood_scores, key=lambda x: x[1], reverse=True)
    best_matches = []
    for (name, score, budget, age, commute, safety, likes) in top_neighborhoods[:9]:
        subway_data = [
            {"name": "1", "img-url": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/NYCS-bull-trans-M-Std.svg/40px-NYCS-bull-trans-M-Std.svg.png"}]
        rent = {'median': renthop_data[name]['1BR']['Median'], 'top': renthop_data[name]
                ['1BR']['Top 25%'], 'bottom': renthop_data[name]['1BR']['Bottom 25%']}
        n = {'name': name, 'score': round(score, 2), 'budget': round(budget, 2), 'age': round(age, 2), 'commute': round(commute, 2), 'safety': round(
            safety, 2), 'likes': round(likes, 2),  'image-url': all_data[name]['images'].split(',')[0], 'short description': goodmigrations_data[name]["short description"], 'long description': goodmigrations_data[name]["long description"].split("<br>")[0], 'rent': rent, 'budget order': int(renthop_data[name]['1BR']['Median'].replace('$', '').replace(',', '')), 'div-id': name.lower().replace(' ', '-').replace("'", ''), "love": compass_data[name]['FALL IN LOVE']['short'] if (name in compass_data) else "", "subway": subway_data, "commute destination": query['commute-destination'].split(",")[0]}
        if(query['commute-destination']!=''):
            n['duration']= durations[name]
        else:
            n['duration']=''

        best_matches.append(n)
    return best_matches


def main():
    """
        Function will be loading all the data to update the global data variable
        """
    # query = {}
    # query["budget-min"] = "1500"
    # query["budget-max"] = "3000"
    # query["age"] = 22
    # query["commute-type"] = "walk"
    # query["likes"] = ["theatre"]
    # #a = getTopNeighborhoods(query)
    # output =  calculateTextSimLikes(query['likes'], True)

    # output =  calculateTextSimLikes(["asdf","dolphin"], True)

    # loadCrimeScores()
    # calculateBudget(1500, 1750)
    # calculateAgeScore(22)
    # calculateCommuteScore('walk')
    print(calculateTextSimLikes(['coffee']))

    # otherWeights = 1/5.0
    # neighborhood_scores = []
    # for k, v in data.items():
    #     score = otherWeights*v['budget score'] + otherWeights*v['age score'] + otherWeights*v['commute score'] + otherWeights*v['safety score'] + 0#(otherWeights*v['likes score'] if query['likes'][0]!='' else 0.0)

    #     neighborhood_scores.append(
    #         (k, score, v['budget score'], v['age score'], v['commute score'], v['safety score'], v['likes score']))
    # top_neighborhoods = sorted(
    #     neighborhood_scores, key=lambda x: x[1], reverse=True)[:9]

    # print(neighborhood_scores)
    # for ss in wn.synsets('coffee shop'): # Each synset represents a diff concept.
    #     print(ss.lemma_names())


# main()
