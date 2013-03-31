from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route('/')
def index():
    top_posts = {}
    return render_template('main.html', top_posts=top_posts)

@app.route('/ama/<id>')
def ama(post_id):
    responses = get_responses(limit=10)
    return render_template('ama.html', responses)

if __name__ == '__main__':
	app.run(debug=True)
