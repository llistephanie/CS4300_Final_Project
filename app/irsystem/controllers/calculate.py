import json
import numpy as np
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
    for k,v in updates.items():
        new_val={key_name: v}
        original[k].update(new_val)

def loadCrimeScores():
	"""
	Function adds in the attributes "description" and "safety_score" for each neighborhood.
	Description is pulled from the niche data
	Safety score ranges from (0-100)
	"""
	# global data # declare global in order to update global data variable
    
	with open("app/irsystem/controllers/data/safety.json","r") as f:
		input_data = json.load(f)
	mergeDict(data, input_data, "safety score")
	return input_data
	# data.update(input_data)

def calculateAgeScore(age):
    """
    Input:
        age         value (int) if user included it, None otherwise
    
    Output:
        age_scores  dictionary indexed by neighborhood of score (0-100) assigned to each
    """

    print(f"[AGE] {data}")
    if age=='':
        age=24
    else:
        age=int(age)

    with open("app/irsystem/controllers/data/niche.json") as f:
        niche_data = json.load(f)
    
    age_dist=["<10 years", "10-17 years", "18-24 years", "25-34 years", "35-44 years", "45-54 years", "55-64 years","65+ years"]

    age_dist=""
    if age<10:
        age_dist="<10 years"
    elif age<=17:
        age_dist="10-17 years"
    elif age<=24:
        age_dist="18-24 years"
    elif age<=34:
        age_dist="25-34 years"
    elif age<=44:
        age_dist="35-44 years"
    elif age<=54:
        age_dist="45-54 years"
    elif age<=64:
        age_dist="55-64 years"
    else:
        age_dist="65+ years"

    # for k,v in niche_data.items():
    if not age:
        return None

    percentages=np.array([int(v["age distribution"][age_dist].replace('%', '')) for k,v in niche_data.items()])
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

    normalized=(percentages-min(percentages))/(max(percentages)-min(percentages))*100
    # # [0.      0.25    0.3125  0.75    0.28125 0.53125 0.375   0.25    0.65625
    # # 0.5     0.25    0.21875 0.25    0.5625  0.1875  0.1875  0.25    0.125
    # # 1.      0.15625 0.125   0.46875 0.15625 0.125   0.34375 0.21875 0.03125
    # # 0.125   0.09375 0.09375 0.25    0.125  ]

    norm_age_scores={ neighborhood_list[i] :v for i,v in enumerate(normalized)}

    # data.update(norm_age_scores)
    mergeDict(data, norm_age_scores, "age score")
    return norm_age_scores

def calculateBudget(minBudget, maxBudget):
    with open("app/irsystem/controllers/data/renthop.json") as f:
        renthop_data = json.load(f)

    fit_budget=[]
    print(f"[BUDGET] {data}")
    # top_25s=[]
    # essentially finding percentage of homes under [min,max] range 
    for k,v in renthop_data.items():

        bottom=int(v.get("Studio", v.get("1BR"))["Bottom 25%"].replace('$','').replace(',', ''))
        median=int(v.get("Studio", v.get("1BR"))["Median"].replace('$','').replace(',', ''))
        top=int(v.get("Studio", v.get("1BR"))["Top 25%"].replace('$','').replace(',', ''))
        # top_25s.append(top)

        my_range=set(list(range(minBudget, maxBudget)))
        n_range=set(list(range(bottom, top)))

        intersect=my_range.intersection(n_range)
        percentage_points=50.0/(top-bottom)
        
        if(len(intersect)==0):
            fit_budget.append(0)
        else:
            fit_budget.append((max(intersect)-min(intersect))*percentage_points)

    fit_budget=np.array(fit_budget)
    normalized=(fit_budget-min(fit_budget))/(max(fit_budget)-min(fit_budget))*100

    # keywords={}
    # if maxBudget>=mean(top_25s):
        # for text analysis
    norm_budget_scores={ neighborhood_list[i] :v for i,v in enumerate(normalized)}

    # data.update(norm_budget_scores)
    mergeDict(data, norm_budget_scores, "budget score")
    return norm_budget_scores

def calculateCommuteScore(commuteType):
    with open("app/irsystem/controllers/data/walkscore.json") as f:
        walkscore_data = json.load(f)
    
    print(f"[COMMUTE] {data}")
    
    type_key={'walk': "walk score", 'bike': "bike score", 'public transit': "transit score", 'car': "transit score"}

    commute_scores=np.array([int(v['rankings'][type_key[commuteType.lower()]]) for k,v in walkscore_data.items()])
    normalized=(commute_scores-min(commute_scores))/(max(commute_scores)-min(commute_scores))*100
    norm_commute_scores={ neighborhood_list[i] :v for i,v in enumerate(normalized)}
    mergeDict(data, norm_commute_scores, "commute score")
    return norm_commute_scores

def getTopNeighborhoods(query):

    with open("app/irsystem/controllers/data/neighborhoods.json","r") as f:
        all_data = json.load(f)
    
    with open("app/irsystem/controllers/data/niche.json") as f:
        niche_data = json.load(f)
    
    loadCrimeScores()
    calculateBudget(int(query['budget-min']), int(query['budget-max']))
    calculateAgeScore(query['age'])
    calculateCommuteScore(query['commute-type'])
    safetyWeight=0.25*(int(query['safety'])/5)
    otherWeights=(1.0-safetyWeight)/3


    neighborhood_scores=[]
    for k,v in data.items():
        print(v['safety score'])
        score=otherWeights*v['budget score']+otherWeights*v['age score']+otherWeights*v['commute score']+safetyWeight*v['safety score']
        neighborhood_scores.append((k,score))
    top_neighborhoods=sorted(neighborhood_scores, key = lambda x: x[1], reverse=True)[:10]

    best_matches=[]
    for (name,score) in top_neighborhoods:
        n={'name': name, 'score': round(score, 2), 'image-url': all_data[name]['images'].split(',')[0], 'description': niche_data[name]['description']}
        best_matches.append(n)
    return best_matches

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
