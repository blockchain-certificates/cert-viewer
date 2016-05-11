import json
import logging
from collections import namedtuple

import certificates.verification_helpers as v
import gridfs
import requests
from bson.objectid import ObjectId
from certificates import config
from certificates.mail import Mail
from pymongo import MongoClient

CONFIG_SECTION = 'certificate_service'

UserData = namedtuple('UserData', ['pubkey', 'email', 'degree', 'comments', 'first_name', 'last_name',
                                   'street_address', 'city', 'state', 'zip_code', 'country'])

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
        self.mail_sender = Mail()

    def get_formatted_certificate(self, identifier, format):
        logging.debug('Retrieving certificate for uid=%s', identifier)
        certificate = self.find_user_by_uid(uid=identifier)
        if certificate:
            award, verification_info = self.get_award_and_verification_for_certificate(certificate)
            if len(award) > 0 and len(verification_info) > 0:
                if format == "json":
                    return self.find_file_in_gridfs(str(certificate["_id"])), None
                return award, verification_info

    def request_certificate(self, user_data):
        # check if we already have a user associated with the public key
        user = self.find_user_by_pub_key(user_data.pubkey)
        if user is None:
            logging.info('User not found for public key; creating user')
            self.create_user(user_data)
        self.create_certificate(user_data.pubkey)
        logging.trace('Created certificate; sending receipt')
        sent = self.mail_sender.send_receipt_email(user_data.email,
                                                   {"givenName": user_data.first_name,
                                                    "familyName": user_data.last_name})
        return sent

    def get_verify_response(self, transaction_id, uid):
        signed_local_file = self.find_file_in_gridfs(uid)
        signed_local_json = json.loads(signed_local_file)
        r = requests.get("https://blockchain.info/rawtx/%s?cors=true" % transaction_id)
        if r.status_code != 200:
            logging.warning('Error looking up by transaction_id=%s, status_code=%d', transaction_id, r.status_code)
            return None
        else:
            verify_response = []
            verified = False
            verify_response.append(("Computing SHA256 digest of local certificate", "DONE"))
            verify_response.append(("Fetching hash in OP_RETURN field", "DONE"))
            remote_json = r.json()

            # compare hashes
            local_hash = v.compute_hash(signed_local_file)
            remote_hash = v.fetch_hash_from_chain(remote_json)
            compare_hashes = v.compare_hashes(local_hash, remote_hash)
            verify_response.append(("Comparing local and blockchain hashes", compare_hashes))

            # check author
            issuing_address = config.get_key_by_type('CERT_PUBKEY')
            verify_authors = v.check_author(issuing_address, signed_local_json)
            verify_response.append(("Checking Media Lab signature", verify_authors))

            # check revocation
            revocation_address = config.get_key_by_type('CERT_REVOKEKEY')
            not_revoked = v.check_revocation(remote_json, revocation_address)
            verify_response.append(("Checking not revoked by issuer", not_revoked))

            if compare_hashes and verify_authors and not_revoked:
                verified = True
            verify_response.append(("Verified", verified))
        return verify_response

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

    def find_user_by_pub_key(self, pubkey):
        return self.db.recipients.find_one({"pubkey": pubkey})

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

    def create_certificate(self, pubkey):
        cert_json = {'pubkey': pubkey, 'issued': False, 'txid': None}
        cert_id = self.insert_certificate(cert_json=cert_json)
        return cert_id

    def get_awards_and_verifications_for_certificates(self, certificates):
        awards = []
        verifications = []
        for certificate in certificates:
            award, verification_info = self.get_award_and_verification_for_certificate(certificate)
            awards.append(award)
            verifications.append(verification_info)
        return awards, verifications

    def get_award_and_verification_for_certificate(self, certificate):
        pubkey_content = config.get_key_by_type('CERT_PUBKEY')
        tx_id = certificate['txid']
        uid = str(certificate['_id'])
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

    def insert_user(self, user_json):
        """Exposed separately to ease testing"""
        user_id = CertificateRepo.insert_shim(self.db.recipients, user_json)
        return user_id

    def insert_certificate(self, cert_json):
        """Exposed separately to ease testing"""
        cert_id = CertificateRepo.insert_shim(self.db.certificates, cert_json)
        return cert_id

    @staticmethod
    def insert_shim(collection, document):
        """This is an unfortunate workaround for mongo mock. It doesn't support insert, so this allows an easy patch"""
        inserted_id = collection.insert_one(document)
        return inserted_id

    @staticmethod
    def check_display(award):
        if award['display'] == 'FALSE':
            award['subtitle'] = ''
        return award

