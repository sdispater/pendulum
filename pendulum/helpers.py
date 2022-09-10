from __future__ import annotations

import os
import struct

from contextlib import contextmanager
from datetime import date
from datetime import datetime
from datetime import timedelta
from math import copysign
from typing import TYPE_CHECKING
from typing import Iterator
from typing import TypeVar
from typing import overload

import pendulum

from pendulum.constants import DAYS_PER_MONTHS
from pendulum.formatting.difference_formatter import DifferenceFormatter
from pendulum.locales.locale import Locale


if TYPE_CHECKING:
    # Prevent import cycles
    from pendulum.period import Period

with_extensions = os.getenv("PENDULUM_EXTENSIONS", "1") == "1"

_DT = TypeVar("_DT", bound=datetime)
_D = TypeVar("_D", bound=date)

try:
    # nopycln: file # noqa: E800
    if not with_extensions or struct.calcsize("P") == 4:
        raise ImportError()

    from pendulum._extensions._helpers import days_in_year
    from pendulum._extensions._helpers import is_leap
    from pendulum._extensions._helpers import is_long_year
    from pendulum._extensions._helpers import local_time
    from pendulum._extensions._helpers import precise_diff
    from pendulum._extensions._helpers import timestamp
    from pendulum._extensions._helpers import week_day
except ImportError:
    from pendulum._extensions.helpers import days_in_year  # noqa: F401
    from pendulum._extensions.helpers import is_leap
    from pendulum._extensions.helpers import is_long_year  # noqa: F401
    from pendulum._extensions.helpers import local_time  # noqa: F401
    from pendulum._extensions.helpers import precise_diff  # noqa: F401
    from pendulum._extensions.helpers import timestamp  # noqa: F401
    from pendulum._extensions.helpers import week_day  # noqa: F401


difference_formatter = DifferenceFormatter()


@overload
def add_duration(
    dt: _DT,
    years: int = 0,
    months: int = 0,
    weeks: int = 0,
    days: int = 0,
    hours: int = 0,
    minutes: int = 0,
    seconds: int = 0,
    microseconds: int = 0,
) -> _DT:
    pass


@overload
def add_duration(
    dt: _D,
    years: int = 0,
    months: int = 0,
    weeks: int = 0,
    days: int = 0,
) -> _D:
    pass


def add_duration(
    dt,
    years=0,
    months=0,
    weeks=0,
    days=0,
    hours=0,
    minutes=0,
    seconds=0,
    microseconds=0,
):
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


def format_diff(
    diff: Period, is_now: bool = True, absolute: bool = False, locale: str | None = None
) -> str:
    if locale is None:
        locale = get_locale()

    return difference_formatter.format(diff, is_now, absolute, locale)


def _sign(x):
    return int(copysign(1, x))


# Global helpers


@contextmanager
def test(mock: pendulum.DateTime) -> Iterator[None]:
    set_test_now(mock)
    try:
        yield
    finally:
        set_test_now()


def set_test_now(test_now: pendulum.DateTime | None = None) -> None:
    pendulum._TEST_NOW = test_now


def get_test_now() -> pendulum.DateTime | None:
    return pendulum._TEST_NOW


def has_test_now() -> bool:
    return pendulum._TEST_NOW is not None


def locale(name: str) -> Locale:
    return Locale.load(name)


def set_locale(name: str) -> None:
    locale(name)

    pendulum._LOCALE = name


def get_locale() -> str:
    return pendulum._LOCALE


def week_starts_at(wday: int) -> None:
    if wday < pendulum.SUNDAY or wday > pendulum.SATURDAY:
        raise ValueError("Invalid week day as start of week.")

    pendulum._WEEK_STARTS_AT = wday


def week_ends_at(wday: int) -> None:
    if wday < pendulum.SUNDAY or wday > pendulum.SATURDAY:
        raise ValueError("Invalid week day as start of week.")

    pendulum._WEEK_ENDS_AT = wday
