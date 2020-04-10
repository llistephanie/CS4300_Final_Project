import praw
import csv

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

print("Starting data download...")

def get_posts(writer1, writer2, subreddit, subreddit_id):
    # https://praw.readthedocs.io/en/latest/code_overview/models/submission.html#praw.models.Submission
    for submission in subreddit.hot(limit=200):
        title = submission.title
        body = submission.selftext
        distinguished = submission.distinguished # whether the submission is distinguished
        post_id = submission.id
        original_content = submission.is_original_content # Whether submission is set as original content
        upvote_ratio = submission.upvote_ratio
        upvotes = submission.score
        url = submission.url

        writer1.writerow([subreddit_id, post_id, title, body, distinguished, original_content, upvote_ratio, upvotes, url])

        for comment in submission.comments:
            c_id = comment.id
            c_body = comment.body
            c_subredditid = comment.subreddit_id
            c_score = comment.score
            c_url = comment.permalink

            writer2.writerow([post_id, c_id, c_body, c_score, c_url])
    

def readFile():
    with open("subreddit_list.txt","r",encoding="utf-8") as r:
        subreddit_list = r.read().splitlines()
    return subreddit_list

def main():
    subreddit_list = readFile()
    
    with open("post_data.csv", "w", encoding="utf-8") as f1, open("comment_data.csv","w",encoding="utf-8") as f2:
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

main()


