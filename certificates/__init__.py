import logging
import os

import certificates.ui_helpers as helpers
from certificates import config
from certificates.certificate_repo import CertificateRepo
from certificates.certificate_repo import UserData
from certificates.forms import RegistrationForm, BitcoinForm
from flask import Flask

app = Flask(__name__)

import certificates.views


app.secret_key = config.get_config().get('ui', 'SECRET_KEY')

certificate_repo = CertificateRepo()


# Configure logging
def initialize_logger(output_dir):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to info
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # create file handler and set level to info
    handler = logging.FileHandler(os.path.join(output_dir, "info.log"), "w", encoding=None, delay="true")
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)


# TODO: clean this up
initialize_logger('/tmp/')



