

Detailed Installation
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



