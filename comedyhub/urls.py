from django.conf import settings
from django.conf.urls.defaults import patterns, url, include
from django.conf.urls.static import static
from django.contrib import admin

from profiles.views import Playlists

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^a/', include('accounts.urls')),
    url(r'^u/', include('profiles.urls')),
    url(r'^c/', include('django.contrib.comments.urls')),
    url(r'^', include('content.urls', namespace='content')),
    url(r'^playlists/$', Playlists.as_view(), {'g': True},
        name='playlists'),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
