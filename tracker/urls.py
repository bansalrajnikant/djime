from django.conf.urls.defaults import *

urlpatterns = patterns('djime.tracker.views',
    (r'^$', 'index'),
    (r'^slip/(?P<slip_id>\d+)/$', 'slip'),
    (r'^slip/(?P<slip_id>\d+)/(?P<action>(start|stop|get_json))/$', 'slip_action'),
    (r'^slip/add', 'slip_create'),
)
