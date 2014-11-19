from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.models import User
from django.core import serializers
from django.forms import ModelForm
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
    # HOWEVER: it still has JS on the frontend to validate and send data,
    # which also needs to be change if changes are made there
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
        form = LocationForm(request.POST)
        location = form.save(commit=False)
        location.date = datetime.now()
        location.latest_data = datetime.now()
        # TODO: add multiple users
        location.user = User.objects.get(username='test')

        if form.is_valid():
            location.save()
            response_data['result'] = 'success'
            response_data['message'] = 'Location was successfully added.'
        else:
            response_data['result'] = 'failed'
            response_data['message'] = 'Data is invalid.'

    return HttpResponse(json.dumps(response_data), content_type="application/json")
