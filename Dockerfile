FROM phusion/baseimage:0.9.15

MAINTAINER Dakota Nelson "dakota@blackhillsinfosec.com"

# Use baseimage-docker's init system.
CMD ["/sbin/my_init"]

# disable SSH
RUN rm -rf /etc/service/sshd /etc/my_init.d/00_regen_ssh_host_keys.sh

# install things
RUN apt-get -qq update && apt-get install -y \
      python3-pip \
      rabbitmq-server \
      python-dev \
      libpq-dev

# use pip to install requirements
COPY requirements.txt /root/requirements.txt
RUN pip3 install -r /root/requirements.txt

# set up all of the service directories for runit
RUN mkdir /etc/service/static-server && \
    mkdir /etc/service/rabbitmq && \
    mkdir /etc/service/celerybeat && \
    mkdir /etc/service/celery && \
    mkdir /etc/service/django-server

# Serve the static files
COPY runscripts/static-server.sh /etc/service/static-server/run
EXPOSE 8001

# run rabbitmq for celery to use
COPY runscripts/rabbitmq.sh /etc/service/rabbitmq/run

# Run celery
COPY runscripts/celery.sh /etc/service/celery/run

# and celerybeat
COPY runscripts/celerybeat.sh /etc/service/celerybeat/run

# Run the Django server
ADD runscripts/django-server.sh /etc/service/django-server/run
EXPOSE 8000

# Set up the startup scripts
RUN mkdir -p /etc/my_init.d
ADD runscripts/init_scripts/ /etc/my_init.d/

# copy in the rest of the django project
COPY . /root/

# create a symlink to the static files for the admin pages
RUN ln -s /usr/local/lib/python3.4/dist-packages/django/contrib/admin/static/admin /root/static/

# Clean up APT when done.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
