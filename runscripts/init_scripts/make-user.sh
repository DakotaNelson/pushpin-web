#!/bin/sh

cd /root/pushpin-app && \
   python3 manage.py createsuperuser --noinput --username admin --email 'test@example.com' && \
   python3 deploy.py
