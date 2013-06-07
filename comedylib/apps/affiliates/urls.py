from django.conf.urls import patterns, url

from affiliates.views import Offers

urlpatterns = patterns('',
    url('^offers/$', Offers.as_view(), name='offers'),
)
