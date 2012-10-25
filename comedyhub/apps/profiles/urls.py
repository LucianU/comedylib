from django.conf.urls.defaults import patterns, url

from profiles.views import LoginView, logout

urlpatterns = patterns('',
    url('^login/$', LoginView.as_view(), name='login'),
    url('^logout/$', logout, name='logout'),
)
