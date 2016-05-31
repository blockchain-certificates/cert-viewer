import json
import os
import sys

if sys.version > '3':
    from configparser import ConfigParser
else:
    from ConfigParser import ConfigParser


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

DEFAULT_CONFIG_FILE = os.path.join(BASE_DIR, 'conf.ini')
TEST_CONFIG_FILE = os.path.join(BASE_DIR, 'conf_test.ini')


def create_config(config_file=None):
    parser = ConfigParser()
    config_env = os.environ.get('CONFIG_FILE', DEFAULT_CONFIG_FILE)
    config_files = []
    if config_file:
        config_files.append(config_file)
    if config_env:
        config_files.append(config_env)

    config_files.append(DEFAULT_CONFIG_FILE)
    config_files.append(TEST_CONFIG_FILE)
    parser.read(config_files)
    return parser


CONFIG = create_config()


def read_file(path):
    with(path) as f:
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
    issuer_path = get_config().get('keys', 'ISSUER_PATH')
    # TODO: load this through flask at startup
    issuer_file = read_file(os.path.join(BASE_DIR, 'cert_viewer', issuer_path))
    issuer = json.loads(issuer_file)
    address = key_mappings.get(key_name, None)
    return issuer[address][0]["key"]
