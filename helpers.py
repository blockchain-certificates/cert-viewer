import os
import json
from bson.objectid import ObjectId
import config
import secrets
from pymongo import MongoClient
from createjsonmodule import create

client = MongoClient(host=secrets.MONGO_URI)

def findUser_by_id(id):
	user = client.admin.coins.find_one({'_id':ObjectId(id)})
	return user

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

def get_id_info(recipient):
	pubkey_content = read_file(config.MLPUBKEY_PATH)
	txidmap_content = recipient["txid"]
	tx_id = get_txid(txidmap_content, str(recipient["_id"]))
	verification_info = {
		"uid": id,
		"transactionID": tx_id
	}
	award = {
		"logoImg": recipient["json"]["certificate"]["issuer"]["image"],
		"name": recipient["json"]["recipient"]["givenName"]+' '+recipient["recipient"]["familyName"],
		"title": recipient["json"]["certificate"]["title"],
		"subtitle": recipient["json"]["certificate"]["subtitle"]["content"],
		"display": recipient["json"]["certificate"]["subtitle"]["display"],
		"organization":recipient["json"]["certificate"]["issuer"]["name"],
		"text": recipient["json"]["certificate"]["description"],
		"signatureImg": recipient["json"]["assertion"]["image:signature"],
		"mlPublicKey": pubkey_content,
		"mlPublicKeyURL": recipient["json"]["verify"]["signer"],
		"transactionID": tx_id,
		"transactionIDURL": 'https://blockchain.info/tx/'+tx_id
	}
	award = check_display(award)
	return award, verification_info