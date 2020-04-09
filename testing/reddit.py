import praw
import requests 
import requests.auth

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

subreddit = reddit.subreddit('nyc')

print(subreddit.display_name)  # Output: redditdev
print(subreddit.title)         # Output: reddit Development
print(subreddit.description)   # Output: A subreddit for discussion of ...

print("STARTING ")
for submission in subreddit.hot(limit=10):
    print(submission.title)  # Output: the submission's title
    print(submission.score)  # Output: the submission's score
    print(submission.id)     # Output: the submission's ID
    print(submission.url)    # Output: the URL the submission points to
                             # or the submission's URL if it's a self post
    submission.comment_sort = 'new'
    comments = list(submission.comments)
