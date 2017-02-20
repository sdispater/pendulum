# -*- coding: utf-8 -*-

import re
from .lang import TRANSLATIONS


class Translator(object):

    def __init__(self, locale='en'):
        self._locale = self._format_locale(locale)
        self._translations = TRANSLATIONS

    @property
    def locale(self):
        return self._locale

    @locale.setter
    def locale(self, locale):
        self._locale = locale

    def trans(self, id, parameters=None, locale=None):
        if parameters is None:
            parameters = {}

        if not locale:
            locale = self._locale
        else:
            locale = self._format_locale(locale)

        while not self.has_translations(locale):
            fallback = locale.split('_')[0]
            if locale == fallback:
                raise ValueError('Locale [{}] could not be found.'.format(locale))

        if id not in self._translations[locale]:
            return id

        translation = self._translations[locale][id]

        return translation.format(**parameters)

    def transchoice(self, id, number, parameters=None, locale=None):
        if parameters is None:
            parameters = {}

        if 'count' not in parameters:
            parameters['count'] = number

        if not locale:
            locale = self._locale
        else:
            locale = self._format_locale(locale)

        while not self.has_translations(locale):
            fallback = locale.split('_')[0]
            if locale == fallback:
                raise ValueError('Locale [{}] could not be found.'.format(locale))

            locale = fallback

        if id not in self._translations[locale]:
            return id

        translation = self._translations[locale][id]

        if isinstance(translation, list):
            translation = translation[PluralizationRules.get(number, locale)]
        elif isinstance(translation, dict):
            if number in translation:
                translation = translation[number]
            else:
                for key in translation.keys():
                    if isinstance(key, tuple) and number in range(*key):
                        return translation[key].format(**parameters)

                translation = translation['default']
        elif callable(translation):
            translation = translation(number)

        return translation.format(**parameters)

    def has_translations(self, locale):
        locale = self._format_locale(locale)

        return locale in self._translations

    def add_translations(self, locale, translations):
        self._translations[locale] = translations

    def _format_locale(cls, locale):
        """
        Properly format locale.

        :param locale: The locale
        :type locale: str

        :rtype: str
        """
        m = re.match('([a-z]{2})[-_]([a-z]{2})', locale, re.I)
        if m:
            return '{}_{}'.format(m.group(1).lower(), m.group(2).lower())
        else:
            return locale.lower()


