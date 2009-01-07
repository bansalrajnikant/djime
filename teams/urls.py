from django.conf.urls.defaults import *
from teams.models import Team
# @@@ should qs really be here?

urlpatterns = patterns('teams.views',
        url(r'^create/$', 'create', name="team_create"),
        url(r'^$', 'index', name="team_index"),
        url(r'^(?P<slug>\w+)/$', 'team', name="team_display"),
        url(r'^(?P<slug>\w+)/delete/$', 'delete', name="team_delete"),
        url(r'^(?P<slug>\w+)/edit/$', 'edit', name="team_edit"),
    )

