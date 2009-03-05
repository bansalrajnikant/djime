from django.conf.urls.defaults import *

urlpatterns = patterns('djime.statistics.views',
    url(r'^$', 'index', name='statistics_index'),
    (r'^user/(?P<user_id>\d+)/year/(?P<year>\d{4,4})/week/(?P<week>[1-9]|[1-4][0-9]|5[0-3])/$', 'display_user_week'),
    (r'^user/(?P<user_id>\d+)/year/(?P<year>\d{4,4})/month/(?P<month>[1-9]|1[0-2])/$', 'display_user_month'),
    (r'^user/(?P<user_id>\d+)/date/selection/$', 'user_date_selection_form'),
    (r'^user/(?P<user_id>\d+)/date/(?P<start_date>[0-9-]+)/(?P<end_date>[0-9-]+)/$', 'display_user_date_selection'),

    (r'^team/(?P<team_id>\d+)/year/(?P<year>\d{4,4})/week/(?P<week>[1-9]|[1-4][0-9]|5[0-3])/$', 'display_team_week'),
    (r'^team/(?P<team_id>\d+)/year/(?P<year>\d{4,4})/month/(?P<month>[1-9]|1[0-2])/$', 'display_team_month'),
    (r'^team/(?P<team_id>\d+)/date/selection/$', 'team_date_selection_form'),
    (r'^team/(?P<team_id>\d+)/date/(?P<start_date>[0-9-]+)/(?P<end_date>[0-9-]+)/$', 'display_team_date_selection'),

    (r'^team_stat/(?P<team_id>\d+)/year/(?P<year>\d{4,4})/week/(?P<week>[1-9]|[1-4][0-9]|5[0-3])/$', 'display_team_stat_week'),
    (r'^team_stat/(?P<team_id>\d+)/year/(?P<year>\d{4,4})/month/(?P<month>[1-9]|1[0-2])/$', 'display_team_stat_month'),
    (r'^team_stat/(?P<team_id>\d+)/date/selection/$', 'team_stat_date_selection_form'),
    (r'^team_stat/(?P<team_id>\d+)/date/(?P<start_date>[0-9-]+)/(?P<end_date>[0-9-]+)/$', 'display_team_stat_date_selection'),

    (r'^data/user/(?P<user_id>\d+)/year/(?P<year>\d{4,4})/week/(?P<week>[1-9]|[1-4][0-9]|5[0-3])/$', 'data_user_week'),
    (r'^data/user/(?P<user_id>\d+)/year/(?P<year>\d{4,4})/month/(?P<month>[1-9]|1[0-2])/$', 'data_user_month'),
    (r'^data/user/(?P<user_id>\d+)/date/(?P<start_date>[0-9-]+)/(?P<end_date>[0-9-]+)/$', 'data_user_date'),

    (r'^data/team/(?P<team_id>\d+)/year/(?P<year>\d{4,4})/week/(?P<week>[1-9]|[1-4][0-9]|5[0-3])/$', 'data_team_week'),
    (r'^data/team/(?P<team_id>\d+)/year/(?P<year>\d{4,4})/month/(?P<month>[1-9]|1[0-2])/$', 'data_team_month'),
    (r'^data/team/(?P<team_id>\d+)/date/(?P<start_date>[0-9-]+)/(?P<end_date>[0-9-]+)/$', 'data_team_date'),

    (r'^data/team_stat/(?P<team_id>\d+)/year/(?P<year>\d{4,4})/week/(?P<week>[1-9]|[1-4][0-9]|5[0-3])/$', 'data_team_stat_week'),
    (r'^data/team_stat/(?P<team_id>\d+)/year/(?P<year>\d{4,4})/month/(?P<month>[1-9]|1[0-2])/$', 'data_team_stat_month'),
    (r'^data/team_stat/(?P<team_id>\d+)/date/(?P<start_date>[0-9-]+)/(?P<end_date>[0-9-]+)/$', 'data_team_stat_date'),

    url(r'^billing/$', 'billing_index', name='billing_index'),
    url(r'^billing/(?P<user_id>\d+)/$', 'user_billing', name='billing_page'),
    url(r'^billing/(?P<user_id>\d+)/week/(?P<date>[0-9-]+)/(?P<number_of_weeks>\d+)/$', 'user_billing_weeks', name='weekly_billings'),
    url(r'^billing/(?P<user_id>\d+)/date/(?P<start_date>[0-9-]+)/(?P<end_date>[0-9-]+)/$', 'user_billing_date', name='date_billings'),
)
