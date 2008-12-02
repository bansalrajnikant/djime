from django.conf.urls.defaults import *

urlpatterns = patterns('data_import.views',
    url(r'^$', 'import_form', name='data_import_form'),
    url(r'^confirm/$', 'confirm', name='data_import_confirm'),
    url(r'^reusults/$', 'results',name='data_import_results'),
)
