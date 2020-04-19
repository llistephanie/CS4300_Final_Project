import json
import numpy as np
import re
import math
from nltk.tokenize import TreebankWordTokenizer
from sklearn import preprocessing
import os

# Full list of neighborhoods
# NOTE: if you use these as keys, you can simply update the shared data dictionary variable (data)

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

relevant_keywords = {"Coffee Shops": ["coffee shops", "tea", "coffee", "cafe", "cafes", "coffee shop", "coffee stores", "bakeries", "bookstores"],
                     "Working Out": ["working out", "gym", "yoga", "run", "skating", "basketball", "volleyball", "running"],
                     "Watching Movies": ["watching movies", "movie theatre", "movies", "movie"],
                     "Nightlife": ["nightlife", "bars", "going out", "clubs", "rooftops", "party", "cocktail", "drinking", "partiers"],
                     "Music": ["music", "entertainment", "jazz", "performance", "performances", "concert", "talent"],
                     "Theater": ["theatre", "entertainment", "house theaters", "broadway", "performances", "off-Broadway", "dance", "drama", "talent", "shows"],
                     "Restaurants": ["restaurants", "restaurant", "foodie", "foodies", "food", "eat", "eateries", "culinary", "cuisine", "bistros", "dining", "meal", "farmer's market", "eats", "snack"],
                     "Shopping": ["shopping", "shopper", "boutiques", "shopper's", "commercial", "fashion-forward", "fashion", "retailers", "commerce", "stores", "markets"],
                     "Art": ["art", "artsy", "architecture", "buildings", "artists", "gallery", "galleries", "artistic", "photographers", "sculptors", "painters", "trendy", "bohemian", "creative", "museum", "museums", "picturesque", "creative"],
                     "Outdoors": ["outdoors", "parks", "park", "recreation", "waterfront", "public spaces", "outdoor spaces", "trees", "flowers", "garden", "gardens", "picnics", "green", "nature", "greenspace", "green spaces", "open spaces", "bike", "water", "biking", "kayaking", "boating", "piers", "pier"],
                     "Expensive": ["expensive", "pricey", "luxury", "affluent", "posh", "expensive"],
                     "Affordable": ["affordable", "inexpensive", "below-market", "diverse budgets", "cheap"],
                     "Quiet": ["quiet", "escape", "peaceful", "serene", "calm", "laid-back", "tranquil", "mellow", "low key", "low-key", "early to bed", "secluded", "simplicity", "empty", "uncluttered", "simple", "slower", "relaxed", "grace", "crowded"],
                     "Loud": ["loud", "lively", "fast-paced", "congested", "energetic", "traffic", "hustle", "noise", "vibrant", "packed", "tight"], 
                     "Old": ["old"], 
                     "Young": ["young", "students", "younger"], 
                     "Modern": ["modern", "high-rises", "skyscrapers", "lofts", "skyline", "industrial", "posh", "elevator", "doorman"], 
                     "Rustic": ["rustic", "pre-war", "historic", "brownstones", "historical", "walk-ups", "old-world", "character"]}

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
    normalized = (percentages-min(percentages)) / \
        (max(percentages)-min(percentages))*100
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

    with open("app/irsystem/controllers/data/niche.json") as f:
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
    # percentages=preprocessing.normalize(percentages.reshape(1, -1)).flatten()
    # [0.02673567 0.13367837 0.16041405 0.34756377 0.14704621 0.25398891
    # 0.18714972 0.13367837 0.30746026 0.24062107 0.13367837 0.12031053
    # 0.13367837 0.26735674 0.1069427  0.1069427  0.13367837 0.08020702
    # 0.45450646 0.09357486 0.08020702 0.22725323 0.09357486 0.08020702
    # 0.17378188 0.12031053 0.04010351 0.08020702 0.06683919 0.06683919
    # 0.13367837 0.08020702]

    # percentages=percentages-np.mean(percentages)/np.std(percentages)
    # [ 0.3814625  8.3814625 10.3814625 24.3814625  9.3814625 17.3814625
    # 12.3814625  8.3814625 21.3814625 16.3814625  8.3814625  7.3814625
    # 8.3814625 18.3814625  6.3814625  6.3814625  8.3814625  4.3814625
    # 32.3814625  5.3814625  4.3814625 15.3814625  5.3814625  4.3814625
    # 11.3814625  7.3814625  1.3814625  4.3814625  3.3814625  3.3814625
    # 8.3814625  4.3814625 ]

    normalized = (percentages-min(percentages)) / \
        (max(percentages)-min(percentages))*100
    # # [0.      0.25    0.3125  0.75    0.28125 0.53125 0.375   0.25    0.65625
    # # 0.5     0.25    0.21875 0.25    0.5625  0.1875  0.1875  0.25    0.125
    # # 1.      0.15625 0.125   0.46875 0.15625 0.125   0.34375 0.21875 0.03125
    # # 0.125   0.09375 0.09375 0.25    0.125  ]

    norm_age_scores = {neighborhood_list[i]                       : v for i, v in enumerate(normalized)}

    # data.update(norm_age_scores)
    mergeDict(data, norm_age_scores, "age score")
    return norm_age_scores


