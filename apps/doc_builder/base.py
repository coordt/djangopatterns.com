from functools import wraps
import os, subprocess


def restoring_chdir(fn):
    #XXX:dc: This would be better off in a neutral module
    @wraps(fn)
    def decorator(*args, **kw):
        try:
            path = os.getcwd()
            return fn(*args, **kw)
        finally:
            os.chdir(path)
    return decorator


class BaseBuilder(object):
    """
    The Base for all Builders. Defines the API for subclasses.
    All workflow steps need to return true, otherwise it is assumed something
    went wrong and the Builder will stop
    """

    workflow = ['clean', 'build', 'move']

    def __init__(self, source_path, dest_path):
        self.source_path = source_path
        self.dest_path = dest_path

    def run(self):
        for step in self.workflow:
            fn = getattr(self, step)
            result = fn()
            assert result

    @restoring_chdir
    def force(self):
        """
        An optional step to force a build even when nothing has changed.
        """
        print "Forcing a build by touching files"
        os.chdir(self.version.project.conf_dir(self.version.slug))
        os.system('touch * && touch */*')

    def clean(self):
        """
        Clean up the version so it's ready for usage.

        This is used to add RTD specific stuff to Sphinx, and to
        implement whitelists on projects as well.

        It is guaranteed to be called before your project is built.
        """
        raise NotImplementedError

    def build(self):
        """
        Do the actual building of the documentation.
        """
        raise NotImplementedError

    def move(self):
        """
        Move the documentation from it's generated place to its final home.

        This needs to understand both a single server dev environment,
        as well as a multi-server environment.
        """
        raise NotImplementedError

    @property
    def changed(self):
        """
        Says whether the documentation has changed, and requires further action.

        This is mainly used to short-circuit more expensive builds of other
        output formats if the project docs didn't change on an update.
        Subclasses are recommended to override for more efficient builds.

        Defaults to `True`
        """
        return True

    @staticmethod
    def run(*commands):
        """
        Run one or more commands, and return ``(status, out, err)``.
        If more than one command is given, then this is equivalent to
        chaining them together with ``&&``; if all commands succeed, then
        ``(status, out, err)`` will represent the last successful command.
        If one command failed, then ``(status, out, err)`` will represent
        the failed command.
        """
        environment = os.environ.copy()
        environment['READTHEDOCS'] = 'True'
        cwd = os.getcwd()
        if not commands:
            raise ValueError("run() requires one or more command-line strings")

        for command in commands:
            print("Running: '%s'" % command)
            try:
                p = subprocess.Popen(command.split(), shell=False, cwd=cwd,
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                     env=environment)

                out, err = p.communicate()
                ret = p.returncode
            except:
                out = ''
                err = traceback.format_exc()
                ret = -1
                print "Command failed: %s" % err

        return (ret, out, err)
