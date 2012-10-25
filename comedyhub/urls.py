from django.conf import settings
from django.conf.urls.defaults import patterns, url, include
from django.conf.urls.static import static
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('content.urls', namespace='content')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^a/', include('captcha.backends.default.urls')),
    url(r'^a/', include('registration.backends.default.urls')),
    url(r'^a/', include('profiles.urls', namespace='profiles')),
    url(r'^u/', include('social_auth.urls')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
