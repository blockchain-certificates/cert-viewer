import os
import json

import config

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
	if id+'.json' in os.listdir(config.JSONS_PATH):
		pubkey_content = read_file(config.MLPUBKEY_PATH)
		txidmap_content = read_json(config.TXIDMAP_PATH)
		tx_id = get_txid(txidmap_content,id)
		recipient = read_json(config.JSONS_PATH+id+'.json')	
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

def get_recently_issued():
	recent_hashes = config.RECENTLY_ADDED
	recently_issued = {
		"hashes": recent_hashes,
		"urls": ['/'+ h for h in recent_hashes]
	}
	return recently_issued


