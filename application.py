from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route('/')
def index():
    top_posts = None
    return render_template('main.html', top_posts=top_posts)

if __name__ == '__main__':
	app.run(debug=True)
