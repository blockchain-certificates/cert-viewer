from flask import Flask, render_template
from flask.ext.pymongo import PyMongo

app = Flask(__name__)
mongo = PyMongo(app)

@app.route('/')
def home_page():
	online_users = mongo.db.users.find({'online': True})
	return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)