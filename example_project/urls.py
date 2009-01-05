from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
import os.path
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'djimeboard.views.index', name='djime_index'),
    (r'^accounts/', include('account.urls')),
    (r'^import/', include('data_import.urls')),
    (r'^tracker/', include('tracker.urls')),
    (r'^statistics/', include('statistics.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/(.*)', admin.site.root),
    (r'^teams/', include('teams.urls')),
    (r'^project/', include('project.urls')),
    (r'^client/', include('project.client_urls')),
)

# If in debug mode, serve site_media through Django.
if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
        (r'^%s(?P<path>.*)' % settings.STATIC_URL[1:], 'serve',
         {'document_root': settings.STATIC_ROOT}),
        (r'^%s(?P<path>.*)' % settings.MEDIA_URL[1:], 'serve',
         {'document_root': settings.MEDIA_ROOT}),
    )
