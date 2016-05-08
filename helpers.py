import binascii
import json
import sys

import config

unhexlify = binascii.unhexlify
hexlify = binascii.hexlify
if sys.version > '3':
    unhexlify = lambda h: binascii.unhexlify(h.encode('utf8'))
    hexlify = lambda b: binascii.hexlify(b).decode('utf8')

def get_keys(key_name):
    key_mappings = {config.ML_PUBKEY: "issuer_key", config.ML_REVOKEKEY: "revocation_key"}
    issuer = json.loads(read_file(config.MLISSUER_PATH))
    address = key_mappings.get(key_name, None)
    return issuer[address][0]["key"]


def read_file(path):
    with open(path) as f:
        data = f.read()
    return data


def format_email(email):
    hidden_email_parts = email.split("@")
    hidden_email = hidden_email_parts[0][:2] + ("*" * (len(hidden_email_parts[0]) - 2)) + "@" + hidden_email_parts[1]
    return hidden_email
