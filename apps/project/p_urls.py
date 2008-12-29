from django.conf.urls.defaults import *

urlpatterns = patterns('project.views',
    (r'^(?P<user_type>(user|team|client))/(?P<user_id>\d+)/projects/$', 'show_all_projects'),
    (r'^(?P<project_id>\d+)/$', 'show_project')
)
