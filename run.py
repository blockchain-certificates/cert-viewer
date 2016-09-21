#!/usr/bin/env python


import os
import sys

import cert_viewer
from cert_viewer import config

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]

    conf = config.get_config()
    cert_viewer.initialize_logger(conf)
    cert_viewer.set_cert_store(conf)
    port = int(os.environ.get('PORT', 5000))
    from cert_viewer import app
    cert_viewer.initialize_logger(conf)
    app.secret_key = conf.secret_key
    app.run('0.0.0.0', port=port)


if __name__ == "__main__":
    main()
