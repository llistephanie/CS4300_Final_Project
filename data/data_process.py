
import csv
import json


def readData():
	data = {}
	with open("post_data.csv", "r", encoding="utf-8") as post_data:#, open("comment_data.csv","w",encoding="utf-8") as comment_data:
		
		post_reader = csv.DictReader(post_data,fieldnames=('subreddit_id', 'post_id', 'title','body','upvote_ratio','upvotes'))
		#comment_reader = csv.DictReader(comment_data)
		
		next(post_reader)
		for line in post_reader:
			post_id = line['post_id']
			entry = data[post_id] = {}

			entry["subreddit_id"] = line['subreddit_id']
			entry["title"] = line['title']
			entry["body"] = line['body']
			entry["upvote_ratio"] = (line['upvote_ratio'])
			entry["upvotes"] = (line['upvotes'])
			entry["comments"] = []

			break
	return data

data = readData()
print(data)