Pushpin modules broken out of [recon-ng](https://bitbucket.org/LaNMaSteR53/recon-ng/) and turned into a webapp.


Good instructions on usage coming soon.

### Quick (and incomplete) list of dependencies:

 * django >= 1.7.1
 * python >= 3.3.3
 * postgreSQL >= 9.2.8
 * psycopg2 >= 2.5.4
 * requests >= 2.1.0
 * pytz >= 2014.9

### Rough notes on local usage:

* In `pushpin-web/static`, run `python -m http.server 8001`. This is to serve static files, because doing so with Django will make you feel many terrible feels.
* Create a symlink in `pushpin-web/static` that points to `your-django-path/django/contrib/admin/static/admin` so that your new server will also serve that static files for Django's admin interface.
* Run `postmaster -D ./db/` to start the PostgreSQL server, where `./db/` is a directory you create to hold the database.
* cd to `pushpin-web/pushpin-app` and run `python manage.py migrate` to set up the database
* Then run `python manage.py runserver` to start the django server
* Before use, create a user named `test` (it MUST be called test, for now) by cd'ing to `pushpin-web/pushpin-app/` and running `python manage.py createsuperuser --username test`. It will then prompt you for an email, which is currently never used by the app but required nonetheless. This test user is currently the only implemented user in pushpin-web, and therefore must exist, yet is essentially unused. Full access control and multiple users are coming soon\*.

### To deploy:

* Change `STATIC_URL` in `pushpin-web/pushpin-app/pushpin/settings.py` to the location where you're hosting static files.
* Change `SECRET_KEY` in `pushpin-web/pushpin-app/pushpin/settings.py` to something... well... secret.
* Add someone(s) ADMINS in settings.py. They'll get an email if any errors are thrown on the site.
* Set `DEBUG` (in settings.py) to False.
* Change `ALLOWED_HOSTS` (you can probably guess where that is by now) to the valid host/domain names.

### Once it's set up:
 * run `python manage.py getdata` to pull data and populate the database. This could be done with cron.

### Other notes:

* If you'd like to host your own static files, change `STATIC_URL` in settings.py to point to your custom location.



\* Soon is a very relative term, don't you think?
