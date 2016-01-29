import os
import json
from bson.objectid import ObjectId
import config
import secrets
from pymongo import MongoClient
import gridfs
import datetime
from collections import OrderedDict

client = MongoClient(host=secrets.MONGO_URI)
fs = gridfs.GridFS(client.admin)

def get_keys(key_name):
	key_mappings = {config.ML_PUBKEY: "issuer_address", config.ML_REVOKEKEY: "revocation_address"}
	address = key_mappings.get(key_name, None)
	issuer = json.loads(read_file(config.MLISSUER_PATH))
	current = OrderedDict(( datetime.datetime( year=int(k.split("-")[0]),  month=int(k.split("-")[1]), day=int(k.split("-")[2])), v) for k, v in sorted(issuer.iteritems(), reverse=True))
	return current.items()[0][1].get(address, None)

def find_file_in_gridfs(uid):
	filename = uid + ".json"
	certfile = fs.find_one({"filename": filename})
	if certfile:
		return certfile.read()
	return None

def findUser_by_txid_or_uid(identifier):
	user = None
	certificate = None
	if len(identifier) == 24: # check if it is the length of a uid
		certificate = client.admin.certificates.find_one({'_id': ObjectId(identifier), 'issued': True})
	else:
		certificate = client.admin.certificates.find_one({'txid': identifier, 'issued': True})
	if certificate:
		user = client.admin.recipients.find_one({'pubkey': certificate['pubkey']})
	return user, certificate

def findUser_by_pubkey(pubkey):
	user = None
	certificates = None
	user = client.admin.recipients.find_one({'pubkey': pubkey})
	certificates = client.admin.certificates.find({'pubkey': pubkey, 'issued': True})
	if user:
		user["_id"] = str(user['_id'])
	if certificates:
		certificates = list(certificates)
	return user, certificates

def get_info_for_certificates(certificates):
	awards = []
	verifications = []
	for certificate in certificates:
		award, verification_info = get_id_info(certificate)
		awards.append(award)
		verifications.append(verification_info)
	return awards, verifications

def createUser(form):
	userJson = {}
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
	return userJson

def createCert(form):
	certJson = {}
	certJson["pubkey"] = form.pubkey.data
	certJson["issued"] = False
	certJson["txid"] = None
	client.admin.certificates.insert_one(certJson)
	return certJson["pubkey"]

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
	pubkey_content = get_keys(config.ML_PUBKEY)
	tx_id = cert["txid"]
	json_info = json.loads(find_file_in_gridfs(str(cert["_id"])))
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
