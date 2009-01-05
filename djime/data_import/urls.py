from django.conf.urls.defaults import *

urlpatterns = patterns('djime.data_import.views',
    url(r'^$', 'import_form', name='data_import_form'),
    url(r'^(?P<import_id>\d+)/(?P<action>(confirm|save|cancel))/$',
        'action', name='data_import_action'),
)

