import logging


from bson.objectid import ObjectId
from pymongo import MongoClient
import gridfs
from . import config
from . import formatters
from .verification_helpers import Verifier
from .mail import Mail

CONFIG_SECTION = 'certificate_service'


class CertificateStore:
    def __init__(self, client=None, gfs=None, verifier=Verifier(), notifier=Mail()):
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

        self.notifier = notifier
        self.verifier = verifier

    def request_certificate(self, user_data):
        # check if we already have a user associated with the public key
        user = self.find_recipient_by_pub_key(user_data.pubkey)
        if user is None:
            logging.info('User not found for public key; creating user')
            self.create_user(user_data)
        self.create_certificate_request(user_data.pubkey)
        logging.trace('Created certificate; sending receipt')
        sent = self.notifier.send_receipt_email(user_data.user_email, user_data.first_name, user_data.last_name)
        return sent

    def get_formatted_certificate(self, certificate_uid, format):
        logging.debug('Retrieving certificate for uid=%s', certificate_uid)
        award = None
        verification_info = None
        certificate = self.find_certificate_by_certificate_uid(uid=certificate_uid)
        if certificate:
            if format == "json":
                award = self.find_file_in_gridfs(formatters.certificate_to_filename(certificate))
                verification_info = None
            else:
                award, verification_info = self.get_award_and_verification_for_certificate(certificate)
        else:
            logging.warning('Certificate metadata not found for recipient uid=%s', certificate_uid)

        if certificate and not award:
            logging.error('Problem looking up certificate for recipient=%s, '
                          'but certificate metadata was found', certificate_uid)
        return award, verification_info

    def get_award_and_verification_for_certificate(self, certificate):
        filename = formatters.certificate_to_filename(certificate)
        gfs_file = self.find_file_in_gridfs(filename)
        if not gfs_file:
            logging.warning('File not found in gridfs, filename=%s', filename)
            return None, None

        pubkey_content = config.get_key_by_type('CERT_PUBKEY')
        award = formatters.gfs_file_to_award(gfs_file, pubkey_content, certificate)
        verification_info = formatters.format_verification_info(certificate)
        return award, verification_info

    def verify(self, transaction_id, uid):
        signed_local_file = self.find_file_in_gridfs(uid)
        return self.verifier.verify(transaction_id, signed_local_file)

    def find_certificate_by_txid(self, txid):
        certificate = None
        if txid:
            certificate = self.db.certificates.find_one({'txid': txid, 'issued': True})
        return certificate

    def find_certificate_by_certificate_uid(self, uid=None):
        certificate = None
        if uid:
            certificate = self.db.certificates.find_one({'_id': ObjectId(uid), 'issued': True})
        return certificate

    def find_recipient_by_pub_key(self, pubkey):
        return self.db.recipients.find_one({'pubkey': pubkey})

    def find_user_and_certificate_by_pubkey(self, pubkey):
        # if certificate is missing pubkey, it will be returned by the filter below.
        if pubkey is None:
            return None, None
        user = self.find_recipient_by_pub_key(pubkey)
        certificates = self.db.certificates.find({'pubkey': pubkey, 'issued': True})
        if user:
            user['_id'] = formatters.parse_user_uid(user)  # TODO: create new object instead of overwriting
        if certificates:
            certificates = list(certificates)
        return user, certificates

    def find_file_in_gridfs(self, filename):
        certfile = self.gfs.find_one({'filename': filename})
        if certfile:
            contents = certfile.read()
            if isinstance(contents, (bytes, bytearray)):
                return contents.decode("utf-8")
            return contents
        return None

    def create_user(self, user_data):
        user_json = formatters.user_data_to_json(user_data)
        rec_id = self.insert_user(user_json)
        logging.info('inserted user with recipient id=%s', rec_id)

        return user_json

    def create_certificate_request(self, pubkey):
        cert_json = formatters.pubkey_to_cert_request(pubkey)
        cert_id = self.insert_certificate(cert_json=cert_json)
        return cert_id

    def insert_user(self, user_json):
        """Exposed separately to ease testing"""
        user_id = CertificateStore.insert_shim(self.db.recipients, user_json)
        return user_id

    def insert_certificate(self, cert_json):
        """Exposed separately to ease testing"""
        cert_id = CertificateStore.insert_shim(self.db.certificates, cert_json)
        return cert_id

    @staticmethod
    def insert_shim(collection, document):
        """This is an unfortunate workaround for mongo mock. It doesn't support insert, so this allows an easy patch"""
        inserted_id = collection.insert_one(document)
        return inserted_id
