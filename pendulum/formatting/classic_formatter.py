# -*- coding: utf-8 -*-

import re
import datetime

from .formatter import Formatter


class ClassicFormatter(Formatter):

    _CUSTOM_FORMATTERS = ['_z', '_t']
    _FORMATTERS_REGEX = re.compile('%%(%s)' % '|'.join(_CUSTOM_FORMATTERS))

    def format(self, dt, fmt, locale=None):
        """
        Formats a Pendulum instance with a given format and locale.

        :param dt: The instance to format
        :type dt: pendulum.Pendulum or pendulum.Date

        :param fmt: The format to use
        :type fmt: str

        :param locale: The locale to use
        :type locale: str or None

        :rtype: str
        """
        if not locale:
            locale = dt.get_locale()

        # Checking for custom formatters
        fmt = self._FORMATTERS_REGEX.sub(lambda m: self._strftime(dt, m, locale), fmt)

        # Checking for localizable directives
        fmt = re.sub('%(a|A|b|B|p)', lambda m: self._localize_directive(dt, m.group(1), locale), fmt)

        if hasattr(dt, '_datetime'):
            return dt._datetime.strftime(fmt)

        if hasattr(dt, '_time'):
            return dt._time.strftime(fmt)

        return datetime.date(dt.year, dt.month, dt.day).strftime(fmt)

    def _localize_directive(self, dt, directive, locale):
        """
        Localize a native strftime directive.

        :param dt: The instance to format
        :type dt: pendulum.Pendulum

        :param directive: The directive to localize
        :type directive: str

        :param locale: The locale to use for localization
        :type locale: str

        :rtype: str
        """
        if directive == 'a':
            id = 'days_abbrev'
            number = dt.day_of_week
        elif directive == 'A':
            id = 'days'
            number = dt.day_of_week
        elif directive == 'b':
            id = 'months_abbrev'
            number = dt.month
        elif directive == 'B':
            id = 'months'
            number = dt.month
        elif directive == 'p':
            id = 'meridian'
            number = (dt.hour, dt.minute)
        else:
            raise ValueError('Unlocalizable directive [{}]'.format(directive))

        translation = dt.translator().transchoice(id, number, locale=locale)
        if translation == id:
            return ''

        return translation

    def _strftime(self, dt, m, locale):
        """
        Handles custom formatters in format string.

        :param dt: The instance to format
        :type dt: pendulum.Pendulum

        :return: str
        """
        fmt = m.group(1)

        if fmt == '_z':
            offset = dt.utcoffset() or datetime.timedelta()
            minutes = offset.total_seconds() / 60

            if minutes >= 0:
                sign = '+'
            else:
                sign = '-'

            hour, minute = divmod(abs(int(minutes)), 60)

            return '{0}{1:02d}:{2:02d}'.format(sign, hour, minute)
        elif fmt == '_t':
            translation = dt.translator().transchoice('ordinal', dt.day, locale=locale)
            if translation == 'ordinal':
                translation = ''

            return translation

        raise ValueError('Unknown formatter %%{}'.format(fmt))
