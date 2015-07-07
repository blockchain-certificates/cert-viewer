from bson.json_util import dumps, loads
from flask import Flask, render_template
from flask.ext.pymongo import PyMongo

app = Flask(__name__)
mongo = PyMongo(app)

@app.route('/')
def home_page():
	return render_template('index.html')

@app.route('/awards/<id>')
def award(id=None):
	awardJson = mongo.db.awards.find_one({"recipient": id})
	return dumps(awardJson)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)