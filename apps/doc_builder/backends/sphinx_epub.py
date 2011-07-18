from doc_builder.backends.sphinx import Builder as HtmlBuilder


class Builder(HtmlBuilder):
    build_type = 'html'
