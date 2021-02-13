import datetime as _datetime

from typing import Optional
from typing import Union

from .__version__ import __version__
from .constants import DAYS_PER_WEEK
from .constants import FRIDAY
from .constants import HOURS_PER_DAY
from .constants import MINUTES_PER_HOUR
from .constants import MONDAY
from .constants import MONTHS_PER_YEAR
from .constants import SATURDAY
from .constants import SECONDS_PER_DAY
from .constants import SECONDS_PER_HOUR
from .constants import SECONDS_PER_MINUTE
from .constants import SUNDAY
from .constants import THURSDAY
from .constants import TUESDAY
from .constants import WEDNESDAY
from .constants import WEEKS_PER_YEAR
from .constants import YEARS_PER_CENTURY
from .constants import YEARS_PER_DECADE
from .date import Date
from .datetime import DateTime
from .duration import Duration
from .formatting import Formatter
from .helpers import format_diff
from .helpers import get_locale
from .helpers import get_test_now
from .helpers import has_test_now
from .helpers import locale
from .helpers import set_locale
from .helpers import set_test_now
from .helpers import test
from .helpers import week_ends_at
from .helpers import week_starts_at
from .parser import parse
from .period import Period
from .time import Time
from .tz import POST_TRANSITION
from .tz import PRE_TRANSITION
from .tz import TRANSITION_ERROR
from .tz import UTC
from .tz import local_timezone
from .tz import set_local_timezone
from .tz import test_local_timezone
from .tz import timezone
from .tz import timezones
from .tz.timezone import Timezone as _Timezone


_TEST_NOW = None  # type: Optional[DateTime]
_LOCALE = "en"
_WEEK_STARTS_AT = MONDAY
_WEEK_ENDS_AT = SUNDAY

_formatter = Formatter()


def _safe_timezone(
    obj: Optional[Union[str, float, _datetime.tzinfo, _Timezone]]
) -> _Timezone:
    """
    Creates a timezone instance
    from a string, Timezone, TimezoneInfo or integer offset.
    """
    if isinstance(obj, _Timezone):
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
    tz: Optional[Union[str, float, _Timezone]] = UTC,
    dst_rule: str = POST_TRANSITION,
) -> DateTime:
    """
    Creates a new DateTime instance from a specific date and time.
    """
    if tz is not None:
        tz = _safe_timezone(tz)

    dt = _datetime.datetime(year, month, day, hour, minute, second, microsecond)

    if tz is not None:
        dt = tz.convert(dt, dst_rule=dst_rule)

    return DateTime(
        dt.year,
        dt.month,
        dt.day,
        dt.hour,
        dt.minute,
        dt.second,
        dt.microsecond,
        tzinfo=dt.tzinfo,
        fold=dt.fold,
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
) -> DateTime:
    """
    Return a naive DateTime.
    """
    return DateTime(year, month, day, hour, minute, second, microsecond)


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


def instance(
    dt: _datetime.datetime, tz: Optional[Union[str, _Timezone]] = UTC
) -> DateTime:
    """
    Create a DateTime instance from a datetime one.
    """
    if not isinstance(dt, _datetime.datetime):
        raise ValueError("instance() only accepts datetime objects.")

    if isinstance(dt, DateTime):
        return dt

    tz = dt.tzinfo or tz

    # Checking for pytz/tzinfo
    if isinstance(tz, _datetime.tzinfo) and not isinstance(tz, _Timezone):
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


def now(tz: Optional[Union[str, _Timezone]] = None) -> DateTime:
    """
    Get a DateTime instance for the current date and time.
    """
    if has_test_now():
        test_instance = get_test_now()
        _tz = _safe_timezone(tz)

        if tz is not None and _tz != test_instance.timezone:
            test_instance = test_instance.in_tz(_tz)

        return test_instance

    if tz is None or tz == "local":
        dt = _datetime.datetime.now(local_timezone())
    elif tz is UTC or tz == "UTC":
        dt = _datetime.datetime.now(UTC)
    else:
        dt = _datetime.datetime.now(UTC)
        tz = _safe_timezone(tz)
        dt = tz.convert(dt)

    return DateTime(
        dt.year,
        dt.month,
        dt.day,
        dt.hour,
        dt.minute,
        dt.second,
        dt.microsecond,
        tzinfo=dt.tzinfo,
        fold=dt.fold,
    )


def today(tz: Union[str, _Timezone] = "local") -> DateTime:
    """
    Create a DateTime instance for today.
    """
    return now(tz).start_of("day")


def tomorrow(tz: Union[str, _Timezone] = "local") -> DateTime:
    """
    Create a DateTime instance for today.
    """
    return today(tz).add(days=1)


def yesterday(tz: Union[str, _Timezone] = "local") -> DateTime:
    """
    Create a DateTime instance for today.
    """
    return today(tz).subtract(days=1)


def from_format(
    string: str,
    fmt: str,
    tz: Union[str, _Timezone] = UTC,
    locale: Optional[str] = None,  # noqa
) -> DateTime:
    """
    Creates a DateTime instance from a specific format.
    """
    parts = _formatter.parse(string, fmt, now(), locale=locale)
    if parts["tz"] is None:
        parts["tz"] = tz

    return datetime(**parts)


def from_timestamp(
    timestamp: Union[int, float], tz: Union[str, _Timezone] = UTC
) -> DateTime:
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
