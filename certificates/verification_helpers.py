from __future__ import absolute_import, division, unicode_literals

import hashlib
import json
import logging

import requests
from bitcoin.signmessage import BitcoinMessage, VerifyMessage
from certificates import config
from certificates.ui_helpers import unhexlify, hexlify


def verify(self, transaction_id, signed_local_file):
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


def get_hash_from_bc_op(tx_json):
    tx_outs = tx_json["out"]
    for o in tx_outs:
        if int(o.get("value", 1)) == 0:
            op_tx = o
    hashed_json = unhexlify(op_tx["script"])
    return hashed_json


def check_revocation(tx_json, revoke_address):
    tx_outs = tx_json["out"]
    for o in tx_outs:
        if o.get("addr") == revoke_address and o.get("spent") == False:
            return True
    return False


def compute_hash(doc):
    return hashlib.sha256(doc).hexdigest()


def fetch_hash_from_chain(tx_json):
    hash_from_bc = hexlify(get_hash_from_bc_op(tx_json))
    return hash_from_bc


def compare_hashes(hash1, hash2):
    if hash1 in hash2 or hash1 == hash2:
        return True
    return False


def check_author(address, signed_json):
    uid = signed_json['assertion']['uid']
    message = BitcoinMessage(uid)
    if signed_json.get('signature', None):
        signature = signed_json['signature']
        logging.debug('Found signature for uid=%s; verifying message', uid)
        return VerifyMessage(address, message, signature)
    logging.warning('Missing signature for uid=%s', uid)
    return False
