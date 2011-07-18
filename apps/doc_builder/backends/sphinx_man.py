from doc_builder.backends.sphinx import Builder as ManpageBuilder

class Builder(ManpageBuilder):
    build_type = 'man'
