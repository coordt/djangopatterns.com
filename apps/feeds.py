from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.utils.feedgenerator import Atom1Feed
from bookmarks.feeds import BookmarkFeed

class RecentChangesFeed(BookmarkFeed):
    """
    Slight alterations to the default bookmark feed
    """
    def get_object(self, request, username='coordt', *args, **kwargs):
        return get_object_or_404(User, username=username)
    
    def title(self):
        return 'Latest entries on %s' % Site.objects.get_current().domain
    
    def description(self):
        return "Additions and changes to articles on %s" % Site.objects.get_current().domain    
    
    def link(self):
        absolute_url = reverse('rss-feed')
        return "http://%s%s" % (
                Site.objects.get_current().domain,
                absolute_url,
            )

class AtomRecentChangesFeed(RecentChangesFeed):
    feed_type = Atom1Feed
    subtitle = RecentChangesFeed.description
    
    def feed_guid(self):
        return self.link()
