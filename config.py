import json
import os
from configparser import ConfigParser  # TODO: switch for python 2/3

import helpers

DEFAULT_CONFIG_FILE = '/Users/kim/projects/coins.media.mit.edu/conf.ini'  # TODO: rel path


def get_config_file():
    return os.environ.get('CONFIG_FILE', DEFAULT_CONFIG_FILE)

CONFIG_FILE = get_config_file()


def create_config(config_file=None):
    parser = ConfigParser()
    ConfigParser()

    parser.read(config_file or CONFIG_FILE)
    return parser

CONFIG = create_config()


def get_config():
    return CONFIG

def get_key_by_type(key_type):
    key_name = get_config().get('keys', key_type)
    return get_key_by_name(key_name)

def get_key_by_name(key_name):
    """Ugh, todo: clean this up"""
    pubkey = get_config().get('keys', 'CERT_PUBKEY')
    revokekey = get_config().get('keys', 'CERT_REVOKEKEY')

    key_mappings = {pubkey: "issuer_key", revokekey: "revocation_key"}
    issuer = json.loads(helpers.read_file(get_config().get('keys', 'MLISSUER_PATH')))
    address = key_mappings.get(key_name, None)
    return issuer[address][0]["key"]