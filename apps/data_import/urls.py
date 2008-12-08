from django.conf.urls.defaults import *

urlpatterns = patterns('data_import.views',
    url(r'^$', 'import_form', name='data_import_form'),
    url(r'^confirm/(?P<import_id>\d+)/$', 'confirm', name='data_import_confirm'),
    url(r'^reusults/(?P<import_id>\d+)/(?P<action>(save|delete))$', 'results',name='data_import_results'),
)
