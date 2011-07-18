import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

SOURCE_DIR = os.path.join(os.path.dirname(__file__), 'test_docs')
DEST_DIR = os.path.join(os.path.dirname(__file__), 'done')

from backends import sphinx, sphinx_epub, sphinx_htmldir, sphinx_json, sphinx_man

bld = sphinx.Builder(SOURCE_DIR, DEST_DIR)
bld.clean()
bld.build()
bld.move()

bld = sphinx_epub.Builder(SOURCE_DIR, DEST_DIR)
bld.clean()
bld.build()
bld.move()

bld = sphinx_htmldir.Builder(SOURCE_DIR, DEST_DIR)
bld.clean()
bld.build()
bld.move()

bld = sphinx_json.Builder(SOURCE_DIR, DEST_DIR)
bld.clean()
bld.build()
bld.move()

bld = sphinx_man.Builder(SOURCE_DIR, DEST_DIR)
bld.clean()
bld.build()
bld.move()
