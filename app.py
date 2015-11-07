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
from mail import send_confirm_email, check_token, send_reciept_email

app = Flask(__name__)
app.secret_key = secrets.SECRET_KEY
client = MongoClient(host=secrets.MONGO_URI)

@app.route('/', methods=['GET', 'POST'])
def home_page():
	form = RegistrationForm(request.form)
	if request.method == 'POST' and form.validate():
		try:
			name = helpers.createUser(form)
			hidden_email_parts = form.email.data.split("@")
			hidden_email = hidden_email_parts[0][:2]+("*"*(len(hidden_email_parts[0])-2))+"@"+hidden_email_parts[1]
			sent = send_reciept_email(form.email.data, name)
			flash('We just sent a confirmation email to %s.' % (hidden_email))
			return render_template('done.html', form=form)
		except:
			flash('There seems to be an erorr with our system. Please try again later.')
	return render_template('index.html', form=form)

@app.route('/faq', methods=['GET'])
def faq_page():
	return render_template('faq.html')

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
	if globalHash == 'error':
		return 'error'
	if v.compareHashes(localHash, globalHash) == True:
		return "True"
	return "False"

@app.route('/checkAuthor')
def checkAuthor(uid=None):
	if uid == None:
		uid = request.args.get('uid')
	signed_cert_path = config.JSONS_PATH+uid+".json"
	signed_local_json = json.loads(helpers.read_file(signed_cert_path))
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
	print verify_doc
	if verify_doc == 'error':
		return 'Error! Could not connect to blockchain.info API. Please try again later.'
	if verify_author == "True" and verify_doc == "True":
		return "Success! The certificate has been verified."
	elif verify_author == "True":
		return "Oops! Certificate content could not be verified"
	else:
		return "Oops! Author could not be verfied"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