def calculateBudget(minBudget, maxBudget):
    with open("app/irsystem/controllers/data/renthop.json") as f:
        renthop_data = json.load(f)

    fit_budget = []
    # top_25s=[]
    # essentially finding percentage of homes under [min,max] range
    for k, v in renthop_data.items():

        bottom = int(v.get("Studio", v.get("1BR"))[
                     "Bottom 25%"].replace('$', '').replace(',', ''))
        median = int(v.get("Studio", v.get("1BR"))[
                     "Median"].replace('$', '').replace(',', ''))
        top = int(v.get("Studio", v.get("1BR"))[
                  "Top 25%"].replace('$', '').replace(',', ''))
        # top_25s.append(top)

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
    normalized = (fit_budget-min(fit_budget)) / \
        (max(fit_budget)-min(fit_budget))*100

    # keywords={}
    # if maxBudget>=mean(top_25s):
    # for text analysis
    norm_budget_scores = {
        neighborhood_list[i]: v for i, v in enumerate(normalized)}

    # data.update(norm_budget_scores)
    mergeDict(data, norm_budget_scores, "budget score")
    return norm_budget_scores


def calculateCommuteScore(commuteType):
    with open("app/irsystem/controllers/data/walkscore.json") as f:
        walkscore_data = json.load(f)
    type_key = {'walk': "walk score", 'bike': "bike score",
                'public transit': "transit score", 'car': "transit score"}

    commute_scores = np.array(
        [int(v['rankings'][type_key[commuteType.lower()]]) for k, v in walkscore_data.items()])
    normalized = (commute_scores-min(commute_scores)) / \
        (max(commute_scores)-min(commute_scores))*100
    norm_commute_scores = {
        neighborhood_list[i]: v for i, v in enumerate(normalized)}
    mergeDict(data, norm_commute_scores, "commute score")
    return norm_commute_scores

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
        desc = input_niche[input_neighborhood]['description']
        reviews_list = input_niche[input_neighborhood]['reviews']
        if desc is not None:
            tokenized_desc = tokenize_method(desc)
            token_list.extend(tokenized_desc)
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
            tokenized_lifestyle = tokenize_method(lifestyle['short'] + ' ' + lifestyle['long'])
            token_list.extend(tokenized_lifestyle)
        if market is not None:
            tokenized_market = tokenize_method(market['short'] + ' ' + market['long'])
            token_list.extend(tokenized_market)
        if highlight is not None:
            tokenized_highlight = tokenize_method(highlight['short'] + ' ' + highlight['long'])
            token_list.extend(tokenized_highlight)
        if expectation is not None:
            tokenized_expectation = tokenize_method(expectation['short'] + ' ' + expectation['long'])
            token_list.extend(tokenized_expectation)
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
    tokens.extend(tokenize_streeteasy(tokenizer, data_files[1], input_neighborhood))
    tokens.extend(tokenize_compass(tokenizer, data_files[2], input_neighborhood))
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
        tokenized_niche= set(tokenize_niche(tokenizer, data[0], neighborhood))
        tokenized_streeteasy = set(tokenize_streeteasy(tokenizer, data[1], neighborhood))
        tokenized_compass = set(tokenize_compass(tokenizer, data[2], neighborhood))
        neighborhood_tokens = tokenized_niche.union(tokenized_streeteasy).union(tokenized_compass)
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
    all_words = input_word_matrix[neighborhood_n,:]
    total_num_words = np.sum(all_words)
    return w_freq/(total_num_words + 1)

def build_inverted_index(tokenize_method,
                         neighborhoods_to_id,
                         data,
                         tokenize_data_methods):
    """ Builds an inverted index from the messages."""
    inv_idx = {}
    for neighborhood_name, neighborhood_id in neighborhoods_to_id.items():
        tokens = get_neighborhood_tokens(tokenize_method, data, tokenize_data_methods, neighborhood_name)
        distinct_toks = set(tokens)
        for tok in distinct_toks:
            tok_count = tokens.count(tok)
            if tok not in inv_idx.keys():
                inv_idx[tok] = []
                inv_idx[tok].append((neighborhood_id, tok_count))
            else:
                term_tups = inv_idx[tok]
                term_tups.append((neighborhood_id, tok_count))
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
    return idf_dict

