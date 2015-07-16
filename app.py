import json
import os
import urllib
from flask import Flask, render_template, request

app = Flask(__name__)

KEYS_PATH = 'keys/'
JSONS_PATH = 'data/jsons/'
MLPUBKEY_PATH = 'keys/ml-certs-public-key.asc'
TXIDMAP_PATH = 'data/transaction_id_mappings.json'

def read_json(path):
	with open(path) as json_file:
		data = json.load(json_file)
	json_file.close()
	return data 

def read_file(path):
	with open(path) as f:
		data = f.read()
	f.close()
	return data
 
def get_txid(data,id):
	return data[id]

def check_display(award):
	if award['display'] == 'FALSE':
		award['subtitle'] = '';
	return award

@app.route('/')
def home_page():
	return render_template('index.html')

@app.route('/keys/<key_name>')
def key_page(key_name=None):
	if key_name in os.listdir(KEYS_PATH):
		content = read_file(KEYS_PATH+key_name)
		return content
	else:
		return 'Sorry, this page does not exist.'

@app.route('/<id>')
def award(id=None):
	if id+'.json' in os.listdir(JSONS_PATH):
		pubkey_content = read_file(MLPUBKEY_PATH)
		txidmap_content = read_json(TXIDMAP_PATH)
		tx_id = get_txid(txidmap_content,id)
		recipient = read_json(JSONS_PATH+id+'.json')	
		if recipient:
			verification_info = {
				"uid": recipient["assertion"]["uid"],
				"rawJson": recipient
			}
			award = {
				"logoImg": recipient["certificate"]["issuer"]["image"],
				"name": recipient["recipient"]["givenName"]+' '+recipient["recipient"]["familyName"],
				"title": recipient["certificate"]["title"],
				"subtitle": recipient["certificate"]["subtitle"]["content"],
				"display": recipient["certificate"]["subtitle"]["display"],
				"organization":recipient["certificate"]["issuer"]["name"],
				"text": recipient["certificate"]["description"],
				"signatureImg": recipient["assertion"]["image:signature"],
				"mlPublicKey": pubkey_content,
				"mlPublicKeyURL": recipient["verify"]["signer"],
				"transactionID": tx_id,
				"transactionIDURL": 'https://blockchain.info/tx/'+tx_id
			}
			award = check_display(award)
			return render_template('award.html', award=award, verification_info=urllib.urlencode(verification_info))
	else:
		return "Sorry, this page does not exist."

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)