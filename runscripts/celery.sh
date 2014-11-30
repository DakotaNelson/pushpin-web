#!/bin/sh

cd /root/pushpin-app && exec python3 manage.py celery worker --concurrency=2
