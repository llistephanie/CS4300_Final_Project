
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

def creatingNeighborhoods():
    post_mapping = {}
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
    key_list = []
    for i in neighborhood_list:
        key = " ".join(preprocessing(i))
        post_mapping[key] = []
        key_list.append(key)
    return key_list, post_mapping

def readData(neighborhood_mapping):
    data = {}
    with open("maximum.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    print("Total entries = " + str(len(data)))

    counter = 0 
    new_data = {}
    for post_id, post_data in data.items():
        text = post_data['title'] + ' ' + post_data['body']
        text = text.lower()
        for c in post_data["comments"]:
            c_text = c["body"].lower()
            text += ' ' + c_text
        cleaned_text = preprocessing(text)
        data[post_id]["text"] = cleaned_text

        post_used = False
        for k,v in neighborhood_mapping.items():
            joined_text = " ".join(cleaned_text)
            count = joined_text.count(k)

            if count > 0:
                post_used = True
                neighborhood_mapping[k].append(post_id)
                
        if post_used:
            counter+=1
    print("Posts used " + str(counter))
    return data, neighborhood_mapping

def preprocessing(text):
    cleaned_text = re.sub(r"http\S+", "", text.lower())
    tokens = word_tokenize(cleaned_text)

    cleaned_tokens = []
    for t in tokens:
        if t == " " or t in punctuation:
            continue
        cleaned_tokens.append(t)
    return cleaned_tokens

def sentiment_analysis(post_list, niche_list):
    # https://github.com/cjhutto/vaderSentiment
    analyzer = SentimentIntensityAnalyzer()

    cumulative_score = 0
    for post in post_list:
        body = post["body"]
        sentence_list = sent_tokenize(body)
        comments = post["comments"]
        for c in comments:
            sentence_list.append(sent_tokenize(c["body"]))
        #print(sentence_list)

        score = 0 
        for s in sentence_list:
            score+=analyzer.polarity_scores(s)["compound"]
        
        if (len(sentence_list) != 0): score /= len(sentence_list)

        cumulative_score +=score
        # pos if score >= 0.05, neg if <= -0.05, neutral otherwise

    for review in niche_list:
        sentence_list = sent_tokenize(review["text"])
        score = 0 
        for s in sentence_list:
            score+=analyzer.polarity_scores(s)["compound"]

        if (len(sentence_list) != 0): score /= len(sentence_list)
        cumulative_score +=score

    return cumulative_score / (len(post_list) + len(niche_list))

def getRelevant():
    key_list, neighborhood_mapping = creatingNeighborhoods()
    data, reddit_data = readData(neighborhood_mapping)
    counter = 0 

    new_data = {}
    for k,v in neighborhood_mapping.items():
        index = key_list.index(k)
        key = full_name[index]
        counter += len(v)

        new_data[key] = []
        for item in v:
            new_data[key].append(data[item])
        #print(k + "  " + str(len(v)))

    with open("relevant_data.json","w") as f:
        json.dump(new_data, f)

def main():
    with open("relevant_data.json","r") as f:
        data = json.load(f)
    counter = 0 

    ### Notes: there could be more processing on the data
    ### some posts double counts since multiple tags of neighborhoods.
    sentiment_scores = {}

    with open("niche.json", "r", encoding="utf-8") as f:
        niche_data = json.load(f)

    for key,value in niche_data.items():
        k = key.lower()
        v = data[k]
        score = sentiment_analysis(v, value["reviews"])
        sentiment_scores[k] = {}
        sentiment_scores[k]["score"] = score
        sentiment_scores[k]["post_num"] = len(v)
        length = len(v) + len(value["reviews"])
        print(k +" - " + '{:.3f}'.format(score) + ", " + str(length))
    #print(sentiment_scores)
#getRelevant()

main()