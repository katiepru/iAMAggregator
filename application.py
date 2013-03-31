from flask import Flask
from flask import render_template
from flask import request
from helpers import *

app = Flask(__name__)

@app.route('/')
def index():
    top_posts = get_top_posts()
    top_qas = get_teasers()
    print(dir(top_qas))
    print(dir(top_posts))
    return render_template('main.html', top_posts=top_posts, top_qas=top_qas)

@app.route('/ama/<post_id>')
def ama(post_id):
    responses = get_responses(limit=10)
    print(dir(responses))
    return render_template('ama.html', responses)

if __name__ == '__main__':
	app.run(debug=True)
