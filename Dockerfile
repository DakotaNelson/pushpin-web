#FROM phusion/baseimage:0.9.16
FROM ubuntu:trusty
# FROM python:3.4

MAINTAINER Dakota Nelson "dakota@blackhillsinfosec.com"

# install things
RUN apt-get -qq update && apt-get install -y \
      python3-pip \
      python-dev \
      libpq-dev

# use pip to install requirements
COPY ./requirements.txt /root/requirements.txt
RUN pip3 install -r /root/requirements.txt

# set up all of the service directories for runit
#RUN mkdir /etc/service/static-server && \
#mkdir /etc/service/rabbitmq && \
#mkdir /etc/service/celerybeat && \
#mkdir /etc/service/celery && \
#mkdir /etc/service/django-server

# Serve the static files
#COPY runscripts/static-server.sh /etc/service/static-server/run
#EXPOSE 8001

# run rabbitmq for celery to use
#COPY runscripts/rabbitmq.sh /etc/service/rabbitmq/run

# Run celery
#COPY runscripts/celery.sh /etc/service/celery/run

# and celerybeat
#COPY runscripts/celerybeat.sh /etc/service/celerybeat/run

# Run the Django server
#ADD runscripts/django-server.sh /etc/service/django-server/run
EXPOSE 8000

# Set up the startup scripts
#RUN mkdir -p /etc/my_init.d
#ADD runscripts/init_scripts/ /etc/my_init.d/

# Clean up APT when done.
#RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# add a non-root user to run the app as
RUN useradd -ms /bin/bash app
#ENV HOME /home/app

# copy in the static files
#COPY ./static/ /root/static

# create a symlink to the static files for the admin pages
#RUN ln -s /usr/local/lib/python3.4/dist-packages/django/contrib/admin/static/admin /root/static/

# copy in the Django files
#COPY ./pushpin-app/ /root/pushpin-app

#RUN chown -R app:app /root
#chown -R app:app /usr/local && \
#chown -R app:app /usr/lib

# Use baseimage-docker's init system.
#CMD ["/sbin/my_init"]
