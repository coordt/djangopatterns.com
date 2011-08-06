# Django settings for project project.

import calloway
import os
import sys

CALLOWAY_ROOT = os.path.abspath(os.path.dirname(calloway.__file__))
sys.path.insert(0, os.path.join(CALLOWAY_ROOT, 'apps'))
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'apps'))
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'lib'))
SITE_ROOT = PROJECT_ROOT

try:
    from local_settings import DEBUG as LOCAL_DEBUG
    DEBUG = LOCAL_DEBUG
except ImportError:
    DEBUG = False
TEMPLATE_DEBUG = DEBUG

from calloway.settings import *

ADMINS = (
    ('coordt', 'webmaster@djangopatterns.com'),
)
MANAGERS = ADMINS
DEFAULT_FROM_EMAIL='webmaster@djangopatterns.com'
SERVER_EMAIL='webmaster@djangopatterns.com'

SECRET_KEY = 'ipviu=n(t&27lxc+-a=nuoiw_1pn0gmik%=%c2nr@upyeu=gv_'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', 
        'NAME': 'dev.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
USE_I18N = True

try:
    from local_settings import MEDIA_URL_PREFIX
except ImportError:
    MEDIA_URL_PREFIX = "/media/"
try:
    from local_settings import MEDIA_ROOT_PREFIX
except ImportError:
    MEDIA_ROOT_PREFIX = os.path.join(PROJECT_ROOT, 'media')
try:    
    from local_settings import MEDIA_ROOT
except ImportError:
    MEDIA_ROOT = os.path.join(MEDIA_ROOT_PREFIX, 'uploads')
try:
    from local_settings import STATIC_ROOT
except ImportError:
    STATIC_ROOT = os.path.join(MEDIA_ROOT_PREFIX, 'static')
    

MEDIA_URL = '%suploads/' % MEDIA_URL_PREFIX
STATIC_URL = "%sstatic/" % MEDIA_URL_PREFIX

MMEDIA_DEFAULT_STORAGE = 'media_storage.MediaStorage'
MMEDIA_IMAGE_UPLOAD_TO = 'image/%Y/%m/%d'

AUTH_PROFILE_MODULE = ''

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, 'templates'),
) + CALLOWAY_TEMPLATE_DIRS

CACHE_BACKEND = 'memcached://localhost:11211/'

INSTALLED_APPS = APPS_DJANGO_BASE + \
    APPS_MESSAGES + \
    APPS_ADMIN + \
    APPS_STAFF + \
    APPS_REVERSION + \
    APPS_STORIES + \
    APPS_CALLOWAY_DEFAULT + \
    APPS_TINYMCE + \
    APPS_CACHING + \
    APPS_MPTT + \
    APPS_CATEGORIES + \
    APPS_MEDIA + \
    APPS_REGISTRATION + \
    APPS_REVERSION + \
    APPS_TINYMCE + (
        'viewpoint',
        'staticfiles',
        'calloway',
        'debug_toolbar',
        'hiermenu',
        'google_analytics',
        'robots',
        'native_tags',
        'positions',
        'doc_builder',
        'django.contrib.redirects',
        'disqus',
    )

##########################
# Viewpoint settings
##########################

VIEWPOINT_SETTINGS = {
    'ENTRY_RELATION_MODELS': [
        'massmedia.audio', 'massmedia.image', 'massmedia.document',
        'massmedia.video', 'massmedia.collection', 
        'viewpoint.entry',  ],
    'DEFAULT_STORAGE': 'media_storage.MediaStorage',
    'AUTHOR_MODEL': 'staff.StaffMember',
    'USE_CATEGORIES': True,
    'USE_TAGGING': False,
    'STAFF_ONLY': True,
    'USE_APPROVAL': False,
    'DEFAULT_BLOG': 'default',
    'MONTH_FORMAT': r"%b",
    'URL_REGEXES': {
        'blog': r'^(?P<blog_slug>[-\w]+)/$',
        'year': r'^(?P<blog_slug>[-\w]+)/(?P<year>\d{4})/$',
        'month': r'^(?P<blog_slug>[-\w]+)/(?P<year>\d{4})/(?P<month>%b)/$',
        'day': r'^(?P<blog_slug>[-\w]+)/(?P<year>\d{4})/(?P<month>%b)/(?P<day>\d{1,2})/$',
        'entry': r'^(?P<blog_slug>[-\w]+)/(?P<year>\d{4})/(?P<month>%b)/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$',
    }
}

##########################
# Massmedia settings
##########################

MMEDIA_DEFAULT_STORAGE = 'media_storage.MediaStorage'
MMEDIA_IMAGE_UPLOAD_TO = 'image/%Y/%m/%d'

