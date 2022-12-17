import os
from fabric.api import *

from fab_settings import (PROJECTS_ROOT, VIRTUALENV_ROOT, CURRENT_SITE, 
                        REQUIREMENTS_PATH, EXTRA_INDEXES, WSGI_PATH)

VENV = os.path.join(VIRTUALENV_ROOT, CURRENT_SITE)
SITE_PATH = os.path.join(PROJECTS_ROOT, CURRENT_SITE)

def _join_path(*args):
    """
    Join a set of paths
    """
    return os.path.abspath(os.path.normpath(os.path.join(*args)))

@runs_once
def _update_requirements(package, version):
    """
    Update the project requirements on the local machine
    """
    pkg_re = re.compile(r'%s\s*==\s*.+' % package)
    if version is None:
        pkg = package
    else:
        pkg = "%s==%s" % (package, version)
    current_reqs = open('requirements.txt').read()
    if pkg_re.search(current_reqs):
        print "Updating %s entry to version %s in the requirements file..." % (package, version)
        new_reqs = pkg_re.sub(pkg, current_reqs)
    else:
        print "Adding %s entry in the requirements file..."
        new_reqs = current_reqs.strip('\n') + '\n' + pkg
    try:
        reqs_file = open('requirements.txt', 'w')
        reqs_file.write(new_reqs)
        set_env(updated_reqs = True)
    except IOError:
        print "Couldn't write to the requirements file."
    
    reqs_file.close()
    

def install_pkg(package, version=None):
    """
    Install a package. Ideally should be in the format pkgname==vnum
    """
    pip = f"{VENV}bin/python {VENV}bin/pip -q install"
    virtenv = f"-E {VENV}"
    extra_idx = " ".join(f"--extra-index-url={x}" for x in EXTRA_INDEXES)
    pkg = package if version is None else f"{package}=={version}"
    cmd = [pip, virtenv, extra_idx, pkg]
    run(" ".join(cmd))
    _update_requirements(package, version)


@runs_once
def install_pkg_local(package, version):
    pip = "pip -q install"
    extra_idx = "--extra-index-url=http://opensource.washingtontimes.com/simple/"
    pkg = package if version is None else f"{package}=={version}"
    cmd = [pip, extra_idx, pkg]
    local(" ".join(cmd))

def pkg_version(package):
    """
    Print out the version installed for a particular package
    """
    run(f"{VENV}bin/pip freeze | grep {package}")

def update_reqs():
    """
    Have pip install the requirements file. This will update any dependencies
    that have changed in the requirements file.
    """
    
    req_path = os.path.join(VIRTUALENV_ROOT, CURRENT_SITE, REQUIREMENTS_PATH)
    run(f'{VENV}/bin/pip install -E {VENV} -r {req_path}')

def reload_site():
    """
    Reload the apache process by touching the wsgi file
    """
    with cd(SITE_PATH):
        run(f'touch {WSGI_PATH}')

def update():
    """
    Cause the site to pull in the latest changes to its code and touch the
    wsgi file so it reloads
    """
    with cd(SITE_PATH):
        run('git pull --all')
    reload_site()
