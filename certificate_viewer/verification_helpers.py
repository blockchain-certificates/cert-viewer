from __future__ import absolute_import, division, unicode_literals

import hashlib
import json
import logging

import requests
from bitcoin.signmessage import BitcoinMessage, VerifyMessage
from . import config
from .ui_helpers import unhexlify, hexlify
from functools import partial


def lookup_transaction_from_blockchain(transaction_id):
    return requests.get("https://blockchain.info/rawtx/%s?cors=true" % transaction_id)


def verify_with_lookup_function(transaction_id, signed_local_file, transaction_lookup):
    signed_local_json = json.loads(signed_local_file)
    r = transaction_lookup(transaction_id)
    verify_response = []
    verified = False
    if r.status_code != 200:
        logging.error('Error looking up by transaction_id=%s, status_code=%d', transaction_id, r.status_code)
        verify_response.append(('Looking up by transaction_id', False))
        verify_response.append(("Verified", False))
    else:
        verify_response.append(("Computing SHA256 digest of local certificate", "DONE"))
        verify_response.append(("Fetching hash in OP_RETURN field", "DONE"))
        remote_json = r.json()

        # compare hashes
        local_hash = compute_hash(signed_local_file)
        remote_hash = fetch_hash_from_chain(remote_json)
        compare_hash_result = compare_hashes(local_hash, remote_hash)
        verify_response.append(("Comparing local and blockchain hashes", compare_hash_result))

        # check author
        issuing_address = config.get_key_by_type('CERT_PUBKEY')
        verify_authors = check_author(issuing_address, signed_local_json)
        verify_response.append(("Checking signature", verify_authors))

        # check revocation
        revocation_address = config.get_key_by_type('CERT_REVOKEKEY')
        not_revoked = check_revocation(remote_json, revocation_address)
        verify_response.append(("Checking not revoked by issuer", not_revoked))

        if compare_hash_result and verify_authors and not_revoked:
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
    doc_bytes = doc
    if not isinstance(doc, (bytes, bytearray)):
        doc_bytes = doc.encode('utf-8')
    return hashlib.sha256(doc_bytes).hexdigest()


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


default_verifier = partial(verify_with_lookup_function, transaction_lookup=lookup_transaction_from_blockchain)
