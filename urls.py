from django.conf.urls.defaults import *
from django.contrib import admin
import os
from django.conf import settings
import globalviews as views
from viewpoint.feeds import LatestEntries
admin.autodiscover()

handler500 = 'django_ext.views.custom_server_error'

sitemaps = {
}
FEEDS = {
    'rss': LatestEntries(feed_type='rss'),
    'atom': LatestEntries(feed_type='atom'),
}

urlpatterns = patterns('django.contrib.syndication.views',
    url(r'^rss/$', 'feed', {'feed_dict': FEEDS, 'url': 'rss'}, name="rss-feed"),
    url(r'^atom/$', 'feed', {'feed_dict': FEEDS, 'url': 'atom'}, name="atom-feed"),
)

urlpatterns += patterns('',
    (r'^admin/', include(admin.site.urls)),
    url(
        r'^patterns/$',
        views.document,
        name = 'document-index',
        kwargs = {'url': ''},
    ),
    url(
        r'^patterns/(?P<url>[\w./-]*)/$',
        views.document,
        name = 'document-detail',
    ),
)
from calloway.urls import urlpatterns as calloway_patterns

urlpatterns += calloway_patterns

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': os.path.join(os.path.dirname(__file__), 'media2')}),
    )
