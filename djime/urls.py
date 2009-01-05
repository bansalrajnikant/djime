from django.conf.urls.defaults import *

urlpatterns = patterns('djime.views',
    url(r'^$', 'index', name="slip_index"),
    url(r'^slip/(?P<slip_id>\d+)/$', 'slip', name="slip_page"),
    url(r'^slip/(?P<slip_id>\d+)/(?P<action>(start|stop|get_json))/$',
        'slip_action', name="slip_action"),
    url(r'^slip/add', 'slip_create', name="slip_create"),
    (r'^import/', include('djime.data_import.urls')),
    (r'^statistics/', include('djime.statistics.urls')),
)
