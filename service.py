import json
from collections import namedtuple

import gridfs
import requests

import config
import helpers
import verify as v
from certificates import Certificates
from mail import send_receipt_email

UserData = namedtuple('UserData', ['pubkey', 'email', 'degree', 'comments', 'first_name', 'last_name',
                                   'street_address', 'city', 'state', 'zip_code', 'country'])

class Service:
    def __init__(self, client, fs):
        self.client = client
        self.fs = fs
        self.certificates = Certificates(client, fs)

    def get_formatted_certificate(self, identifier, format):
        certificate = self.certificates.find_user_by_uid(uid=identifier)
        if certificate:
            award, verification_info = self.certificates.get_id_info(certificate)
            if len(award) > 0 and len(verification_info) > 0:
                if format == "json":
                    return self.certificates.find_file_in_gridfs(str(certificate["_id"])), None
                return award, verification_info

    def get_or_create_certificate(self, user_data):
        user = self.client.admin.recipients.find_one({"pubkey": user_data.pubkey})
        if user is None:
            self.certificates.create_user(user_data)
        self.certificates.create_cert(user_data.pubkey)
        # TODO exceptions
        sent = send_receipt_email(user_data.email,
                                  {"givenName": user_data.first_name, "familyName": user_data.last_name})
        return sent

    def get_verify_response(self, transaction_id, uid):
        signed_local_file = self.certificates.find_file_in_gridfs(uid)
        signed_local_json = json.loads(signed_local_file)
        r = requests.get("https://blockchain.info/rawtx/%s?cors=true" % transaction_id)
        if r.status_code != 200:
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
            issuing_address = helpers.get_keys(config.ML_PUBKEY)
            verify_authors = v.check_author(issuing_address, signed_local_json)
            verify_response.append(("Checking Media Lab signature", verify_authors))

            # check revocation
            revocation_address = helpers.get_keys(config.ML_REVOKEKEY)
            not_revoked = v.check_revocation(remote_json, revocation_address)
            verify_response.append(("Checking not revoked by issuer", not_revoked))

            if compare_hashes and verify_authors and not_revoked:
                verified = True
            verify_response.append(("Verified", verified))
        return verify_response
