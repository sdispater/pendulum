# -*- coding: utf-8 -*-

from __future__ import division

from .parsing import Parser as BaseParser
from .tz import UTC
from .pendulum import Pendulum
from .date import Date
from .time import Time
from ._global import Global


class Parser(BaseParser):
    """
    Parser that returns known types (Pendulum, Date, Time)
    """

    def parse(self, text):
        """
        Parses a string with the given options.

        :param text: The string to parse.
        :type text: str

        :rtype: mixed
        """
        # Handling special cases
        if text == 'now':
            return Pendulum.now()

        parsed = super(Parser, self).parse(text)

        if not self.is_exact():
            return self._create_pendulum_object(parsed)

        # Checking for date
        if 'year' in parsed:
            # Checking for time
            if 'hour' in parsed:
                return self._create_pendulum_object(parsed)
            else:
                return self._create_date_object(parsed)

        return self._create_time_object(parsed)

    def _create_pendulum_object(self, parsed):
        if parsed['offset'] is None:
            tz = self._options.get('tz', UTC)
        else:
            tz = parsed['offset'] / 3600

        return Pendulum(
            parsed['year'], parsed['month'], parsed['day'],
            parsed['hour'], parsed['minute'], parsed['second'],
            parsed['subsecond'],
            tzinfo=tz
        )

    def _create_date_object(self, parsed):
        return Date(
            parsed['year'], parsed['month'], parsed['day']
        )

    def _create_time_object(self, parsed):
        return Time(
            parsed['hour'], parsed['minute'], parsed['second'],
            parsed['subsecond']
        )


def parse(text, **options):
    # Use the mock now value if it exists
    options['now'] = options.get('now', Global.get_test_now())

    return Parser(**options).parse(text)
