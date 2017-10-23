[![Build Status](https://travis-ci.org/blockchain-certificates/cert-viewer.svg?branch=master)](https://travis-ci.org/blockchain-certificates/cert-viewer)

# cert-viewer

The cert-viewer project is a Flask webapp to display and verify blockchain certificates after they have been issued and to allow learners to request a certificate and generate their own Bitcoin identity needed for the certificate creation process. 

## Install and Run

1. Ensure you have a python environment. [Recommendations](https://github.com/blockchain-certificates/cert-issuer/blob/master/docs/virtualenv.md)

2. Git clone the repository and change to the directory

    ```bash
    git clone https://github.com/blockchain-certificates/cert-viewer.git && cd cert-viewer
    ```

3. Setup your conf.ini file (see 'Configuration')

4. Run cert-viewer setup

    ```bash
    pip install .
    ```

5. Run the flask server

    ```shell
    python run.py -c conf_local.ini
    ```

6. Open `http://localhost:5000`

### Using GridFS

The basic configuration uses a file system certificate store, under the `cert_data` directory. To use GridFS instead, install [mongodb](https://docs.mongodb.com/v3.0/installation/) and start mongo database before running cert-viewer.

## Deployment considerations

The quick start made simplifications that you would not want in a real deployment. Here are some of the factors to consider:

### Certificate storage

Cert-viewer relies on the Blockchain Certificates module [cert-store](https://github.com/blockchain-certificates/cert-store) for accessing certificates. This uses the [simplekv](https://github.com/mbr/simplekv) for extensibility. By default, cert-viewer is configured to use a file system key value store, pointing to the `cert-data` folder. See [cert-store](https://github.com/blockchain-certificates/cert-store) for information on other certificate storage options. 

### Recipient introductions/requests

Early Blockchain Certificates deployments assumed recipients would fill out the 'certificate request' form (included in this project) to provide their information such as name, email, and bitcoin address. This web form is no longer needed if your recipients are using [cert-wallet](https://github.com/blockchain-certificates/cert-wallet). Cert-wallet is easier for recipients to use because it handles key generation.

Cert-viewer exposes an `introduction` REST endpoint used by both cert-wallet and, if you are using it, the web form. Advanced configuration options allow the `introduction` endpoint to store the certificates in mongodb, but this would ideally be changes to an interface supporting a broad range of data stores.

You may host the `introduction` endpoint in a separate location, but make sure to specify that location in the issuer identity json.

It is assumed that you will perform your own orchestration after receiving an introduction/request and before issuing. For example, you would want to verify the recipient is eligible, etc.

#### Notifications

If you expose the 'certificate request' form, you may enable mandrill email alerts. This is mainly kept for backwards compatibility -- if you want to use this, you may choose to generalize or improve the `notifier.py` class.

If you are enabling mandrill email notificates, you may use a template like this [receipt-template Mandrill template](https://us13.admin.mailchimp.com/templates/share?id=56461169_1921351b9adabaa4610f_us13). 

Also see the `notifier`, `mandrill_api_key`, and `subject` configuration options.

### Site templates and themes

Cert-viewer uses [Flask-Themes2](http://flask-themes2.readthedocs.io/en/latest/) to allow you to personalize your deployment. This would include your organization's images, stylesheets, and flask templates. See cert_viewer\themes for examples.

You would also include your issuer identification json file under <your_theme>\static\issuer


## Configuration

The quick start instructions use the basic configuration options in `conf_local.ini`. This describes all available configuration options. Refer to 'Deployment considerations' for additional details about these options.

1. Copy the template ini file

    ```bash
    cp conf_template.ini conf.ini
    ```
    
2. Basic configuration options:
    - `secret_key` is a random string used by Flask as a secret key to enable cryptographically signed session
    - `cert_store_path` is the file system path to the certificates
    - `theme` is the Flask Theme you want to use for your styling, static content, and templates. We provide a few configuration options for your issuer branding, but in a real deployment, issuers should extend the base theme to provide their own styling. Cert-viewer uses [Flask-Themes2](http://flask-themes2.readthedocs.io/en/latest/)
    - `issuer_email` is used in the flask templates for your contact info
    - `issuer_name` is used in the flask templates for your organization name
    - `issuer_logo_path` is used in the flask templates as a path to organization's logo
    - `recent_certids` is a comma-separated list of certificate uids. Use this if you want to show sample certificates on your home page.  
        
3. Advanced configuration options:
    - `cert_store_type` is the type of key value store to use for certificates, using simplekv. simplekv_fs uses the file system, and simplekv_gridfs uses gridfs
        - when using gridfs (mongodb) as a certificate store you can use `mongo-seed/load_gfs.py` script to load the certificates into mongodb    
    - `mongodb_uri` is used to access your mongodb instance for storing recipient introductions/requests. The canonical form is `mongodb://<username>:<password>@<domain>:<mongo_port>/<db_name>`. Examples follow:
        - Local mongo installation: `mongodb_uri = mongodb://localhost:27017/test`
        - Docker installation: `mongodb_uri = mongodb://<DOCKER_MACHINE_IP>:27017/test`, where DOCKER_MACHINE_IP is given by `docker-machine ip`
    - `notifier` is a noop by default. This is used if you want to enable web form certificate requests, as opposed to or in addition to, cert-wallet introductions. To send mandrill notifications, use `mail`
    - `mandrill_api_key` if notifier is `mail`, this is used to send out notifications when a user signs up. Setup your mandrill account at https://www.mandrill.com/
    - `subject` if using a `mail` notifier, this is the subject line to use

## Advanced: Docker Setup

To experiment with running cert-viewer and enable recipient introductions stored in MongoDB, you can use our Docker files.

1. First ensure you have Docker installed. [See our Docker installation help](https://github.com/blockchain-certificates/cert-issuer/blob/master/docs/docker_install.md).
   
2. Git clone the repository and change to the directory

    ```bash
    git clone https://github.com/blockchain-certificates/cert-viewer.git && cd cert-viewer
    ```

3. From a command line in the cert-viewer dir, run docker-compose

    ```bash
    docker-compose build
    ```

4. Start the container

    ```bash
    docker-compose up
    ```

5. The output of the previous command (example below) will tell you how to access the site. You can enter that value in a browser.
    ```
    web_1         | INFO -  * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
    ```

## Unit tests

This project uses tox to validate against several python environments.

1. Ensure you have an python environment. [Recommendations](https://github.com/blockchain-certificates/cert-issuer/blob/master/docs/virtualenv.md)

2. Run tests
    ```
    ./run_tests.sh
    ```

## Contact

Contact us at [the Blockcerts community forum](http://community.blockcerts.org/).

