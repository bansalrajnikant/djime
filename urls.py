from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
import os.path
admin.autodiscover()

urlpatterns = patterns('',
    (r'^tracker/', include('tracker.urls')),
    (r'^accounts/', include('account.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/(.*)', admin.site.root),
)

# If in debug mode, serve site_media through Django.
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': os.path.join(os.path.dirname(__file__), "site_media")}),
    )
