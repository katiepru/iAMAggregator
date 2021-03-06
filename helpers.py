import pymongo
import praw
import json
import sendgrid
from config import *

reddit = praw.Reddit(user_agent='iAMAggregator scanning for new content.')
subreddit = reddit.get_subreddit("iama")
submissions = subreddit.get_top(limit=10)

dbconnection = pymongo.Connection()
db = dbconnection.iamaggregator
collect = db.people
users = db.users

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

        if responses:
            collect.insert({'sub_id': sub_id, 'title': sub.title, 'op': sub.author.name, 'text': text,
                'responses': responses})

def get_teasers(limit=10):
    amas = collect.find()[0:limit-1]

    qas = []
    for ama in amas:
        qas.append(ama['responses'])

    return qas


def get_top_posts(limit=10):
    posts_cursor = collect.find()[0:limit-1]

    posts=[]
    for post in posts_cursor:
        posts.append(post)

    return posts

def get_responses(post_id, limit=50):
    replies_cursor = collect.find({'sub_id': post_id})[0:limit-1]

    replies=[]
    for reply in replies_cursor:
        replies.append(reply['responses'])

    return replies

def send_email(user, ama_title, email):
	s = sendgrid.Sendgrid(sg_user, sg_pass, secure=True)
	message = sendgrid.Message(sg_email, "New AMA", "A new AMA has been posted: " + ama_title)
	message.add_to(email, user)
	s.smtp.send(message)

def get_old():
    post = collect.find_one()
    user = users.find_one()
    send_email(user['user'], post['title'], user['email'])
    result = users.remove(spec_or_id={'_id': user['_id']}, safe=True)
    print result

def addto_db(user, email):
	post = {"user" : user,
			"email" : email,
			}
	users.insert(post)	
