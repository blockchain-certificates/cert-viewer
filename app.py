import json
import os
import urllib
from flask import Flask, render_template, request
from pymongo import MongoClient
import sys

import config
import helpers
import secrets
from verify import verify_doc
from createjsonmodule import create
from forms import RegistrationForm, AddressForm
from mail import send_confirm_email

app = Flask(__name__)
client = MongoClient(host=secrets.MONGO_URI)
app.secret_key = secrets.SECRET_KEY

def findUser(familyName, givenName):
	query = givenName + " " + familyName
	userId = list(client.admin.coins.find({'$text': {'$search': query}}, fields={'user.name.familyName':100, 'user.name.givenName':100}))[0]["_id"]
	user = client.admin.coins.find_one(userId)
	print user
	return user
	
def createJson(user):
	updated_json = create.run(user)
	# next update the DB with new document
	return updated_json

@app.route('/')
def home_page():
	client.admin.coins.ensure_index([
			('user.name.familyName', 'text'),
			('user.name.givenName', 'text'),
	  	],
	  	name="search_index",
	  	weights={
	      	'user.name.familyName':100,
	      	'user.name.givenName':100
	  	}
		)
	user = findUser('Giorgos', 'Zacharia')
	created_json = createJson(user)
	recents = helpers.get_recently_issued()
	return render_template('index.html', recents=recents)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        first_name = form.first.data
        last_name = form.last.data
        #print client.admin.coins.find({'$text': {'$search': first_name}}, fields={'user.name.givenName':100}).count() > 0
        #print client.admin.coins.find({'$text': {'$search': last_name}}, fields={'user.name.familyName':100}).count() > 0
        #if client.admin.coins.find({'$text': {'$search': first_name}}, fields={'user.name.givenName':100}).count() > 0 and client.admin.coins.find({'$text': {'$search': last_name}}, fields={'user.name.familyName':100}).count() > 0:
        if client.admin.coins.find_one({'$text': {'$search': first_name}}, fields={'user.name.givenName':100}) and client.admin.coins.find_one({'$text': {'$search': last_name}}, fields={'user.name.familyName':100}):

        	flash('We send you an email. Go check it out.')
        	return redirect(url_for('home_page'))
        else:
        	form.last.errors.append('Hmm... we cannot find you. Try again?')
    return render_template('register.html', form=form)

@app.route('/confirm/<token>', methods=['GET', 'POST'])
def confirm(token=None):
	confirm = {'name': "Katherine"}
	form = AddressForm(request.form)
	if request.method == 'POST' and form.validate():
		flash('You did it! Your coin is on the way!')
		return redirect(url_for('home_page'))
	return render_template('confirm.html', form=form, confirm=confirm)

@app.route('/keys/<key_name>')
def key_page(key_name=None):
	if key_name in os.listdir(config.KEYS_PATH):
		content = helpers.read_file(config.KEYS_PATH+key_name)
		return content
	else:
		return 'Sorry, this page does not exist.'

@app.route('/<identifier>')
def award_by_hash(identifier=None):
	award = None
	if identifier+'.json' in os.listdir(config.JSONS_PATH):
		id = identifier
	else:
		hashmap_content = helpers.read_json(config.HASHMAP_PATH)
		id = hashmap_content.get(identifier, None)
	if id:
		award, verification_info = helpers.get_id_info(id)
	if award:
		return render_template('award.html', award=award, verification_info=urllib.urlencode(verification_info))
	return "Sorry, this page does not exist."

@app.route('/verify')
def verify():
	uid = request.args.get('uid')
	transactionID = request.args.get('transactionID')
	signed_cert_path = config.JSONS_PATH+uid+".json"
	verified = verify_doc(transactionID, signed_cert_path, config.CERT_MARKER)
	return str(verified)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
