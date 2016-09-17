"""Utilities to convert certificates to user-friendly award display"""
import binascii
import json
import sys

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


def certificate_to_filename(certificate):
    return certificate_uid_to_filename(parse_certificate_uid(certificate))


def certificate_uid_to_filename(uid):
    return uid + '.json'


def parse_standard_id_location(json_obj):
    return str(json_obj['_id'])


def parse_certificate_uid(certificate):
    return parse_standard_id_location(certificate)


def parse_txid(certificate):
    return certificate['txid']


def format_verification_info(certificate):
    return {
        'uid': parse_certificate_uid(certificate),
        'transactionID': parse_txid(certificate)
    }


def gfs_file_to_award(gfs_file, pubkey_content, certificate):
    json_certificate = json.loads(gfs_file)
    award = {
        'logoImg': json_certificate['certificate']['issuer']['image'],
        'name': json_certificate['recipient']['givenName'] + ' ' + json_certificate['recipient']['familyName'],
        'title': json_certificate['certificate']['title'],
        'subtitle': json_certificate['certificate']['subtitle']['content'],
        'display': json_certificate['certificate']['subtitle']['display'],
        'organization': json_certificate['certificate']['issuer']['name'],
        'text': json_certificate['certificate']['description'],
        'signatureImg': json_certificate['assertion']['image:signature'],
        'publicKey': pubkey_content,
        'publicKeyURL': json_certificate['verify']['signer'],
        'transactionID': parse_txid(certificate),
        'transactionIDURL': 'https://blockchain.info/tx/' + parse_txid(certificate),
        'issuedOn': json_certificate['assertion']['issuedOn']
    }
    award = check_display(award)
    return award


def check_display(award):
    if award['display'] == 'FALSE':
        award['subtitle'] = ''
    return award
