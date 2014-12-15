#!/bin/sh

# check for updates
sudo docker pull dakotanelson/pushpin
sudo docker pull postgres

sudo docker run --name pushpin-postgres -e POSTGRES_PASSWORD=mysecretpassword -e POSTGRES_USER=pushpin -d postgres

# postgres takes a few seconds to start
sleep 5

sudo docker run --name pushpin -p 8000:8000 -p 8001:8001 --link pushpin-postgres:postgres -e POSTGRES_PASSWORD=mysecretpassword -e POSTGRES_PORT=5432 -e PUSHPIN_PASSWORD=test -e SECRET_KEY='asdf1234!@#$jkl;5678%^&*[]{}qwertyuiop' -e DEBUG=True -e ALLOWED_HOSTS='localhost' -e STATIC_URL='http://localhost:8001/' -d dakotanelson/pushpin

# NOTE: change out the passwords, and create a better secret key!
# This will give you an idea: http://www.miniwebtool.com/django-secret-key-generator/

# the -p flags define ports to expose: changing the first of the numbers will expose a different port on the host. I.e., if you wanted pushpin to exist on port 80, change the first -p to '-p 80:8000'. The second port, 8001, serves static files.
