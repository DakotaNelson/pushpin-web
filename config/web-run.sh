#!/bin/sh

cd /root/pushpin-app && \
  python3 manage.py makemigrations && \
  python3 manage.py migrate

cd /root/pushpin-app && \
  python3 manage.py createsuperuser --noinput --username admin --email 'test@example.com' && \
  python3 deploy.py

exec /usr/local/bin/uwsgi --ini /root/pushpin-app/config/wsgi_config.ini
