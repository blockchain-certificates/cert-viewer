---
layout: page
title: Verifying a certificate
---

# Manually verify a certificate
To manually verify a digital certificate, follow the instructions below. These instructions will require Python 2.7 and the Python [python-bitcoinlib](https://github.com/petertodd/python-bitcoinlib). These can be installed with:

```
pip install python-bitcoinlib
```

#### 1. Download the certificate and blockchain transaction
To compare the local certificate to the certificate transacted on the Bitcoin blockchain, first download a copy of both the local certificate and the record of the certificate's transaction on the blockchain. For example, the json of a local certificate can be found at `https://coins.media.mit.edu/<CERTIFICATE_UID>?format=json`. The json from [blockchain.info](http://blockchain.info) can be found at `http://blockchain.info/tx/<TRANSACTION_ID>?format=json`.

#### 2. Check that the certificate was authored by the Media Lab
To check that the certificate was authored by the Media Lab, we will verify that the signature in the local certificate file was signed by the Media Lab's private key.

Our public key can be found at [https://coins.media.mit.edu/keys/ml-certs-public-key.asc](https://coins.media.mit.edu/keys/ml-certs-public-key.asc). This needs to be copy/pasted into the code.

```python
import json
import binascii
import hashlib
from bitcoin.signmessage import BitcoinMessage, VerifyMessage, SignMessage

valid_author = False

ml_pubkey = <INSERT_MEDIA_LAB_PUBLIC_KEY_HERE>

with open(<INSERT_PATH_TO_LOCAL_CERTIFICATE_FILE>) as coin_file:
    coin_data = json.load(coin_file)
coin_file.close()
uid = BitcoinMessage(coin_data["assertion"]["uid"])
if coin_data.get("signature", None):
    signed_uid = coin_data["signature"]
    valid_author = VerifyMessage(ml_pubkey, uid, signed_uid)

print "Valid author:"
print valid_author
```

#### 3. Compare the hash of the local certificate to the hash embedded in the certificate transaction on the Bitcoin blockchain
To check that the certificate was sent to the Bitcoin blockchain by the Media Lab, we will compare the hash of the local certificate with the hash embedded in the record of its transaction on the Bitcoin blockchain.

```python
valid_hash = False
blockchain_data = json.loads(open(<INSERT_PATH_TO_BLOCKCHAIN_TRANSACTION_FILE>).read())
raw_coin_data = open(<INSERT_PATH_TO_LOCAL_CERTIFICATE_FILE>).read()
local_hash = hashlib.sha256(raw_coin_data).hexdigest()

transaction_outs = blockchain_data["out"]
for tx_out in transaction_outs:
    if tx_out.get("addr") == None:
        opreturn_tx = tx_out
op_field = opreturn_tx["script"].decode("hex")
hash_from_chain = binascii.hexlify(op_field)

if local_hash in hash_from_chain or local_hash == hash_from_chain:
    valid_hash = True

print "Valid hash:"
print valid_hash
```

#### 4. Check that the certificate has not been revoked
We will check that the certificate has not been revoked by the issuer. To do this, we will check that the BTC transferred to the Media Lab’s revocation address has not been spent. 

Our revocation key can be found at [https://coins.media.mit.edu/keys/ml-certs-revoke-key.asc](https://coins.media.mit.edu/keys/ml-certs-revoke-key.asc). This needs to be copy/pasted into the code.

```python
not_revoked = False

revocation_address = <INSERT_REVOCATION_ADDRESS_HERE>

transaction_outs = blockchain_data["out"]
for tx_out in transaction_outs:
    if tx_out.get("addr", None) == revocation_address and tx_out.get("spent", None) == False:
        not_revoked = True

print "Not revoked:"
print not_revoked
```

#### 5. Check that all three criteria are met and return if the certificate is valid.
Lastly, we will check that all the above steps are valid. If so, the certificate is valid!

```python
valid_coin = False
if valid_author and valid_hash and not_revoked:
    valid_coin = True

print "Valid coin:" 
print valid_coin
```

Questions / Comments? Please contact Juliana at [juliana@media.mit.edu](mailto:juliana@media.mit.edu) or send a pull request.
