import datetime as _datetime
from typing import Union

from .__version__ import __version__

# Types
from .datetime import DateTime
from .date import Date
from .time import Time
from .duration import Duration
from .period import Period

from .tz.timezone import Timezone
from .tz.timezone_info import TimezoneInfo

from .formatting import Formatter

# Helpers
from .helpers import (
    test, set_test_now, has_test_now, get_test_now,
    set_locale, get_locale, locale, format_diff,
    week_starts_at, week_ends_at
)

from .tz import (
    timezone, timezones,
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

PRE_TRANSITION = Timezone.PRE_TRANSITION
POST_TRANSITION = Timezone.POST_TRANSITION
TRANSITION_ERROR = Timezone.TRANSITION_ERROR

_TEST_NOW = None
_LOCALE = 'en'
_WEEK_STARTS_AT = MONDAY
_WEEK_ENDS_AT = SUNDAY

_formatter = Formatter()


def _safe_timezone(obj: Union[str, int, float, _datetime.tzinfo]) -> Timezone:
    """
    Creates a timezone instance
    from a string, Timezone, TimezoneInfo or integer offset.
    """
    if isinstance(obj, TimezoneInfo):
        return obj.tz

    if isinstance(obj, Timezone):
        return obj

    if obj is None or obj == 'local':
        return local_timezone()

    if isinstance(obj, (int, float)):
        obj = int(obj * 60 * 60)
    elif isinstance(obj, _datetime.tzinfo):
        # pytz
        if hasattr(obj, 'localize'):
            obj = timezone(obj.zone)
        else:
            offset = obj.utcoffset(None)

            if offset is None:
                offset = _datetime.timedelta(0)

            obj = int(offset.total_seconds())

    return timezone(obj)


# Public API
def datetime(year: int, month: int, day: int,
             hour: int = 0, minute: int = 0, second: int = 0,
             microsecond: int = 0,
             tz: Union[str, Timezone] = UTC) -> DateTime:
    """
    Creates a new DateTime instance from a specific date and time.
    """
    return create(year, month, day, hour, minute, second, microsecond, tz=tz)


def date(year: int, month: int, day: int):
    """
    Create a new Date instance.
    """
    return Date(year, month, day)


def time(hour: int = 0, minute: int = 0, second: int = 0, microsecond: int = 0):
    """
    Create a new Time instance.
    """
    return Time(hour, minute, second, microsecond)


def create(year: Union[int, None] = None,
           month: Union[int, None] = None,
           day: Union[int, None] = None,
           hour: int = 0,
           minute: int = 0,
           second: int = 0,
           microsecond: int = 0,
           tz: Union[str, Timezone] = UTC,
           *,
           dst_rule: str = Timezone.POST_TRANSITION) -> DateTime:
    """
    Creates a new DateTime instance from a specific date and time.

    If any of year, month or day are set to None their now() values will
    be used.
    """
    if tz is not None:
        tz = _safe_timezone(tz)

    if any([year is None, month is None, day is None]):
        if tz is not None:
            if has_test_now():
                now = get_test_now().in_tz(tz)
            else:
                now = _datetime.datetime.now(UTC)
                now = tz.convert(now)

            if year is None:
                year = now.year

            if month is None:
                month = now.month

            if day is None:
                day = now.day

    dt = _datetime.datetime(
        year, month, day,
        hour, minute, second, microsecond
    )
    if tz is not None:
        dt = tz.convert(dt, dst_rule=dst_rule)

    return DateTime(
        dt.year, dt.month, dt.day,
        dt.hour, dt.minute, dt.second, dt.microsecond,
        tzinfo=dt.tzinfo
    )


def instance(dt: _datetime.datetime,
             tz: Union[str, Timezone] = UTC) -> DateTime:
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
            and not isinstance(tz, (Timezone, TimezoneInfo))):
        # pytz
        if hasattr(tz, 'localize') and tz.zone:
            tz = tz.zone
        else:
            # We have no sure way to figure out
            # the timezone name, we fallback
            # on a fixed offset
            tz = tz.utcoffset(dt).total_seconds() / 3600

    return create(
        dt.year, dt.month, dt.day,
        dt.hour, dt.minute, dt.second, dt.microsecond,
        tz=tz
    )


def now(tz: Union[str, Timezone, None] = None) -> DateTime:
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


def today(tz: Union[str, Timezone] = 'local') -> DateTime:
    """
    Create a DateTime instance for today.
    """
    return now(tz).start_of('day')


def tomorrow(tz: Union[str, Timezone] = 'local') -> DateTime:
    """
    Create a DateTime instance for today.
    """
    return today(tz).add(days=1)


def yesterday(tz: Union[str, Timezone] = 'local') -> DateTime:
    """
    Create a DateTime instance for today.
    """
    return today(tz).subtract(days=1)


def from_format(string: str, fmt: str,
                *,
                tz: Union[str, Timezone] = UTC,
                locale: Union[str, None] = None) -> DateTime:
    """
    Creates a DateTime instance from a specific format.
    """
    parts = _formatter.parse(string, fmt, now(), locale=locale)
    if parts['tz'] is None:
        parts['tz'] = tz

    return create(**parts)


def from_timestamp(timestamp: Union[int, float],
                   tz: Union[str, Timezone] = UTC) -> DateTime:
    """
    Create a DateTime instance from a timestamp.
    """
    dt = _datetime.datetime.utcfromtimestamp(timestamp)

    dt = create(
        dt.year, dt.month, dt.day,
        dt.hour, dt.minute, dt.second, dt.microsecond
    )

    if tz is not UTC or tz != 'UTC':
        dt = dt.in_timezone(tz)

    return dt


def duration(days: float = 0, seconds: float = 0, microseconds: float = 0,
             milliseconds: float = 0, minutes: float = 0, hours: float = 0,
             weeks: float = 0, years: int = 0, months: int = 0) -> Duration:
    """
    Create a Duration instance.
    """
    return Duration(
        days=days, seconds=seconds, microseconds=microseconds,
        milliseconds=milliseconds, minutes=minutes, hours=hours,
        weeks=weeks, years=years, months=months
    )


def period(start: DateTime,
           end: DateTime,
           absolute: bool = False) -> Period:
    """
    Create a Period instance.
    """
    return Period(start, end, absolute=absolute)
