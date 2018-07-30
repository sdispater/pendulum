from __future__ import absolute_import

import datetime as _datetime
from typing import Union

from .__version__ import __version__

# Types
from .datetime import DateTime
from .date import Date
from .time import Time
from .duration import Duration
from .period import Period

from .tz import timezone
from .tz import PRE_TRANSITION, POST_TRANSITION, TRANSITION_ERROR
from .tz.timezone import Timezone as _Timezone

from .formatting import Formatter

# Helpers
from .helpers import (
    test, set_test_now, has_test_now, get_test_now,
    set_locale, get_locale, locale, format_diff,
    week_starts_at, week_ends_at
)

from .utils._compat import _HAS_FOLD

from .tz import (
    timezones,
    local_timezone, test_local_timezone, set_local_timezone,
    UTC
)

from .parser import parse

# Constants
from .constants import (
    MONDAY, TUESDAY, WEDNESDAY,
    THURSDAY, FRIDAY, SATURDAY, SUNDAY,
    YEARS_PER_CENTURY, YEARS_PER_DECADE,
    MONTHS_PER_YEAR, WEEKS_PER_YEAR, DAYS_PER_WEEK,
    HOURS_PER_DAY, MINUTES_PER_HOUR, SECONDS_PER_MINUTE,
    SECONDS_PER_HOUR, SECONDS_PER_DAY
)

_TEST_NOW = None
_LOCALE = 'en'
_WEEK_STARTS_AT = MONDAY
_WEEK_ENDS_AT = SUNDAY

_formatter = Formatter()


def _safe_timezone(obj):
    # type: (Union[str, int, float, _datetime.tzinfo]) -> _Timezone
    """
    Creates a timezone instance
    from a string, Timezone, TimezoneInfo or integer offset.
    """
    if isinstance(obj, _Timezone):
        return obj

    if obj is None or obj == 'local':
        return local_timezone()

    if isinstance(obj, (int, float)):
        obj = int(obj * 60 * 60)
    elif isinstance(obj, _datetime.tzinfo):
        # pytz
        if hasattr(obj, 'localize'):
            obj = obj.zone
        else:
            offset = obj.utcoffset(None)

            if offset is None:
                offset = _datetime.timedelta(0)

            obj = int(offset.total_seconds())

    return timezone(obj)


# Public API
def datetime(year,                      # type: int
             month,                     # type: int
             day,                       # type: int
             hour=0,                    # type: int
             minute=0,                  # type: int
             second=0,                  # type: int
             microsecond=0,             # type: int
             tz=UTC,                    # type: Union[str, _Timezone]
             dst_rule=POST_TRANSITION,  # type: str
             ):  # type: (...) -> DateTime
    """
    Creates a new DateTime instance from a specific date and time.
    """
    if tz is not None:
        tz = _safe_timezone(tz)

    if not _HAS_FOLD:
        dt = naive(
            year, month, day,
            hour, minute, second, microsecond
        )
    else:
        dt = _datetime.datetime(
            year, month, day,
            hour, minute, second, microsecond
        )
    if tz is not None:
        dt = tz.convert(dt, dst_rule=dst_rule)

    return DateTime(
        dt.year, dt.month, dt.day,
        dt.hour, dt.minute, dt.second, dt.microsecond,
        tzinfo=dt.tzinfo,
        fold=dt.fold
    )


def local(year, month, day,
          hour=0, minute=0, second=0, microsecond=0
          ):  # type: (int, int, int, int, int, int, int) -> DateTime
    """
    Return a DateTime in the local timezone.
    """
    return datetime(year, month, day, hour, minute, second, microsecond,
                    tz=local_timezone())


def naive(year, month, day,
          hour=0, minute=0, second=0, microsecond=0
          ):  # type: (int, int, int, int, int, int, int) -> DateTime
    """
    Return a naive DateTime.
    """
    return DateTime(
        year, month, day,
        hour, minute, second, microsecond
    )


def date(year, month, day):  # type: (int, int, int) -> Date
    """
    Create a new Date instance.
    """
    return Date(year, month, day)


