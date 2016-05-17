import json


def certificate_to_filename(certificate):
    return certificate_uid_to_filename(parse_certificate_uid(certificate))


def certificate_uid_to_filename(uid):
    return uid + '.json'

def parse_standard_id_location(json_obj):
    return str(json_obj['_id'])


def parse_user_uid(user):
    return parse_standard_id_location(user)


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
        'mlPublicKey': pubkey_content,
        'mlPublicKeyURL': json_certificate['verify']['signer'],
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


def user_data_to_json(user_data):
    user_json = {'pubkey': user_data.pubkey, 'info': {}}
    user_json['info']['email'] = user_data.email
    user_json['info']['degree'] = user_data.degree
    user_json['info']['comments'] = user_data.comments
    user_json['info']['name'] = {'familyName': user_data.last_name, 'givenName': user_data.first_name}
    user_json['info']['address'] = {
        'streetAddress': user_data.street_address,
        'city': user_data.city,
        'state': user_data.state,
        'zipcode': user_data.zip_code,
        'country': user_data.country
    }
    return user_json


def pubkey_to_cert_request(pubkey):
    return {'pubkey': pubkey, 'issued': False, 'txid': None}