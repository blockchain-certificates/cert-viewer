import os
import json

import config
import secrets
from pymongo import MongoClient
from createjsonmodule import create

client = MongoClient(host=secrets.MONGO_URI)

def findUser_by_email(email):
	user = client.admin.coins.find_one({'user.email': email})
	return user

def findUser_by_name(familyName, givenName):
	query = givenName + " " + familyName
	try:
		userId = list(client.admin.coins.find({'$text': {'$search': query}}, fields={'user.name.familyName':100, 'user.name.givenName':100}))[0]["_id"]
		user = client.admin.coins.find_one(userId)
		return user
	except IndexError:
		return None

def createJson(user):
	updated_json = create.run(user)
	userId = user["_id"]
	client.admin.coins.update_one({"_id": userId}, {"$set":{"json": updated_json}})
	client.admin.coins.update_one({"_id": userId}, {"$set":{"requested": True}})
	return updated_json

def updateRequested(user):
	userId = user["_id"]
	client.admin.coins.update_one({"_id": userId}, {"$set":{"requested": True}})
	return True

def addAddress(user, form):
	userId = user["_id"]
	client.admin.coins.update_one({"_id": userId}, {"$set":{"user.address.streetAddress": form.address.data}})
	client.admin.coins.update_one({"_id": userId}, {"$set":{"user.address.city": form.city.data}})
	client.admin.coins.update_one({"_id": userId}, {"$set":{"user.address.state": form.state.data}})
	client.admin.coins.update_one({"_id": userId}, {"$set":{"user.address.zipcode": "\'"+form.zipcode.data}})
	client.admin.coins.update_one({"_id": userId}, {"$set":{"user.address.country": form.country.data}})
	return True

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