import pendulum

from .parsing import parse as base_parse, ParserError
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
    parsed = base_parse(text, **options)

    if parsed.is_duration:
        return pendulum.duration(
            years=parsed.years, months=parsed.months, weeks=parsed.weeks,
            days=parsed.days, hours=parsed.hours, minutes=parsed.minutes,
            seconds=parsed.seconds, microseconds=parsed.microseconds
        )

    if not options.get('exact'):
        return _create_datetime_object(parsed, **options)

    # Checking for date
    if parsed.is_datetime:
        return _create_datetime_object(parsed, **options)

    if parsed.is_date:
        return _create_date_object(parsed, **options)

    if parsed.is_time:
        return _create_time_object(parsed, **options)

    raise ParserError(f'Unable to parse [{text}] to a known type')


def _create_datetime_object(parsed, **options):
    if parsed.offset is None:
        tz = options.get('tz', UTC)
    else:
        tz = parsed.offset / 3600

    return pendulum.datetime(
        parsed.year, parsed.month, parsed.day,
        parsed.hour, parsed.minute, parsed.second,
        parsed.microsecond,
        tzinfo=tz
    )


def _create_date_object(parsed, **options):
    return pendulum.date(
        parsed.year, parsed.month, parsed.day
    )


def _create_time_object(parsed, **options):
    return pendulum.time(
        parsed.hour, parsed.minute, parsed.second,
        parsed.microsecond
    )
