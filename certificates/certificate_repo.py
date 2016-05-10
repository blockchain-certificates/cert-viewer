import json
import logging

import config
import gridfs
from bson.objectid import ObjectId
from pymongo import MongoClient

CONFIG_SECTION = 'certificate_service'


class CertificateRepo:
    def __init__(self, client=None, gfs=None):
        self.certificates_db_name = config.get_config().get(CONFIG_SECTION, 'CERTIFICATES_DB')

        if client:
            self.client = client
        else:
            self.client = MongoClient(host=config.get_config().get(CONFIG_SECTION, 'MONGO_URI'))

        if gfs:
            self.gfs = gfs
        else:
           self.gfs = gridfs.GridFS(self.client[self.certificates_db_name])

        self.db = self.client[self.certificates_db_name]

    def find_file_in_gridfs(self, uid):
        filename = uid + '.json'
        certfile = self.gfs.find_one({'filename': filename})
        if certfile:
            contents = certfile.read()
            if isinstance(contents, (bytes, bytearray)):
                return contents.decode("utf-8")
            return contents
        logging.warning('File not found in gridfs, uid=%s', uid)
        return None

    def find_user_by_txid(self, txid):
        certificate = None
        if txid:
            certificate = self.db.certificates.find_one({'txid': txid, 'issued': True})
        return certificate

    def find_user_by_uid(self, uid=None):
        certificate = None
        if uid:
            certificate = self.db.certificates.find_one({'_id': ObjectId(uid), 'issued': True})
        return certificate

    def find_user_and_certificate_by_pubkey(self, pubkey):
        # if certificate is missing pubkey, it will be returned by the filter below.
        if pubkey is None:
            return None, None
        user = self.find_user_by_pub_key(pubkey)
        certificates = self.db.certificates.find({'pubkey': pubkey, 'issued': True})
        if user:
            user["_id"] = str(user['_id'])
        if certificates:
            certificates = list(certificates)
        return user, certificates

    def find_user_by_pub_key(self, pubkey):
        return self.db.recipients.find_one({"pubkey": pubkey})

    def create_user(self, user_data):
        user_json = {'pubkey': user_data.pubkey, 'info': {}}
        user_json['info']['email'] = user_data.email
        user_json['info']['degree'] = user_data.degree
        user_json['info']['comments'] = user_data.comments
        user_json['info']['name'] = {'familyName': user_data.last_name, 'givenName': user_data.first_name}
        user_json['info']['address'] = {
            'streetAddress': user_data.street_address,
            'city': user_data.city,
            'state': user_data.state,
            'zipcode': "\'" + user_data.zip_code,  # TODO why?
            'country': user_data.country
        }

        rec_id = self.insert_user(user_json)
        logging.info('inserted user with recipient id=%s', rec_id)

        return user_json

    def create_cert(self, pubkey):
        cert_json = {'pubkey': pubkey, 'issued': False, 'txid': None}
        cert_id = self.insert_cert(cert_json=cert_json)
        return cert_id

    def insert_user(self, user_json):
        user_id = CertificateRepo.insert_shim(self.db.recipients, user_json)
        return user_id

    def insert_cert(self, cert_json):
        cert_id = CertificateRepo.insert_shim(self.db.certificates, cert_json)
        return cert_id

    def get_info_for_certificates(self, certificates):
        awards = []
        verifications = []
        for certificate in certificates:
            award, verification_info = self.get_id_info(certificate)
            awards.append(award)
            verifications.append(verification_info)
        return awards, verifications

    def get_id_info(self, cert):
        pubkey_content = config.get_key_by_type('CERT_PUBKEY')
        tx_id = cert['txid']
        uid = str(cert['_id'])
        gfs_file = self.find_file_in_gridfs(uid)
        json_info = json.loads(gfs_file)
        verification_info = {
            'uid': uid,
            'transactionID': tx_id
        }
        award = {
            'logoImg': json_info['certificate']['issuer']['image'],
            'name': json_info['recipient']['givenName'] + ' ' + json_info['recipient']['familyName'],
            'title': json_info['certificate']['title'],
            'subtitle': json_info['certificate']['subtitle']['content'],
            'display': json_info['certificate']['subtitle']['display'],
            'organization': json_info['certificate']['issuer']['name'],
            'text': json_info['certificate']['description'],
            'signatureImg': json_info['assertion']['image:signature'],
            'mlPublicKey': pubkey_content,
            'mlPublicKeyURL': json_info['verify']['signer'],
            'transactionID': tx_id,
            'transactionIDURL': 'https://blockchain.info/tx/' + tx_id,
            'issuedOn': json_info['assertion']['issuedOn']
        }
        award = CertificateRepo.check_display(award)
        return award, verification_info

    @staticmethod
    def insert_shim(collection, document):
        inserted_id = collection.insert_one(document)
        return inserted_id

    @staticmethod
    def check_display(award):
        if award['display'] == 'FALSE':
            award['subtitle'] = ''
        return award