def time(hour, minute=0, second=0, microsecond=0
         ):  # type: (int, int, int, int) -> Time
    """
    Create a new Time instance.
    """
    return Time(hour, minute, second, microsecond)


def instance(dt,     # type: _datetime.datetime
             tz=UTC  # type: Union[str, _Timezone, None]
             ):  # type: (...) -> DateTime
    """
    Create a DateTime instance from a datetime one.
    """
    if not isinstance(dt, _datetime.datetime):
        raise ValueError('instance() only accepts datetime objects.')

    if isinstance(dt, DateTime):
        return dt

    tz = dt.tzinfo or tz

    # Checking for pytz/tzinfo
    if (isinstance(tz, _datetime.tzinfo)
            and not isinstance(tz, _Timezone)):
        # pytz
        if hasattr(tz, 'localize') and tz.zone:
            tz = tz.zone
        else:
            # We have no sure way to figure out
            # the timezone name, we fallback
            # on a fixed offset
            tz = tz.utcoffset(dt).total_seconds() / 3600

    return datetime(
        dt.year, dt.month, dt.day,
        dt.hour, dt.minute, dt.second, dt.microsecond,
        tz=tz
    )


def now(tz=None):  # type: (Union[str, _Timezone, None]) -> DateTime
    """
    Get a DateTime instance for the current date and time.
    """
    if has_test_now():
        test_instance = get_test_now()
        _tz = _safe_timezone(tz)

        if tz is not None and _tz != test_instance.timezone:
            test_instance = test_instance.in_tz(_tz)

        return test_instance

    if tz is None or tz == 'local':
        dt = _datetime.datetime.now(local_timezone())
    elif tz is UTC or tz == 'UTC':
        dt = _datetime.datetime.now(UTC)
    else:
        dt = _datetime.datetime.now(UTC)
        tz = _safe_timezone(tz)
        dt = tz.convert(dt)

    return instance(dt, tz)


def today(tz='local'):  # type: (Union[str, _Timezone]) -> DateTime
    """
    Create a DateTime instance for today.
    """
    return now(tz).start_of('day')


def tomorrow(tz='local'):  # type: (Union[str, _Timezone]) -> DateTime
    """
    Create a DateTime instance for today.
    """
    return today(tz).add(days=1)


def yesterday(tz='local'):  # type: (Union[str, _Timezone]) -> DateTime
    """
    Create a DateTime instance for today.
    """
    return today(tz).subtract(days=1)


def from_format(string,      # type: str
                fmt,         # type: str
                tz=UTC,      # type: Union[str, _Timezone]
                locale=None  # type: Union[str, None]
                ):  # type: (...) -> DateTime
    """
    Creates a DateTime instance from a specific format.
    """
    parts = _formatter.parse(string, fmt, now(), locale=locale)
    if parts['tz'] is None:
        parts['tz'] = tz

    return datetime(**parts)


def from_timestamp(timestamp,  # type: Union[int, float]
                   tz=UTC      # type: Union[str, _Timezone]
                   ):  # type: (...) -> DateTime
    """
    Create a DateTime instance from a timestamp.
    """
    dt = _datetime.datetime.utcfromtimestamp(timestamp)

    dt = datetime(
        dt.year, dt.month, dt.day,
        dt.hour, dt.minute, dt.second, dt.microsecond
    )

    if tz is not UTC or tz != 'UTC':
        dt = dt.in_timezone(tz)

    return dt


def duration(days=0,          # type: float
             seconds=0,       # type: float
             microseconds=0,  # type: float
             milliseconds=0,  # type: float
             minutes=0,       # type: float
             hours=0,         # type: float
             weeks=0,         # type: float
             years=0,         # type: float
             months=0         # type: float
             ):  # type: (...) -> Duration
    """
    Create a Duration instance.
    """
    return Duration(
        days=days, seconds=seconds, microseconds=microseconds,
        milliseconds=milliseconds, minutes=minutes, hours=hours,
        weeks=weeks, years=years, months=months
    )


def period(start,          # type: DateTime
           end,            # type: DateTime
           absolute=False  # type: bool
           ):  # type: (...) -> Period
    """
    Create a Period instance.
    """
    return Period(start, end, absolute=absolute)
