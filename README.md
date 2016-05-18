About
===
Check out the web application at [https://coins.media.mit.edu](https://coins.media.mit.edu).


Example Certificate
===
Check out documentation of the certificate itself [here](https://github.com/ml-learning/coins.media.mit.edu/blob/master/CERTIFICATE.md).


Quick Start
===

1. [Install docker](https://docs.docker.com/engine/installation)
  * There's a lot of introductory information; installation steps start at the #installation anchor for your os. For
example, mac instructions start at [https://docs.docker.com/engine/installation/mac/#installation](https://docs.docker.com/engine/installation/mac/#installation)

2. Git clone the repository

`git clone https://github.com/learningmachine/coins.media.mit.edu.git`

3. Build the container with docker-compose

`docker-compose build`

4. Start the container

`docker-compose up`

5. Access the certificate-viewer pre-populated with test data at http://<hostname>:5000, where hostname is given by
`docker-machine ip`


About Quick Start
===
The quick start steps do the following:

1. Creates a container that runs the certificate-viewer Flask app with MongoDB using Docker Compose [details](http://containertutorials.com/docker-compose/flask-mongo-compose.html)
2. Seeds the MongoDB database with sample data. This data is located in the mongo-seed folder
3. Starts the container. This configuration exposes port 5000.


Quick Start Limitations
===
- The quick start configuration is for demo purposes and not intended for production release. See step 5 in "Detailed
 Installation Description"
- As of now, I've only populated an unverified certificate; see http://<hostname>:5000/572f76d4faf8904cc0dc0e21. More
will be available soon

You can also follow the setup steps outside of Docker, below.


Tests
===
This project uses tox and currently validates against python 2.7 and python 3.4 environments.

```shell
# ensure your virtual python environment is activated (example)
source ./venv/bin/activate

# run tests
./run-tests.sh
```

Detailed Installation Description
===
These steps allow you to install and run outside outside of Docker. Step 5 describes the configuration options that
should be changed if you're using this for anything other than demo purposes.

1. Git clone the repository

```bash
git clone https://github.com/learningmachine/coins.media.mit.edu.git
```

2. Install [mongodb](https://docs.mongodb.com/v3.0/installation/)

3. Set up a virtual environment [details](http://docs.python-guide.org/en/latest/dev/virtualenvs/) and run setup

```bash
cd coins.media.mit.edu
pip install .
```

4. Copy the template ini file

`cp conf_template.ini conf.ini`

5. And edit the following entries (refer to sample-cert.json for examples):
  * `SECRET_KEY` is used by Flask as a secret key to enable cryptographically signed session

`SECRET_KEY = <random string>`

  * `MANDRILL_API_KEY` is used to send out notifications when a user signs up. Setup your mandrill account at https://www.mandrill.com/

`MANDRILL_API_KEY = <mandrill_api_key>`

  *  `MONGO_URL` is used to access your mongodb instance. The canonical form is `mongodb://<username>:<password>@<domain>:<mongo_port>`. Examples follow:

     * Local mongo installation: `MONGO_URI = mongodb://localhost:27017`
     * Docker installation: `MONGO_URI = mongodb://<DOCKER_MACHINE_IP>:27017`, where CONTAINER_IP is given by `docker-machine ip`


6. Start mongo database. --dbpath can be left off if you used the default location

```shell
mongod --dbpath <path to data directory>

```
7. Run the flask server
```shell
python run.py
```

8. Open http://localhost:5000



Database Collections
===
This webapp uses MongoDB. There are two collections, one for recipients and one for certificates. GridFs is used to store the certificates themselves.

Example of a recipient object:
```
{
  "_id": ObjectId(),
  "pubkey": "<recipient public key>",
  "info": {
    "email": "",
    "name": {
      "givenName": "",
      "familyName": ""
    },
    "degree": "<mas-ms/mas-phd/other>",
    "address": {
      "streetAddress": "",
      "city": "",
      "state": "",
      "zipcode": "",
      "country": ""
    }
  }
}
```

Example of a certificate object:
```
{
  "_id": "<uid string of certificate file>",
  "issued": <true/false>,
  "pubkey": "<recipient public key>",
  "txid": "<certificate transaction id>"
}
```

A recipient object can have multiple certificate objects. The objects are linked together by the "pubkey" field.

TODO
===
  - note: we will rename this repo to certificate-viewer after merging back to MIT
  - better sample data
  - switch to configargparse
  - document from user entry to cert creation
  - ensure issues with zip entry export
  - load recent txids dynamically

Contact
===
Contact [coins@media.mit.edu](mailto:coins@media.mit.edu) with questions

