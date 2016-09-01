Digital Certificates Viewer Project
===================================

Flask webapp to display and verify digital certificates after they have been issued and to allow learners to request a certificate and generate their own Bitcoin identity needed for the certificate creation process. [See the schema](https://github.com/blockchain-certificates/cert-schema>) and [how to issue a certificate](https://github.com/blockchain-certificates/cert-issuer).

Example Deployments
-------------
The Media Lab issued digital certificates (nicknamed "coins") to Media Lab alumni who attended the Lab's 30th anniversary in October 2015. [Check out the certificates here.](https://coins.media.mit.edu/)

Learning Machine issued digital certificates to all of its employees. Check out two example certificates [here](https://hr.learningmachine.com/52d8acfc86584d0c40700631) and [here](https://hr.learningmachine.com/1c56735cd6a4320c61583b9d).

MIT's Global Entrepreneurship Bootcamp issued digital certificates to the students that attended their workshop in Seoul, South Korea in March 2016. [Check out the certificates here.](http://certificates-bootcamp.mit.edu/)

The Laboratorio para la Ciudad issued digital certificates to participants of a week-long workshop in Mexico City in September 2016. [Check out the certificates here.](http://certs.labcd.mx/)

[//]: # "start_docker_instructions"

Quick Start
-----------

### Steps

1. [Install Docker Engine and Docker Compose](https://docs.docker.com/engine/installation)
    - If you are using Mac OSX or Windows, your installation includes both Engine and Compose, so you can skip to the #installation anchor for your OS.
        - Mac OSX: [https://docs.docker.com/docker-for-mac/](https://docs.docker.com/docker-for-mac/)
        - Windows: [https://docs.docker.com/docker-for-windows/](https://docs.docker.com/docker-for-windows/)
    - If you already have Docker installed, ensure your version is >= 1.10.0, and that you have both Engine and Compose
        - Note that if you're using an old version of Docker (or if you're using Docker Toolbox) you may not get hosted at localhost. If you run `docker-machine ip`, you'll find out what IP the machine is being run from.

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

5. Access cert-viewer pre-populated with test data at `http://localhost:5000`.


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

Project Documentation
---------------------

Project documentation is under docs/ and summarized here: [docs/index.md](/docs/index.md)

This content is also available at [http://cert-viewer.readthedocs.io/](http://cert-viewer.readthedocs.io/)


About the Digital Certificates Project
--------------------------------------

The [MIT Media Lab Digital Certificates](http://certificates.media.mit.edu/) is an incubation project. We're looking for feedback, contributions, and general
discussion. This is not currently intended for production release, but we are improving our approach for future releases.


Contact
-------

Contact [certs@media.mit.edu](mailto:certs@media.mit.edu) with questions
