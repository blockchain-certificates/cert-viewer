import binascii
import sys

from cert_schema import Chain, UnknownChainError

unhexlify = binascii.unhexlify
hexlify = binascii.hexlify
if sys.version > '3':
    unhexlify = lambda h: binascii.unhexlify(h.encode('utf8'))
    hexlify = lambda b: binascii.hexlify(b).decode('utf8')


def obfuscate_email_display(email):
    """Partially hides email before displaying"""
    hidden_email_parts = email.split("@")
    hidden_email = hidden_email_parts[0][:2] + ("*" * (len(hidden_email_parts[0]) - 2)) + "@" + hidden_email_parts[1]
    return hidden_email


def get_tx_lookup_prefix_for_chain(chain):
    if chain == Chain.testnet:
        return 'https://tbtc.blockr.io/tx/info/'
    elif chain == Chain.mainnet:
        return 'https://blockchain.info/tx/'
    else:
        raise UnknownChainError(
            'unsupported chain (%s) requested with blockcypher collector. Currently only testnet and mainnet are supported' % chain)