MASSMEDIA_STORAGE = {
    'DEFAULT': 'media_storage.MediaStorage',
    'IMAGE': 'media_storage.MediaStorage',
    'VIDEO': 'media_storage.MediaStorage',
    'AUDIO': 'media_storage.MediaStorage',
    'FLASH': 'media_storage.MediaStorage',
    'DOC': 'media_storage.MediaStorage',
}
MASSMEDIA_UPLOAD_TO = {
    'IMAGE': 'image/%Y/%m/%d'
}
MASSMEDIA_SERVICES = {
    'YOUTUBE': {
        'EMAIL': 'twtweb@gmail.com',
        'USERNAME': 'washingtontimes',
        'PASSWORD': 'timesweb10',
    }
}

##########################
# Tiny MCE settings
##########################

TINYMCE_JS_URL = '/media/static/js/tiny_mce/tiny_mce.js'
TINYMCE_JS_ROOT = '/media/static/js/tiny_mce'
TINYMCE_DEFAULT_CONFIG = {
    'theme': "advanced",
    'relative_urls': False,
    'plugins': "safari,paste,advimage,advlink,preview,fullscreen,searchreplace",
    'theme_advanced_toolbar_location' : "top",
    'theme_advanced_toolbar_align' : "left",
    'theme_advanced_buttons1' : "bold,italic,underline,strikethrough,blockquote,justifyleft,justifycenter,justifyright|,bullist,numlist,|,link,unlink,|,charmap,image,media,pastetext,pasteword,|,code,preview",
    'theme_advanced_buttons2' : "",
    'theme_advanced_buttons3' : "",
    'theme_advanced_statusbar_location' : "bottom",
    'width': "600",
    'height': "600",
    'gecko_spellcheck': True,
    'valid_elements' : "@[id|class|title|dir<ltr?rtl|lang|xml::lang|onclick|"
        "ondblclick|onmousedown|onmouseup|onmouseover|onmousemove|onmouseout|"
        "onkeypress|onkeydown|onkeyup],"
        "a[rel|rev|charset|hreflang|tabindex|accesskey|type|name|href|target|"
           "onfocus|onblur],"
        "strong/b,em/i,strike,u,#p,-ol[type|compact],-ul[type|compact],-li,br,"
        "img[longdesc|usemap|src|border|alt=|title|hspace|vspace|width|height|align],"
        "-sub,-sup,-blockquote,"
        "-table[border=0|cellspacing|cellpadding|width|frame|rules|height|"
           "align|summary|bgcolor|background|bordercolor],"
        "-tr[rowspan|width|height|align|valign|bgcolor|background|bordercolor],"
        "tbody,thead,tfoot,#td[colspan|rowspan|width|height|align|valign|"
           "bgcolor|background|bordercolor|scope],"
        "#th[colspan|rowspan|width|height|align|valign|scope],"
        "caption,-div,-span,-code,-pre,address,-h1,-h2,-h3,-h4,-h5,-h6,"
        "hr[size|noshade]|size|color],dd,dl,dt,cite,abbr,acronym,"
        "del[datetime|cite],ins[datetime|cite],"
        "object[classid|width|height|codebase|*],"
        "param[name|value|_value],embed[type|width|height|src|*],"
        "script[src|type],map[name],area[shape|coords|href|alt|target],"
        "bdo,button,col[align|char|charoff|span|valign|width],"
        "colgroup[align|char|charoff|span|valign|width],dfn,fieldset,"
        "form[action|accept|accept-charset|enctype|method],"
        "input[accept|alt|checked|disabled|maxlength|name|readonly|size|src|type|value],"
        "kbd,label[for],legend,noscript,optgroup[label|disabled],"
        "option[disabled|label|selected|value],q[cite],samp,"
        "select[disabled|multiple|name|size],small,"
        "textarea[cols|rows|disabled|name|readonly],tt,var,big,"
        "iframe[align<bottom?left?middle?right?top|frameborder|height"
          "|longdesc|marginheight|marginwidth|name|scrolling<auto?no?yes|src|style"
          "|width]",
}

NATIVE_TAGS = (
    'viewpoint.template',
    'native_tags.contrib.comparison',
    'native_tags.contrib.generic_content',
)

ADMIN_TOOLS_THEMING_CSS = 'calloway/admin/css/theming.css'
# ADMIN_TOOLS_MENU = 'menu.CustomMenu'

TINYMCE_JS_URL = '%scalloway/js/tiny_mce/tiny_mce.js' % STATIC_URL
TINYMCE_JS_ROOT = os.path.join(STATIC_ROOT, 'js/tiny_mce')

DOC_GIT = "git://github.com/coordt/djangopatterns.git"
DOC_SOURCE = os.path.join(PROJECT_ROOT, 'doc_src')

STATICFILES_FINDERS = (
    'staticfiles.finders.FileSystemFinder', 
    'staticfiles.finders.AppDirectoriesFinder',
    'staticfiles.finders.LegacyAppDirectoriesFinder',
)
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

try:
    from local_settings import *
except ImportError:
    pass
