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

    @classmethod
    def parse(cls, text, **options):
        """
        Parses a string with the given options.

        :param text: The string to parse.
        :type text: str

        :rtype: mixed
        """
        parsed = super(Parser, cls).parse(text, **options)

        if not options.get('strict'):
            return cls._create_pendulum_object(parsed, **options)

        # Checking for date
        if 'year' in parsed:
            # Checking for time
            if 'hour' in parsed:
                return cls._create_pendulum_object(parsed, **options)
            else:
                return cls._create_date_object(parsed, **options)

        return cls._create_time_object(parsed, **options)

    @classmethod
    def _create_pendulum_object(cls, parsed, **options):
        if parsed['offset'] is None:
            tz = options.get('tz', UTC)
        else:
            tz = parsed['offset'] / 3600

        return Pendulum(
            parsed['year'], parsed['month'], parsed['day'],
            parsed['hour'], parsed['minute'], parsed['second'],
            parsed['subsecond'],
            tzinfo=tz
        )

    @classmethod
    def _create_date_object(cls, parsed, **options):
        return Date(
            parsed['year'], parsed['month'], parsed['day']
        )

    @classmethod
    def _create_time_object(cls, parsed, **options):
        return Time(
            parsed['hour'], parsed['minute'], parsed['second'],
            parsed['subsecond']
        )


def parse(text, **options):
    # Use the mock now value if it exists
    options['now'] = options.get('now', Global.get_test_now())

    return Parser.parse(text, **options)
