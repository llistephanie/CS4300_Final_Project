
import csv
import json
import re
from nltk.tokenize import sent_tokenize, word_tokenize
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

punctuation = ['.','!',',','?',')','(','"',"'",'[',']']
full_name = ['battery park',
                         'chelsea',
                         'chinatown',
                         'civic center',
                         'east harlem',
                         'east village',
                         'financial district',
                         'flatiron',
                         'gramercy',
                         'greenwich village',
                         'harlem',
                         "hell's kitchen",
                         'inwood',
                         'kips bay',
                         'little italy',
                         'lower east side',
                         'marble hill',
                         'midtown',
                         'morningside heights',
                         'murray hill',
                         'noho',
                         'nolita',
                         'roosevelt island',
                         'soho',
                         'stuyvesant town',
                         'theater district',
                         'tribeca',
                         'two bridges',
                         'upper east side',
                         'upper west side',
                         'washington heights',
                         'west village']

neighborhood_list = ['battery park',
                         'chelsea',
                         'chinatown',
                         'civic',
                         'east harlem',
                         'east village',
                         'financial district',
                         'flatiron',
                         'gramercy',
                         'greenwich',
                         'harlem',
                         "hell's kitchen",
                         'inwood',
                         'kips bay',
                         'little italy',
                         'lower east',
                         'marble hill',
                         'midtown',
                         'morningside',
                         'murray',
                         'noho',
                         'nolita',
                         'roosevelt',
                         'soho',
                         'stuyvesant',
                         'theater district',
                         'tribeca',
                         'two bridges',
                         'upper east',
                         'upper west',
                         'washington heights',
                         'west village']
name_mapping = {}
for x in range(len(full_name)):
    name_mapping[neighborhood_list[x]] = full_name[x]

def creatingNeighborhoods():
    post_mapping = {}
    


    key_list = []
    for i in neighborhood_list:
        key = mergeList((preprocessing(i)))
        post_mapping[key] = []
        key_list.append(key)
    return key_list, post_mapping

def mergeList(l):
    s = ""
    for x in l:
        if (x[0] == "'" or x[0] == '"' ):
            s +=x
        else:
            s+= " " + x
    return s.strip()

def checkingMatchText(neighborhood_mapping, text_list):
    joined_text = mergeList(text_list)

    text_used = False
    for k,v in neighborhood_mapping.items():
        if(joined_text.count(k) > 0):
            text_used = True
            v.append(joined_text)
    return text_used


