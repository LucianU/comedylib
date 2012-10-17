from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('content.urls', namespace='content')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^u/', include('registration.backends.default.urls')),
    url(r'^u/', include('social_auth.urls')),
	)
