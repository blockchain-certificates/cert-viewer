import logging

import os
from flask import Flask
from . import config
from .certificate_store import CertificateStore
from .forms import RegistrationForm, BitcoinForm

app = Flask(__name__)

app.secret_key = config.get_config().SECRET_KEY

cert_store = CertificateStore()


def initialize_logger():
    """Configure logging settings"""
    log_output_dir = config.get_config().LOG_DIR
    log_file_name = config.get_config().LOG_FILE_NAME
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to info
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # create file handler and set level to info
    handler = logging.FileHandler(
        os.path.join(
            log_output_dir,
            log_file_name),
        "w",
        encoding=None,
        delay="true")
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)


initialize_logger()

# keep here to avoid circular dependencies
from . import views
