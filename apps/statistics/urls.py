from django.conf.urls.defaults import *

urlpatterns = patterns('statistics.views',
    (r'^user/(?P<user_id>\d+)/year/(?P<year>\d{4,4})/week/(?P<week>\d{1,2})/$', 'week'),
    (r'^user/(?P<user_id>\d+)/year/(?P<year>\d{4,4})/month/(?P<month>\d{1,2})/$', 'month'),
    (r'^user/(?P<user_id>\d+)/week/$', 'todays_week'),
    (r'^user/(?P<user_id>\d+)/month/$', 'todays_month'),
    (r'^user/(?P<user_id>\d+)/date/$', 'date'),
    (r'^user/(?P<user_id>\d+)/date/selection/$', 'date_selection_form'),
    (r'^user/(?P<user_id>\d+)/date/(?P<start_date>[0-9-]+)/(?P<end_date>[0-9-]+)/$', 'date_selection_display'),
    (r'^data/user/(?P<user_id>\d+)/date/(?P<start_date>[0-9-]+)/(?P<end_date>[0-9-]+)/$', 'get_date_data'),
    (r'^data/user/(?P<user_id>\d+)/(?P<action>(week|month))/(?P<data>\d{1,2})/year/(?P<year>\d{4,4})/$', 'get_data'),
)
