# -*- coding: utf-8 -*-

import re
import datetime

from .formatter import Formatter


class AlternativeFormatter(Formatter):

    _TOKENS = '\[([^\[]*)\]|\\\(.)|' \
              '(' \
              'Mo|MM?M?M?' \
              '|Do|DDDo|DD?D?D?|ddd?d?|do?' \
              '|w[o|w]?|W[o|W]?|Qo?' \
              '|YYYY|YY|Y' \
              '|gg(ggg?)?|GG(GGG?)?' \
              '|e|E|a|A' \
              '|hh?|HH?|kk?' \
              '|mm?|ss?|S{1,9}' \
              '|x|X' \
              '|zz?|ZZ?' \
              '|LTS|LT|LL?L?L?' \
              ')'

    _FORMAT_RE = re.compile(_TOKENS)

    _LOCALIZABLE_TOKENS = (
        'Mo', 'MMM', 'MMMM',
        'Qo',
        'Do',
        'DDDo',
        'do', 'dd', 'ddd', 'dddd',
        'wo',
        'Wo',
        'A', 'a',
    )

    _TOKENS_RULES = {
        # Year
        'YYYY': lambda dt: '{:d}'.format(dt.year),
        'YY': lambda dt: '{:d}'.format(dt.year)[2:],
        'Y': lambda dt: '{:d}'.format(dt.year),

        # Quarter
        'Q': lambda dt: '{:d}'.format(dt.quarter),

        # Month
        'MM': lambda dt: '{:02d}'.format(dt.month),
        'M': lambda dt: '{:d}'.format(dt.month),

        # Day
        'DD': lambda dt: '{:02d}'.format(dt.day),
        'D': lambda dt: '{:d}'.format(dt.day),

        # Day of Year
        'DDDD': lambda dt: '{:03d}'.format(dt.day_of_year),
        'DDD': lambda dt: '{:d}'.format(dt.day_of_year),

        # Day of Week
        'd': lambda dt: '{:d}'.format(dt.day_of_week),

        # Hour
        'HH': lambda dt: '{:02d}'.format(dt.hour),
        'H': lambda dt: '{:d}'.format(dt.hour),
        'hh': lambda dt: '{:02d}'.format(dt.hour % 12 or 12),
        'h': lambda dt: '{:d}'.format(dt.hour % 12 or 12),

        # Minute
        'mm': lambda dt: '{:02d}'.format(dt.minute),
        'm': lambda dt: '{:d}'.format(dt.minute),

        # Second
        'ss': lambda dt: '{:02d}'.format(dt.second),
        's': lambda dt: '{:d}'.format(dt.second),

        # Fractional second
        'S': lambda dt: '{:01d}'.format(dt.microsecond // 100000),
        'SS': lambda dt: '{:02d}'.format(dt.microsecond // 10000),
        'SSS': lambda dt: '{:03d}'.format(dt.microsecond // 1000),
        'SSSS': lambda dt: '{:04d}'.format(dt.microsecond // 100),
        'SSSSS': lambda dt: '{:05d}'.format(dt.microsecond // 10),
        'SSSSSS': lambda dt: '{:06d}'.format(dt.microsecond),

        # Timestamp
        'X': lambda dt: '{:d}'.format(dt.int_timestamp),

        # Timezone
        'z': lambda dt: '{}'.format(dt.tzinfo.abbrev),
        'zz': lambda dt: '{}'.format(dt.timezone_name),
    }

    _DEFAULT_DATE_FORMATS = {
        'LTS': 'h:mm:ss A',
        'LT': 'h:mm A',
        'L': 'MM/DD/YYYY',
        'LL': 'MMMM D, YYYY',
        'LLL': 'MMMM D, YYYY h:mm A',
        'LLLL': 'dddd, MMMM D, YYYY h:mm A',
    }

    def format(self, dt, fmt, locale=None):
        """
        Formats a Pendulum instance with a given format and locale.

        :param dt: The instance to format
        :type dt: pendulum.Pendulum

        :param fmt: The format to use
        :type fmt: str

        :param locale: The locale to use
        :type locale: str or None

        :rtype: str
        """
        if not locale:
            locale = dt.get_locale()

        return self._FORMAT_RE.sub(
            lambda m: m.group(1)
                if m.group(1)
                else m.group(2)
                if m.group(2)
                else self._format_token(dt, m.group(3), locale),
            fmt
        )

    def _format_token(self, dt, token, locale):
        """
        Formats a Pendulum instance with a given token and locale.

        :param dt: The instance to format
        :type dt: pendulum.Pendulum

        :param token: The token to use
        :type token: str

        :param locale: The locale to use
        :type locale: str or None

        :rtype: str
        """
        if token in self._DEFAULT_DATE_FORMATS:
            fmt = dt.translator().transchoice('date_formats', token, locale=locale)
            if fmt == 'date_formats':
                fmt = self._DEFAULT_DATE_FORMATS[token]

            return self.format(dt, fmt, locale)
        if token in self._LOCALIZABLE_TOKENS:
            return self._format_localizable_token(dt, token, locale)

        if token in self._TOKENS_RULES:
            return self._TOKENS_RULES[token](dt)

        # Timezone
        if token in ['ZZ', 'Z']:
            separator = ':' if token == 'ZZ' else ''
            offset = dt.utcoffset() or datetime.timedelta()
            minutes = offset.total_seconds() / 60

            if minutes >= 0:
                sign = '+'
            else:
                sign = '-'

            hour, minute = divmod(abs(int(minutes)), 60)

            return '{}{:02d}{}{:02d}'.format(sign, hour, separator, minute)

    def _format_localizable_token(self, dt, token, locale):
        """
        Formats a Pendulum instance
        with a given localizable token and locale.

        :param dt: The instance to format
        :type dt: pendulum.Pendulum

        :param token: The token to use
        :type token: str

        :param locale: The locale to use
        :type locale: str or None

        :rtype: str
        """
        trans_id = ''
        count = 0

        if token == 'MMM':
            count = dt.month
            trans_id = 'months_abbrev'
        elif token == 'MMMM':
            count = dt.month
            trans_id = 'months'
        elif token in ('dd', 'ddd'):
            count = dt.day_of_week
            trans_id = 'days_abbrev'
        elif token == 'dddd':
            count = dt.day_of_week
            trans_id = 'days'
        elif token == 'Do':
            count = dt.day
            trans_id = 'ordinal'
        elif token == 'do':
            count = dt.day_of_week
            trans_id = 'ordinal'
        elif token == 'Mo':
            count = dt.month
            trans_id = 'ordinal'
        elif token == 'Qo':
            count = dt.quarter
            trans_id = 'ordinal'
        elif token == 'wo':
            count = dt.week_of_year
            trans_id = 'ordinal'
        elif token == 'DDDo':
            count = dt.day_of_year
            trans_id = 'ordinal'
        elif token == 'A':
            count = (dt.hour, dt.minute)
            trans_id = 'meridian'

        trans = dt.translator().transchoice(trans_id, count, locale=locale)

        if trans_id == 'ordinal':
            trans = '{:d}{}'.format(count, trans)

        if trans_id == trans:
            # Unable to find the corresponding translation
            # Defaulting to english
            return self._format_localizable_token(dt, token, 'en')

        return trans
