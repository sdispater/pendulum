# -*- coding: utf-8 -*-

from math import copysign
from datetime import timedelta

try:
    from ._extensions._helpers import local_time
except ImportError:
    from ._extensions.helpers import local_time

from .constants import DAYS_PER_MONTHS


def is_leap(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


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
