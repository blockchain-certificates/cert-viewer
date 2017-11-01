#!/usr/bin/env python
import os

from cert_viewer import configure_app
from cert_viewer.config import get_config

def main():
    port = int(os.environ.get('PORT', 5000))
    conf = get_config()
    configure_app(conf)
    from cert_viewer import app
    app.run('0.0.0.0', port=port, threaded=True)


if __name__ == "__main__":
    main()
