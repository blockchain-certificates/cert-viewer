import os
import json
from bson.objectid import ObjectId
import config
import secrets
from pymongo import MongoClient
from createjsonmodule import create

client = MongoClient(host=secrets.MONGO_URI)

def findUser_by_id(id):
	user = client.admin.recipients.find_one({'_id':ObjectId(id)})
	return user

def findUser_by_txid(txid):
	certificate = client.admin.certificates.find_one({'txid': txid})
	user = client.admin.recipients.find_one({'pubkey': certificate['pubkey']})
	return user, certificate

def findUser_by_pubkey(pubkey):
	user = client.admin.recipients.find_one({'pubkey': pubkey})
	certificates = None
	if user:
		user["_id"] = str(user['_id'])
		certificates = list(client.admin.certificates.find({'pubkey': pubkey}))
	return user, certificates

def findUser_by_email(email):
	user = client.admin.recipients.find_one({'info.email': email})
	return user

def findUser_by_name(familyName, givenName):
	query = givenName + " " + familyName
	try:
		userId = list(client.admin.coins.find({'$text': {'$search': query}}, fields={'user.name.familyName':100, 'user.name.givenName':100}))[0]["_id"]
		user = client.admin.coins.find_one(userId)
		return user
	except IndexError:
		return None

def showIssuedOnly(certs):
	issued_certs = []
	for cert in certs:
		if cert['issued'] == True:
			issued_certs.append(cert)
	return issued_certs

def get_info_for_certificates(certificates):
	awards = []
	verifications = []
	for certificate in certificates:
		award, verification_info = get_id_info(certificate)
		awards.append(award)
		verifications.append(verification_info)
	return awards, verifications

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
	# userJson["issued"] = False
	# userJson["txid"] = None
	# userJson["requested"] = True
	userJson["pubkey"] = form.pubkey.data
	userJson["info"] = {}
	userJson["info"]["email"] = form.email.data
	userJson["info"]["degree"] = form.degree.data
	userJson["info"]["comments"] = form.comments.data
	userJson["info"]["name"] = {"familyName": form.last_name.data, "givenName": form.first_name.data}
	userJson["info"]["address"] = {
		"streetAddress": form.address.data,
		"city": form.city.data,
		"state": form.state.data,
		"zipcode": "\'"+form.zipcode.data,
		"country": form.country.data
	}
	client.admin.recipients.insert_one(userJson)
	return userJson["info"]["name"]

def createCert(form):
	certJson = {}
	certJson["pubkey"] = form.pubkey.data
	certJson["issued"] = False
	certJson["txid"] = None
	client.admin.certificates.insert_one(certJson)
	return certJson["pubkey"]

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

def get_id_info(cert):
	pubkey_content = read_file(config.MLPUBKEY_PATH)
	tx_id = cert["txid"]
	json_info = read_json("%s%s.json" % (config.JSONS_PATH, cert["_id"]))
	verification_info = {
		"uid": str(cert["_id"]),
		"transactionID": tx_id
	}
	award = {
		"logoImg": json_info["certificate"]["issuer"]["image"],
		"name": json_info["recipient"]["givenName"]+' '+json_info["recipient"]["familyName"],
		"title": json_info["certificate"]["title"],
		"subtitle": json_info["certificate"]["subtitle"]["content"],
		"display": json_info["certificate"]["subtitle"]["display"],
		"organization":json_info["certificate"]["issuer"]["name"],
		"text":json_info["certificate"]["description"],
		"signatureImg":json_info["assertion"]["image:signature"],
		"mlPublicKey": pubkey_content,
		"mlPublicKeyURL": json_info["verify"]["signer"],
		"transactionID": tx_id,
		"transactionIDURL": 'https://blockchain.info/tx/'+tx_id,
		"issuedOn": json_info["assertion"]["issuedOn"]
	}
	award = check_display(award)
	return award, verification_info
