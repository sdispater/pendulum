# -*- coding: utf-8 -*-

import re
import datetime

from .._compat import decode
from .formatter import Formatter


_MATCH_1 = re.compile('\d')
_MATCH_2 = re.compile('\d\d')
_MATCH_3 = re.compile('\d{3}')
_MATCH_4 = re.compile('\d{4}')
_MATCH_6 = re.compile('[+-]?\d{6}')
_MATCH_1_TO_2 = re.compile('\d\d?')
_MATCH_1_TO_3 = re.compile('\d{1,3}')
_MATCH_1_TO_4 = re.compile('\d{1,4}')
_MATCH_1_TO_6 = re.compile('[+-]?\d{1,6}')
_MATCH_3_TO_4 = re.compile('\d{3}\d?')
_MATCH_5_TO_6 = re.compile('\d{5}\d?')
_MATCH_UNSIGNED = re.compile('\d+')
_MATCH_SIGNED = re.compile('[+-]?\d+')
_MATCH_OFFSET = re.compile('(?i)Z|[+-]\d\d:?\d\d')
_MATCH_SHORT_OFFSET = re.compile('(?i)Z|[+-]\d\d(?::?\d\d)?')
_MATCH_TIMESTAMP = re.compile('[+-]?\d+(\.\d{1,3})?')
_MATCH_WORD = re.compile("[0-9]*['a-z\u00A0-\u05FF\u0700-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]+|[\u0600-\u06FF\/]+(\s*?[\u0600-\u06FF]+){1,2}")



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

    _REGEX_TOKENS = {
        'Y': _MATCH_SIGNED,
        'YY': (_MATCH_1_TO_2, _MATCH_2),
        'YYYY': (_MATCH_1_TO_4, _MATCH_4),
        'Q': _MATCH_1,
        'Qo': None,
        'M': _MATCH_1_TO_2,
        'MM': (_MATCH_1_TO_2, _MATCH_2),
        'MMM': None,
        'MMMM': None,
        'D': _MATCH_1_TO_2,
        'DD': (_MATCH_1_TO_2, _MATCH_2),
        'DDD': _MATCH_1_TO_3,
        'DDDD': _MATCH_3,
        'Do': None,
        'H': _MATCH_1_TO_2,
        'HH': (_MATCH_1_TO_2, _MATCH_2),
        'h': _MATCH_1_TO_2,
        'hh': (_MATCH_1_TO_2, _MATCH_2),
        'm': _MATCH_1_TO_2,
        'mm': (_MATCH_1_TO_2, _MATCH_2),
        's': _MATCH_1_TO_2,
        'ss': (_MATCH_1_TO_2, _MATCH_2),
        'S': (_MATCH_1_TO_3, _MATCH_1),
        'SS': (_MATCH_1_TO_3, _MATCH_2),
        'SSS': (_MATCH_1_TO_3, _MATCH_3),
        'SSSS': _MATCH_UNSIGNED,
        'SSSSS': _MATCH_UNSIGNED,
        'SSSSSS': _MATCH_UNSIGNED,
        'a': None,
        'x': _MATCH_SIGNED,
        'X': re.compile('[+-]?\d+(\.\d{1,3})?')
    }

    _PARSE_TOKENS = {
        'YYYY': lambda year: int(year),
        'YY': lambda year: 1900 + int(year),
        'Q': lambda quarter: int(quarter),
        'MMMM': lambda month: None,
        'MMM': lambda month: None,
        'MM': lambda month: int(month),
        'M': lambda month: int(month),
        'DDDD': lambda day: int(day),
        'DDD': lambda day: int(day),
        'DD': lambda day: int(day),
        'D': lambda day: int(day),
        'HH': lambda hour: int(hour),
        'H': lambda hour: int(hour),
        'hh': lambda hour: int(hour),
        'h': lambda hour: int(hour),
        'mm': lambda minute: int(minute),
        'm': lambda minute: int(minute),
        'ss': lambda second: int(second),
        's': lambda second: int(second),
        'S': lambda us: int(us) * 100000,
        'SS': lambda us: int(us) * 10000,
        'SSS': lambda us: int(us) * 1000,
        'SSSS': lambda us: int(us) * 100,
        'SSSSS': lambda us: int(us) * 10,
        'SSSSSS': lambda us: int(us),
        'a': lambda meridiem: None,
        'X': lambda ts: float(ts),
        'x': lambda ts: float(ts) / 1e3,
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

        return decode(trans)

    def parse(self, time, fmt):
        """
        Parses a time string matching a given format as a tuple.

        :param time: The timestring
        :type time: str

        :param fmt: The format
        :type fmt: str

        :rtype: tuple
        """
        fmt = re.escape(fmt)
        tokens = self._FORMAT_RE.findall(fmt)
        if not tokens:
            return time

        parsed = {
            'year': None,
            'month': None,
            'day': None,
            'hour': None,
            'minute': None,
            'second': None,
            'microsecond': None,
            'tz': None,
            'quarter': None,
            'day_of_week': None,
            'day_of_year': None,
            'meridiem': None,
            'timestamp': None
        }

        pattern = self._FORMAT_RE.sub(lambda m: self._replace_tokens(m.group(0)), fmt)

        if not re.match(pattern, time):
            raise ValueError('String does not match format {}'.format(fmt))

        re.sub(pattern, lambda m: self._get_parsed_values(m, parsed), time)

        return parsed

    def _get_parsed_values(self, m, parsed):
        for token, index in m.re.groupindex.items():
            self._get_parsed_value(token, m.group(index), parsed)

    def _get_parsed_value(self, token, value, parsed):
        parsed_token = self._PARSE_TOKENS[token](value)

        if 'Y' in token:
            parsed['year'] = parsed_token
        elif 'Q' == token:
            parsed['quarter'] = parsed_token
        elif 'M' in token:
            parsed['month'] = parsed_token
        elif token in ['DDDD', 'DDD']:
            parsed['day_of_year'] = parsed_token
        elif 'D' in token:
            parsed['day'] = parsed_token
        elif 'H' in token:
            parsed['hour'] = parsed_token
        elif token in ['hh', 'h']:
            parsed['hour'] = parsed_token
        elif 'm' in token:
            parsed['minute'] = parsed_token
        elif 's' in token:
            parsed['second'] = parsed_token
        elif 'S' in token:
            parsed['microsecond'] = parsed_token
        elif token in ['MMM', 'MMMM']:
            parsed['day_of_week'] = parsed_token
        elif token == 'a':
            pass
        elif token in ['X', 'x']:
            parsed['timestamp'] = parsed_token

    def _replace_tokens(self, token):
        if token.startswith('[') and token.endswith(']'):
            return token[1:-1]
        elif token.startswith('\\'):
            return token
        elif token not in self._REGEX_TOKENS:
            raise ValueError('Unsupported token: {}'.format(token))

        candidates = self._REGEX_TOKENS[token]
        if not candidates:
            raise ValueError('Unsupported token: {}'.format(token))

        if not isinstance(candidates, tuple):
            candidates = (candidates,)

        pattern = '(?P<{}>{})'.format(token, '|'.join([p.pattern for p in candidates]))

        return pattern
