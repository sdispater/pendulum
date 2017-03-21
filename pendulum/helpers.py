# -*- coding: utf-8 -*-

import pendulum

from math import copysign
from datetime import timedelta

try:
    from ._extensions._helpers import local_time, parse_iso8601 as _parse_iso8601

    def parse_iso8601(text, day_first=False):
        return _parse_iso8601(text, day_first)

except ImportError:
    from ._extensions.helpers import local_time

    parse_iso8601 = None

from .constants import (
    DAYS_PER_MONTHS, DAY_OF_WEEK_TABLE, DAYS_PER_L_YEAR, DAYS_PER_N_YEAR
)


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


def precise_diff(d1, d2):
    """
    Calculate a precise difference between two datetimes.

    :param d1: The first datetime
    :type d1: pendulum.Pendulum or pendulum.Date

    :param d2: The second datetime
    :type d2: pendulum.Pendulum or pendulum.Date

    :rtype: dict
    """
    diff = {
        'years': 0,
        'months': 0,
        'days': 0,
        'hours': 0,
        'minutes': 0,
        'seconds': 0,
        'microseconds': 0
    }
    sign = 1

    if d1 == d2:
        return diff

    if d1 > d2:
        d1, d2 = d2, d1
        sign = -1

    y_diff = d2.year - d1.year
    m_diff = d2.month - d1.month
    d_diff = d2.day - d1.day
    hour_diff = 0
    min_diff = 0
    sec_diff = 0
    mic_diff = 0

    if hasattr(d2, 'hour'):
        hour_diff = d2.hour - d1.hour
        min_diff = d2.minute - d1.minute
        sec_diff = d2.second - d1.second
        mic_diff = d2.microsecond - d1.microsecond

        if mic_diff < 0:
            mic_diff += 1000000
            sec_diff -= 1

        if sec_diff < 0:
            sec_diff += 60
            min_diff -= 1

        if min_diff < 0:
            min_diff += 60
            hour_diff -= 1

        if hour_diff < 0:
            hour_diff += 24
            d_diff -= 1

    if d_diff < 0:
        year = d2.year
        month = d2.month

        if month == 1:
            month = 12
            year -= 1
        else:
            month -= 1

        leap = int(is_leap(year))

        days_in_last_month = DAYS_PER_MONTHS[leap][month]
        days_in_month = DAYS_PER_MONTHS[int(is_leap(d2.year))][d2.month]

        if d_diff < days_in_month - days_in_last_month:
            # We don't have a full month, we calculate days
            if days_in_last_month < d1.day:
                d_diff += d1.day
            else:
                d_diff += days_in_last_month
        elif d_diff == days_in_month - days_in_last_month:
            # We have exactly a full month
            # We remove the days difference
            # and add one to the months difference
            d_diff = 0
            m_diff += 1
        else:
            # We have a full month
            d_diff += days_in_last_month

        m_diff -= 1

    if m_diff < 0:
        m_diff += 12
        y_diff -= 1

    diff['microseconds'] = sign * mic_diff
    diff['seconds'] = sign * sec_diff
    diff['minutes'] = sign * min_diff
    diff['hours'] = sign * hour_diff
    diff['days'] = sign * d_diff
    diff['months'] = sign * m_diff
    diff['years'] = sign * y_diff

    return diff


def week_day(year, month, day):
    if month < 3:
        year -= 1

    w = (year + year//4 - year//100 + year//400 + DAY_OF_WEEK_TABLE[month - 1] + day) % 7

    if not w:
        w = 7

    return w


def days_in_year(year):
    if is_leap(year):
        return DAYS_PER_L_YEAR

    return DAYS_PER_N_YEAR

def _sign(x):
    return int(copysign(1, x))
