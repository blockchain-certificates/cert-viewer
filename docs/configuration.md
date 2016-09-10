---
layout: page
title: Configuration
---

If you want to quickly try out this application, we recommend using the quick start (docker) installation steps. If you
go that route, you do not have to customize the configuration; the application will work with limited features, including
no Mandrill notificatinos.

If you want to try out the application with your own settings, or especially if you are using this project as a baseline for
a project you will deploy to production, you should update these settings.

1. Copy the template ini file

    `cp conf_template.ini conf.ini`

2. And edit the following entries (refer to conf_sample.ini for examples):
    - `SECRET_KEY` is used by Flask as a secret key to enable cryptographically signed session

         - `SECRET_KEY = <random string>`

    - `MANDRILL_API_KEY` is used to send out notifications when a user signs up. Setup your mandrill account at https://www.mandrill.com/

         - `MANDRILL_API_KEY = <mandrill_api_key>`

    - `MONGO_URL` is used to access your mongodb instance. The canonical form is `mongodb://<username>:<password>@<domain>:<mongo_port>`. Examples follow:

         - Local mongo installation: `MONGO_URI = mongodb://localhost:27017`
         - Docker installation: `MONGO_URI = mongodb://<DOCKER_MACHINE_IP>:27017`, where DOCKER_MACHINE_IP is given by `docker-machine ip`
