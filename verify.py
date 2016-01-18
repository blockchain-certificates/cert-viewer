from __future__ import absolute_import, division, unicode_literals
import hashlib
import json
import binascii
import os
import urllib2

import config
from bitcoin.signmessage import BitcoinMessage, VerifyMessage, SignMessage

def fetchurl(url, data=None):
        try:
                result = urllib2.urlopen(url, data=data)
                return result.read()
        except urllib2.URLError, e:
                print e
                return 'error'

def get_rawtx(tx_index):
        url = "https://blockchain.info/rawtx/%s" % tx_index
        data = fetchurl(url)
        if data == 'error':
                return data
        tx_json = json.loads(data)
        return tx_json

def get_hash_from_bc_op(tx_json, cert_marker):
        tx_outs = tx_json["out"]
        for o in tx_outs:
            if o.get("addr") == None:
                op_tx = o
        op_field = op_tx["script"].decode("hex")
        hashed_json = op_field.split(cert_marker)[-1]
        return hashed_json

def get_address_from_bc_op(tx_json, address):
        for tx in tx_json["inputs"]:
                if tx["prev_out"]["addr"]==address:
                        return True
        return False

def check_revocation(tx_json, revoke_address):
    # tx_json = get_rawtx(tx_id)
    tx_outs = tx_json["out"]
    for o in tx_outs:
        if o.get("addr") == revoke_address and o.get("spent") == False:
            return True
    return False

def computeHash(doc):
        return hashlib.sha256(doc).hexdigest()

def fetchHashFromChain(tx_json, cert_marker):
        # tx_json = get_rawtx(tx_id)
        if tx_json == 'error':
                return 'error'
        hash_from_bc = binascii.hexlify(get_hash_from_bc_op(tx_json, cert_marker))
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
