from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^accounts/', include('socialregistration.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
    url(r'^$', 'main.views.get_panoramio_pics', name='get_panoramio_pics'),
    url(r'^map/$', 'main.views.map', name='map'),
    url(r'^twitt/$', 'main.views.twitt', name='twitt'),
)
