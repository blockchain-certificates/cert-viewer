"""Utilities to convert certificates to user-friendly award display"""
import binascii
import json
import logging
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


def format_verification_info_v1_2(certificate):
    return {
        'uid': str(certificate['document']['assertion']['uid'])
    }


def format_verification_info_v1_1(certificate, txid):
    return {
        'uid': str(certificate['_id']),
        'transactionID': txid
    }

def gfs_file_to_award_v1_2(json_certificate):
    certificate = json_certificate['document']['certificate']
    assertion = json_certificate['document']['assertion']
    recipient = json_certificate['document']['recipient']
    award = {
        'logoImg': certificate['issuer']['image'],
        'name': recipient['givenName'] + ' ' + recipient['familyName'],
        'title': certificate['title'],
        'organization': certificate['issuer']['name'],
        'text': certificate['description'],
        'signatureImg': assertion['image:signature'],
        'publicKeyURL': json_certificate['document']['verify']['signer'],
        #'transactionID': txid,
        #'transactionIDURL': 'https://blockchain.info/tx/' + txid,
        'issuedOn': assertion['issuedOn']
    }
    if 'subtitle' in certificate:
        award['subtitle'] = certificate['subtitle']

    return award


def gfs_file_to_award_v1_1(json_certificate, txid):
    award = {
        'logoImg': json_certificate['certificate']['issuer']['image'],
        'name': json_certificate['recipient']['givenName'] + ' ' + json_certificate['recipient']['familyName'],
        'title': json_certificate['certificate']['title'],
        'subtitle': json_certificate['certificate']['subtitle']['content'],
        'display': json_certificate['certificate']['subtitle']['display'],
        'organization': json_certificate['certificate']['issuer']['name'],
        'text': json_certificate['certificate']['description'],
        'signatureImg': json_certificate['assertion']['image:signature'],
        'publicKeyURL': json_certificate['verify']['signer'],
        'transactionID': txid,
        'transactionIDURL': 'https://blockchain.info/tx/' + txid,
        'issuedOn': json_certificate['assertion']['issuedOn']
    }
    award = check_display(award)
    return award


def check_display(award):
    if award['display'] == 'FALSE':
        award['subtitle'] = ''
    return award


def get_award_and_verification_for_certificate(certificate_json, txid):
    award = gfs_file_to_award_v1_2(certificate_json)
    verification_info = format_verification_info_v1_2(certificate_json)
    return award, verification_info
