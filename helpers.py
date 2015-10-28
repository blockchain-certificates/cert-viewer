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

def findUser_by_txid(txid):
	user = client.admin.coins.find_one({'txid': txid})
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

def makeListOfAllNames():
	names = {}
	users = list(client.admin.coins.find({}))
	for doc in users:
		fullname = str(doc["user"]["name"]["givenName"]+ " " + doc["user"]["name"]["familyName"])
		names[fullname]=str(doc["_id"])
		# names = names + doc["user"]["name"]["givenName"]+ " " + doc["user"]["name"]["familyName"] + ","
	return names

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

def createUser(form):
	userJson = {}
	userJson["issued"] = False
	userJson["txid"] = None
	userJson["requested"] = True
	userJson["user"] = {}
	userJson["user"]["email"] = form.email.data
	userJson["user"]["degree"] = form.degree.data
	userJson["user"]["name"] = {"familyName": form.last_name.data, "givenName": form.first_name.data}
	userJson["user"]["address"] = {
		"streetAddress": form.address.data,
		"city": form.city.data,
		"state": form.state.data,
		"zipcode": "\'"+form.zipcode.data,
		"country": form.country.data
	}
	client.admin.coins.insert_one(userJson)
	return userJson["user"]["name"]

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
 

def check_display(award):
	if award['display'] == 'FALSE':
		award['subtitle'] = '';
	return award

def get_id_info(recipient):
	pubkey_content = read_file(config.MLPUBKEY_PATH)
	tx_id = recipient["txid"]
	json_info = recipient["json"]
	verification_info = {
		"uid": str(recipient["_id"]),
		"transactionID": tx_id
	}
	award = {
		"logoImg": json_info["certificate"]["issuer"]["image"],
		"name": json_info["recipient"]["givenName"]+' '+recipient["json"]["recipient"]["familyName"],
		"title": json_info["certificate"]["title"],
		"subtitle": json_info["certificate"]["subtitle"]["content"],
		"display": json_info["certificate"]["subtitle"]["display"],
		"organization":json_info["certificate"]["issuer"]["name"],
		"text":json_info["certificate"]["description"],
		"signatureImg":json_info["assertion"]["image:signature"],
		"mlPublicKey": pubkey_content,
		"mlPublicKeyURL": json_info["verify"]["signer"],
		"transactionID": tx_id,
		"transactionIDURL": 'https://blockchain.info/tx/'+tx_id
	}
	award = check_display(award)
	return award, verification_info
