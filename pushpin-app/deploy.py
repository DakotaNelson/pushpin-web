#!/bin/python3

# This script handles pre-deploy Django tasks.
# Specifically: it adds a user (test), configures its permissions,
#               and adds an empty db entry to put API keys in

import os

# set up django's settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'pushpin.settings'

import django
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from map.models import Keys, Location
from getenv import env

django.setup()

os.chdir('/root/pushpin-app')

#User.objects.create_superuser(username='admin', email='test@example.com')

password = env("PUSHPIN_PASSWORD","test")
try:
    testUser = User.objects.get(username="test")
    print("Updating test user password...")
    testUser.set_password(password)
except ObjectDoesNotExist:
    print("No test user found. Creating test user...")
    testUser = User.objects.create_user('test', None, password)
    testUser.is_staff = True

    # give the user the ability to edit keys
    content_type = ContentType.objects.get_for_model(Keys)
    permission = Permission.objects.get(content_type=content_type,
                                        codename='change_keys')
    testUser.user_permissions.add(permission)

    # manually add and remove locations
    content_type = ContentType.objects.get_for_model(Location)
    add_permission = Permission.objects.get(content_type=content_type,
                                        codename='add_location')
    delete_permission = Permission.objects.get(content_type=content_type,
                                        codename='delete_location')
    testUser.user_permissions.add(add_permission, delete_permission)

    print("Creating empty keychain for user...")
    Keys.objects.create(user=testUser)

testUser.save()
