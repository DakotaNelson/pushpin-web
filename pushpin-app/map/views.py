from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.core import serializers

from map.models import Pushpin, Location


def mapLocation(request):
    locName = "Center of the World"

    location = get_object_or_404(Location, name=locName)

    # then get pins based on that location
    pushpins = Pushpin.objects.filter(location__name=locName)

    # or just get all pins
    #pushpins = get_list_or_404(Pushpin.objects.all())

    sources = []

    for pin in pushpins:
        if pin.source not in sources:
            sources.append(pin.source)

    #template = loader.get_template('map/index.html')

    context = {
                'sources': sources,
                'location': location,
                'pushpins': serializers.serialize('json', pushpins)
              }

    #return HttpResponse(template.render(context))
    return render(request, 'map/index.html', context)
