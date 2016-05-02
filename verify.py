from __future__ import absolute_import, division, unicode_literals

import binascii
import hashlib

from bitcoin.signmessage import BitcoinMessage, VerifyMessage


def get_hash_from_bc_op(tx_json):
    tx_outs = tx_json["out"]
    for o in tx_outs:
        if int(o.get("value", 1)) == 0:
            op_tx = o
    hashed_json = op_tx["script"].decode("hex")
    return hashed_json


def check_revocation(tx_json, revoke_address):
    tx_outs = tx_json["out"]
    for o in tx_outs:
        if o.get("addr") == revoke_address and o.get("spent") == False:
            return True
    return False


def computeHash(doc):
    return hashlib.sha256(doc).hexdigest()


def fetchHashFromChain(tx_json):
    hash_from_bc = binascii.hexlify(get_hash_from_bc_op(tx_json))
    return hash_from_bc


def compareHashes(hash1, hash2):
    if hash1 in hash2 or hash1 == hash2:
        return True
    return False


def checkAuthor(address, signed_json):
    message = BitcoinMessage(signed_json["assertion"]["uid"])
    if signed_json.get("signature", None):
        signature = signed_json["signature"]
        return VerifyMessage(address, message, signature)
    return False
