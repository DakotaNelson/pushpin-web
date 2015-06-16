Pushpin modules broken out of [recon-ng](https://bitbucket.org/LaNMaSteR53/recon-ng/) and turned into a webapp. Pushpin-web provides an easy web interface to keep track of geotagged social media activity. Deployed using Docker for ease of use.

A project by [Black Hills Information Security](http://blackhillsinfosec.com).

![Black Hills Information Security](http://static.wixstatic.com/media/75fce7_138b6d3a00cd4441a800ab0163ab5803.jpg_srb_p_287_287_75_22_0.50_1.20_0.00_jpg_srb "Black Hills Information Security")

## Quickstart:
First, make sure you've got Docker installed: https://docs.docker.com/installation/

Second, make sure you've got Docker Compose installed: https://docs.docker.com/compose/install/

To start, change to the project's root directory and run `docker-compose up`. This should start all the containers, link them all together, and get everything set up.

Head to `localhost:8080` to take a look. Default username/password is 'test'. That's it - you're done!

Run `cleanup.sh` to remove a few artifacts (logs) left behind from each pushpin deploy - they're RO files, so you can't start up a new deploy until they're gone. Then run `docker-compose up` to start again.

## Acquiring API Keys
* Taken from https://bitbucket.org/LaNMaSteR53/recon-ng/wiki/Usage%20Guide#!acquiring-api-keys
* Google API Key (used for Youtube) - Go to the [Google Developer's Console](https://console.developers.google.com/) and create a project. Once it's created, under "APIs & auth" on the left bar, select "APIs" and then search for Youtube and click "enable." Then, under "APIs & auth" on the left bar, select "Credentials" and then under "Public API access" select "Create new key."
* Picasa - None required.
* Flickr API Key (flickr_api) - TBD
* Instagram API Key (instagram_api) - Log in [here](http://instagram.com/developer/clients/register/) with an existing Instagram account and register a new application. Add `http://localhost:31337` as the "OAuth redirect_uri". Click "Manage Clients" at the top of the screen and the API key will be available as the "CLIENT ID".
* Instagram Secret (instagram_secret) - Log in [here](http://instagram.com/developer/). Click "Manage Clients" at the top of the screen and the Secret key will be available as the "CLIENT SECRET".
* Twitter Consumer Key (twitter_api) - Create an application https://dev.twitter.com/apps. The Consumer key will be available on the application management page.
* Twitter Consumer Secret (twitter_secret) - The Consumer secret will be available on the application management page for the application created above.
* Shodan API Key (shodan_api) - Create an account or sign in to Shodan using one of the many options available http://www.shodanhq.com/. The API key will be available on the right side of the screen. An upgraded account is required to access advanced search features.

## FAQ:

##### Q: I'm trying to deploy this to somewhere other than localhost, and it's super broken. Help?
Check out the section below on deploying places other than localhost. There are a few special things you have to do.

##### Q: How do I use this thing?
Once you've run `start.sh`, go to localhost:8080, where you will be prompted to log in. Enter `test` and `test`, unless you configured the `PUSHPIN_PASSWORD` environment variable to be something else. Either way, username is test. Once you've logged in, you'll be redirected to the admin page, where you can add API keys. You should do so, or else you won't get any data. Once that's done, head back to localhost:8000 and you'll see the pushpin interface. Have fun!

##### Q: When does data get pulled?
Data is pulled periodically (depends on the module - Flickr is every 15 minutes, for example) by celerybeat and manually every time a new location is added. If you don't see any data for a location you just added, try refreshing - it sometimes takes a minute or two to pull data from the various APIs. Ideallly, the interface will eventually allow you to monitor the progress of background API pulls.

##### Q: I'm getting an error `IOError: [Errno 13] Permission denied: '/some/path/to/pushpin-web/logs/error.log'`. What do?
Run `cleanup.sh` to delete the logs left over from a previous deploy. The logs are currently read-only, and so cannot be overwritten by the new deploy. Hopefully this will have a cleaner solution soon.

##### Q: Can I run this in the background?
Yep: `docker-compose up -d` will run the cluster of containers in detached mode, and `docker-compose stop` will stop the detached cluster.

##### Q: Can I configure more things?
Yep: open up `docker-compose.yml` and you can fiddle arround with settings and variables. There are some comments there to help you out.

### Deploying other than localhost:

Set the `ALLOWED_HOSTS` environment variable in `docker-compose.yml` to be the address of your host. (IP address or domain name, or both) See [Django's docs](https://docs.djangoproject.com/en/1.7/ref/settings/#allowed-hosts) for details.

You'll also want to tighten up security a bit - in `docker-compose.yml`, changing at least the `SECRET_KEY` and `PUSHPIN_PASSWORD` variables is a good start.


### Rough notes on local usage for development:

* Install dependencies:
  * python >= 3.3.3
  * RabbitMQ: `apt-get install rabbitmq-server` or `yum install rabbitmq-server`
  * postgreSQL >= 9.2.8
  * `pip install -r requirements.txt`
* Create a symlink in `pushpin-web/static` that points to `your-django-path/django/contrib/admin/static/admin` so that your new server (next step) will also serve the static files for Django's admin interface.
* In `pushpin-web/static`, run `python -m http.server 8001`. This is to serve static files, because doing so with Django will make you feel many terrible feels.
* Run `postmaster -D ./db/` to start the PostgreSQL server, where `./db/` is a directory you create to hold the database.
* Run `sudo rabbitmq-server` (with an optional `-detached`) to run the RabbitMQ message queue
* Set some environment variables: `POSTGRES_PASSWORD`, `POSTGRES_USER`, `POSTGRES_HOST`, `PUSHPIN_PASSWORD`, and `DEBUG`. Take a look at `pushpin-app/pushpin/settings.py` for more configuration options.
* cd to `pushpin-web/pushpin-app` and run `python manage.py migrate` to set up the database
* Run `python manage.py runserver` to start the django server
* Run `python manage.py celery worker --loglevel=info --concurrency=2` to start the celery server
* Run `python manage.py celery beat` to run celery's scheduling engine
* Run `pushpin-app/deploy.py` to set up some users and a place to put you API keys.

### To add a module:
 * Create the actual module in `pushpin-app/modules`. Take a look at some other modules in that folder to get an idea of how to make it work.
 * In `pushpin-app/map/tasks.py`, add a task for your module by copying another module and modifying it
 * In `pushpin-app/map/management/commands/getdata.py`, add your task to the list that needs to be run
 * Rebuild the Docker container (or restart celery and celery beat if not using Docker)

### Wishlist:
* Capable of handling multiple users/authentication.
* Ability to narrow displayed pins by date.
* Break down Celery tasks to the point of getting a single location's data from a single API, use a lock to make sure only one worker pulls from an API at a time. This would help with scaling someday.
* Intelligently deal with rate limiting, rather than just throttling API calls to safe levels without ever checking. (Could help with previous wishlist item.)
* Use RabbitMQ as a backend to have Celery keep task status updated, show user progress of data-pulling tasks.
* Be able to manually trigger a data pull from the webapp. (Especially useful if only one location is triggered.)
* Linkify links in pushpins. The linkify library is already in place, it just needs to be used.
