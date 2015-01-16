from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.http import HttpResponseRedirect

admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Examples:
    # url(r'^$', 'pushpin.views.home', name='home'),
    # url(r'^pushpin/', include('pushpin.foo.urls')),
    url(r'^map/', include('map.urls', namespace="map")),

    # visiting root redirects to the map
    url(r'^$', lambda r : HttpResponseRedirect('map/location/')),
)
