# -*- coding: utf-8 -*-

import sys

PY2 = sys.version_info[0] == 2
PY3K = sys.version_info[0] >= 3
PY33 = sys.version_info >= (3, 3)


if PY2:
    import imp

    long = long
    unicode = unicode
    basestring = basestring


    def load_module(module, path):
        with open(path, 'rb') as fh:
            mod = imp.load_source(module, path, fh)

            return mod
else:
    long = int
    unicode = str
    basestring = str

    if PY33:
        from importlib import machinery


        def load_module(module, path):
            return machinery.SourceFileLoader(
                module, path
            ).load_module(module)
    else:
        import imp


        def load_module(module, path):
            with open(path, 'rb') as fh:
                mod = imp.load_source(module, path, fh)

                return mod
