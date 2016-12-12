# -*- coding: utf-8 -*-

import re
import copy

from dateutil import parser

from .exceptions import ParserError


class Parser(object):

    COMMON = re.compile(
        # Date
        '^'
        '(\d{4})'  # Year
        '('
        '    ((?:-|/)?(\d{1,2}))?'  # Month (optional)
        '    ((?:-|/)?(\d{1,2}))?'  # Day (optional)
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
        '        (-|\+)\d{2}:?\d{2}|Z'  # Offset (+HH:mm or +HHmm or Z)
        '    )?'
        ')?'
        '$',
        re.VERBOSE
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
                    # Month and day
                    if self._options['day_first']:
                        month = int(m.group(6))
                        day = int(m.group(4))
                    else:
                        month = int(m.group(4))
                        day = int(m.group(6))
                else:
                    # Only month
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
                        off_hour = tz[0:2]
                        off_minute = tz[2:4]
                    else:
                        off_hour, off_minute = tz.split(':')

                    offset = ((int(off_hour) * 60) + int(off_minute)) * 60

                    if negative:
                        offset = -1 * offset

                parsed['offset'] = offset

            return parsed

    def parse(self, text):
        """
        Parses a string with the given options.

        :param text: The string to parse.
        :type text: str

        :rtype: dict
        """
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
            'subsecond': dt.microsecond,
            'offset': dt.utcoffset().total_seconds() if dt.tzinfo else None,
        }
