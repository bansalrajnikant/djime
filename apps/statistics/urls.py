from django.conf.urls.defaults import *

urlpatterns = patterns('statistics.views',
    (r'^user/(?P<user_id>\d+)/year/(?P<year>\d{4,4})/week/(?P<week>\d{1,2})/$', 'week'),
    (r'^user/(?P<user_id>\d+)/year/(?P<year>\d{4,4})/month/(?P<month>\d{1,2})/$', 'month'),
    (r'^user/(?P<user_id>\d+)/week/$', 'todays_week'),
    (r'^user/(?P<user_id>\d+)/month/$', 'todays_month'),
    (r'^user/(?P<user_id>\d+)/date/$', 'date'),
    (r'^data/user/(?P<user_id>\d+)/date/$', 'get_date_data', {'start_date': [2008, 11,14], 'end_date' : [2008, 12, 01]}),
    (r'^data/user/(?P<user_id>\d+)/(?P<action>(week|month))/(?P<data>\d{1,2})/year/(?P<year>\d{4,4})/$', 'get_data'),
)
