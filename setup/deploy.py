from __future__ import with_statement
import os
from fabric.api import *
from fabric.contrib.files import exists, append

SERVER_CMDS = {
    'ubuntu': {
        'install_pkg': 'apt-get install -ym %(package)s',
        'list_pkgs': 'dpkg --get-selections | grep ^%(package)s[[:space:]]'
    }
}


def _has_os_package(opsys, package):
    """
    Check if the server os has the package installed
    """
    if isinstance(package, basestring):
        pkgs = package.split(' ')
    else:
        pkgs = package
    
    final_output = []
    has_everything = True
    list_pkg_cmd = SERVER_CMDS[opsys]['list_pkgs']
    with settings(
        hide('warnings', 'running', 'stdout', 'stderr'),
        warn_only=True
    ):
        for item in pkgs:
            if '%(package)s' in list_pkg_cmd:
                output = run(list_pkg_cmd % {'package': item})
            elif '%s' in list_pkg_cmd:
                output = run(list_pkg_cmd % item)
            else:
                output = run('%s %s' % (list_pkg_cmd, item))
            final_output.append(output)
            has_everything = not output.failed
    return has_everything

def install_os_packages(opsys, packages):
    if isinstance(packages, basestring):
        pkgs = packages.split(' ')
    else:
        pkgs = packages
    failed_pkgs = []
    with settings(
        hide('warnings', 'running', 'stdout', 'stderr'),
        warn_only=True
    ):
        for pkg in pkgs:
            if not _has_os_package(opsys, pkg):
                print "Installing %s" % pkg
                if '%(package)s' in SERVER_CMDS[opsys]['install_pkg']:
                    output = sudo(SERVER_CMDS[opsys]['install_pkg'] % {'package': pkg})
                elif '%s' in SERVER_CMDS[opsys]['install_pkg']:
                    output = sudo(SERVER_CMDS[opsys]['install_pkg'] % pkg)
                else:
                    output = sudo('%s %s' % (SERVER_CMDS[opsys]['install_pkg'], pkg))
                if output.failed:
                    failed_pkgs.append(pkg)
    if failed_pkgs:
        print "The following packages didn't install:"
        for item in failed_pkgs:
            print '\t', item

def _install_pip():
    with settings(
        hide('warnings', 'running', 'stdout', 'stderr'),
        warn_only = True
    ):
        output = run('which pip')
        if output:
            env.has_pip = True
            return
        output = sudo('easy_install pip')
        env.has_pip = not output.failed

def _install_python_pkgs(packages, virtualenv=None):
    require('has_pip', provided_by=[_install_pip,])
    if not env.has_pip:
        abort("pip is not installed, so the python packages can't be installed.")
    if isinstance(packages, (list, tuple)):
        pkgs = ' '.join(packages)
    else:
        pkgs = packages
    
    with settings(
        hide('warnings', 'running', 'stdout', 'stderr'),
        warn_only=True
    ):
        if virtualenv:
            sudo('pip install -E %s %s' % (venv, pkgs))
        else:
            sudo('pip install %s' % pkgs)

def _install_git_scripts():
    if exists('git-scripts'):
        print "Updating the git scripts."
        with cd('git-scripts'): run('git pull origin master')
    else:
        run('git clone git://github.com/coordt/git-scripts.git')
    with cd('git-scripts'):
        sudo('./linkscripts')

def new_user(admin_username, admin_password):
    """
    Modified from https://gist.github.com/814870, btompkins
    """
    
    # Create the admin group and add it to the sudoers file
    admin_group = 'admin'
    sudo('addgroup {group}'.format(group=admin_group))
    sudo('echo "%{group} ALL=(ALL) ALL" >> /etc/sudoers'.format(
        group=admin_group))
    
    # Create the new admin user (default group=username); add to admin group
    sudo('adduser {username} --disabled-password --gecos ""'.format(
        username=admin_username))
    sudo('adduser {username} {group}'.format(
        username=admin_username,
        group=admin_group))
    
    # Set the password for the new admin user
    sudo('echo "{username}:{password}" | chpasswd'.format(
        username=admin_username,
        password=admin_password))


def setup(opsys='ubuntu'):
    """
    Set up a computer, getting it ready to deploy a website.
    
    fab --hosts=newsystem setup
    """
    print "Installing OS packages"
    install_os_packages(opsys, env.REQUIRED_PKGS[opsys])
    print "Installing Python packages"
    _install_pip()
    _install_python_pkgs(env.PYTHON_PKGS[opsys])
    print "Installing Git scripts"
    _install_git_scripts()
    sudo('mkdir -p %s' % env.PROJECTS_ROOT)
    new_user()
