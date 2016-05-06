import json
import sys

import secrets

import binascii
import config
import gridfs
from pymongo import MongoClient

unhexlify = binascii.unhexlify
hexlify = binascii.hexlify
if sys.version > '3':
    unhexlify = lambda h: binascii.unhexlify(h.encode('utf8'))
    hexlify = lambda b: binascii.hexlify(b).decode('utf8')

client = MongoClient(host=secrets.MONGO_URI)
fs = gridfs.GridFS(client.admin)


def get_keys(key_name):
    key_mappings = {config.ML_PUBKEY: "issuer_key", config.ML_REVOKEKEY: "revocation_key"}
    issuer = json.loads(read_file(config.MLISSUER_PATH))
    address = key_mappings.get(key_name, None)
    return issuer[address][0]["key"]


def find_file_in_gridfs(uid):
    filename = uid + ".json"
    certfile = fs.find_one({"filename": filename})
    if certfile:
        return certfile.read()
    return None


def find_user_by_txid_or_uid(txid=None, uid=None):
    certificate = None
    if uid:
        certificate = client.admin.certificates.find_one({'_id': uid, 'issued': True})
    if txid:
        certificate = client.admin.certificates.find_one({'txid': txid, 'issued': True})
    return certificate


def find_user_by_pubkey(pubkey):
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


def create_user(form):
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
        "zipcode": "\'" + form.zipcode.data,
        "country": form.country.data
    }
    client.admin.recipients.insert_one(userJson)
    return userJson


def create_cert(form):
    certJson = {}
    certJson["pubkey"] = form.pubkey.data
    certJson["issued"] = False
    certJson["txid"] = None
    client.admin.certificates.insert_one(certJson)
    return certJson["pubkey"]


def read_file(path):
    with open(path) as f:
        data = f.read()
    return data


def check_display(award):
    if award['display'] == 'FALSE':
        award['subtitle'] = ''
    return award


def get_id_info(cert):
    pubkey_content = get_keys(config.ML_PUBKEY)
    tx_id = cert["txid"]
    uid = str(cert["_id"])
    json_info = json.loads(find_file_in_gridfs(uid))
    verification_info = {
        "uid": uid,
        "transactionID": tx_id
    }
    award = {
        "logoImg": json_info["certificate"]["issuer"]["image"],
        "name": json_info["recipient"]["givenName"] + ' ' + json_info["recipient"]["familyName"],
        "title": json_info["certificate"]["title"],
        "subtitle": json_info["certificate"]["subtitle"]["content"],
        "display": json_info["certificate"]["subtitle"]["display"],
        "organization": json_info["certificate"]["issuer"]["name"],
        "text": json_info["certificate"]["description"],
        "signatureImg": json_info["assertion"]["image:signature"],
        "mlPublicKey": pubkey_content,
        "mlPublicKeyURL": json_info["verify"]["signer"],
        "transactionID": tx_id,
        "transactionIDURL": 'https://blockchain.info/tx/' + tx_id,
        "issuedOn": json_info["assertion"]["issuedOn"]
    }
    award = check_display(award)
    return award, verification_info
