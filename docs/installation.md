

Detailed Installation
===
These steps allow you to install and run outside outside of Docker. Step 5 describes the configuration options that
should be changed if you're using this for anything other than demo purposes.

1. Git clone the repository

    ```bash
    git clone https://github.com/digital-certificates/viewer.git
    ```

2. Install [mongodb](https://docs.mongodb.com/v3.0/installation/)

3. Set up a virtual environment [details](http://docs.python-guide.org/en/latest/dev/virtualenvs/) and run setup

    ```bash
    cd coins.media.mit.edu
    pip install .
    ```

4. Setup your conf.ini file (see 'Configuration')

5. Start mongo database. `--dbpath` can be left off if you used the default location

    ```shell
    mongod --dbpath <path to data directory>
    ```

6. Run the flask server

    ```shell
    python run.py
    ```

7. Open `http://localhost:5000`



