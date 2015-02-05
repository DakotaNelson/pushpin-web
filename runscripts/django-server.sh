#!/bin/sh

cd /root/pushpin-app && exec /sbin/setuser app python3 manage.py runserver 0.0.0.0:8000
