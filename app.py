import os
import urllib
from flask import Flask, render_template, request, flash, redirect, url_for
from pymongo import MongoClient

import config
import helpers
import secrets
from verify import verify_doc
from forms import RegistrationForm, AddressForm
from mail import send_confirm_email, check_token

app = Flask(__name__)
app.secret_key = secrets.SECRET_KEY
client = MongoClient(host=secrets.MONGO_URI)

@app.route('/', methods=['GET', 'POST'])
def home_page():
	# client.admin.coins.ensure_index([
	# 		('user.name.familyName', 'text'),
	# 		('user.name.givenName', 'text'),
	#   	],
	#   	name="search_index",
	#   	weights={
	#       	'user.name.familyName':100,
	#       	'user.name.givenName':100
	#   	}
	# 	)

	form = RegistrationForm(request.form)
	if request.method == 'POST' and form.validate():
		first = form.first_name.data
		last = form.last_name.data
		user = helpers.findUser_by_name(first,last)
		if user:
			temp = send_confirm_email('katherine.mcconachie@gmail.com',user['user']['name'])
			flash('We sent you an email. Go check it out.')
		else:
			form.last_name.errors.append('Hmm... we cannot find you. Try again?')
	return render_template('index.html', form=form)

@app.route('/confirm/<token>', methods=['GET', 'POST'])
def confirm(token=None):
	if check_token(token):
		#email = check_token(token)
		email = "zacharia@alum.mit.edu"
		user = helpers.findUser_by_email(email)
		userId = user["_id"]
		client.admin.coins.update_one({"_id": userId}, {"$set":{"requested": True}})
		name = user["user"]["name"]["givenName"]
		form = AddressForm(request.form)
		if request.method == 'POST' and form.validate():
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

# @app.route('/<identifier>')
# def award_by_hash(identifier=None):
# 	award = None
# 	if identifier+'.json' in os.listdir(config.JSONS_PATH):
# 		id = identifier
# 	else:
# 		hashmap_content = helpers.read_json(config.HASHMAP_PATH)
# 		id = hashmap_content.get(identifier, None)
# 	if id:
# 		award, verification_info = helpers.get_id_info(id)
# 	if award:
# 		return render_template('award.html', award=award, verification_info=urllib.urlencode(verification_info))
# 	return "Sorry, this page does not exist."

# @app.route('/verify')
# def verify():
# 	uid = request.args.get('uid')
# 	transactionID = request.args.get('transactionID')
# 	signed_cert_path = config.JSONS_PATH+uid+".json"
# 	verified = verify_doc(transactionID, signed_cert_path, config.CERT_MARKER)
# 	return str(verified)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
