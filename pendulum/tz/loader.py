# -*- coding: utf-8 -*-

import os
import pytz
import inspect

from .parser import Parser
from .._compat import decode


class Loader(object):

    path = os.path.join(os.path.dirname(inspect.getfile(pytz)), 'zoneinfo')

    @classmethod
    def load(cls, name):
        name = decode(name)

        name_parts = name.lstrip('/').split('/')

        for part in name_parts:
            if part == os.path.pardir or os.path.sep in part:
                raise ValueError('Bad path segment: %r' % part)

        filepath = os.path.join(cls.path, *name_parts)

        if not os.path.exists(filepath):
            raise ValueError('Unknown timezone [{}]'.format(name))

        return Parser.parse(filepath)
