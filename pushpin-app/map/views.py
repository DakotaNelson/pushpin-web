from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core import serializers

from map.models import Pushpin, Location


def mapLocation(request):
    location = get_object_or_404(Location, name="Center of the World")
    print(location)

    # then get pins based on that location
    # pushpins = get_list_or_404(Pushpin, location

    # for now, just get all pins
    pushpins = get_list_or_404(Pushpin.objects.all())

    sources = []

    for pin in pushpins:
        if pin.source not in sources:
            sources.append(pin.source)

    print(pushpins)

    template = loader.get_template('map/index.html')

    context = RequestContext( request, {
        'sources': sources,
        'location': location,
        'pushpins': serializers.serialize('json', pushpins)
        })

    return HttpResponse(template.render(context))
