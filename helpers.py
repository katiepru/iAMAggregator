import pymongo
import praw
import json
#from config import *

reddit = praw.Reddit(user_agent='iAMAggregator scanning for new content.')
subreddit = reddit.get_subreddit("iama")
submissions = subreddit.get_top(limit=10)

dbconnection = pymongo.Connection()
db = dbconnection.iamaggregator
collect = db.people

sub = submissions
while sub != None:
	sub = sub.next
	print sub.comments[0]
