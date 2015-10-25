import os
import urllib
from flask import Flask, render_template, request, flash, redirect, url_for
from pymongo import MongoClient
import json
import config
import helpers
import secrets
import verify as v
from forms import RegistrationForm, AddressForm
from mail import send_confirm_email, check_token

app = Flask(__name__)
app.secret_key = secrets.SECRET_KEY
client = MongoClient(host=secrets.MONGO_URI)

@app.route('/', methods=['GET', 'POST'])
def home_page():
	form = RegistrationForm(request.form)
	names = helpers.makeListOfAllNames()
	if request.method == 'POST' and form.validate():
		name = form.name.data
		uid = names.get(name, None)
		if uid:
			user = helpers.findUser_by_id(uid)
			if user:
				temp = send_confirm_email(user['user']['email'], user['user']['name'])
				hidden_email_parts = user['user']['email'].split("@")
				hidden_email = hidden_email_parts[0][:2]+("*"*(len(hidden_email_parts[0])-2))+"@"+hidden_email_parts[1]
				flash('We just sent an email to %s with details on how to collect your coin.' % (hidden_email))
		else:
			form.name.errors.append('Oops! We cannot find your name.' )
	return render_template('index.html', form=form, names=json.dumps(names))

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

@app.route('/computeHash')
def computeHash(uid=None):
	if uid == None:
		uid = request.args.get('uid')
	signed_cert_path = config.JSONS_PATH+uid+".json"
        signed_json = open(signed_cert_path).read()
	hashed = v.computeHash(signed_json)
	return hashed

@app.route('/fetchHashFromChain')
def fetchHashFromChain(transactionID=None):
	if transactionID == None:
		transactionID = request.args.get('transactionID')
	hashed = v.fetchHashFromChain(transactionID, "TESTING")#config.CERT_MARKER)
	return hashed

@app.route('/compareHashes')
def compareHashes(uid=None, transactionID=None):
	if uid == None or transactionID == None:
		transactionID = request.args.get('transactionID')
		uid = request.args.get('uid')
	localHash = computeHash(uid)
	globalHash = fetchHashFromChain(transactionID)
	if v.compareHashes(localHash, globalHash) == True:
		return "True"
	return "False"

@app.route('/checkAuthor')
def checkAuthor(uid=None):
	if uid == None:
		uid = request.args.get('uid')
	signed_local_json = helpers.findUser_by_id(uid)["json"]
	verify_authors = v.checkAuthor("1HW53ZHzK6uPBWgQrnZ4WHynVojvJ2Vfqv", signed_local_json) #change this to config.BLOCKCHAIN_ADDRESS
	if verify_authors:
		return "True"
	return "False"

@app.route('/verify')
def verify():
        uid = request.args.get('uid')
        transactionID = request.args.get('transactionID')
        verify_author = checkAuthor(uid)
	verify_doc = compareHashes(uid, transactionID)
	signed_cert_path = config.JSONS_PATH+uid+".json"
	if verify_author == "True" and verify_doc == "True":
		return "Success!"
	elif verify_author == "True":
		return "Oops! Certificate content could not be verified"
	else:
		return "Oops! Author could not be verfied"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
