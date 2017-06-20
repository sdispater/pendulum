import pendulum
import datetime

from .parsing import parse as base_parse

try:
    from .parsing._iso8601 import Duration as CDuration
except ImportError:
    CDuration = None

from .tz import UTC


def parse(text, **options):
    # Use the mock now value if it exists
    options['now'] = options.get('now', pendulum.get_test_now())

    return _parse(text, **options)


def _parse(text, **options):
    """
    Parses a string with the given options.

    :param text: The string to parse.
    :type text: str

    :rtype: mixed
    """
    # Handling special cases
    if text == 'now':
        return pendulum.now()

    parsed = base_parse(text, **options)

    if isinstance(parsed, datetime.datetime):
        return pendulum.instance(parsed, tz=options.get('tz', UTC))

    if isinstance(parsed, datetime.date):
        return pendulum.date.instance(parsed)

    if isinstance(parsed, datetime.time):
        return pendulum.time.instance(parsed)

    if CDuration and isinstance(parsed, CDuration):
        return pendulum.duration(
            years=parsed.years, months=parsed.months, weeks=parsed.weeks, days=parsed.days,
            hours=parsed.hours, minutes=parsed.minutes, seconds=parsed.seconds,
            microseconds=parsed.microseconds
        )

    return parsed
