"""
Global project URLs
"""
from django.conf import settings
from django.conf.urls.defaults import patterns, url, include
from django.conf.urls.static import static
from django.contrib import admin

from haystack.forms import SearchForm
from haystack.views import search_view_factory

from search.views import CustomSearchView

admin.autodiscover()

flatpages_urls = patterns('django.contrib.flatpages.views',
    url(r'^about/$', 'flatpage', {'url': '/about/'}, name='about'),
    url(r'^terms/$', 'flatpage', {'url': '/terms/'}, name='terms'),
    url(r'^privacy/$', 'flatpage', {'url': '/privacy/'}, name='privacy'),
    url(r'^ads/$', 'flatpage', {'url': '/ads/'}, name='ads'),
)

urlpatterns = patterns('',
    url(r'^a52/', include(admin.site.urls)),
    url(r'^a/', include('accounts.urls')),
    url(r'^u/', include('profiles.urls')),
    url(r'^c/', include('django.contrib.comments.urls')),
    url(r'^feedback/', include('feedback.urls')),
    url(r'^search/', search_view_factory(
        view_class=CustomSearchView,
        form_class=SearchForm,
        ), name='haystack_search'),
    url(r'^com/', include('affiliates.urls', namespace='affiliates')),
    url(r'^', include(flatpages_urls, namespace='flatpages')),
    url(r'^', include('content.urls', namespace='content')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
