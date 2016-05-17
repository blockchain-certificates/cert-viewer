import logging
import os

from . import config
from .certificate_store import CertificateStore
from .models import UserData
from .forms import RegistrationForm, BitcoinForm
from flask import Flask

app = Flask(__name__)

app.secret_key = config.get_config().get('ui', 'SECRET_KEY')

certificate_service = CertificateStore()


def initialize_logger():
    """Configure logging settings"""
    log_output_dir = config.get_config().get('logging', 'LOG_DIR')
    log_file_name = config.get_config().get('logging', 'LOG_FILE_NAME')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to info
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # create file handler and set level to info
    handler = logging.FileHandler(os.path.join(log_output_dir, log_file_name), "w", encoding=None, delay="true")
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

initialize_logger()

# keep here to avoid circular dependencies
from . import views




