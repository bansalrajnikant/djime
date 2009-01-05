from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login', name="acct_login"),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name="acct_logout"),
    url(r'^signup/$', 'account.views.signup', name="acct_signup"),
)

