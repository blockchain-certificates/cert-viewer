FROM python:3
MAINTAINER Kim Duffy "kimhd@mit.edu"

WORKDIR /cert-viewer

COPY /conf_local.ini /cert-viewer/conf.ini
COPY requirements.txt /cert-viewer/
COPY run.py /cert-viewer/
RUN pip install -r /cert-viewer/requirements.txt
ADD . /cert-viewer
ADD cert_data /etc/cert_data

EXPOSE 5000
CMD ["python", "/cert-viewer/run.py"]

