from django.conf.urls import patterns, url

from map import views

urlpatterns = patterns('',
        url(r'(?P<locName>.+)/$', views.mapLocation, name='map location'),
)
