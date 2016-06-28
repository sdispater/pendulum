# -*- coding: utf-8 -*-

import sys

PY2 = sys.version_info[0] == 2
PY3K = sys.version_info[0] >= 3
PY33 = sys.version_info >= (3, 3)


if PY2:
    long = long
    unicode = unicode
    basestring = basestring
else:
    long = int
    unicode = str
    basestring = str
