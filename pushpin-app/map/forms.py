from django.forms import ModelForm

from map.models import Location

class LocationForm(ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'latitude', 'longitude', 'radius']
