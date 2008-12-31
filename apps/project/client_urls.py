from django.conf.urls.defaults import *

urlpatterns = patterns('project.views',
    url(r'^$', 'client_index', name='client_index'),
    url(r'^(?P<client_id>\d+)/$', 'show_client', name='client_page'),
    url(r'^(?P<user_type>(user|team|project))/(?P<user_id>\d+)/clients/$',
        'show_user_clients'name='user_client_list'),
)

