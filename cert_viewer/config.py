import json
import os

import configargparse

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))


def create_config():
    p = configargparse.getArgumentParser(default_config_files=[os.path.join(BASE_DIR, 'conf_test.ini'),
                                                               os.path.join(BASE_DIR, 'conf.ini'),
                                                               '/etc/cert-issuer/conf.ini'])
    p.add('-c', '--my-config', required=False,
          is_config_file=True, help='config file path')
    p.add_argument('--NOTIFIER_TYPE', default='noop', type=str, env_var='NOTIFIER_TYPE',
                   help='type of notification on certificate introduction')
    p.add_argument('--MONGO_URI', default='mongodb://localhost:27017', type=str, env_var='MONGO_URI',
                   help='mongo connection URI')
    # TODO: update canned data to test db
    p.add_argument('--CERTIFICATES_DB', default='admin', type=str, env_var='CERTIFICATES_DB',
                   help='mongo db name')

    p.add_argument('--FROM_EMAIL', type=str, env_var='FROM_EMAIL',
                   help='email address from which notification should be sent')
    p.add_argument('--FROM_NAME', type=str, env_var='FROM_NAME', help='name from which notification should be sent')
    p.add_argument('--SUBJECT', type=str, env_var='SUBJECT', help='notification subject line')

    p.add_argument('--RECENT_CERTIDS', type=str, env_var='RECENT_CERTIDS', help='recent certificate ids')

    p.add_argument('--LOG_DIR', type=str, env_var='LOG_DIR', help='application log directory')
    p.add_argument('--LOG_FILE_NAME', type=str, env_var='LOG_FILE_NAME', help='application log file name')

    p.add_argument('--SECRET_KEY', type=str, env_var='SECRET_KEY',
                   help='Flask secret key, to enable cryptographically signed sessions')
    p.add_argument('--CRITERIA_PATH', type=str, env_var='CRITERIA_PATH', help='TODO criteria path')
    p.add_argument('--KEY_PATH', type=str, env_var='KEY_PATH', help='TODO key path')
    p.add_argument('--CERT_PUBKEY', type=str, env_var='CERT_PUBKEY', help='TODO pub key')
    p.add_argument('--CERT_REVOKEKEY', type=str, env_var='CERT_REVOKEKEY', help='TODO revoke key')
    p.add_argument('--ISSUER_PATH', type=str, env_var='ISSUER_PATH', help='TODO issuer path')

    p.add_argument('--INTRO_ENDPOINT', type=str, env_var='INTRO_ENDPOINT', help='endpoint for submitting intros')

    args, _ = p.parse_known_args()
    return args


def read_file(path):
    with open(path) as f:
        data = f.read()
    return data


def get_key_by_name(key_name):
    pubkey = get_config().CERT_PUBKEY
    revokekey = get_config().CERT_REVOKEKEY

    key_mappings = {pubkey: "issuer_key", revokekey: "revocation_key"}
    issuer_path = get_config().ISSUER_PATH
    # TODO: load this through flask at startup
    issuer_file = read_file(os.path.join(BASE_DIR, 'cert_viewer', issuer_path))
    issuer = json.loads(issuer_file)
    address = key_mappings.get(key_name, None)
    return issuer[address][0]["key"]


parsed_config = None


def get_config():
    global parsed_config
    if parsed_config:
        return parsed_config
    parsed_config = create_config()
    return parsed_config
