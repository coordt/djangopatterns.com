CONVORE_SETTINGS = {
    'USERNAME': '',
    'PASSWORD': '',
    'CREATE_MESSAGE_URL': "https://convore.com/api/topics/%s/messages/create.json",
    'ACTIVITY_TOPIC_ID': 0,
}

PROJECTS_ROOT = '/var/code/'

VIRTUALENV_ROOT = '/home/coordt/.virtualenvs/'

CURRENT_SITE = 'djangopatterns'

EXTRA_INDEXES = (
    "--extra-index-url=http://opensource.washingtontimes.com/simple/",
)

USERS = (
    'demo1', 'demopass'
    'demo2', 'demopass2'
)

# A site-relative path to the requirements
REQUIREMENTS_PATH = 'setup/requirements.txt'
WSGI_PATH = 'conf/djangopatterns.wsgi'


APACHE_PKGS = {
    'ubuntu': ('apache2','apache2.2-common','apache2-mpm-worker',
               'apache2-utils','libapache2-mod-wsgi',)
}

PG_PKGS = {
    'ubuntu': ('postgresql-client-8.4', 'postgresql-client-common')
}

PG_SERVER_PKGS = {
    'ubuntu': ('postgresql-8.4', 'postgresql-server-dev-8.4', 
               'postgresql-8.4-postgis', 'postgresql-contrib-8.4')
}

SCM_PKGS = {
    'ubuntu': ('git-core',)
}

SYS_PKGS = {
    'ubuntu': ('python-setuptools', 'python-dev', 'python-psycopg2',
                'python-imaging', 'libjpeg-progs', 'supervisor', 'g++', 
                'libgmp3-dev', 'htop', 'memcached')
}

##  Used by Deploy

REQUIRED_PKGS = {
    'ubuntu': (APACHE_PKGS['ubuntu'] + SYS_PKGS['ubuntu'] + PG_PKGS['ubuntu'] + 
        SCM_PKGS['ubuntu'])
}

PYTHON_PKGS = {
    'ubuntu': ('virtualenvwrapper', 'virtualenv', 'Fabric', 'distribute')
}

