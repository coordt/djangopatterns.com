from fab_settings import CONVORE_SETTINGS as CONVORE
from fabric.api import *

@runs_once
def send_convore_update(msg, extra=""):
    """
    Send an update to a convore topic
    """
    try:
        import urllib, urllib2, base64
        url = CONVORE['CREATE_MESSAGE_URL'] % CONVORE['ACTIVITY_TOPIC_ID']
        
        username = CONVORE['USERNAME']
        password = CONVORE['PASSWORD']
        msg = "%s \n %s" % (msg, extra)
        
        values = {'message': msg}
        # a great password
        data = urllib.urlencode(values)
        req = urllib2.Request(url, data)
        
        base64string = base64.encodestring('%s:%s' % (username, password))[:-1]
        authheader =  "Basic %s" % base64string
        req.add_header("Authorization", authheader)
        
        handle = urllib2.urlopen(req)
    except Exception, e:
        print e

def link_apache_conf(site_name):
    dest = '/etc/apache2/sites-available/%s' % site_name
    if not exists(dest):
        sudo('ln -s %s/conf/apache2-%s %s' % (site_path, site_name, dest))

def enable_site(site_name):
    """
    Enable an Apache site configuration and restart the process
    """
    sudo('a2ensite %s' % site_name)
    sudo('/etc/init.d/apache2 restart')

def disable_site(site_name):
    """
    Disable an Apache site configuration and restart the process
    """
    sudo('a2dissite %s' % site_name)
    sudo('/etc/init.d/apache2 restart')
