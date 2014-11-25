from django.conf.urls import patterns, url

from map import views

urlpatterns = patterns('',
        url(r'location/(?P<locName>.+)/delete/$', views.deleteLocation, name='delete location'),
        url(r'location/(?P<locName>.+)/', views.mapLocation, name='map location'),
        url(r'add-new-location/$', views.addLocation, name='track new location'),
)
