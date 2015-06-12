FROM ubuntu:trusty
# FROM python:3.4

MAINTAINER Dakota Nelson "dakota@blackhillsinfosec.com"

RUN apt-get -qq update && apt-get install -y \
      python3-pip \
      python-dev \
      libpq-dev

COPY ./requirements.txt /root/requirements.txt
RUN pip3 install -r /root/requirements.txt

EXPOSE 8000

# add a non-root user to run the app as
RUN useradd -ms /bin/bash app
#ENV HOME /home/app
