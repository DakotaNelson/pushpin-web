#!/bin/sh

cd /root/pushpin-app && \
  python3 manage.py makemigrations && \
  python3 manage.py migrate

#cd /root/pushpin-app && \
#  python3 manage.py createsuperuser --noinput --username admin --email 'test@example.com'
# this will fail if the account already exists; that's totally OK

cd /root/pushpin-app && \
  python3 deploy.py

exec /usr/local/bin/uwsgi --ini /root/pushpin-app/config/wsgi_config.ini

#TODO don't run as root
# shared volumes cause problems...
#su -c 'exec /usr/local/bin/uwsgi --ini /root/pushpin-app/config/wsgi_config.ini' app
