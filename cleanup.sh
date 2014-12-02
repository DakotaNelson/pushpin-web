#!/bin/sh

sudo docker stop pushpin
sudo docker stop pushpin-postgres

sudo docker rm pushpin
sudo docker rm pushpin-postgres
