import pymongo
import praw
from config import *

reddit = praw.Reddit(user_agent='iAMAggregator scanning for new content.')
subreddit = reddit.get_subreddit("iama")

dbconnection = pymongo.Connection()
db = dbconnection.iamaggregator
