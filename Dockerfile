# from https://github.com/Kalimaha/simple_flask_dockerizer
FROM ubuntu:14.04
MAINTAINER Kim Duffy "kimhd@mit.edu"

RUN apt-get update

# Install Python.
RUN apt-get install -y -q build-essential python-gdal python-simplejson
RUN apt-get install -y python python-pip wget
RUN apt-get install -y python-dev

# Create a working directory.
RUN mkdir deployment

# Install VirtualEnv.
RUN pip install virtualenv

# Add requirements file.
ADD requirements.txt /deployment/requirements.txt

# Add the script that will start everything.
ADD run.py /deployment/run.py

# Run VirtualEnv.
RUN virtualenv /deployment/env/
RUN /deployment/env/bin/pip install wheel

RUN /deployment/env/bin/pip install -r /deployment/requirements.txt

COPY . /deployment
RUN pip install /deployment
