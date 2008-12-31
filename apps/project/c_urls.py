from django.conf.urls.defaults import *

urlpatterns = patterns('project.views',
    (r'^all/$', 'show_all_clients'),
    (r'^(?P<client_id>\d+)/$', 'show_client'),
    (r'^(?P<user_type>(user|team|project))/(?P<user_id>\d+)/clients/$', 'show_user_clients'),
)