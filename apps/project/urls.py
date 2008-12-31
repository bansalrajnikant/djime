from django.conf.urls.defaults import *

urlpatterns = patterns('project.views',
    (r'^$', 'index'),
    (r'^(?P<user_type>(user|team|project))/(?P<user_id>\d+)/projects/$', 'show_user_projects'),
    (r'^(?P<project_id>\d+)/$', 'show_project'),
)