class PluralizationRules(object):
    """
    Returns the plural rules for a given locale.

    Attributes:
        rules  list
    """

    # The plural rules are derived from code of the Zend Framework (2010-09-25),
    # which is subject to the new BSD license (http://framework.zend.com/license/new-bsd).
    # Copyright (c) 2005-2010 Zend Technologies USA Inc. (http://www.zend.com)
    _rules = {
        'bo': lambda number: 0,
        'dz': lambda number: 0,
        'id': lambda number: 0,
        'ja': lambda number: 0,
        'jv': lambda number: 0,
        'ka': lambda number: 0,
        'km': lambda number: 0,
        'kn': lambda number: 0,
        'ko': lambda number: 0,
        'ms': lambda number: 0,
        'th': lambda number: 0,
        'tr': lambda number: 0,
        'vi': lambda number: 0,
        'zh': lambda number: 0,
        'af': lambda number: 0 if number == 1 else 1,
        'az': lambda number: 0 if number == 1 else 1,
        'bn': lambda number: 0 if number == 1 else 1,
        'bg': lambda number: 0 if number == 1 else 1,
        'ca': lambda number: 0 if number == 1 else 1,
        'da': lambda number: 0 if number == 1 else 1,
        'de': lambda number: 0 if number == 1 else 1,
        'el': lambda number: 0 if number == 1 else 1,
        'en': lambda number: 0 if number == 1 else 1,
        'eo': lambda number: 0 if number == 1 else 1,
        'es': lambda number: 0 if number == 1 else 1,
        'et': lambda number: 0 if number == 1 else 1,
        'eu': lambda number: 0 if number == 1 else 1,
        'fa': lambda number: 0 if number == 1 else 1,
        'fi': lambda number: 0 if number == 1 else 1,
        'fo': lambda number: 0 if number == 1 else 1,
        'fur': lambda number: 0 if number == 1 else 1,
        'fy': lambda number: 0 if number == 1 else 1,
        'gl': lambda number: 0 if number == 1 else 1,
        'gu': lambda number: 0 if number == 1 else 1,
        'ha': lambda number: 0 if number == 1 else 1,
        'he': lambda number: 0 if number == 1 else 1,
        'hu': lambda number: 0 if number == 1 else 1,
        'is': lambda number: 0 if number == 1 else 1,
        'it': lambda number: 0 if number == 1 else 1,
        'ku': lambda number: 0 if number == 1 else 1,
        'lb': lambda number: 0 if number == 1 else 1,
        'ml': lambda number: 0 if number == 1 else 1,
        'mn': lambda number: 0 if number == 1 else 1,
        'mr': lambda number: 0 if number == 1 else 1,
        'nah': lambda number: 0 if number == 1 else 1,
        'nb': lambda number: 0 if number == 1 else 1,
        'ne': lambda number: 0 if number == 1 else 1,
        'nl': lambda number: 0 if number == 1 else 1,
        'nn': lambda number: 0 if number == 1 else 1,
        'no': lambda number: 0 if number == 1 else 1,
        'om': lambda number: 0 if number == 1 else 1,
        'or': lambda number: 0 if number == 1 else 1,
        'pa': lambda number: 0 if number == 1 else 1,
        'pap': lambda number: 0 if number == 1 else 1,
        'ps': lambda number: 0 if number == 1 else 1,
        'pt': lambda number: 0 if number == 1 else 1,
        'so': lambda number: 0 if number == 1 else 1,
        'sq': lambda number: 0 if number == 1 else 1,
        'sv': lambda number: 0 if number == 1 else 1,
        'sw': lambda number: 0 if number == 1 else 1,
        'ta': lambda number: 0 if number == 1 else 1,
        'te': lambda number: 0 if number == 1 else 1,
        'tk': lambda number: 0 if number == 1 else 1,
        'ur': lambda number: 0 if number == 1 else 1,
        'zu': lambda number: 0 if number == 1 else 1,
        'am': lambda number: 0 if number in (0, 1) else 1,
        'bh': lambda number: 0 if number in (0, 1) else 1,
        'fil': lambda number: 0 if number in (0, 1) else 1,
        'fr': lambda number: 0 if number in (0, 1) else 1,
        'gun': lambda number: 0 if number in (0, 1) else 1,
        'hi': lambda number: 0 if number in (0, 1) else 1,
        'ln': lambda number: 0 if number in (0, 1) else 1,
        'mg': lambda number: 0 if number in (0, 1) else 1,
        'nso': lambda number: 0 if number in (0, 1) else 1,
        'xbr': lambda number: 0 if number in (0, 1) else 1,
        'ti': lambda number: 0 if number in (0, 1) else 1,
        'wa': lambda number: 0 if number in (0, 1) else 1,
        'be': lambda number: 0 if number % 10 == 1 and number % 100 != 11 else (1 if ((number % 10 >= 2) and (number % 10 <= 4)) and ((number % 100 < 10) or (number % 100 >= 20)) else 2),
        'bs': lambda number: 0 if number % 10 == 1 and number % 100 != 11 else (1 if ((number % 10 >= 2) and (number % 10 <= 4)) and ((number % 100 < 10) or (number % 100 >= 20)) else 2),
        'hr': lambda number: 0 if number % 10 == 1 and number % 100 != 11 else (1 if ((number % 10 >= 2) and (number % 10 <= 4)) and ((number % 100 < 10) or (number % 100 >= 20)) else 2),
        'ru': lambda number: 0 if number % 10 == 1 and number % 100 != 11 else (1 if ((number % 10 >= 2) and (number % 10 <= 4)) and ((number % 100 < 10) or (number % 100 >= 20)) else 2),
        'sr': lambda number: 0 if number % 10 == 1 and number % 100 != 11 else (1 if ((number % 10 >= 2) and (number % 10 <= 4)) and ((number % 100 < 10) or (number % 100 >= 20)) else 2),
        'uk': lambda number: 0 if number % 10 == 1 and number % 100 != 11 else (1 if ((number % 10 >= 2) and (number % 10 <= 4)) and ((number % 100 < 10) or (number % 100 >= 20)) else 2),
        'cs': lambda number: 0 if number == 1 else (1 if 2 <= number <= 4 else 2),
        'sk': lambda number: 0 if number == 1 else (1 if 2 <= number <= 4 else 2),
        'ga': lambda number: 0 if number == 1 else (1 if number == 2 else 2),
        'lt': lambda number: 0 if (number % 10 == 1 and number % 100 != 11) else (1 if ((number % 10 >= 2 and number % 100 < 10) or number % 100 >= 20) else 2),
        'sl': lambda number: 0 if number % 100 == 1 else (1 if number % 100 == 2 else (2 if number % 100 in (3, 4) else 3)),
        'mk': lambda number: 0 if number % 10 == 1 else 1,
        'mt': lambda number: 0 if number == 1 else (1 if number == 0 or 1 < number % 100 < 11 else (2 if 10 < number % 100 < 20 else 3)),
        'lv': lambda number: 0 if number == 0 else (1 if number % 10 != 1 and number % 100 != 11 else 2),
        'pl': lambda number: 0 if number == 1 else (1 if (2 <= number % 10 <= 4) and (number % 100 < 12 or number % 100 > 14) else 2),
        'cy': lambda number: 0 if number == 1 else (1 if number == 2 else (2 if number in (8, 11) else 3)),
        'ro': lambda number: 0 if number == 1 else (1 if number == 0 or 0 < number % 100 < 20 else 2),
        'ar': lambda number: 0 if number == 0 else (1 if number == 1 else (2 if number == 2 else (3 if 3 <= number % 100 <= 10 else (4 if 11 <= number % 100 <= 99 else 5))))
    }

    @staticmethod
    def get(number, locale):
        """
        Returns the plural position to use for the given locale and number.

        @type number: int
        @param number: The number

        @type locale: str
        @param locale: The locale

        @rtype: int
        @return: The plural position
        """
        if locale == 'pt_br':
            # temporary set a locale for brazilian
            locale = 'xbr'

        if len(locale) > 3:
            locale = locale.split("_")[0]

        rule = PluralizationRules._rules.get(locale, lambda _: 0)
        _return = rule(number)
        if not isinstance(_return, int) or _return < 0:
            return 0
        return _return

    @staticmethod
    def set(rule, locale):
        """
        Overrides the default plural rule for a given locale.

        @type rule: str
        @param rule: Callable

        @type locale: str
        @param locale: The locale

        @raises: ValueError
        """

        if locale == 'pt_br':
            # temporary set a locale for brazilian
            locale = 'xbr'

        if len(locale) > 3:
            locale = locale.split("_")[0]

        if not hasattr(rule, '__call__'):
            raise ValueError('The given rule can not be called')

        PluralizationRules._rules[locale] = rule
