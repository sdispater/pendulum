# -*- coding: utf-8 -*-

import os
import re

from importlib import import_module

from pendulum.utils._compat import basestring
from pendulum.utils._compat import decode


class Locale:
    """
    Represent a specific locale.
    """

    _cache = {}

    def __init__(self, locale, data):
        self._locale = locale
        self._data = data
        self._key_cache = {}

    @classmethod
    def load(cls, locale):
        if isinstance(locale, Locale):
            return locale

        locale = cls.normalize_locale(locale)
        if locale in cls._cache:
            return cls._cache[locale]

        # Checking locale existence
        actual_locale = locale
        locale_path = os.path.join(os.path.dirname(__file__), actual_locale)
        while not os.path.exists(locale_path):
            if actual_locale == locale:
                raise ValueError('Locale [{}] does not exist.'.format(locale))

            actual_locale = actual_locale.split('_')[0]

        m = import_module('pendulum.locales.{}.locale'.format(actual_locale))

        cls._cache[locale] = cls(locale, m.locale)

        return cls._cache[locale]

    @classmethod
    def normalize_locale(cls, locale):
        m = re.match('([a-z]{2})[-_]([a-z]{2})', locale, re.I)
        if m:
            return '{}_{}'.format(m.group(1).lower(), m.group(2).lower())
        else:
            return locale.lower()

    def get(self, key, default=None):
        if key in self._key_cache:
            return self._key_cache[key]

        parts = key.split('.')
        try:
            result = self._data[parts[0]]
            for part in parts[1:]:
                result = result[part]
        except KeyError:
            result = default

        if isinstance(result, basestring):
            result = decode(result)

        self._key_cache[key] = result

        return self._key_cache[key]

    def translation(self, key):
        return self.get('translations.{}'.format(key))

    def plural(self, number):
        return decode(self._data['plural'](number))

    def ordinal(self, number):
        return decode(self._data['ordinal'](number))

    def ordinalize(self, number):
        ordinal = self.get('custom.ordinal.{}'.format(self.ordinal(number)))

        if not ordinal:
            return decode('{}'.format(number))

        return decode('{}{}'.format(number, ordinal))

    def match_translation(self, key, value):
        translations = self.translation(key)
        if value not in translations.values():
            return None

        return {v: k for k, v in translations.items()}[value]

    def __repr__(self):
        return "{}('{}')".format(self.__class__.__name__, self._locale)
