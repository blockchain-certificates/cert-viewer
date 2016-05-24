Quick Start
===========

Steps
-----

1. [Install docker](https://docs.docker.com/engine/installation)
    - There's a lot of introductory information; installation steps start at the #installation anchor for your os. For
example, mac instructions start at [https://docs.docker.com/engine/installation/mac/#installation](https://docs.docker.com/engine/installation/mac/#installation)

2. Git clone the repository

    `git clone https://github.com/learningmachine/coins.media.mit.edu.git`

3. Build the container with docker-compose

    `docker-compose build`

4. Start the container

    `docker-compose up`

5. Access the certificate-viewer pre-populated with test data at `http://<hostname>:5000`, where hostname is given by
    `docker-machine ip`


About Docker Setup
------------------
The quick start steps do the following:

1. Creates a container that runs the certificate-viewer Flask app with MongoDB using Docker Compose [details](http://containertutorials.com/docker-compose/flask-mongo-compose.html)
2. Seeds the MongoDB database with sample data. This data is located in the mongo-seed folder
3. Starts the container. This configuration exposes port 5000.


Limitations
-----------
- The quick start configuration is for demo purposes and not intended for production release. See "Detailed Installation"
- As of now, I've only populated an unverified certificate; see `http://<hostname>:5000/572f76d4faf8904cc0dc0e21`. More
will be available soon

