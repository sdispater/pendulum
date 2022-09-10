from __future__ import annotations

import datetime as _datetime

from typing import Optional
from typing import Union

from pendulum.__version__ import __version__
from pendulum.constants import DAYS_PER_WEEK
from pendulum.constants import FRIDAY
from pendulum.constants import HOURS_PER_DAY
from pendulum.constants import MINUTES_PER_HOUR
from pendulum.constants import MONDAY
from pendulum.constants import MONTHS_PER_YEAR
from pendulum.constants import SATURDAY
from pendulum.constants import SECONDS_PER_DAY
from pendulum.constants import SECONDS_PER_HOUR
from pendulum.constants import SECONDS_PER_MINUTE
from pendulum.constants import SUNDAY
from pendulum.constants import THURSDAY
from pendulum.constants import TUESDAY
from pendulum.constants import WEDNESDAY
from pendulum.constants import WEEKS_PER_YEAR
from pendulum.constants import YEARS_PER_CENTURY
from pendulum.constants import YEARS_PER_DECADE
from pendulum.date import Date
from pendulum.datetime import DateTime
from pendulum.duration import Duration
from pendulum.formatting import Formatter
from pendulum.helpers import format_diff
from pendulum.helpers import get_locale
from pendulum.helpers import get_test_now
from pendulum.helpers import has_test_now
from pendulum.helpers import locale
from pendulum.helpers import set_locale
from pendulum.helpers import set_test_now
from pendulum.helpers import test
from pendulum.helpers import week_ends_at
from pendulum.helpers import week_starts_at
from pendulum.parser import parse
from pendulum.period import Period
from pendulum.time import Time
from pendulum.tz import POST_TRANSITION
from pendulum.tz import PRE_TRANSITION
from pendulum.tz import TRANSITION_ERROR
from pendulum.tz import UTC
from pendulum.tz import local_timezone
from pendulum.tz import set_local_timezone
from pendulum.tz import test_local_timezone
from pendulum.tz import timezone
from pendulum.tz import timezones
from pendulum.tz.timezone import FixedTimezone
from pendulum.tz.timezone import Timezone


_TEST_NOW: DateTime | None = None
_LOCALE = "en"
_WEEK_STARTS_AT = MONDAY
_WEEK_ENDS_AT = SUNDAY

_formatter = Formatter()


def _safe_timezone(obj: str | float | _datetime.tzinfo | Timezone | None) -> Timezone:
    """
    Creates a timezone instance
    from a string, Timezone, TimezoneInfo or integer offset.
    """
    if isinstance(obj, (Timezone, FixedTimezone)):
        return obj

    if obj is None or obj == "local":
        return local_timezone()

    if isinstance(obj, (int, float)):
        obj = int(obj * 60 * 60)
    elif isinstance(obj, _datetime.tzinfo):
        # pytz
        if hasattr(obj, "localize"):
            obj = obj.zone
        elif obj.tzname(None) == "UTC":
            return UTC
        else:
            offset = obj.utcoffset(None)

            if offset is None:
                offset = _datetime.timedelta(0)

            obj = int(offset.total_seconds())

    return timezone(obj)


# Public API
def datetime(
    year: int,
    month: int,
    day: int,
    hour: int = 0,
    minute: int = 0,
    second: int = 0,
    microsecond: int = 0,
    tz: str | float | Timezone | None = UTC,
    fold: int | None = 1,
    raise_on_unknown_times: bool = False,
) -> DateTime:
    """
    Creates a new DateTime instance from a specific date and time.
    """
    return DateTime.create(
        year,
        month,
        day,
        hour=hour,
        minute=minute,
        second=second,
        microsecond=microsecond,
        tz=tz,
        fold=fold,
        raise_on_unknown_times=raise_on_unknown_times,
    )


def local(
    year: int,
    month: int,
    day: int,
    hour: int = 0,
    minute: int = 0,
    second: int = 0,
    microsecond: int = 0,
) -> DateTime:
    """
    Return a DateTime in the local timezone.
    """
    return datetime(
        year, month, day, hour, minute, second, microsecond, tz=local_timezone()
    )


def naive(
    year: int,
    month: int,
    day: int,
    hour: int = 0,
    minute: int = 0,
    second: int = 0,
    microsecond: int = 0,
    fold: int | None = 1,
) -> DateTime:
    """
    Return a naive DateTime.
    """
    return DateTime(year, month, day, hour, minute, second, microsecond, fold=fold)


def date(year: int, month: int, day: int) -> Date:
    """
    Create a new Date instance.
    """
    return Date(year, month, day)


def time(hour: int, minute: int = 0, second: int = 0, microsecond: int = 0) -> Time:
    """
    Create a new Time instance.
    """
    return Time(hour, minute, second, microsecond)


def instance(dt: _datetime.datetime, tz: str | Timezone | None = UTC) -> DateTime:
    """
    Create a DateTime instance from a datetime one.
    """
    if not isinstance(dt, _datetime.datetime):
        raise ValueError("instance() only accepts datetime objects.")

    if isinstance(dt, DateTime):
        return dt

    tz = dt.tzinfo or tz

    # Checking for pytz/tzinfo
    if isinstance(tz, _datetime.tzinfo) and not isinstance(tz, Timezone):
        # pytz
        if hasattr(tz, "localize") and tz.zone:
            tz = tz.zone
        else:
            # We have no sure way to figure out
            # the timezone name, we fallback
            # on a fixed offset
            tz = tz.utcoffset(dt).total_seconds() / 3600

    return datetime(
        dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond, tz=tz
    )


def now(tz: str | Timezone | None = None) -> DateTime:
    """
    Get a DateTime instance for the current date and time.
    """
    return DateTime.now(tz)


def today(tz: str | Timezone = "local") -> DateTime:
    """
    Create a DateTime instance for today.
    """
    return now(tz).start_of("day")


def tomorrow(tz: str | Timezone = "local") -> DateTime:
    """
    Create a DateTime instance for today.
    """
    return today(tz).add(days=1)


def yesterday(tz: str | Timezone = "local") -> DateTime:
    """
    Create a DateTime instance for today.
    """
    return today(tz).subtract(days=1)


def from_format(
    string: str,
    fmt: str,
    tz: str | Timezone = UTC,
    locale: str | None = None,  # noqa
) -> DateTime:
    """
    Creates a DateTime instance from a specific format.
    """
    parts = _formatter.parse(string, fmt, now(), locale=locale)
    if parts["tz"] is None:
        parts["tz"] = tz

    return datetime(**parts)


def from_timestamp(timestamp: int | float, tz: str | Timezone = UTC) -> DateTime:
    """
    Create a DateTime instance from a timestamp.
    """
    dt = _datetime.datetime.utcfromtimestamp(timestamp)

    dt = datetime(
        dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond
    )

    if tz is not UTC or tz != "UTC":
        dt = dt.in_timezone(tz)

    return dt


def duration(
    days: float = 0,
    seconds: float = 0,
    microseconds: float = 0,
    milliseconds: float = 0,
    minutes: float = 0,
    hours: float = 0,
    weeks: float = 0,
    years: float = 0,
    months: float = 0,
) -> Duration:
    """
    Create a Duration instance.
    """
    return Duration(
        days=days,
        seconds=seconds,
        microseconds=microseconds,
        milliseconds=milliseconds,
        minutes=minutes,
        hours=hours,
        weeks=weeks,
        years=years,
        months=months,
    )


def period(start: DateTime, end: DateTime, absolute: bool = False) -> Period:
    """
    Create a Period instance.
    """
    return Period(start, end, absolute=absolute)
