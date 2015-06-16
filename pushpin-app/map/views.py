from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_POST
from django.core import serializers
from django.core.management import call_command
from django.forms import ModelForm
from django.core.exceptions import ObjectDoesNotExist
from map.tasks import youtubeTask, twitterTask, picasaTask, shodanTask
from datetime import datetime, timedelta, timezone
import json
import logging

from map.models import Pushpin, Location
from map.forms import LocationForm

logger = logging.getLogger('pushpin')

@login_required
@require_GET
def mapView(request, locName):
    # the unique location
    location = get_object_or_404(Location, name=locName)

    # every other location
    # (this is a wasted DB hit, but saves some parsing - TODO)
    locations = list(Location.objects.exclude(name=locName).order_by('-date'))

    # then get pins based on that location
    pushpins = Pushpin.objects.filter(location__name=locName)

    sources = []

    for pin in pushpins:
        # build a list of active sources
        if pin.source not in sources:
            sources.append(pin.source)

    # NOTE: this will change if the class is changed in map/forms.py
    locationForm = LocationForm()

    context = {
                'sources': sources,
                'location': location,
                'locations': locations, # active location always first
                'pushpins': serializers.serialize('json', pushpins),
                'locationForm': locationForm
              }

    return render(request, 'map/map.html', context)

@login_required
@require_GET
def locationData(request, locName):
    # the unique location
    location = get_object_or_404(Location, name=locName)

    # then get pins based on that location
    pushpins = Pushpin.objects.filter(location__name=locName).order_by('-date')[:1000]

    sources = []

    for pin in pushpins:
        # build a list of active sources
        if pin.source not in sources:
            sources.append(pin.source)

    response_data = {
                'sources': sources,
                'pushpins': serializers.serialize('json', pushpins)
              }

    return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required
@require_GET
def mediaView(request, locName):
    # the unique location
    location = get_object_or_404(Location, name=locName)

    # then get pins based on that location
    start = datetime.now()
    pushpins = Pushpin.objects.filter(location__name=locName).order_by('-date').values("date","profile_name","thumb_url","message","source","profile_url", "media_url")[:2000]
    time = datetime.now() - start
    logger.info("Querying pins for media page took {}".format(time))

    sources = []

    for pin in pushpins:
        # build a list of active sources
        if pin['source'] not in sources:
            sources.append(pin['source'])

    # NOTE: this will change if the class is changed in map/forms.py
    locationForm = LocationForm()

    context = {
                'sources': sources,
                'location': location,
                'pushpins': pushpins,
                'locationForm': locationForm
              }

    return render(request, 'map/media.html', context)

@login_required
@require_GET
def noLocation(request):
    # every available location
    locations = list(Location.objects.all().order_by('-date'))

    # NOTE: this will change if the class is changed in map/forms.py
    locationForm = LocationForm()

    context = {
                'locations': locations,
                'locationForm': locationForm
              }

    return render(request, 'map/noLocation.html', context)

@login_required
@require_POST
def addLocation(request):
    response_data = {}

    # fill the form template with the incoming data
    form = LocationForm(request.POST)
    # save the form, but wait to let us make some changes
    try:
        location = form.save(commit=False)
    except ValueError:
        response_data['result'] = 'failed'
        response_data['message'] = 'Error saving location: name must be unique and all fields filled.'
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    location.date = datetime.now(timezone.utc).astimezone()
    location.radius = round(location.radius)
    if location.radius < 1:
        location.radius = 1
    if location.radius > 32:
        location.radius = 32

    # TODO: add multiple users
    location.user = User.objects.get(username='test')

    if form.is_valid():
        # add the new location
        location.save()
        response_data['result'] = 'success'
        response_data['message'] = 'Location was successfully added.'

        # run all modules to get data for this new location
        call_command('getdata')
    else:
        # form is not valid
        response_data['result'] = 'failed'
        response_data['message'] = 'Data is invalid.'

    return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required
@require_POST
def deleteLocation(request, locName):
    response_data = {}
    # TODO: add multiple users
    user = User.objects.get(username='test')
    try:
        location = Location.objects.get(name=locName, user__username=user.username)
    except ObjectDoesNotExist:
        response_data['result'] = 'failed'
        response_data['message'] = 'Location name is invalid (location not found or user does not have permission).'
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    # the location exists, and the user has permission, so go ahead:
    location.delete()

    response_data['result'] = 'success'
    response_data['message'] = 'Location was successfully deleted.'
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@login_required
@require_GET
def getLocations(request):
    # TODO: add multiple users
    user = User.objects.get(username='test')

    locations = list(Location.objects.filter(user__username=user.username)
                                     .values_list('latitude','longitude','radius','name','date')
                                     .order_by('date'))

    locObject = []
    for location in locations:
        obj = {}
        obj['latitude'] = location[0]
        obj['longitude'] = location[1]
        obj['radius'] = location[2]
        obj['name'] = location[3]
        obj['date'] = str(location[4])
        locObject.append(obj)

    return HttpResponse(json.dumps(locObject), content_type="application/json")
