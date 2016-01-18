import os
import urllib
from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory
from pymongo import MongoClient
import json
import config
import helpers
import secrets
import verify as v
import snippets
from urllib import quote
from forms import RegistrationForm, AddressForm
from mail import send_confirm_email, check_token, send_reciept_email

app = Flask(__name__)
app.secret_key = secrets.SECRET_KEY
client = MongoClient(host=secrets.MONGO_URI)

TX_JSON = None

@app.route('/', methods=['GET', 'POST'])
def home_page():
	form = RegistrationForm(request.form)
	done=False
	if request.method == 'POST' and form.validate():
		try:
			name = helpers.createUser(form)
			hidden_email_parts = form.email.data.split("@")
			hidden_email = hidden_email_parts[0][:2]+("*"*(len(hidden_email_parts[0])-2))+"@"+hidden_email_parts[1]
			sent = send_reciept_email(form.email.data, name)
			flash('We just sent a confirmation email to %s.' % (hidden_email))
			done=True
			return render_template('index.html', form=form, done=done)
		except:
			flash('There seems to be an erorr with our system. Please try again later.')
	return render_template('index.html', form=form, done=done)

@app.route('/search', methods=['GET', 'POST'])
def search():
	term = request.args.get('term', None)
	return redirect(url_for('get_award', identifier=term))

@app.route('/request', methods=['GET', 'POST'])
def request_page():
	form = RegistrationForm(request.form)
	done=False
	if request.method == 'POST' and form.validate():
		try:
			name = helpers.createUser(form)
			hidden_email_parts = form.email.data.split("@")
			hidden_email = hidden_email_parts[0][:2]+("*"*(len(hidden_email_parts[0])-2))+"@"+hidden_email_parts[1]
			sent = send_reciept_email(form.email.data, name)
			flash('We just sent a confirmation email to %s.' % (hidden_email))
			done=True
			return render_template('request.html', form=form, done=done)
		except:
			flash('There seems to be an erorr with our system. Please try again later.')
	return render_template('request.html', form=form, done=done)

@app.route('/faq', methods=['GET'])
def faq_page():
	return render_template('faq.html')

@app.route('/keys/<key_name>')
def key_page(key_name=None):
	if key_name in os.listdir(config.KEYS_PATH):
		content = helpers.read_file(config.KEYS_PATH+key_name)
		return content
	else:
		return 'Sorry, this page does not exist.'

@app.route('/<identifier>')
def get_award(identifier=None):
	user, certificates = helpers.findUser_by_pubkey(identifier)
	if user:
		certificates = helpers.showIssuedOnly(certificates)
		awards, verfications_info = helpers.get_info_for_certificates(certificates)
		return render_template('user.html', user=user, awards=awards)
	user, certificate = helpers.findUser_by_txid(identifier)
	if user:
		certificate = helpers.showIssuedOnly([certificate])[0]
		award, verification_info = helpers.get_id_info(certificate)
		linkedin_url = config.LINKEDIN_PATH % (quote(config.DOMAIN_NAME+identifier, safe=''))
		return render_template('award.html', award=award, verification_info=urllib.urlencode(verification_info), linkedin_url=linkedin_url)
	return "Sorry, this page does not exist."

@app.route('/data/jsons/<path:filename>')
def get_file(filename):
	return helpers.read_file(config.JSONS_PATH+filename)

@app.route('/manual-verification-instructions')
def get_manual_verification_page(transactionID=None, uid=None):
	if transactionID == None:
		transactionID = request.args.get('transactionID')
	if uid == None:
		uid = request.args.get('uid')
	local_download_url = "/"+config.JSONS_PATH+uid+".json"
	blockchain_download = json.dumps(v.get_rawtx(transactionID))
	blockchain_download = "text/json;charset=utf-8," + urllib.quote(blockchain_download.encode("utf-8"))
	issuer_pubkey = helpers.read_file(config.MLPUBKEY_PATH)
	return render_template('manual-verification.html', local_download_url=local_download_url, blockchain_download=blockchain_download, issuer_pubkey=issuer_pubkey, highlighted_snippets=snippets.HIGHLIGHTED_SNIPPETS)

@app.route('/manual-verification-script')
def get_manual_script():
	return snippets.COMPLETE_CODE

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
	signed_cert_path = config.JSONS_PATH+uid+".json"
	signed_json = open(signed_cert_path).read()
	hashed = v.computeHash(signed_json)
	return hashed

@app.route('/fetchHashFromChain')
def fetchHashFromChain(): #transactionID=None):
	# if transactionID == None:
	# 	transactionID = request.args.get('transactionID')
	hashed = v.fetchHashFromChain(TX_JSON, config.CERT_MARKER)
	return hashed

@app.route('/compareHashes')
def compareHashes(uid=None, transactionID=None):
	if uid == None or transactionID == None:
		transactionID = request.args.get('transactionID')
		uid = request.args.get('uid')
	localHash = computeHash(uid)
	globalHash = fetchHashFromChain() #transactionID)
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
	issuing_address = helpers.read_file(config.MLPUBKEY_PATH)
	verify_authors = v.checkAuthor(issuing_address, signed_local_json) #change this to config.BLOCKCHAIN_ADDRESS
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
	# print "verify_author: %s, verify_doc: %s, verify_not_revoked: %s" % (verify_author, verify_doc, verify_not_revoked) 
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
