# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import,
    division,
    unicode_literals,
    print_function,
)

from functools import wraps

import inspect
import pendulum


class WrappedGenerator(object):
    def __init__(self, wrapped):
        self.wrapped = wrapped

    def __iter__(self):
        return self

    def __next__(self, *args, **kwargs):
        return self.next(*args, **kwargs)

    def next(self):
        return pendulumify(next(self.wrapped))


def pendulumify(obj):
    '''

    Recursively turns all datetime objects in a container type iterable (think
    dictionaries, lists, sets, etc.) into a Pendulum object, including those
    returned by generator objects

    '''

    def is_sequence_or_callable(arg):
        return (not hasattr(arg, 'strip') and
                (hasattr(arg, '__getitem__') or
                hasattr(arg, '__iter__') or
                hasattr(arg, '__call__')))

    if not is_sequence_or_callable(obj):
        try:
            return pendulum.instance(obj)
        except AttributeError:
            return obj

    if hasattr(obj, '__call__'):
        @wraps(obj)
        def wrapped(*args, **kwargs):
            return pendulumify(obj(*args, **kwargs))

        return wrapped

    if inspect.isgenerator(obj):
        return WrappedGenerator(obj)

    if isinstance(obj, dict):
        return {k: pendulumify(v) for k, v in obj.items()}

    constructor = type(obj)

    return constructor(map(pendulumify, obj))
