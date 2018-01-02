import pendulum

from math import copysign
from datetime import timedelta
from contextlib import contextmanager


try:
    from ._extensions._helpers import (
        local_time, precise_diff,
        is_leap, week_day, days_in_year
    )
except ImportError:
    from ._extensions.helpers import (
        local_time, precise_diff,
        is_leap, week_day, days_in_year
    )

from .constants import DAYS_PER_MONTHS


def add_duration(dt, years=0, months=0, weeks=0, days=0,
                 hours=0, minutes=0, seconds=0, microseconds=0):
    """
    Adds a duration to a datetime instance.

    :param dt: The datetime instance
    :type dt: datetime.datetime

    :param years: The number of years
    :type years: int

    :param months: The number of months
    :type months: int

    :param weeks: The number of weeks
    :type weeks: int

    :param days: The number of days
    :type days: int

    :param hours: The number of hours
    :type hours: int

    :param minutes: The number of minutes
    :type minutes: int

    :param seconds: The number of seconds
    :type seconds: int

    :param microseconds: The number of microseconds
    :type microseconds: int

    :rtype: datetime.datetime
    """
    days += weeks * 7

    # Normalizing
    if abs(microseconds) > 999999:
        s = _sign(microseconds)
        div, mod = divmod(microseconds * s, 1000000)
        microseconds = mod * s
        seconds += div * s

    if abs(seconds) > 59:
        s = _sign(seconds)
        div, mod = divmod(seconds * s, 60)
        seconds = mod * s
        minutes += div * s

    if abs(minutes) > 59:
        s = _sign(minutes)
        div, mod = divmod(minutes * s, 60)
        minutes = mod * s
        hours += div * s

    if abs(hours) > 23:
        s = _sign(hours)
        div, mod = divmod(hours * s, 24)
        hours = mod * s
        days += div * s

    if abs(months) > 11:
        s = _sign(months)
        div, mod = divmod(months * s, 12)
        months = mod * s
        years += div * s

    year = dt.year + years
    month = dt.month

    if months:
        month += months
        if month > 12:
            year += 1
            month -= 12
        elif month < 1:
            year -= 1
            month += 12

    day = min(DAYS_PER_MONTHS[int(is_leap(year))][month], dt.day)

    dt = dt.replace(year=year, month=month, day=day)

    return dt + timedelta(
        days=days,
        hours=hours,
        minutes=minutes,
        seconds=seconds,
        microseconds=microseconds
    )


def _sign(x):
    return int(copysign(1, x))


# Global helpers

@contextmanager
def test(mock):
    set_test_now(mock)

    yield

    set_test_now()


def set_test_now(test_now=None):
    pendulum._TEST_NOW = test_now


def get_test_now():
    return pendulum._TEST_NOW


def has_test_now():
    return pendulum._TEST_NOW is not None


def set_locale(locale):
    if not pendulum._TRANSLATOR.has_translations(locale):
        raise ValueError(f'Unsupported locale [{locale}]')

    pendulum._LOCALE = locale
    pendulum._TRANSLATOR.locale = locale


def get_locale():
    return pendulum._LOCALE


def translator():
    return pendulum._TRANSLATOR


def week_starts_at(wday):
    if wday < pendulum.SUNDAY or wday > pendulum.SATURDAY:
        raise ValueError('Invalid week day as start of week.')

    pendulum._WEEK_STARTS_AT = wday


def week_ends_at(wday):
    if wday < pendulum.SUNDAY or wday > pendulum.SATURDAY:
        raise ValueError('Invalid week day as start of week.')

    pendulum._WEEK_ENDS_AT = wday
