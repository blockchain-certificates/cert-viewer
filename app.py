import os
import urllib
from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory
from pymongo import MongoClient
import json
import config
import helpers
import secrets
import verify as v
from urllib import quote
from forms import RegistrationForm, AddressForm, BitcoinForm
from mail import send_reciept_email

app = Flask(__name__)
app.secret_key = secrets.SECRET_KEY
client = MongoClient(host=secrets.MONGO_URI)

TX_JSON = None

# Home page
@app.route('/', methods=['GET', 'POST'])
def home_page():
	recent_txids = ['5b8ba2f5eed0281fe2d47c7b651c22cf1d2fc942f59e9c5cd3950341d2c2112e', 
					'5b8ba2f5eed0281fe2d47c7b651c22cf1d2fc942f59e9c5cd3950341d2c2112e']
	if request.method == 'POST':
		identifier = request.form.get('identifier', None)
		return redirect(url_for('get_award', identifier=identifier))
	return render_template('index.html', recent_txids=recent_txids)

# FAQ page
@app.route('/faq', methods=['GET'])
def faq_page():
	return render_template('faq.html')

# Shows keys in the /keys folder
@app.route('/keys/<key_name>')
def key_page(key_name=None):
	if key_name in os.listdir(config.KEYS_PATH):
		content = helpers.read_file(config.KEYS_PATH+key_name)
		return content
	else:
		return 'Sorry, this page does not exist.'

# Shows issuer in the /issuer folder
@app.route('/issuer/<issuer_name>')
def issuer_page(issuer_name=None):
	if issuer_name in os.listdir(config.ISSUER_PATH):
		content = helpers.read_file(config.ISSUER_PATH+issuer_name)
		return content
	else:
		return 'Sorry, this page does not exist.'

# Shows issuer in the /issuer folder
@app.route('/criteria/<year>/<month>/<criteria_name>')
def criteria_page(year, month, criteria_name):
	filename = year+"-"+month+"-"+criteria_name
	print filename
	if filename in os.listdir(config.CRITERIA_PATH):
		content = helpers.read_file(config.CRITERIA_PATH+filename)
		return content
	else:
		return 'Sorry, this page does not exist.'

# Render user's certificates or individual certificate based on search query
@app.route('/<identifier>')
def get_award(identifier=None):
	user, certificates = helpers.findUser_by_pubkey(identifier)
	if user and certificates:
		awards, _ = helpers.get_info_for_certificates(certificates)
		if len(awards) > 0:
			return render_template('user.html', user=user, awards=awards)
	_, certificate = helpers.findUser_by_txid_or_uid(identifier)
	if certificate:
		award, verification_info = helpers.get_id_info(certificate)
		if len(award) > 0 and len(verification_info) > 0:
			if request.args.get("format", None)=="json":
				return helpers.find_file_in_gridfs(str(certificate["_id"]))
			return render_template('award.html', award=award, verification_info=urllib.urlencode(verification_info))
	return "Sorry, this award does not exist."

# Create Bitcoin identity for a user so they can request a certificate
@app.route('/bitcoinkeys', methods=['GET'])
def generate_keys():
	return render_template('bitcoinkeys.html')

# Request a certificate
@app.route('/request', methods=['GET', 'POST'])
def request_page():
	done=False
	form = RegistrationForm(request.form)
	bitcoin = BitcoinForm(request.form)
	if request.method == 'POST' and form.validate():
		try:
			user = client.admin.recipients.find_one({"pubkey": form.pubkey.data})
			if user == None:
				user = helpers.createUser(form)
			pubkey = helpers.createCert(form)
			sent = send_reciept_email(form.email.data, {"givenName": form.first_name.data, "familyName": form.last_name.data})
			hidden_email_parts = form.email.data.split("@")
			hidden_email = hidden_email_parts[0][:2]+("*"*(len(hidden_email_parts[0])-2))+"@"+hidden_email_parts[1]
			flash('We just sent a confirmation email to %s.' % (hidden_email))	
			done=True
			return render_template('request.html', form=form, done=done, bitcoin=bitcoin)
		except:
			flash('There seems to be an erorr with our system. Please try again later.')
	return render_template('request.html', form=form, done=done, bitcoin=bitcoin)

# Verify scripts
@app.route('/prepareVerification')
def prepareVerification(transactionID=None):
	if transactionID == None:
		transactionID = request.args.get('transactionID')
	global TX_JSON
	TX_JSON = v.get_rawtx(transactionID)
	return "True"

@app.route('/computeHash')
def computeHash(uid=None):
	if uid == None:
		uid = request.args.get('uid')
	signed_json = helpers.find_file_in_gridfs(uid)
	hashed = v.computeHash(signed_json)
	return hashed

@app.route('/fetchHashFromChain')
def fetchHashFromChain():
	hashed = v.fetchHashFromChain(TX_JSON)
	return hashed

@app.route('/compareHashes')
def compareHashes(uid=None, transactionID=None):
	if uid == None or transactionID == None:
		transactionID = request.args.get('transactionID')
		uid = request.args.get('uid')
	localHash = computeHash(uid)
	globalHash = fetchHashFromChain()
	if globalHash == 'error':
		return 'error'
	if v.compareHashes(localHash, globalHash) == True:
		return "True"
	return "False"

@app.route('/checkAuthor')
def checkAuthor(uid=None):
	if uid == None:
		uid = request.args.get('uid')
	signed_local_json = json.loads(helpers.find_file_in_gridfs(uid))
	issuing_address = helpers.read_file(config.MLPUBKEY_PATH)
	verify_authors = v.checkAuthor(issuing_address, signed_local_json)
	if verify_authors:
		return "True"
	return "False"

@app.route('/checkRevocation')
def checkRevocation(revokeKey=None, transactionID=None):
	if transactionID == None or revokeKey == None:
		transactionID = request.args.get('transactionID')
		revokeKey = helpers.read_file(config.MLREVOKEKEY_PATH)
	not_revoked = v.check_revocation(TX_JSON, revokeKey)
	if not_revoked:
		return "True"
	return "False"

@app.route('/verify')
def verify():
	uid = request.args.get('uid')
	transactionID = request.args.get('transactionID')
	verify_author = checkAuthor(uid)
	verify_doc = compareHashes(uid, transactionID)
	verify_not_revoked = checkRevocation(helpers.read_file(config.MLREVOKEKEY_PATH), transactionID)
	if verify_doc == 'error':
		return 'Error! Could not connect to blockchain.info API. Please try again later.'
	if verify_author == "True" and verify_doc == "True" and verify_not_revoked == "True":
		return "Success! The certificate has been verified."
	elif verify_doc == "False":
		return "Oops! Certificate content could not be verified"
	elif verify_author == "False":
		return "Oops! Author could not be verfied"
	else:
		return "Oops! The certificate has been revoked by the issuer"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
