#!/bin/sh

sudo docker build -t pushpin .

sudo docker stop pushpin-postgres
sudo docker stop pushpin

sudo docker rm pushpin-postgres
sudo docker rm pushpin

sudo docker run --name pushpin-postgres -e POSTGRES_PASSWORD=mysecretpassword -e POSTGRES_USER=pushpin -d postgres
sleep 5
sudo docker run --name pushpin -p 8000:8000 -p 8001:8001 --link pushpin-postgres:postgres -e POSTGRES_PASSWORD=mysecretpassword -e DJANGO_PASSWORD=test -e DEBUG=True -d pushpin

sleep 20

sudo docker logs pushpin
