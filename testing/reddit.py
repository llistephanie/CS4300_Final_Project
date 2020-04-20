import praw
import json
from praw.models import MoreComments


#import requests 
#import requests.auth

u_agent = "testing user"
print("Enter your Reddit username: ")
username = input()
print("Enter your password ")
password = input()


reddit = praw.Reddit(client_id='qFoEh9MIfLA75Q',
                     client_secret='1alqN5SAAVLx0QsFExjHH1f_8QQ',
                     user_agent=u_agent,
                     username=username,
                     password=password)
reddit.read_only = True

"""
subreddit = reddit.subreddit("nyc")
print(subreddit.id)
try:
    print(subreddit.display_name)  # Output: redditdev
    print(subreddit.title)         # Output: reddit Development
    print(subreddit.description)   # Output: A subreddit for discussion of ...
except:
    print("error")
"""
def getSubmission(post_id, save=False):
    submission = reddit.submission(id=post_id)
    data = {}
    data[post_id] = {}
    entry = data[post_id]
    entry["subreddit_id"] = submission.subreddit.id
    entry['title'] = submission.title
    entry['body'] = submission.selftext
    entry["upvote_ratio"] = float(submission.upvote_ratio)

    #original_content = submission.is_original_content # Whether submission is set as original content
    entry["upvotes"] = int(submission.score)
    #url = submission.url
    #writer1.writerow([subreddit_id, post_id, title, body, distinguished, original_content, upvote_ratio, upvotes, url])
    
    entry["comments"] = []

    for comment in submission.comments:
        if isinstance(comment, MoreComments):
            continue

        c_dict = {}
        c_dict["comment_id"] = comment.id
        c_dict["body"] = comment.body
        c_dict["upvotes"] = int(comment.score)
        entry["comments"].append(c_dict)
    if (save):
        with open("maximum.json", "r+") as file:
            d = json.load(file)
            if (post_id in d):
                return
            d.update(data)
            file.seek(0)
            json.dump(d,file)
    
    return data

addTolist = ["brvwn2","81t97o","5ayguz","cqrp5","5tioig","aiw1r4","922xba","97t6w9","e36x4s"]
for x in addTolist:
    getSubmission(x, save = True)

print("Starting data download...")
data = {}
def get_posts(subreddit, subreddit_id):
    # https://praw.readthedocs.io/en/latest/code_overview/models/submission.html#praw.models.Submission
    global data

    for submission in subreddit.hot(limit=None):
        #distinguished = submission.distinguished # whether the submission is distinguished
        
        post_id = submission.id
        data[post_id] = {}
        entry = data[post_id]
        entry["subreddit_id"] = subreddit_id
        entry['title'] = submission.title
        entry['body'] = submission.selftext
        entry["upvote_ratio"] = float(submission.upvote_ratio)

        #original_content = submission.is_original_content # Whether submission is set as original content
        entry["upvotes"] = int(submission.score)
        #url = submission.url
        #writer1.writerow([subreddit_id, post_id, title, body, distinguished, original_content, upvote_ratio, upvotes, url])
        
        entry["comments"] = []

        for comment in submission.comments:
            if isinstance(comment, MoreComments):
                continue

            c_dict = {}
            c_dict["comment_id"] = comment.id
            c_dict["body"] = comment.body
            c_dict["upvotes"] = int(comment.score)
            entry["comments"].append(c_dict)
            
            #c_url = comment.permalink
            #writer2.writerow([post_id, c_id, c_body, c_score, c_url])

    for submission in subreddit.top(limit=None):
        #distinguished = submission.distinguished # whether the submission is distinguished
        if post_id in data:
            continue
        post_id = submission.id
        data[post_id] = {}
        entry = data[post_id]
        entry["subreddit_id"] = subreddit_id
        entry['title'] = submission.title
        entry['body'] = submission.selftext
        entry["upvote_ratio"] = float(submission.upvote_ratio)

        #original_content = submission.is_original_content # Whether submission is set as original content
        entry["upvotes"] = int(submission.score)
        #url = submission.url
        #writer1.writerow([subreddit_id, post_id, title, body, distinguished, original_content, upvote_ratio, upvotes, url])
        
        entry["comments"] = []

        for comment in submission.comments:
            if isinstance(comment, MoreComments):
                continue

            c_dict = {}
            c_dict["comment_id"] = comment.id
            c_dict["body"] = comment.body
            c_dict["upvotes"] = int(comment.score)
            entry["comments"].append(c_dict)
            
            #c_url = comment.permalink
            #writer2.writerow([post_id, c_id, c_body, c_score, c_url])

    for submission in subreddit.new(limit=None):
        #distinguished = submission.distinguished # whether the submission is distinguished
        if post_id in data:
            continue
        post_id = submission.id
        data[post_id] = {}
        entry = data[post_id]
        entry["subreddit_id"] = subreddit_id
        entry['title'] = submission.title
        entry['body'] = submission.selftext
        entry["upvote_ratio"] = float(submission.upvote_ratio)

        #original_content = submission.is_original_content # Whether submission is set as original content
        entry["upvotes"] = int(submission.score)
        #url = submission.url
        #writer1.writerow([subreddit_id, post_id, title, body, distinguished, original_content, upvote_ratio, upvotes, url])
        
        entry["comments"] = []

        for comment in submission.comments:
            if isinstance(comment, MoreComments):
                continue

            c_dict = {}
            c_dict["comment_id"] = comment.id
            c_dict["body"] = comment.body
            c_dict["upvotes"] = int(comment.score)
            entry["comments"].append(c_dict)
            
            #c_url = comment.permalink
            #writer2.writerow([post_id, c_id, c_body, c_score, c_url])
    
    

def readFile():
    with open("subreddit_list.txt","r",encoding="utf-8") as r:
        subreddit_list = r.read().splitlines()
    return subreddit_list

def main():
    global data
    subreddit_list = readFile()
    """
    with open("post_data.json", "w", encoding="utf-8") as f1, open("comment_data.csv","w",encoding="utf-8") as f2:
        writer1 = csv.writer(f1, delimiter=",", quotechar = '"')
        writer1.writerow(["subreddit_id", "submission_id", "title", "body", "distinguished","original content", "upvote ratio","upvotes","url"])

        writer2 = csv.writer(f2, delimiter=",", quotechar = '"')
        writer2.writerow(["submission_id", "comment_id","body","upvotes","url"])
        
        for s in subreddit_list:
            subreddit = reddit.subreddit(s)
            try:
                get_posts(writer1, writer2, subreddit, subreddit.id)
            except:
                print("Could not retrieve: Subreddit " + s)
    """
    for s in subreddit_list:
        subreddit = reddit.subreddit(s)
        get_posts(subreddit, subreddit.id)

    

    with open("maximum.json", "w") as f:
        json.dump(data, f)
        print(len(data))



#main()


