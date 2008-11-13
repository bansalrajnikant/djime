from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
import os.path
admin.autodiscover()

urlpatterns = patterns('',
    (r'^tracker/', include('djime.tracker.urls')),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/(.*)', admin.site.root),
)

# If in debug mode, serve site_media through Django.
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': os.path.join(os.path.dirname(__file__), "site_media")}),
    )
