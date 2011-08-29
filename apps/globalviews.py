import os, datetime
from django.utils import simplejson
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.conf import settings
from django.http import Http404
from bookmarks.models import Bookmark

def homepage(request):
    """
    Include recent changes
    """
    latest_changes = Bookmark.objects.filter(adder__id=1).order_by("-added")[:5]
    return render(request, 'homepage.html', {'latest_changes': latest_changes})


def get_doc_path(docroot, url):
    """
    Find the correct path. it could be the url with a .fjson extension or
    it could be an additional /index.fjson
    """
    doc_path = os.path.join(docroot, "%s.fjson" % url)
    index_path = os.path.join(docroot, os.path.join(url, "index.fjson"))
    if os.path.exists(doc_path):
        return doc_path
    elif os.path.exists(index_path):
        return index_path
    else:
        raise Http404


def document(request, url):
    docroot = os.path.join(settings.DOC_SOURCE, '_build', 'json')
    doc_path = get_doc_path(docroot, url)

    template_names = [
        'docs/doc.html',
    ]
    global_toc = simplejson.load(open(os.path.join(docroot, 'index.fjson'), 'rb'))
    return render_to_response(template_names, RequestContext(request, {
        'doc': simplejson.load(open(doc_path, 'rb')),
        'env': simplejson.load(open(os.path.join(docroot, 'globalcontext.json'), 'rb')),
        'docurl': url,
        # 'update_date': datetime.datetime.fromtimestamp(docroot.child('last_build').mtime()),
        # 'home': urlresolvers.reverse('document-index', kwargs={'lang':lang, 'version':version}),
        'redirect_from': request.GET.get('from', None),
    }))
