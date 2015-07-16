from __future__ import absolute_import, division, unicode_literals
import hashlib
import json
import binascii
import os
import urllib2

from bitcoin.signmessage import BitcoinMessage, VerifyMessage

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

def get_hash_from_bc_op(tx_json):
        tx_outs = tx_json["out"]
        for o in tx_outs:
                if o.get("addr") == None:
                        op_tx = o
        op_field = op_tx["script"].decode("hex")
        hashed_json = op_field.split(CERT_MARKER)[-1]
        return hashed_json

def verify_signature(address, signed_cert_path):
        signed_json = json.loads(open(signed_cert_path).read())
        message = BitcoinMessage(signed_json["assertion"]["uid"])
        signature = signed_json["signature"]
        return VerifyMessage(address, message, signature)

def verify_doc(tx_id, signed_cert_path):
        doc = open(signed_cert_path).read()
        hash_from_local = hashlib.sha256(open(signed_cert_path).read()).hexdigest()
        tx_json = get_rawtx(tx_id)
        hash_from_bc = binascii.hexlify(get_hash_from_bc_op(tx_json))
        if hash_from_local in hash_from_bc:
                return True
        return False

# outputs = json.loads(open("output.json").read())
# final_folder = "/home/juliana/Desktop/final/"
# for filename in os.listdir(final_folder):
# 	raw_file = open(final_folder+filename).read()
# 	json_file = json.loads(raw_file)
# 	tx_id = outputs[filename.split(".")[0]]
# 	print "SIG_VERIFICATION: \t" + str(verify_signature(BLOCKCHAIN_ADDRESS, json_file))
# 	print "VERIFY_OP_RETURN: \t" + str(verify_doc(final_folder+filename,offline=False,tx_id=tx_id))