def readData(neighborhood_mapping):
    data = {}
    with open("maximum.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    total = len(data)

    counter = 0 

    for post_id, post_data in data.items():
        p_text = post_data['title'] + ' ' + post_data['body']
        p_text = p_text.lower()

        # Comment Analyzer
        total += len(post_data["comments"])
        for c in post_data["comments"]:
            c_text = c["body"].lower()
            cleaned_c_text = preprocessing(c_text)

            used = checkingMatchText(neighborhood_mapping, cleaned_c_text)
            counter+= int(used)

        # Post Analyzer
        cleaned_p_text = preprocessing(p_text)
        used = checkingMatchText(neighborhood_mapping, cleaned_p_text)

        counter+=int(used)

    print("Total entries = " + str(total))
    print("Posts used " + str(counter))
    return data

def preprocessing(text):
    cleaned_text = re.sub(r"http\S+", "", text.lower())
    tokens = word_tokenize(cleaned_text)

    cleaned_tokens = []
    for t in tokens:
        if t == " " or t in punctuation:
            continue
        cleaned_tokens.append(t)
    return cleaned_tokens

def sentiment_analysis(data_list):
    # https://github.com/cjhutto/vaderSentiment
    analyzer = SentimentIntensityAnalyzer()

    length = 0
    score = 0 

    for x in data_list:
        # for the niche data
        if (isinstance(x, dict)):
            x = x["text"]
        sentence_list = sent_tokenize(x)
        length+=len(sentence_list)

        for s in sentence_list:
            score+=analyzer.polarity_scores(s)["compound"]
        # pos if score >= 0.05, neg if <= -0.05, neutral otherwise

    return float(score) / length

def getRelevant():
    key_list, neighborhood_mapping = creatingNeighborhoods()
    data = readData(neighborhood_mapping)
    counter = 0 

    """
    new_data = {}
    for k,v in neighborhood_mapping.items():
        index = key_list.index(k)
        key = full_name[index]
        counter += len(v)

        new_data[key] = []
        for item in v:
            new_data[key].append(data[item])

        #print(k + "  " + str(len(v)))
    """
    reddit_data = {}
    for k,v in neighborhood_mapping.items():
        reddit_data[name_mapping[k]] = v

    with open("relevant_data.json","w") as f:
        json.dump(reddit_data, f)

def test():
    with open("relevant_data.json","r") as f:
        data = json.load(f)

    counter =0 
    for k,v in data.items():
        counter+=len(v)
    print(counter)

def main():
    with open("relevant_data.json","r") as f:
        data = json.load(f)
    counter = 0 

    ### Notes: there could be more processing on the data
    ### some posts double counts since multiple tags of neighborhoods.
    sentiment_scores = {}

    with open("niche.json", "r", encoding="utf-8") as f:
        niche_data = json.load(f)

    switch = {
        'A+': 96.67,
        'A': 93.33,
        'A-': 90.00,
        'B+': 86.87,
        'B': 83.33,
        'B-': 80.00,
        'C+': 76.67,
        'C': 73.33,
        'C-': 70.00,
        'D': 65.00,
        'F': 0.00
    }

    for key,value in niche_data.items():
        k = key.lower()
        v = data[k]
        allData = v + value["reviews"]
        niche_score = value['scores']["Crime & Safety"]


        score = sentiment_analysis(allData)
        sentiment_scores[k] = {}
        sentiment_scores[k]["description"] = value["description"]
        sentiment_scores[k]["crime"] = switch[niche_score]
        sentiment_scores[k]["sentiment"] = score
        sentiment_scores[k]["num_reviews"] = len(v) + len(value["reviews"])
        length = len(v) + len(value["reviews"])
        print(k +" - " + '{:.3f}'.format(score) + ", " + str(length))

    with open("sentiment_scores.json","w") as f:
        json.dump(sentiment_scores, f)
    #print(sentiment_scores)
#getRelevant()
#main()
correct_name = ['Battery Park',
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
                     'Kips bay',
                     'Little Italy',
                     'Lower East Side',
                     'Marble Hill',
                     'Midtown',
                     'Morningside Heights',
                     'Murray Hill',
                     'Noho',
                     'Nolita',
                     'Roosevelt Island',
                     'Soho',
                     'Stuyvesant Town',
                     'Theater District',
                     'Tribeca',
                     'Two Bridges',
                     'Upper East Side',
                     'Upper West Side',
                     'Washington Heights',
                     'West Village']

final_keys = {}
for x in range(len(full_name)):
    final_keys[full_name[x]] = correct_name[x]

def analysis():
    with open("sentiment_scores.json","r") as f:
        data = json.load(f)

        total = 0
        for k, v in data.items():
            total+=v["num_reviews"]

        avg_post = total/len(data)
        print(avg_post)
        final_data = {}
        for k, v in data.items():
            sentiment_weight = 0.9
            crime_weight = 0.1
            if v["num_reviews"] < avg_post:
                sentiment_weight *= (v["num_reviews"]/avg_post)
                crime_weight = 1 - sentiment_weight

            sent_score = (v["sentiment"]+1)*100/2.0 # changing range from -1 to 1 to 0 to 100

            combined_score = sentiment_weight * sent_score + crime_weight * v["crime"] # out of 100
            v["final_score"] = combined_score

            print(k + " " + str(combined_score))

            new_k = final_keys[k]
            final_data[new_k] = {}
            final_data[new_k]["description"] = v["description"]
            final_data[new_k]["safety_score"] = v["final_score"]
            #print(sentiment_weight)
            #print(crime_weight)

    with open("safety.json","w") as f:
        json.dump(final_data, f)
analysis()