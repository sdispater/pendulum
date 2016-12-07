# -*- coding: utf-8 -*-

import re
import copy

from dateutil import parser

from .exceptions import ParserError


class Parser(object):

    COMMON = re.compile(
        '(\d{4})(?:-|/)(\d{1,2})(?:-|/)(\d{1,2})' # YMD or YDM
        '('
        '(?:T| )' # Separator
        '(\d{2}):(\d{2}):(\d{2})' # HH:mm:ss
        '(\.(\d{1,9}))?' # Subsecond
        '((-|\+)\d{2}:\d{2}|Z)?' # Timezone offset
        ')?'
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
            if self._options['day_first']:
                month = int(m.group(3))
                day = int(m.group(2))
            else:
                month = int(m.group(2))
                day = int(m.group(3))

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
            if not m.group(4):
                return parsed

            # Grabbing hh:mm:ss
            parsed['hour'] = int(m.group(5))
            parsed['minute'] = int(m.group(6))
            parsed['second'] = int(m.group(7))

            # Grabbing subseconds, if any
            if m.group(8):
                parsed['subsecond'] = int('{:0<9}'.format(m.group(9)))

            # Grabbing timezone, if any
            tz = m.group(10)
            if tz:
                if tz == 'Z':
                    offset = 0
                else:
                    negative = True if tz.startswith('-') else False
                    off_hour, off_minute = tz[1:].split(':')

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
