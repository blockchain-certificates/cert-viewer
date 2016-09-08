[![Build Status](https://travis-ci.org/blockchain-certificates/cert-viewer.svg?branch=master)](https://travis-ci.org/blockchain-certificates/cert-viewer)

Blockchain Certificates Viewer Project
===================================

Flask webapp to display and verify blockchain certificates after they have been issued and to allow learners to request a certificate and generate their own Bitcoin identity needed for the certificate creation process. [See the schema](https://github.com/blockchain-certificates/cert-schema>) and [how to issue a certificate](https://github.com/blockchain-certificates/cert-issuer).

Example Deployments
-------------
The Media Lab issued blockchain certificates (nicknamed "coins") to Media Lab alumni who attended the Lab's 30th anniversary in October 2015. [Check out the certificates here.](https://coins.media.mit.edu/)

Learning Machine issued blockchain certificates to all of its employees. Check out two example certificates [here](https://hr.learningmachine.com/52d8acfc86584d0c40700631) and [here](https://hr.learningmachine.com/1c56735cd6a4320c61583b9d).

MIT's Global Entrepreneurship Bootcamp issued blockchain certificates to the students that attended their workshop in Seoul, South Korea in March 2016. [Check out the certificates here.](http://certificates-bootcamp.mit.edu/)

The Laboratorio para la Ciudad issued blockchain certificates to participants of a week-long workshop in Mexico City in September 2016. [Check out the certificates here.](http://certs.labcd.mx/)

[//]: # "start_docker_instructions"

Quick Start
-----------

### Steps

1. [Install Docker](https://docs.docker.com/engine/installation/) for your OS, ensuring your installation includes Docker Compose
    - The installation details will vary depending on your OS. For example, if you use Mac OSX, then you can simply install [Docker for Mac](https://docs.docker.com/docker-for-mac/#/download-docker-for-mac), which will include all the tools you need
    - Before moving on, ensure you have all the tools you need by running these 3 commands. Your details may vary depending on the version you installed; you just want to make sure these tools are available on your system
   ```
   $ docker --version
   Docker version 1.12.0, build 8eab29e

   $ docker-compose --version
   docker-compose version 1.8.0, build f3628c7

   $ docker-machine --version
   docker-machine version 0.8.0, build b85aac1
   ```
   
2. Git clone the repository

    ```
    git clone https://github.com/blockchain-certificates/cert-viewer.git
    ```

3. From a command line in the cert-viewer dir, run docker-compose

    ```
    cd cert-viewer
    docker-compose build
    ```

4. Start the container

    ```
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

### Limitations/Warnings

- The quick start configuration is for demo purposes and not intended for production release. See [installation](installation.md).
- As of now, the mongo instance is populated with 2 unverified certificates; they are linked to on the main page. Click
'Verify' to see details on how verification can fail.

[//]: # "end_docker_instructions"


Contact
-------

Contact [certs@media.mit.edu](mailto:certs@media.mit.edu) with questions
