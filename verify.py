from __future__ import absolute_import, division, unicode_literals
import hashlib
import json
import binascii
import os
import urllib2

import config

def fetchurl(url, data=None):
        try:
                result = urllib2.urlopen(url, data=data)
                return result.read()
        except urllib2.URLError, e:
                print e

def get_rawtx(tx_index):
        url = "https://blockchain.info/rawtx/%s" % tx_index
        tx_json = json.loads(fetchurl(url))
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

def verify_doc(tx_id, signed_cert_path, cert_marker):
        doc_integrity = False
        author_integrity = False

        doc = open(signed_cert_path).read()
        hash_from_local = hashlib.sha256(open(signed_cert_path).read()).hexdigest()
        tx_json = get_rawtx(tx_id)
        hash_from_bc = binascii.hexlify(get_hash_from_bc_op(tx_json, cert_marker))

        if hash_from_local in hash_from_bc:
                doc_integrity = True
        if get_address_from_bc_op(tx_json, config.BLOCKCHAIN_ADDRESS) == True:
                author_integrity = True
        if doc_integrity and author_integrity:
                return True
        return False