def compute_norms(index, idf, n_neighborhoods):
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


def cosine_sim(query, index, idf, doc_norms, tokenizer):
    """ Search the collection of documents for the given query based on cosine similarity

    Arguments
    =========
    query: string,
        The query we are looking for.

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
    query_toks = tokenizer.tokenize(query.lower())
    query_tf = {}

    # term frequencies in query
    for tok in set(query_toks):
        query_tf[tok] = query_toks.count(tok)
    # get norm of query
    query_norm_inner_sum = 0
    for word in query_toks:
        if word in idf.keys():
            query_norm_inner_sum += math.pow(query_tf[word] * idf[word] , 2)
    query_norm = math.sqrt(query_norm_inner_sum)

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
    divide_dict = { k: v/(doc_norms[k] * query_norm) for k, v in score_dict.items() }
    return {k: v for k, v in sorted(divide_dict.items(), key=lambda tup: tup[1], reverse=True)}
    # to_list = [(k, v) for k, v in divide_dict.items()]
    # to_list.sort(key=lambda tup: tup[1], reverse=True)
    # return to_list


def print_cossim_results(id_to_neighborhoods, query, results):
    print("#" * len(query))
    print(query)
    print("#" * len(query))
    for score, neighborhood_id in results[:10]:
        print("[{:.2f}] {})".format(score, id_to_neighborhoods[neighborhood_id]))
        print()


def calculateTextSimLikes(likes_list):
    prefix = 'app/irsystem/controllers/data/'
    query_str = ' '.join(likes_list)
    with open(prefix + 'niche.json') as niche_file, open(prefix + 'streeteasy.json') as streeteasy_file, open(prefix + 'compass.json') as compass_file, open(prefix + 'reddit_data.json') as reddit_file:
        niche_data = json.load(niche_file)
        streeteasy_data = json.load(streeteasy_file)
        compass_data = json.load(compass_file)
        tokenize_methods = [tokenize_niche, tokenize_streeteasy, tokenize_compass]
        data_files = [niche_data, streeteasy_data, compass_data]
        neighborhood_name_to_id = {}
        for neighborhood_id in range(len(neighborhood_list)):
            neighborhood = neighborhood_list[neighborhood_id]
            neighborhood_name_to_id[neighborhood] = neighborhood_id
        neighborhood_id_to_name = {v:k for k,v in neighborhood_name_to_id.items()}
        inv_idx = build_inverted_index(tokenize, neighborhood_name_to_id, data_files, tokenize_methods, neighborhood_list)
        idf = compute_idf(inv_idx, n_neighborhoods, min_df=0, max_df_ratio=0.95)
        doc_norms = compute_norms(inv_idx, idf, n_neighborhoods)
        return cosine_sim(query_str, inv_idx, idf, doc_norms, treebank_tokenizer)



# def main():
#     """
# 	Function will be loading all the data to update the global data variable
# 	"""
#     # load_crime_and_descriptions()
#     calculateBudget(1500, 1750)
#     calculateAgeScore(22)
#     calculateCommuteScore('walk')
#     print(data)

# main()

def getTopNeighborhoods(query):

    with open("app/irsystem/controllers/data/neighborhoods.json", "r") as f:
        all_data = json.load(f)

    with open("app/irsystem/controllers/data/niche.json") as f:
        niche_data = json.load(f)

    loadCrimeScores()
    calculateBudget(int(query['budget-min']), int(query['budget-max']))
    calculateAgeScore(query['age'])
    calculateCommuteScore(query['commute-type'])
    calculateTextSimLikes(query['likes'])
    safetyWeight = 0.25*(int(query['safety'])/5)
    otherWeights = (1.0-safetyWeight)/3

    neighborhood_scores = []
    for k, v in data.items():
        score = otherWeights*v['budget score']+otherWeights*v['age score'] + \
            otherWeights*v['commute score']+safetyWeight*v['safety score']
        neighborhood_scores.append((k, score))
    top_neighborhoods = sorted(
        neighborhood_scores, key=lambda x: x[1], reverse=True)[:10]

    best_matches = []
    for (name, score) in top_neighborhoods:
        n = {'name': name, 'score': round(score, 2), 'image-url': all_data[name]['images'].split(
            ',')[0], 'description': niche_data[name]['description']}
        best_matches.append(n)
    return best_matches