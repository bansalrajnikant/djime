from django.conf.urls.defaults import *

from teams.models import Team
# @@@ should qs really be here?

urlpatterns = patterns('teams.views',
        url(r'^create/$', 'create', name="team_create"),
        url(r'^your_teams/$', 'your_teams', name="your_teams"),
        url(r'^team/(\w+)/$', 'team', name="team_detail"),
        url(r'^team/(?P<slug>\w+)/delete/$', 'delete', name="team_delete"),
    )
