"""Retrieves certificates from mongodb and stores certificate requests.  """
import logging

import gridfs
from bson.objectid import ObjectId
from pymongo import MongoClient

from . import config, helpers
from .notifier import Notifier


class CertificateStore:
    def __init__(self,
                 client=None,
                 gfs=None,
                 notifier=None):
        """Create a CertificateStore

        :param client: mongo client
        :param gfs: gridfs
        :param notifier: notifier

        """
        self.client = client or MongoClient(host=config.get_config().MONGO_URI)
        print(config.get_config().MONGO_URI)
        certificates_db_name = config.get_config().CERTIFICATES_DB
        self.gfs = gfs or gridfs.GridFS(self.client[certificates_db_name])
        self.db = self.client[certificates_db_name]
        self.notifier = notifier or Notifier.factory()

    def get_formatted_certificate(self, certificate_uid, requested_format):
        logging.debug('Retrieving certificate for uid=%s', certificate_uid)
        award = None
        verification_info = None
        certificate = self.find_certificate_by_uid(uid=certificate_uid)
        if certificate:
            if requested_format == "json":
                award = self.find_file_in_gridfs(
                    helpers.certificate_to_filename(certificate))
                verification_info = None
            else:
                award, verification_info = self.get_award_and_verification_for_certificate(
                    certificate)
        else:
            logging.warning(
                'Certificate metadata not found for certificate uid=%s',
                certificate_uid)

        if certificate and not award:
            logging.error('Problem looking up certificate for certificate uid=%s, '
                          'but certificate metadata was found', certificate_uid)
        return award, verification_info

    def get_award_and_verification_for_certificate(self, certificate):
        filename = helpers.certificate_to_filename(certificate)
        gfs_file = self.find_file_in_gridfs(filename)
        if not gfs_file:
            logging.warning('File not found in gridfs, filename=%s', filename)
            return None, None

        pubkey_content = config.get_config().CERT_PUBKEY
        award = helpers.gfs_file_to_award(
            gfs_file, pubkey_content, certificate)
        verification_info = helpers.format_verification_info(certificate)
        return award, verification_info

    def find_certificate_by_uid(self, uid=None):
        """
        Find certificate by certificate uid
        :param uid: certificate uid
        :return: certificate from certificates collection
        """
        certificate = None
        if uid:
            certificate = self.db.certificates.find_one(
                {'_id': ObjectId(uid), 'issued': True})
        return certificate

    def find_file_in_gridfs(self, filename):
        certfile = self.gfs.find_one({'filename': filename})
        if certfile:
            contents = certfile.read()
            if isinstance(contents, (bytes, bytearray)):
                return contents.decode("utf-8")
            return contents
        return None

    def insert_certificate(self, cert_json):
        """Exposed separately to ease testing"""
        cert_id = CertificateStore.insert_shim(self.db.certificates, cert_json)
        return cert_id.inserted_id

    @staticmethod
    def insert_shim(collection, document):
        """This is an unfortunate workaround for mongo mock. It doesn't support insert, so this allows an easy patch"""
        inserted_id = collection.insert_one(document)
        return inserted_id
