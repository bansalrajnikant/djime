from django.conf.urls.defaults import *

urlpatterns = patterns('project.views',
    url(r'^$', 'index', name='project_index'),
    url(r'^(?P<project_id>\d+)/$', 'show_project', name='project_page'),
    url(r'^json/$', 'project_json', name='jquery_ajax'),
)

