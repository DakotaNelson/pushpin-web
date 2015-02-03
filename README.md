Pushpin modules broken out of [recon-ng](https://bitbucket.org/LaNMaSteR53/recon-ng/) and turned into a webapp. Pushpin-web provides an easy web interface to keep track of geotagged social media activity. Deployed using Docker for ease of use.

A project by [Black Hills Information Security](http://blackhillsinfosec.com).

![Black Hills Information Security](http://blackhillsinfosec.com/_images/BHIS-Logo.png "Black Hills Information Security")

## Quickstart:
First, make sure you've got Docker installed: https://docs.docker.com/installation/

Run `start.sh` to download a pre-built image from Docker hub and get started super fast. Visit localhost:8000 in your browser to see the results. *In production environments, open up start.sh and configure some unique passwords!*

Run `local.sh` to build the docker image from source and deploy it. This is useful in case you want to make any changes to pushpin locally. *In production environments, open up local.sh and configure some unique passwords!*

Run `cleanup.sh` to remove your current pushpin deploy (either because you've had enough of this pushpin business, because you want to deploy a new version).

Run `redeploy.sh` to manually rebuild pushpin from the local Dockerfile, *destroy your pushpin deployment, including database*, then redeploy, wait a while, and show you some logfiles of the deployment. Useful for testing changes you've made locally.

In case everything goes completely wrong, `panic_mode.sh` will stop and remove all of your Docker containers. **Use with caution!**

## Acquiring API Keys
* Taken from https://bitbucket.org/LaNMaSteR53/recon-ng/wiki/Usage%20Guide#!acquiring-api-keys
* Facebook API Key (facebook_api) - TBD
* Facebook Secret (facebook_secret) - TBD
* Flickr API Key (flickr_api) - TBD
* Instagram API Key (instagram_api) - Log in [here](http://instagram.com/developer/clients/register/) with an existing Instagram account and register a new application. Add `http://localhost:31337` as the "OAuth redirect_uri". Click "Manage Clients" at the top of the screen and the API key will be available as the "CLIENT ID".
* Instagram Secret (instagram_secret) - Log in [here](http://instagram.com/developer/). Click "Manage Clients" at the top of the screen and the Secret key will be available as the "CLIENT SECRET".
* Twitter Consumer Key (twitter_api) - Create an application https://dev.twitter.com/apps. The Consumer key will be available on the application management page.
* Twitter Consumer Secret (twitter_secret) - The Consumer secret will be available on the application management page for the application created above.

## FAQ:

##### Q: I'm trying to deploy this to somewhere other than localhost, and it's super broken. Help?
Check out the section below on deploying places other than localhost. There are a few special things you have to do.

##### Q: How do I use this thing?
Once you've run `start.sh`, go to localhost:8000, where you will be prompted to log in. Enter `test` and `test`, unless you configured the `PUSHPIN_PASSWORD` environment variable to be something else. Either way, username is test. Once you've logged in, you'll be redirected to the admin page, where you can add API keys. You should do so, or else you won't get any data. Once that's done, head back to localhost:8000 and you'll see the pushpin interface. Have fun!

##### Q: When does data get pulled?
Data is pulled hourly by celerybeat and manually every time a new location is added. If you don't see any data for a location you just added, try refreshing - it sometimes takes a minute or two to pull data from the various APIs.

##### Q: I'm getting an error `Error response from daemon: Conflict, The name <name> is already assigned to <some hash value>`. What do?
Run `cleanup.sh` to delete your current pushpin containers in order to create new ones.

##### Q: Everything is broken. HOW DO I MAKE IT STOP?!?
`panic_mode.sh` will bring an end to the chaos. It'll also destroy **all** of your Docker containers, not just pushpin, so **be careful**!


### Deploying other than localhost:

* Make sure to set the `STATIC_URL` environment variable to `http://yourDomainOrIP:8001/`. Note that the trailing slash is *very important*.
* Set the `ALLOWED_HOSTS` environment variable to be the address of your host. (IP address or domain name) See [Django's docs](https://docs.djangoproject.com/en/1.7/ref/settings/#allowed-hosts) for details.


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
* Make timeline on main page brushable to narrow displayed pins by date.
* Break down Celery tasks to the point of getting a single location's data from a single API, use a lock to make sure only one worker pulls from an API at a time.
* Intelligently deal with rate limiting, rather than just throttling API calls to safe levels without ever checking. (Could help with previous wishlist item.)
* Use RabbitMQ as a backend to have Celery keep task status updated, show user progress of data-pulling tasks.
* Be able to manually trigger a data pull from the webapp. (Especially useful if only one location is triggered.)
* Only pull data from APIs since the last update. (i.e. keep track of when run last and use that information)
* Linkify links in pushpins. The linkify library is already in place, it just needs to be used.
