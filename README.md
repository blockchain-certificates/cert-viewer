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

### Limitations/Warnings

- The quick start configuration is for demo purposes and not intended for production release. See [installation](installation.md).
- As of now, the mongo instance is populated with 2 unverified certificates; they are linked to on the main page. Click
'Verify' to see details on how verification can fail.

[//]: # "end_docker_instructions"


Contact
-------

Contact [certs@media.mit.edu](mailto:certs@media.mit.edu) with questions
