# -*- coding: utf-8 -*-

import sys

PY2 = sys.version_info[0] == 2
PY3K = sys.version_info[0] >= 3
PY36 = sys.version_info >= (3, 6)


try:               # Python 2
    long
    unicode
    basestring
except NameError:  # Python 3
    long = int
    unicode = str
    basestring = str

try:               # Python >= 3.3
    FileNotFoundError = FileNotFoundError
except NameError:  # Python < 3.3
    FileNotFoundError = IOError  # cf PEP-3151 


def decode(string, encodings=None):
    if not PY2 and not isinstance(string, bytes):
        return string

    if PY2 and isinstance(string, unicode):
        return string

    encodings = encodings or ['utf-8', 'latin1', 'ascii']

    for encoding in encodings:
        try:
            return string.decode(encoding)
        except (UnicodeEncodeError, UnicodeDecodeError):
            pass

    return string.decode(encodings[0], errors='ignore')


def encode(string, encodings=None):
    if not PY2 and isinstance(string, bytes):
        return string

    if PY2 and isinstance(string, str):
        return string

    encodings = encodings or ['utf-8', 'latin1', 'ascii']

    for encoding in encodings:
        try:
            return string.encode(encoding)
        except (UnicodeEncodeError, UnicodeDecodeError):
            pass

    return string.encode(encodings[0], errors='ignore')
