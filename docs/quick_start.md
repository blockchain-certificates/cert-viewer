Quick Start
===========

Steps
-----

1. [Install Docker Engine and Docker Compose](https://docs.docker.com/engine/installation)
    - If you are using Mac OSX or Windows, your installation includes both Engine and Compose, so you can skip to the #installation anchor for your OS.
        - Mac OSX: [https://docs.docker.com/engine/installation/mac/#installation](https://docs.docker.com/engine/installation/mac/#installatio)
        - Windows: [https://docs.docker.com/engine/installation/windows/#installation](https://docs.docker.com/engine/installation/windows/#installation)
    - If you already have Docker installed, ensure your version is >= 1.10.0, and that you have both Engine and Compose

2. Git clone the repository

    `git clone https://github.com/digital-certificates/cert-viewer.git`

3. Determine your docker machine ip, which you'll use to access the webapp

    ```
    hostname=`docker-machine ip`
    echo $hostname
    ```

4. From a command line in the cert-viewer dir, run docker-compose

    ```
    cd cert-viewer
    docker-compose build
    ```

5. Start the container

    ```
    docker-compose up
    ```

6. Access cert-viewer pre-populated with test data at `http://<hostname>:5000`, where hostname is given by step 3.


About Docker Setup
------------------
The quick start steps do the following:

1. Creates a container that runs the cert-viewer Flask app with MongoDB using Docker Compose [details](http://containertutorials.com/docker-compose/flask-mongo-compose.html)
2. Seeds the MongoDB database with sample fake certificates. This data is located in the mongo-seed folder
3. Starts the container. This configuration exposes port 5000.


Limitations/Warnings
--------------------
- The quick start configuration is for demo purposes and not intended for production release. See [installation](installation.md).
- As of now, the mongo instance is populated with 2 unverified certificates; they are linked to on the main page. Click
'Verify' to see details on how verification can fail.
