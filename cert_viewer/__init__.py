import logging.config
import os
from flasgger import Swagger
from flask import Flask
from pymongo import MongoClient

import gridfs

from .forms import SimpleRegistrationForm, BitcoinForm

from simplekv.fs import FilesystemStore


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

app = Flask(__name__)
Swagger(app)
logging.config.fileConfig(os.path.join(BASE_DIR, 'logging.conf'))
log = logging.getLogger(__name__)

from . import views

mongo_connection = None
cert_store = None
verifier = None
intro_store = None

from cert_store.certificate_store import CertificateStore, V1AwareCertificateStore
from cert_store.gridfs_key_value_store import GridfsKeyValueStore
from cert_viewer.verifier_bridge import V1AwareCertificateVerifierBridge, CertificateVerifierBridge
from cert_viewer.introduction_store_bridge import IntroStore

def configure_app(configuration):
    mongo_client = MongoClient(host=configuration.mongodb_uri)
    conn = mongo_client[
        configuration.mongodb_uri[configuration.mongodb_uri.rfind('/') + 1:len(configuration.mongodb_uri)]]
    global mongo_connection
    mongo_connection = conn

    if configuration.cert_store_type == 'simplekv_fs':
        kv_store = FilesystemStore(configuration.cert_store_path)
        log.info('Configured a file system certificate store with path=%s', configuration.cert_store_path)
    elif configuration.cert_store_type == 'simplekv_gridfs':
        gfs = gridfs.GridFS(conn)
        kv_store = GridfsKeyValueStore(gfs)
        log.info('Configured a gridfs certificate store')


    global cert_store, verifier
    if configuration.v1_aware:
        cert_store = V1AwareCertificateStore(kv_store, mongo_connection)
        verifier = V1AwareCertificateVerifierBridge(cert_store)
    else:
        cert_store = CertificateStore(kv_store)
        verifier = CertificateVerifierBridge(cert_store)

    global intro_store
    intro_store = IntroStore(mongo_connection)
    app.secret_key = configuration.secret_key
