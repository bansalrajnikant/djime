from django.conf.urls.defaults import *

urlpatterns = patterns('project.views',
    url(r'^$', 'client_index', name='client_index'),
    url(r'^(?P<client_id>\d+)/$', 'show_client', name='client_page'),
)

