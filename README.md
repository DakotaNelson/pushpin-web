Pushpin modules broken out of [recon-ng](https://bitbucket.org/LaNMaSteR53/recon-ng/) and turned into a webapp. Pushpin-web provides an easy web interface to keep track of geotagged social media activity. Deployed using Docker for ease of use.

A project by [Black Hills Information Security](http://blackhillsinfosec.com)

![Black Hills Information Security](http://blackhillsinfosec.com/_images/BHIS-Logo.png "Black Hills Information Security")

## Quickstart:
First, make sure you've got Docker installed: https://docs.docker.com/installation/

Run `start.sh` to download a pre-built image from Docker hub and get started super fast. Visit localhost:8000 in your browser to see the results. *In production environments, open up start.sh and configure some unique passwords!*

Run `build.sh` to build the docker image from source in case you want to make any changes. If there's a local copy of an image (i.e. one that you built), Docker (and by extension, `start.sh`) will use that instead.

Run `update.sh` to pull the latest build of pushpin-web for use with `start.sh`.

Run `redeploy.sh` to manually rebuild pushpin from the local Dockerfile, *destroy your pushpin deployment*, then redeploy, wait a while, and show you some logfiles of the deployment. Useful for testing changes you've made locally.


## FAQ:

##### Q: How do I use this thing?
Once you've run `start.sh`, go to localhost:8000, where you will be prompted to log in. Enter `test` and `test`, unless you configured the `PUSHPIN_PASSWORD` environment variable to be something else. Either way, username is test. Once you've logged in, you'll be redirected to the admin page, where you can add API keys. You should do so, or else you won't get any data. Once that's done, head back to localhost:8000 and you'll see the pushpin interface. Have fun!

##### Q: When does data get pulled?
Data is pulled hourly by celerybeat and manually every time a new location is added. If you don't see any data for a location you just added, try refreshing - it sometimes takes a minute or two to pull data from the various APIs.

##### Q: HOW DO I MAKE IT STOP?!?
`sudo docker stop $(sudo docker ps -q)` will stop all running containers and `sudo docker rm $(sudo docker ps -q)` will remove them. Be careful with that second one, it'll blow away your database container and all your data with it.


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

### To deploy:

* Change `ALLOWED_HOSTS` (you can probably guess where that is by now) to the valid host/domain names.

### To add a module:
 * Create the actual module in `pushpin-app/modules`, using another model as a template
 * In `pushpin-app/map/tasks.py`, add a task for your module by copying another module and modifying it
 * In `pushpin-app/map/management/commands/getdata.py`, add your task to the list that needs to be run
 * In `pushpin-app/map/views.py`, add your task to the list of tasks that is run after a new location is added in the addLocation view.
 * Rebuild the Docker container (or restart celery and celery beat if not using docker)

### Other notes:

* If you'd like to host your own static files, change `STATIC_URL` in settings.py to point to your custom location.


### Wishlist:
[] Capable of handling multiple users/authentication.
[] Media view, listing media data directly, for deeper analysis.
[] Make timeline on main page brushable to narrow displayed pins by date.
[] Break down Celery tasks to the point of getting a single location's data from a single API, use a lock to make sure only one worker pulls from an API at a time.
[] Use RabbitMQ as a backend to have Celery keep task status updated, show user progress of data-pulling tasks.
[] Only pull data from APIs since the last update. (i.e. keep track of when run last and use that information)



\* Soon is a very relative term, don't you think?
