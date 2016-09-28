[![Build Status](https://travis-ci.org/blockchain-certificates/cert-viewer.svg?branch=master)](https://travis-ci.org/blockchain-certificates/cert-viewer)

# cert-viewer

The cert-viewer project is a Flask webapp to display and verify blockchain certificates after they have been issued and
to allow learners to request a certificate and generate their own Bitcoin identity needed for the certificate creation
 process. 

## Quick Start using Docker

### Steps


1. First ensure you have Docker installed. [See our Docker installation help](https://github.com/blockchain-certificates/developer-common-docs/blob/master/docker_install.md).
   
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


### About Docker Setup
The quick start steps do the following:

1. Creates a container that runs the cert-viewer Flask app with MongoDB using Docker Compose [details](http://containertutorials.com/docker-compose/flask-mongo-compose.html)
2. Seeds the MongoDB database with sample fake certificates. This data is located in the mongo-seed folder
3. Starts the container. This configuration exposes port 5000.

### Notes
As of now, the mongo instance is populated with 2 unverified certificates; they are linked to on the main page. Click
'Verify' to see details on how verification can fail.

## Installation and Configuration

These steps allow you to install and run outside outside of Docker. Step 5 describes the configuration options that
should be changed if you're using this for anything other than demo purposes.

### Steps

1. Ensure you have an python environment. [Recommendations](https://github.com/blockchain-certificates/developer-common-docs/blob/master/virtualenv.md)

2. Install [mongodb](https://docs.mongodb.com/v3.0/installation/)

3. Git clone the repository and change to the directory

    ```bash
    git clone https://github.com/blockchain-certificates/cert-viewer.git && cd cert-viewer
    ```

4. Setup your conf.ini file (see 'Configuration')

5. Start mongo database. `--dbpath` can be left off if you used the default location

    ```shell
    mongod --dbpath <path to data directory>
    ```

6. Run cert-viewer setup

    ```bash
    pip install .
    ```

7. Run the flask server

    ```shell
    python run.py
    ```

8. Open `http://localhost:5000`


## Configuration

1. Copy the template ini file

    ```bash
    cp conf_template.ini conf.ini
    ```
    
2. Edit the following entries (refer to conf_sample.ini for examples):
    - `secret_key` is a random string used by Flask as a secret key to enable cryptographically signed session
    - `mandrill_api_key` is used to send out notifications when a user signs up. Setup your mandrill account at https://www.mandrill.com/
    - `mongodb_uri` is used to access your mongodb instance. The canonical form is `mongodb://<username>:<password>@<domain>:<mongo_port>`. Examples follow:
         - Local mongo installation: `mongodb_uri = mongodb://localhost:27017`
         - Docker installation: `mongodb_uri = mongodb://<DOCKER_MACHINE_IP>:27017`, where DOCKER_MACHINE_IP is given by `docker-machine ip`



## Unit tests

This project uses tox to validate against several python environments.

1. Ensure you have an python environment. [Recommendations](https://github.com/blockchain-certificates/developer-common-docs/blob/master/virtualenv.md)

2. Run tests
    ```
    ./run_tests.sh
    ```

## Database collections 

[About the database collections](docs/database_collections.md)

## Contact

Contact [info@blockcerts.org](mailto:info@blockcerts.org) with questions
