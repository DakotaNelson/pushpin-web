#!/bin/sh

cd /root/pushpin-app && exec /sbin/setuser app python3 manage.py celery beat
