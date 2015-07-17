import json
import os
import urllib
from flask import Flask, render_template, request
from verify import verify_doc

app = Flask(__name__)

KEYS_PATH = 'keys/'
DATA_PATH = 'data/'
JSONS_PATH = DATA_PATH + 'jsons/'
MLPUBKEY_PATH = KEYS_PATH + '/ml-certs-public-key.asc'
TXIDMAP_PATH = DATA_PATH + 'transaction_id_mappings.json'
HASHMAP_PATH = DATA_PATH + 'hash_id_mappings.json'
BLOCKCHAIN_ADDRESS = '1HYPitzbwR83M3Smw6GWs5XeQzBWoJAEeS'
CERT_MARKER = 'MEDIALAB'

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

def get_id_info(id):
	if id+'.json' in os.listdir(JSONS_PATH):
		pubkey_content = read_file(MLPUBKEY_PATH)
		txidmap_content = read_json(TXIDMAP_PATH)
		tx_id = get_txid(txidmap_content,id)
		recipient = read_json(JSONS_PATH+id+'.json')	
		if recipient:
			verification_info = {
				"uid": id,
				"transactionID": tx_id
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
			return award, verification_info
	return None

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

@app.route('/<identifier>')
def award_by_hash(identifier=None):
	award = None
	if identifier+'.json' in os.listdir(JSONS_PATH):
		id = identifier
	else:
		hashmap_content = read_json(HASHMAP_PATH)
		id = hashmap_content.get(identifier, None) # try to get id by hash
	if id:
		award, verification_info = get_id_info(id)
	if award:
		return render_template('award.html', award=award, verification_info=urllib.urlencode(verification_info))
	return "Sorry, this page does not exist."

@app.route('/verify')
def verify():
	uid = request.args.get('uid')
	transactionID = request.args.get('transactionID')
	signed_cert_path = JSONS_PATH+uid+".json"
	# verify_signature(BLOCKCHAIN_ADDRESS, signed_cert_path)
	verified = verify_doc(transactionID, signed_cert_path, CERT_MARKER)
	return str(verified)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
