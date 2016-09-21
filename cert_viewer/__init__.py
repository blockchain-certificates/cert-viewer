import logging

import os
from flask import Flask
from . import config
from .forms import RegistrationForm, BitcoinForm

import gridfs
from pymongo import MongoClient

app = Flask(__name__)

cert_store_connection = None


def set_cert_store(conf):
    from cert_store.certificate_store import CertificateStore
    global cert_store_connection
    mongo_client = MongoClient(host=conf.mongodb_uri)
    db = mongo_client[conf.mongodb_uri[conf.mongodb_uri.rfind('/') + 1:len(conf.mongodb_uri)]]
    gfs = gridfs.GridFS(db)
    cert_store_connection = CertificateStore(mongo_client, gfs, db)


def initialize_logger(conf):
    """Configure logging settings"""
    log_output_dir = conf.log_dir
    log_file_name = conf.log_file_name
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


# keep here to avoid circular dependencies
from . import views
