from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.models import User
from django.core import serializers
from django.forms import ModelForm
from django.core.exceptions import ObjectDoesNotExist
from map.tasks import youtubeTask, twitterTask, picasaTask, shodanTask
from datetime import datetime
import json

from map.models import Pushpin, Location
from map.forms import LocationForm


def mapLocation(request, locName):
    # the unique location
    location = get_object_or_404(Location, name=locName)

    # every other location
    # (this is a wasted DB hit, but saves some parsing - TODO)
    locations = list(Location.objects.exclude(name=locName).order_by('-date'))

    # then get pins based on that location
    pushpins = Pushpin.objects.filter(location__name=locName)

    sources = []

    for pin in pushpins:
        # get the display name, rather than the two letter abbreviation
        pin.source = pin.get_source_display()
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

    return render(request, 'map/index.html', context)

def addLocation(request):
    response_data = {}

    if request.method != 'POST':
        print("ERROR: addLocation endpoint was sent a " + request.method + " request. Requires POST.")
        return HttpResponseForbidden("only POST requests allowed")
    else:
        # fill the form template with the incoming data
        form = LocationForm(request.POST)
        # save the form, but wait to let us make some changes
        location = form.save(commit=False)
        location.date = datetime.now()
        location.latest_data = datetime.now()
        # TODO: add multiple users
        location.user = User.objects.get(username='test')

        if form.is_valid():
            # add the new location
            location.save()
            response_data['result'] = 'success'
            response_data['message'] = 'Location was successfully added.'

            # run all modules to get data for this new location
            twitterTask.delay()
            youtubeTask.delay()
            picasaTask.delay()
            shodanTask.delay()
        else:
            # form is not valid
            response_data['result'] = 'failed'
            response_data['message'] = 'Data is invalid.'

    return HttpResponse(json.dumps(response_data), content_type="application/json")

def deleteLocation(request, locName):
    response_data = {}
    if request.method != 'POST':
        print("ERROR: deleteLocation endpoint was sent a " + request.method + " request. Requires POST.")
        return HttpResponseForbidden("only POST requests allowed")
    else:
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
