import os
import shutil

from doc_builder.base import BaseBuilder, restoring_chdir

class Builder(BaseBuilder):
    """
    The parent for most sphinx builders.

    Also handles the default sphinx output of html.
    """
    build_type = 'html'
    
    def clean(self):
        return True
    
    @restoring_chdir
    def build(self):
        os.chdir(self.source_path)
        build_command = f"sphinx-build -b {self.build_type} . _build/{self.build_type}"
        build_results = self.run(build_command)
        os.chdir(self.source_path)
        if 'no targets are out of date.' in build_results[1]:
            self._changed = False
        return build_results

    def move(self):
        target = os.path.join(self.dest_path, self.build_type)
        source = os.path.join(self.source_path, '_build', self.build_type)
        if os.path.exists(target):
            shutil.rmtree(target)
        print "Copying docs from %s to %s." % (source, target)
        shutil.copytree(source, target)
        return True