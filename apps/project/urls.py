from django.conf.urls.defaults import *

urlpatterns = patterns('project.views',
    url(r'^$', 'index', name='project_index'),
    url(r'^(?P<user_type>(user|team|project))/(?P<user_id>\d+)/projects/$',
        'show_user_projects', name='user_project_list'),
    url(r'^(?P<project_id>\d+)/$', 'show_project', name='project_page'),
)

