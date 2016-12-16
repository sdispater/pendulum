# -*- coding: utf-8 -*-

import re
import copy

from datetime import datetime
from dateutil import parser

from .exceptions import ParserError


class Parser(object):

    COMMON = re.compile(
        # Date
        '^'
        '(\d{4})'  # Year
        '('
        '    ((?:-|/)?(\d{2,3}))?'  # Month (optional)
        '    ((?:-|/)?(\d{2}))?'  # Day (optional)
        ')?'

        # Time (Optional)
        '('
        '    (?:T|\ )'  # Separator (T or space)
        '    (\d{1,2}):?(\d{1,2})?:?(\d{1,2})?'  # HH:mm:ss (optional mm and ss)
        # Subsecond part (optional)
        '    ('
        '        (?:\.|,)'  # Subsecond separator (optional)
        '        (\d{1,9})'  # Subsecond
        '    )?'
        # Timezone offset
        '    ('
        '        (-|\+)\d{2}:?(?:\d{2})?|Z'  # Offset (+HH:mm or +HHmm or +HH or Z)
        '    )?'
        ')?'
        '$',
        re.VERBOSE
    )

    ISO8601_WEEK = re.compile(
        '^'
        '(\d{4})'  # Year
        '-?'  # Separator (optional)
        'W'  # W separator
        '(\d{2})'  # Week number
        '-?'  # Separator (optional)
        '(\d)?'  # Weekday (optional)
        '$'
    )

    DEFAULT_OPTIONS = {
        'day_first': False
    }

    def __init__(self, **options):
        self._options = copy.copy(self.DEFAULT_OPTIONS)
        self._options.update(options)

    def parse_common(self, text):
        """
        Tries to parse the string as a common datetime format.

        :param text: The string to parse.
        :type text: str

        :rtype: dict or None
        """
        m = self.COMMON.match(text)
        if m:
            year = int(m.group(1))

            if not m.group(2):
                # No month and day
                month = 1
                day = 1
            else:
                if m.group(4) and m.group(6):
                    if len(m.group(4)) == 3:
                        # Should not happen
                        # Ordinal day with extra day set
                        raise ParserError('Invalid date string: {}'.format(text))

                    # Month and day
                    if self._options['day_first']:
                        month = int(m.group(6))
                        day = int(m.group(4))
                    else:
                        month = int(m.group(4))
                        day = int(m.group(6))
                else:
                    # Only month
                    if m.group(4) and len(m.group(4)) == 3:
                        # Ordinal day
                        dt = datetime.strptime(
                            '{}-{}'.format(year, m.group(4)),
                            '%Y-%j'
                        )
                        month = dt.month
                        day = dt.day
                    else:
                        month = int(m.group(4) or m.group(6))
                        day = 1

            parsed = {
                'year': year,
                'month': month,
                'day': day,
                'hour': 0,
                'minute': 0,
                'second': 0,
                'subsecond': 0,
                'offset': None,
            }
            if not m.group(7):
                return parsed

            # Grabbing hh:mm:ss
            parsed['hour'] = int(m.group(8))

            if m.group(9):
                parsed['minute'] = int(m.group(9))

            if m.group(10):
                parsed['second'] = int(m.group(10))

            # Grabbing subseconds, if any
            if m.group(11):
                parsed['subsecond'] = int('{:0<9}'.format(m.group(12)))

            # Grabbing timezone, if any
            tz = m.group(13)
            if tz:
                if tz == 'Z':
                    offset = 0
                else:
                    negative = True if tz.startswith('-') else False
                    tz = tz[1:]
                    if ':' not in tz:
                        if len(tz) == 2:
                            tz = '{}00'.format(tz)

                        off_hour = tz[0:2]
                        off_minute = tz[2:4]
                    else:
                        off_hour, off_minute = tz.split(':')

                    offset = ((int(off_hour) * 60) + int(off_minute)) * 60

                    if negative:
                        offset = -1 * offset

                parsed['offset'] = offset

            return parsed

    def parse_8601_week(self, text):
        m = self.ISO8601_WEEK.match(text)

        if not m:
            return {}

        year = m.group(1)
        week = m.group(2)
        weekday = m.group(3)
        if not weekday:
            weekday = '1'

        fmt = '%YW%W%w'
        string = '{}W{}{}'.format(year, week, weekday)

        dt = datetime.strptime(string, fmt)

        return {
            'year': dt.year,
            'month': dt.month,
            'day': dt.day,
            'hour': dt.hour,
            'minute': dt.minute,
            'second': dt.second,
            'subsecond': dt.microsecond * 1000,
            'offset': dt.utcoffset().total_seconds() if dt.tzinfo else None,
        }

    def parse(self, text):
        """
        Parses a string with the given options.

        :param text: The string to parse.
        :type text: str

        :rtype: dict
        """
        # ISO8601 week notation
        parsed = self.parse_8601_week(text)
        if parsed:
            return parsed

        parsed = self.parse_common(text)
        if parsed:
            return parsed

        try:
            dt = parser.parse(text, dayfirst=self._options['day_first'])
        except ValueError:
            raise ParserError('Invalid date string: {}'.format(text))

        return {
            'year': dt.year,
            'month': dt.month,
            'day': dt.day,
            'hour': dt.hour,
            'minute': dt.minute,
            'second': dt.second,
            'subsecond': dt.microsecond * 1000,
            'offset': dt.utcoffset().total_seconds() if dt.tzinfo else None,
        }
