from glob import glob
import re
import os

from django.conf import settings

from doc_builder.base import BaseBuilder, restoring_chdir


latex_re = re.compile('the LaTeX files are in (.*)\.')
pdf_re = re.compile('Output written on (.+) \(')


class Builder(BaseBuilder):

    @restoring_chdir
    def build(self):
        os.chdir(self.source_path)
        latex_results = run('sphinx-build -b latex '
                            '-d _build/doctrees   . _build/latex')

        if latex_results[0] == 0:
            os.chdir('_build/latex')
            tex_globs = glob('*.tex')
            if tex_globs:
                tex_file = tex_globs[0]
            else:
                return False
            pdf_results = run('pdflatex -interaction=nonstopmode %s' % tex_file)
            pdf_match = pdf_re.search(pdf_results[1])
            if pdf_match:
                src = pdf_re.groups(1)
                to_path = self.dest_path
                from_file = os.path.join(self.source_path, '_bulid', 'latex', src)
                to_file = os.path.join(self.dest_path, src)
                run('mv -f %s %s' % (from_file, to_file))
        else:
            print "PDF Building failed. Moving on."
        return latex_results


    def move(self):
        #This needs to be thought about more because of all the state above.
        #We could just shove the filename on the instance or something.
        return True
