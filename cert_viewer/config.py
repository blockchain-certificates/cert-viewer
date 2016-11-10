import os

import configargparse

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))


def create_config():
    p = configargparse.getArgumentParser(default_config_files=[os.path.join(BASE_DIR, 'conf_local.ini'),
                                                               os.path.join(BASE_DIR, 'conf.ini'),
                                                               '/etc/cert-issuer/conf.ini'])
    p.add('-c', '--my-config', required=False, is_config_file=True, help='config file path')
    p.add_argument('--notifier_type', default='noop', type=str, env_var='NOTIFIER_TYPE',
                   help='type of notification on certificate introduction')
    p.add_argument('--mongodb_uri', default='mongodb://localhost:27017/test', type=str, env_var='MONGODB_URI',
                   help='mongo connection URI')
    p.add_argument('--from_email', type=str, env_var='FROM_EMAIL',
                   help='email address from which notification should be sent')
    p.add_argument('--from_name', type=str, env_var='FROM_NAME', help='name from which notification should be sent')
    p.add_argument('--subject', type=str, env_var='SUBJECT', help='notification subject line')
    p.add_argument('--recent_certids', type=str, env_var='RECENT_CERTIDS', help='recent certificate ids')
    p.add_argument('--secret_key', type=str, env_var='SECRET_KEY',
                   help='Flask secret key, to enable cryptographically signed sessions')
    p.add_argument('--cert_store_type', type=str, env_var='CERT_STORE_TYPE', help='type of key value store to use for Cert Store')
    p.add_argument('--cert_store_path', type=str, env_var='CERT_STORE_PATH', help='path to file system Cert Store')
    p.add_argument('--v1_aware', action='store_true', env_var='V1_AWARE', help='Whether to support v1 certs')

    args, _ = p.parse_known_args()
    return args


parsed_config = None


def get_config():
    global parsed_config
    if parsed_config:
        return parsed_config
    parsed_config = create_config()
    return parsed_config
