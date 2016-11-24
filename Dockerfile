FROM ubuntu:latest
RUN apt-get update --fix-missing
RUN apt-get install -y -q build-essential python-pip python-dev git
RUN pip install --upgrade pip
RUN pip install --upgrade virtualenv
RUN mkdir deployment
COPY . /deployment/
RUN ls -la /deployment/*
RUN virtualenv /deployment/env/
WORKDIR deployment
RUN env/bin/pip install django
RUN env/bin/python greenfield/manage.py migrate
CMD env/bin/python greenfield/manage.py runserver 0.0.0.0:8080
