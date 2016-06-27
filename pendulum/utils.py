# -*- coding: utf-8 -*-

from functools import update_wrapper
from wrapt import ObjectProxy


class PropertyProxy(ObjectProxy):

    _name = None
    _instance = None

    def __init__(self, value, name, instance):
        self._name = name
        self._instance = instance

        super(PropertyProxy, self).__init__(value)

    def __call__(self, value):
        self._instance._datetime = self._instance._datetime.replace(**{self._name: value})

        return self._instance


class hybrid_property(object):
    """
    Property that acts as a method to set value.
    """

    formats = {
        'year': '%Y',
        #'year_iso': '%o',
        'month': '%-m',
        'day': '%-d',
        'hour': '%-H',
        'minute': '%-M',
        'second': '%-S'
    }

    def __init__(self, func=None, name=None):
        self._name = name

        self.set_func(func)

    def set_func(self, func):
        self._func = func

        if self._name is None:
            if isinstance(func, property):
                self._name = func.fget.__name__ if func else None
            else:
                self._name = func.__name__ if func else None

        self.expr = func
        if func is not None:
            update_wrapper(self, func)

    def __get__(self, instance, owner):
        if instance is None:
            return self.expr

        return PropertyProxy(self._func(instance), self._name, instance)

    def __set__(self, instance, value):
        if self._name == 'year':
            instance.set_date(value, instance.month, instance.day)
        elif self._name == 'month':
            instance.set_date(instance.year, value, instance)

    def __call__(self, func):
        self.set_func(func)

        return self
