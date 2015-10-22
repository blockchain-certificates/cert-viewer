import os
import urllib
from flask import Flask, render_template, request, flash, redirect, url_for
from pymongo import MongoClient
import json
import config
import helpers
import secrets
from verify import verify_doc
import verify as v
from forms import RegistrationForm, AddressForm
from mail import send_confirm_email, check_token

app = Flask(__name__)
app.secret_key = secrets.SECRET_KEY
client = MongoClient(host=secrets.MONGO_URI)

@app.route('/', methods=['GET', 'POST'])
def home_page():
	form = RegistrationForm(request.form)
	if request.method == 'POST' and form.validate():
		givenName = form.first_name.data
		familyName = form.last_name.data
		user = helpers.findUser_by_name(familyName, givenName)
		if user:
			temp = send_confirm_email(user['user']['email'],user['user']['name'])
			flash('We sent you an email. Go check it out.')
		else:
			form.last_name.errors.append('Hmm... we cannot find you. Try again?')
	return render_template('index.html', form=form)

@app.route('/confirm/<token>', methods=['GET', 'POST'])
def confirm(token=None):
	if check_token(token):
		email = check_token(token)
		user = helpers.findUser_by_email(email)
		name = user["user"]["name"]["givenName"]
		form = AddressForm(request.form)
		if request.method == 'POST' and form.validate():
			helpers.createJson(user)
			helpers.updateRequested(user)
			helpers.addAddress(user,form)
			flash('You did it! Your coin is on the way!')
			return redirect(url_for('home_page'))
		return render_template('confirm.html', form=form, name=name)
	else:
		return 'Sorry, this page does not exist.'

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
	if len(identifier) == 24:
		user = helpers.findUser_by_id(identifier)
	else:
		user = helpers.findUser_by_txid(identifier)
	if user and user["issued"] == True:
		award, verification_info = helpers.get_id_info(user)
	if award:
		return render_template('award.html', award=award, verification_info=urllib.urlencode(verification_info))
	return "Sorry, this page does not exist."

@app.route('/verify')
def verify():
	uid = request.args.get('uid')
	transactionID = request.args.get('transactionID')
	signed_local_json = helpers.findUser_by_id(uid)["json"]
	#signed_local_json["_id"] = str(signed_local_json["_id"]) #important to ensure this happens when certificates are issued
	verified = verify_doc(transactionID, json.dumps(signed_local_json), config.CERT_MARKER)
	return str(verified)

@app.route('/computeHash')
def computeHash(uid=None):
	if uid == None:
		uid = request.args.get('uid')
	signed_local_json = helpers.findUser_by_id(uid)
	signed_local_json["_id"] = str(signed_local_json["_id"]) 
	signed_local_json = json.dumps(signed_local_json)
	hashed = v.computeHash(signed_local_json)
	return "Hash from local certificate: " + hashed

@app.route('/fetchHashFromChain')
def fetchHashFromChain(transactionID=None):
	if transactionID == None:
		transactionID = request.args.get('transactionID')
	hashed = v.fetchHashFromChain(transactionID, config.CERT_MARKER)
	return "Hash from blockchain: "+ hashed

@app.route('/compareHashes')
def compareHashes():
	transactionID = request.args.get('transactionID')
	uid = request.args.get('uid')
	localHash = computeHash(uid)
	globalHash = fetchHashFromChain(transactionID)
	if v.compareHashes(localHash, globalHash) == True:
		return "True"
	return "False"

@app.route('/checkAuthor')
def checkAuthor():
	uid = request.args.get('uid')
	signed_local_json = helpers.findUser_by_id(uid)["json"]
        #signed_local_json["_id"] = str(signed_local_json["_id"])
	verify_authors = v.checkAuthor(config.BLOCKCHAIN_ADDRESS, signed_local_json)
	if verify_authors:
		return "True"
	return "False"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
