#!/bin/sh

cd /root/pushpin-app && exec python3 manage.py runserver 0.0.0.0:8000
