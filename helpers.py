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

def update_amas():
    for sub in submissions:
        sub_id = sub.id
        if collect.find_one({'sub_id': sub_id}):
            continue

        title = sub.title
        text = sub.selftext
        op = sub.author

        responses = {}

        for comment in sub.comments:
            if str(type(comment)) == "<class 'praw.objects.MoreComments'>":
                break

            if len(comment.replies) >= 2:
                reply = comment.replies[0]
                if reply.author == op:
                    responses[comment.id] = {'question': comment.body,
                                            'answer': reply.body,
                                            'upvotes': comment.score}
                    break
        if responses:
            collect.insert({'sub_id': sub_id, 'op': sub.author.name, 'text': text,
                    'responses': responses})

def get_teasers(limit=10):
    amas = collect.find()[0:limit-1]

    qas = []
    for ama in amas:
        qas.append(ama['responses'])

    return qas


def get_top_posts(limit=10):
    posts = collect.find()[0:limit-1]

    return posts
