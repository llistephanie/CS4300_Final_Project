
import csv
import json
import re
from nltk.tokenize import word_tokenize

punctuation = ['.','!',',','?',')','(','"',"'",'[',']']
def creatingNeighborhoods():
	post_mapping = {}
	neighborhood_list = ['battery park',
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
	#smoothing will be necessary 
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
	for i in neighborhood_list:
		key = " ".join(preprocessing(i))
		post_mapping[key] = []
	return post_mapping

def readData(neighborhood_mapping):
	data = {}
	with open("reddit_data.json", "r", encoding="utf-8") as f:
		data = json.load(f)
	print("Total entries = " + str(len(data)))

	counter = 0 
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

def main():
	neighborhood_mapping = creatingNeighborhoods()
	reddit_data = readData(neighborhood_mapping)
	counter = 0 

	for k,v in neighborhood_mapping.items():
		counter += len(v)
		print(k + "  " + str(len(v)))


main()