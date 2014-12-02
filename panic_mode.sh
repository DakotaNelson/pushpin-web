#!/bin/sh

sudo docker stop $(sudo docker ps -q)
sudo docker rm $(sudo docker ps -a -q)
