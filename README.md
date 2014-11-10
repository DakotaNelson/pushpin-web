Pushpin modules broken out of [recon-ng](https://bitbucket.org/LaNMaSteR53/recon-ng/) and turned into a webapp.


Good instructions on usage coming soon.

### Quick (and incomplete) list of dependencies:

 * django
 * python 3
 * postgreSQL

### Rough notes on local usage:

* In `pushpin-web/static`, run `python -m http.server 8001`. This is to serve static files, because doing so with Django will make you feel many terrible feels.
* Run `postmaster -D ./db/` to start the PostgreSQL server, where `./db/` is a directory you create to hold the database.
* cd to `pushpin-web/pushpin-app` and run `python manage.py migrate`
* Then run `python manage.py runserver`

### To deploy:

* Change `STATIC_URL` in `pushpin-web/pushpin-app/pushpin/settings.py` to the location where you're hosting static files.
* Change `SECRET_KEY` in `pushpin-web/pushpin-app/pushpin/settings.py` to something... well... secret.
* Change ADMINS in settings.py to be you, and not me.
* Set `DEBUG` (in settings.py) to False.
* Change `ALLOWED_HOSTS` (you can probably guess where that is by now) to the valid host/domain names.

### Other notes:

* If you'd like to host your own static files, change `STATIC_URL` in settings.py to point to your custom location.
