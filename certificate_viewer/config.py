import json
import os
import sys

if sys.version > '3':
    from configparser import ConfigParser
else:
    from ConfigParser import ConfigParser


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

DEFAULT_CONFIG_FILE = os.path.join(BASE_DIR, 'conf.ini')


def get_config_file():
    return os.environ.get('CONFIG_FILE', DEFAULT_CONFIG_FILE)


CONFIG_FILE = get_config_file()


def create_config(config_file=None):
    parser = ConfigParser()

    parser.read(config_file or CONFIG_FILE)
    return parser


CONFIG = create_config()


def read_file(path):
    with open(path) as f:
        data = f.read()
    return data


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
    issuer_path = get_config().get('keys', 'MLISSUER_PATH')
    # TODO: load this through flask at startup
    issuer_file = read_file(os.path.join(BASE_DIR, 'certificate_viewer', issuer_path))
    issuer = json.loads(issuer_file)
    address = key_mappings.get(key_name, None)
    return issuer[address][0]["key"]
