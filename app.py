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
import requests

app = Flask(__name__)
app.secret_key = secrets.SECRET_KEY
client = MongoClient(host=secrets.MONGO_URI)

# Home page
@app.route('/', methods=['GET', 'POST'])
def home_page():
	recent_txids = ['56aa4c9bf3a6a0125aaf24bf', 
				'56aa4c9bf3a6a0125aaf24c7']
	return render_template('index.html', recent_txids=recent_txids)

# FAQ page
@app.route('/faq', methods=['GET'])
def faq_page():
	return render_template('faq.html')

# Shows keys in the /keys folder
@app.route('/keys/<key_name>')
def key_page(key_name=None):
	key = helpers.get_keys(key_name)
	if key:
		return key
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
	certificate = helpers.findUser_by_txid_or_uid(uid=identifier)
	if certificate:
		award, verification_info = helpers.get_id_info(certificate)
		if len(award) > 0 and len(verification_info) > 0:
			if request.args.get("format", None)=="json":
				return helpers.find_file_in_gridfs(str(certificate["_id"]))
			return render_template('award.html', award=award, verification_info=urllib.urlencode(verification_info))
	return "Sorry, this page does not exist."

# Create Bitcoin identity for a user so they can request a certificate
@app.route('/bitcoinkeys', methods=['GET'])
def generate_keys():
	return render_template('bitcoinkeys.html')

# Request a certificate
@app.route('/request', methods=['GET', 'POST'])
def request_page():
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
			return redirect(url_for('home_page'))
		except:
			flash('There seems to be an erorr with our system. Please try again later.')
	return render_template('request.html', form=form, registered=False, bitcoin=bitcoin)

@app.route("/verify")
def verify():
	verify_response = []
	verified = False
	uid = request.args.get('uid')
	transactionID = request.args.get('transactionID')

	signed_local_file = helpers.find_file_in_gridfs(uid)
	signed_local_json = json.loads(signed_local_file)

	r = requests.get("https://blockchain.info/rawtx/%s?cors=true" % (transactionID))
	if r.status_code != 200:
		return json.dumps(None)

	verify_response.append(("Computing SHA256 digest of local certificate", "DONE"))
	verify_response.append(("Fetching hash in OP_RETURN field", "DONE"))
	remote_json = r.json()

	# compare hashes
	local_hash = v.computeHash(signed_local_file)
	remote_hash = v.fetchHashFromChain(remote_json)
	compare_hashes = v.compareHashes(local_hash, remote_hash)
	verify_response.append(("Comparing local and blockchain hashes", compare_hashes))

	# check author
	issuing_address = helpers.get_keys(config.ML_PUBKEY)
	verify_authors = v.checkAuthor(issuing_address, signed_local_json)
	verify_response.append(("Checking Media Lab signature", verify_authors))

	# check revocation
	revocation_address = helpers.get_keys(config.ML_REVOKEKEY)
	not_revoked = v.check_revocation(remote_json, revocation_address)
	verify_response.append(("Checking not revoked by issuer", not_revoked))

	if compare_hashes == True and verify_authors == True and not_revoked == True:
		verified = True
	verify_response.append(("Verified", verified))

	return json.dumps(verify_response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
