import json

import config
import helpers


class Certificates:
    def __init__(self, client, fs):
        self.client = client
        self.fs = fs

    def find_file_in_gridfs(self, uid):
        filename = uid + ".json"
        certfile = self.fs.find_one({"filename": filename})
        if certfile:
            return certfile.read()
        return None

    # TODO
    def find_user(self, field, value):
        certificate = self.client.admin.certificates.find_one({field: value, 'issued': True})

    def find_user_by_txid(self, txid):
        certificate = None
        if txid:
            certificate = self.client.admin.certificates.find_one({'txid': txid, 'issued': True})
        return certificate

    def find_user_by_uid(self, uid=None):
        certificate = None
        if uid:
            certificate = self.client.admin.certificates.find_one({'_id': uid, 'issued': True})
        return certificate

    def find_user_by_pubkey(self, pubkey):
        # if certificate is missing pubkey, it will be returned by the filter below.
        if pubkey is None:
            return None, None
        user = None
        certificates = None
        user = self.client.admin.recipients.find_one({'pubkey': pubkey})
        certificates = self.client.admin.certificates.find({'pubkey': pubkey, 'issued': True})
        if user:
            user["_id"] = str(user['_id'])
        if certificates:
            certificates = list(certificates)
        return user, certificates

    def create_user(self, form):
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
        self.client.admin.recipients.insert_one(userJson)
        return userJson

    def create_cert(self, form):
        certJson = {}
        certJson["pubkey"] = form.pubkey.data
        certJson["issued"] = False
        certJson["txid"] = None
        self.client.admin.certificates.insert_one(certJson)
        return certJson["pubkey"]

    def get_info_for_certificates(self, certificates):
        awards = []
        verifications = []
        for certificate in certificates:
            award, verification_info = self.get_id_info(certificate)
            awards.append(award)
            verifications.append(verification_info)
        return awards, verifications

    def get_id_info(self, cert):
        pubkey_content = helpers.get_keys(config.ML_PUBKEY)
        tx_id = cert["txid"]
        uid = str(cert["_id"])
        json_info = json.loads(self.find_file_in_gridfs(uid))
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
        award = Certificates.check_display(award)
        return award, verification_info

    def check_display(award):
        if award['display'] == 'FALSE':
            award['subtitle'] = ''
        return award

