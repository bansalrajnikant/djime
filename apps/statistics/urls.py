from django.conf.urls.defaults import *

urlpatterns = patterns('statistics.views',
    url(r'^$', 'index', name='statistics_index'),
    (r'^(?P<user_type>(user|team))/(?P<user_id>\d+)/year/(?P<year>\d{4,4})/week/(?P<week>[1-9]|[1-4][0-9]|5[0-3])/$', 'display_user_type_week'),
    (r'^(?P<user_type>(user|team))/(?P<user_id>\d+)/year/(?P<year>\d{4,4})/month/(?P<month>[1-9]|1[0-2])/$', 'display_user_type_month'),
    (r'^(?P<user_type>(user|team))/(?P<user_id>\d+)/date/selection/$', 'user_type_date_selection_form'),
    (r'^(?P<user_type>(user|team))/(?P<user_id>\d+)/date/(?P<start_date>[0-9-]+)/(?P<end_date>[0-9-]+)/$', 'user_type_date_selection_display'),

    (r'^team_stat/(?P<team_id>\d+)/year/(?P<year>\d{4,4})/week/(?P<week>[1-9]|[1-4][0-9]|5[0-3])/$', 'display_team_stat_week'),
    (r'^team_stat/(?P<team_id>\d+)/year/(?P<year>\d{4,4})/month/(?P<month>[1-9]|1[0-2])/$', 'display_team_stat_month'),
    (r'^team_stat/(?P<team_id>\d+)/date/selection/$', 'team_stat_date_selection_form'),
    (r'^team_stat/(?P<team_id>\d+)/date/(?P<start_date>[0-9-]+)/(?P<end_date>[0-9-]+)/$', 'display_team_stat_date_selection'),

    (r'^data/(?P<search>(user|team))/(?P<search_id>\d+)/date/(?P<start_date>[0-9-]+)/(?P<end_date>[0-9-]+)/$', 'get_date_data'),
    (r'^data/(?P<search>(user|team))/(?P<search_id>\d+)/year/(?P<year>\d{4,4})/(?P<action>(week|month))/(?P<data>\d{1,2})/$', 'get_data'),

    (r'^data/team_stat/(?P<team_id>\d+)/year/(?P<year>\d{4,4})/week/(?P<week>[1-9]|[1-4][0-9]|5[0-3])/$', 'get_team_stat_week_data'),
    (r'^data/team_stat/(?P<team_id>\d+)/year/(?P<year>\d{4,4})/month/(?P<month>[1-9]|1[0-2])/$', 'get_team_stat_month_data'),
    (r'^data/team_stat/(?P<team_id>\d+)/date/(?P<start_date>[0-9-]+)/(?P<end_date>[0-9-]+)/$', 'get_team_stat_date_data'),
)
