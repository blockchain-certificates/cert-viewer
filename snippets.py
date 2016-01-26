from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
import re
from flask import Markup
import helpers
import config

issuing_address = helpers.read_file(config.MLPUBKEY_PATH)
revocation_address = helpers.read_file(config.MLREVOKEKEY_PATH)

def generate_snippet(s):
	return Markup(highlight(s ,PythonLexer(), HtmlFormatter(full=True, style='monokailight')))

author_code_snippet = r'''
import json
import binascii
import hashlib
from bitcoin.signmessage import BitcoinMessage, VerifyMessage, SignMessage

valid_author = False

ml_pubkey = "%s"

with open("local-coin.json") as coin_file:
    coin_data = json.load(coin_file)
coin_file.close()
uid = BitcoinMessage(coin_data["assertion"]["uid"])
if coin_data.get("signature", None):
    signed_uid = coin_data["signature"]
    valid_author = VerifyMessage(ml_pubkey, uid, signed_uid)

print "Valid author:"
print valid_author
''' % (issuing_address)

hash_code_snippet = r'''
valid_hash = False
blockchain_data = json.loads(open("blockchain-transaction.json").read())
raw_coin_data = open("local-coin.json").read()
local_hash = hashlib.sha256(raw_coin_data).hexdigest()

transaction_outs = blockchain_data["out"]
for tx_out in transaction_outs:
    if tx_out.get("addr") == None:
        opreturn_tx = tx_out
op_field = opreturn_tx["script"].decode("hex")
# hash_from_chain = binascii.hexlify(op_field.split("%s")[-1])
hash_from_chain = binascii.hexlify(op_field)

if local_hash in hash_from_chain or local_hash == hash_from_chain:
    valid_hash = True

print "Valid hash:"
print valid_hash
''' % (config.CERT_MARKER)


revoke_code_snippet = r'''
not_revoked = False

revocation_address = "%s"

transaction_outs = blockchain_data["out"]
for tx_out in transaction_outs:
    if tx_out.get("addr", None) == revocation_address and tx_out.get("spent", None) == False:
        not_revoked = True

print "Not revoked:"
print not_revoked
''' % (revocation_address)

check_all_snippet = r'''
valid_coin = False
if valid_author and valid_hash and not_revoked:
    valid_coin = True

print "Valid coin:" 
print valid_coin
'''

COMPLETE_CODE = generate_snippet(author_code_snippet +"\n\n"+ hash_code_snippet +"\n\n"+ revoke_code_snippet +"\n\n"+ check_all_snippet)

CHECK_AUTHOR_CODE = generate_snippet(author_code_snippet)
CHECK_HASH_CODE = generate_snippet(hash_code_snippet)
CHECK_REVOKE_CODE = generate_snippet(revoke_code_snippet)
CHECK_ALL_CODE = generate_snippet(check_all_snippet)

HIGHLIGHTED_SNIPPETS = [ CHECK_AUTHOR_CODE , CHECK_HASH_CODE, CHECK_REVOKE_CODE, CHECK_ALL_CODE]