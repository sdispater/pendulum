from __future__ import absolute_import

import pendulum
import os
import struct

from math import copysign
from datetime import datetime, date, timedelta
from contextlib import contextmanager
from typing import Union

with_extensions = os.getenv("PENDULUM_EXTENSIONS", "1") == "1"

try:
    if not with_extensions or struct.calcsize("P") == 4:
        raise ImportError()

    from ._extensions._helpers import (
        local_time,
        precise_diff,
        is_leap,
        is_long_year,
        week_day,
        days_in_year,
        timestamp,
    )
except ImportError:
    from ._extensions.helpers import (
        local_time,
        precise_diff,
        is_leap,
        is_long_year,
        week_day,
        days_in_year,
        timestamp,
    )

from .constants import DAYS_PER_MONTHS
from .formatting.difference_formatter import DifferenceFormatter
from .locales.locale import Locale


difference_formatter = DifferenceFormatter()


def add_duration(
    dt,  # type:  Union[datetime, date]
    years=0,  # type: int
    months=0,  # type: int
    weeks=0,  # type: int
    days=0,  # type: int
    hours=0,  # type: int
    minutes=0,  # type: int
    seconds=0,  # type: int
    microseconds=0,
):  # type: (...) -> Union[datetime, date]
    """
    Adds a duration to a date/datetime instance.
    """
    days += weeks * 7

    if (
        isinstance(dt, date)
        and not isinstance(dt, datetime)
        and any([hours, minutes, seconds, microseconds])
    ):
        raise RuntimeError("Time elements cannot be added to a date instance.")

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
        microseconds=microseconds,
    )


def format_diff(diff, is_now=True, absolute=False, locale=None):
    if locale is None:
        locale = get_locale()

    return difference_formatter.format(diff, is_now, absolute, locale)


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


def get_test_now():  # type: () -> pendulum.DateTime
    return pendulum._TEST_NOW


def has_test_now():  # type: () -> bool
    return pendulum._TEST_NOW is not None


def locale(name):
    return Locale.load(name)


def set_locale(name):
    locale(name)

    pendulum._LOCALE = name


def get_locale():
    return pendulum._LOCALE


def week_starts_at(wday):
    if wday < pendulum.SUNDAY or wday > pendulum.SATURDAY:
        raise ValueError("Invalid week day as start of week.")

    pendulum._WEEK_STARTS_AT = wday


def week_ends_at(wday):
    if wday < pendulum.SUNDAY or wday > pendulum.SATURDAY:
        raise ValueError("Invalid week day as start of week.")

    pendulum._WEEK_ENDS_AT = wday
