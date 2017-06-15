# -*- coding: utf-8 -*-

from __future__ import division

import calendar
import datetime

from .date import Date
from .time import Time
from .period import Period
from .exceptions import PendulumException
from .tz import Timezone, UTC, FixedTimezone, local_timezone
from .tz.timezone_info import TimezoneInfo
from .parsing import parse
from .helpers import add_duration
from .constants import (
    YEARS_PER_CENTURY, YEARS_PER_DECADE,
    MONTHS_PER_YEAR,
    MINUTES_PER_HOUR, SECONDS_PER_MINUTE,
    SECONDS_PER_DAY,
    SUNDAY, SATURDAY
)


class Pendulum(Date, datetime.datetime):

    # Formats
    ATOM = '%Y-%m-%dT%H:%M:%S%_z'
    COOKIE = '%A, %d-%b-%Y %H:%M:%S %Z'
    ISO8601 = '%Y-%m-%dT%H:%M:%S%_z'
    ISO8601_EXTENDED = '%Y-%m-%dT%H:%M:%S.%f%_z'
    RFC822 = '%a, %d %b %y %H:%M:%S %z'
    RFC850 = '%A, %d-%b-%y %H:%M:%S %Z'
    RFC1036 = '%a, %d %b %y %H:%M:%S %z'
    RFC1123 = '%a, %d %b %Y %H:%M:%S %z'
    RFC2822 = '%a, %d %b %Y %H:%M:%S %z'
    RFC3339 = '%Y-%m-%dT%H:%M:%S%_z'
    RFC3339_EXTENDED = '%Y-%m-%dT%H:%M:%S.%f%_z'
    RSS = '%a, %d %b %Y %H:%M:%S %z'
    W3C = '%Y-%m-%dT%H:%M:%S%_z'

    _EPOCH = datetime.datetime(1970, 1, 1, tzinfo=UTC)

    _TRANSITION_RULE = Timezone.POST_TRANSITION

    _MODIFIERS_VALID_UNITS = [
        'second', 'minute', 'hour',
        'day', 'week', 'month', 'year',
        'decade', 'century'
    ]

    @classmethod
    def _safe_create_datetime_zone(cls, obj):
        """
        Creates a timezone from a string, Timezone, TimezoneInfo or integer offset.

        :param obj: str or Timezone or TimezoneInfo or int or None

        :rtype: Timezone
        """
        if isinstance(obj, TimezoneInfo):
            return obj.tz

        if obj is None or obj == 'local':
            return cls._local_timezone()

        if isinstance(obj, (int, float)):
            timezone_offset = obj * 60 * 60

            return FixedTimezone.load(timezone_offset)
        elif isinstance(obj, datetime.tzinfo) and not isinstance(obj, Timezone):
            # pytz
            if hasattr(obj, 'localize'):
                return cls._timezone(obj.zone)

            return FixedTimezone.load(obj.utcoffset(None).total_seconds())

        return cls._timezone(obj)

    @classmethod
    def _local_timezone(cls):
        """
        Returns the local timezone using tzlocal.get_localzone
        or the TZ environment variable.

        :rtype: Timezone
        """
        return local_timezone()

    @classmethod
    def _timezone(cls, zone):
        """
        Returns a timezone given its name.

        :param zone: The name of the timezone.
        :type zone: str

        :rtype: Timezone
        """
        if isinstance(zone, Timezone):
            return zone

        return Timezone.load(zone)

    def __new__(cls, year, month, day,
                hour=0, minute=0, second=0, microsecond=0,
                tzinfo=None, fold=None):
        """
        Constructor.

        This will just create a dummy datetime. The heavy lifting will be done
        in __init__().

        :type year: int or str
        """
        obj = super(Pendulum, cls).__new__(cls, year, month, day, hour, minute, second, microsecond, None)

        return obj

    def __init__(self, year, month, day,
                 hour=0, minute=0, second=0, microsecond=0,
                 tzinfo=UTC, fold=None):
        # If a TimezoneInfo is passed we do not convert
        if isinstance(tzinfo, TimezoneInfo):
            self._tz = tzinfo.tz

            self._year = year
            self._month = month
            self._day = day
            self._hour = hour
            self._minute = minute
            self._second = second
            self._microsecond = microsecond
            self._tzinfo = tzinfo

            if fold is None:
                # Converting rule to fold value
                if self._TRANSITION_RULE == Timezone.POST_TRANSITION:
                    fold = 1
                else:
                    fold = 0

            self._fold = fold

            dt = datetime.datetime(
                year, month, day,
                hour, minute, second, microsecond,
                tzinfo
            )
        else:
            self._tz = self._safe_create_datetime_zone(tzinfo)

            # Support for explicit fold attribute
            if fold is None:
                transition_rule = self._TRANSITION_RULE

                # Converting rule to fold value
                if self._TRANSITION_RULE == Timezone.POST_TRANSITION:
                    fold = 1
                else:
                    fold = 0
            elif fold == 1:
                transition_rule = Timezone.POST_TRANSITION
            else:
                transition_rule = Timezone.PRE_TRANSITION

            dt = self._tz.convert(datetime.datetime(
                year, month, day,
                hour, minute, second, microsecond
            ), dst_rule=transition_rule)

            self._year = dt.year
            self._month = dt.month
            self._day = dt.day
            self._hour = dt.hour
            self._minute = dt.minute
            self._second = dt.second
            self._microsecond = dt.microsecond
            self._tzinfo = dt.tzinfo
            self._fold = fold

        self._timestamp = None
        self._int_timestamp = None
        self._datetime = dt

    @classmethod
    def instance(cls, dt, tz=UTC):
        """
        Create a Pendulum instance from a datetime one.

        :param dt: A datetime instance
        :type dt: datetime.datetime

        :param tz: The timezone
        :type tz: Timezone or TimeZoneInfo or str or None

        :rtype: Pendulum
        """
        tz = dt.tzinfo or tz

        # Checking for pytz/tzinfo
        if isinstance(tz, datetime.tzinfo) and not isinstance(tz, (Timezone, TimezoneInfo)):
            # pytz
            if hasattr(tz, 'localize'):
                tz = tz.zone
            else:
                # We have no sure way to figure out
                # the timezone name, we fallback
                # on a fixed offset
                tz = dt.utcoffset().total_seconds() / 3600

        return cls(
            dt.year, dt.month, dt.day,
            dt.hour, dt.minute, dt.second, dt.microsecond,
            tzinfo=tz
        )

    @classmethod
    def parse(cls, time=None, tz=UTC, **options):
        """
        Create a Pendulum instance from a string.

        :param time: The time string
        :type time: str

        :param tz: The timezone
        :type tz: Timezone or TimezoneInfo or str or None

        :rtype: Pendulum
        """
        if time is None:
            return cls.now(tz)

        if time == 'now':
            return cls.now(None)

        parsed = parse(time, **options)

        if parsed['offset'] is None:
            tz = tz
        else:
            tz = parsed['offset'] / 3600

        return cls(
            parsed['year'], parsed['month'], parsed['day'],
            parsed['hour'], parsed['minute'], parsed['second'],
            parsed['subsecond'],
            tzinfo=tz
        )

    @classmethod
    def now(cls, tz=None):
        """
        Get a Pendulum instance for the current date and time.

        :param tz: The timezone
        :type tz: Timezone or TimezoneInfo or str or int or None

        :rtype: Pendulum
        """
        # If the class has a test now set and we are trying to create a now()
        # instance then override as required
        if cls.has_test_now():
            test_instance = cls.get_test_now()

            if tz is not None and tz != test_instance.timezone:
                test_instance = test_instance.in_timezone(tz)

            return test_instance

        if tz is None or tz == 'local':
            dt = datetime.datetime.now()
        elif tz is UTC or tz == 'UTC':
            dt = datetime.datetime.utcnow().replace(tzinfo=UTC)
        else:
            dt = datetime.datetime.utcnow().replace(tzinfo=UTC)
            tz = cls._safe_create_datetime_zone(tz)
            dt = tz.convert(dt)

        return cls.instance(dt, tz)

    @classmethod
    def utcnow(cls):
        """
        Get a Pendulum instance for the current date and time in UTC.

        :param tz: The timezone
        :type tz: Timezone or TimezoneInfo or str or None

        :rtype: Pendulum
        """
        return cls.now(UTC)

    @classmethod
    def today(cls, tz=None):
        """
        Create a Pendulum instance for today.

        :param tz: The timezone
        :type tz: Timezone or TimezoneInfo or str or None

        :rtype: Pendulum
        """
        return cls.now(tz).start_of('day')

    @classmethod
    def tomorrow(cls, tz=None):
        """
        Create a Pendulum instance for tomorrow.

        :param tz: The timezone
        :type tz: Timezone or TimezoneInfo or str or None

        :rtype: Pendulum
        """
        return cls.today(tz).add(days=1)

    @classmethod
    def yesterday(cls, tz=None):
        """
        Create a Pendulum instance for yesterday.

        :param tz: The timezone
        :type tz: Timezone or TimezoneInfo or str or None

        :rtype: Pendulum
        """
        return cls.today(tz).subtract(days=1)

    @classmethod
    def create(cls, year=None, month=None, day=None,
               hour=0, minute=0, second=0, microsecond=0,
               tz=UTC):
        """
        Create a new Pendulum instance from a specific date and time.

        If any of year, month or day are set to None their now() values will
        be used.

        :type year: int
        :type month: int
        :type day: int
        :type hour: int
        :type minute: int
        :type second: int
        :type microsecond: int
        :type tz: tzinfo or str or int or None

        :rtype: Pendulum
        """
        tz = cls._safe_create_datetime_zone(tz)

        if any([year is None, month is None, day is None]):
            if cls.has_test_now():
                now = cls.get_test_now().in_tz(tz)
            else:
                now = datetime.datetime.utcnow().replace(tzinfo=UTC)
                now = tz.convert(now)

            if year is None:
                year = now.year

            if month is None:
                month = now.month

            if day is None:
                day = now.day

        dt = datetime.datetime(
            year, month, day, hour, minute, second, microsecond
        )

        return cls.instance(dt, tz)

    @classmethod
    def create_from_format(cls, time, fmt, tz=UTC):
        """
        Create a Pendulum instance from a specific format.

        :param fmt: The format
        :type fmt: str

        :param time: The time string
        :type time: str

        :param tz: The timezone
        :type tz: tzinfo or str or int or None

        :rtype: Pendulum
        """
        dt = datetime.datetime.strptime(time, fmt)

        return cls.instance(dt, tz)

    @classmethod
    def create_from_timestamp(cls, timestamp, tz=UTC):
        """
        Create a Pendulum instance from a timestamp.

        :param timestamp: The timestamp
        :type timestamp: int or float

        :param tz: The timezone
        :type tz: Timezone or TimezoneInfo or str or int or None

        :rtype: Pendulum
        """
        dt = datetime.datetime.utcfromtimestamp(timestamp).replace(tzinfo=UTC)
        instance = cls(
            dt.year, dt.month, dt.day,
            dt.hour, dt.minute, dt.second, dt.microsecond,
            dt.tzinfo
        )

        if tz is not UTC and tz != 'UTC':
            instance = instance.in_tz(tz)

        return instance

    @classmethod
    def strptime(cls, time, fmt):
        return cls.create_from_format(time, fmt)

    def copy(self):
        """
        Get a copy of the instance.

        :rtype: Pendulum
        """
        return self.instance(self._datetime)

    # Getters/Setters

    def hour_(self, hour):
        return self._setter(hour=hour)

    def minute_(self, minute):
        return self._setter(minute=minute)

    def second_(self, second):
        return self._setter(second=second)

    def microsecond_(self, microsecond):
        return self._setter(microsecond=microsecond)

    def _setter(self, **kwargs):
        kwargs['tzinfo'] = True

        return self._tz.convert(self.replace(**kwargs))

    def timezone_(self, tz):
        return self.__class__(
            self.year, self.month, self.day,
            self.hour, self.minute, self.second, self.microsecond,
            tz
        )

    def tz_(self, tz):
        return self.timezone_(tz)

    def timestamp_(self, timestamp, tz=UTC):
        return self.create_from_timestamp(timestamp, tz)

    @property
    def year(self):
        return self._year

    @property
    def month(self):
        return self._month

    @property
    def day(self):
        return self._day

    @property
    def hour(self):
        return self._hour

    @property
    def minute(self):
        return self._minute

    @property
    def second(self):
        return self._second

    @property
    def microsecond(self):
        return self._microsecond

    @property
    def tzinfo(self):
        return self._tzinfo

    @property
    def fold(self):
        return self._fold

    def timestamp(self):
        if self._timestamp is None:
            delta = self._datetime - self._EPOCH

            self._timestamp = delta.total_seconds()

        return self._timestamp

    @property
    def float_timestamp(self):
        return self.timestamp()

    @property
    def int_timestamp(self):
        if self._int_timestamp is None:
            delta = self._datetime - self._EPOCH

            self._int_timestamp = delta.days * SECONDS_PER_DAY + delta.seconds

        return self._int_timestamp

    @property
    def offset(self):
        return self.get_offset()

    @property
    def offset_hours(self):
        return (self.get_offset()
                / SECONDS_PER_MINUTE
                / MINUTES_PER_HOUR)

    @property
    def local(self):
        return self.offset == self.in_timezone(self._local_timezone()).offset

    @property
    def utc(self):
        return self.offset == 0

    @property
    def is_dst(self):
        return self.tzinfo.is_dst

    @property
    def timezone(self):
        return self.get_timezone()

    @property
    def tz(self):
        return self.get_timezone()

    @property
    def timezone_name(self):
        return self.timezone.name

    @property
    def age(self):
        return self.date().diff(self.now(self._tz).date()).in_years()

    def get_timezone(self):
        return self._tz

    def get_offset(self):
        return int(self._tzinfo.offset)

    def date(self):
        return Date.instance(self._datetime.date())

    def time(self):
        return Time(self.hour, self.minute, self.second, self.microsecond)

    def on(self, year, month, day):
        """
        Returns a new instance with the current date set to a different date.

        :param year: The year
        :type year: int

        :param month: The month
        :type month: int

        :param day: The day
        :type day: int

        :rtype: Pendulum
        """
        return self.replace(
            year=int(year), month=int(month), day=int(day)
        )

    def at(self, hour, minute, second, microsecond=0):
        """
        Returns a new instance with the current time to a different time.

        :param hour: The hour
        :type hour: int

        :param minute: The minute
        :type minute: int

        :param second: The second
        :type second: int

        :param microsecond: The microsecond
        :type microsecond: int

        :rtype: Pendulum
        """
        return self.replace(
            hour=hour, minute=minute, second=second,
            microsecond=microsecond
        )

    def with_date_time(self, year, month, day, hour, minute, second, microsecond=0):
        """
        Return a new instance with the date and time set to the given values.

        :type year: int
        :type month: int
        :type day: int
        :type hour: int
        :type minute: int
        :type second: int

        :rtype: Pendulum
        """
        return self.replace(
            year=year, month=month, day=day,
            hour=hour, minute=minute, second=second,
            microsecond=microsecond
        )

    def with_time_from_string(self, time):
        """
        Returns a new instance with the time set by time string.

        :param time: The time string
        :type time: str

        :rtype: Pendulum
        """
        time = time.split(':')

        hour = int(time[0])
        minute = int(time[1]) if len(time) > 1 else 0
        second = int(time[2]) if len(time) > 2 else 0

        return self.at(hour, minute, second)

    def in_timezone(self, tz):
        """
        Set the instance's timezone from a string or object.

        :param value: The timezone
        :type value: Timezone or TimezoneInfo or str or None

        :rtype: Pendulum
        """
        tz = self._safe_create_datetime_zone(tz)

        return tz.convert(self)

    def in_tz(self, tz):
        """
        Set the instance's timezone from a string or object.

        :param value: The timezone
        :type value: Timezone or TimezoneInfo or str or int or None

        :rtype: Pendulum
        """
        return self.in_timezone(tz)

    def with_timestamp(self, timestamp):
        """
        Set the date and time based on a Unix timestamp.

        :param timestamp: The timestamp
        :type timestamp: int or float
        :rtype: Pendulum
        """
        dt = datetime.datetime.fromtimestamp(timestamp, UTC).astimezone(self._tz)

        return self.instance(dt)

    # Normalization Rule
    @classmethod
    def set_transition_rule(cls, rule):
        if rule not in [Timezone.PRE_TRANSITION,
                        Timezone.POST_TRANSITION,
                        Timezone.TRANSITION_ERROR]:
            raise ValueError('Invalid transition rule: {}'.format(rule))

        cls._TRANSITION_RULE = rule

    @classmethod
    def get_transition_rule(cls):
        return cls._TRANSITION_RULE

    # STRING FORMATTING

    def to_time_string(self):
        """
        Format the instance as time.

        :rtype: str
        """
        return self.format('%H:%M:%S', formatter='classic')

    def to_datetime_string(self):
        """
        Format the instance as date and time.

        :rtype: str
        """
        return self.format('%Y-%m-%d %H:%M:%S', formatter='classic')

    def to_day_datetime_string(self):
        """
        Format the instance as day, date and time.

        :rtype: str
        """
        return self.format('ddd, MMM D, YYYY h:mm A', formatter='alternative')

    def to_atom_string(self):
        """
        Format the instance as ATOM.

        :rtype: str
        """
        return self.format(self.ATOM, formatter='classic')

    def to_cookie_string(self):
        """
        Format the instance as COOKIE.

        :rtype: str
        """
        return self.format(self.COOKIE, formatter='classic')

    def to_iso8601_string(self, extended=False):
        """
        Format the instance as ISO8601.

        :rtype: str
        """
        fmt = self.ISO8601
        if extended:
            fmt = self.ISO8601_EXTENDED

        return self.format(fmt, formatter='classic')

    def to_rfc822_string(self):
        """
        Format the instance as RFC822.

        :rtype: str
        """
        return self.format(self.RFC822, formatter='classic')

    def to_rfc850_string(self):
        """
        Format the instance as RFC850.

        :rtype: str
        """
        return self.format(self.RFC850, formatter='classic')

    def to_rfc1036_string(self):
        """
        Format the instance as RFC1036.

        :rtype: str
        """
        return self.format(self.RFC1036, formatter='classic')

    def to_rfc1123_string(self):
        """
        Format the instance as RFC1123.

        :rtype: str
        """
        return self.format(self.RFC1123, formatter='classic')

    def to_rfc2822_string(self):
        """
        Format the instance as RFC2822.

        :rtype: str
        """
        return self.format(self.RFC2822, formatter='classic')

    def to_rfc3339_string(self, extended=False):
        """
        Format the instance as RFC3339.

        :rtype: str
        """
        fmt = self.RFC3339
        if extended:
            fmt = self.RFC3339_EXTENDED

        return self.format(fmt, formatter='classic')

    def to_rss_string(self):
        """
        Format the instance as RSS.

        :rtype: str
        """
        return self.format(self.RSS, formatter='classic')

    def to_w3c_string(self):
        """
        Format the instance as W3C.

        :rtype: str
        """
        return self.format(self.W3C, formatter='classic')

    # Comparisons
    def __eq__(self, other):
        try:
            return self._datetime == self._get_datetime(other)
        except ValueError:
            return NotImplemented

    def __ne__(self, other):
        try:
            return self._datetime != self._get_datetime(other)
        except ValueError:
            return NotImplemented

    def __gt__(self, other):
        try:
            return self._datetime > self._get_datetime(other)
        except ValueError:
            return NotImplemented

    def __ge__(self, other):
        try:
            return self._datetime >= self._get_datetime(other)
        except ValueError:
            return NotImplemented

    def __lt__(self, other):
        try:
            return self._datetime < self._get_datetime(other)
        except ValueError:
            return NotImplemented

    def __le__(self, other):
        try:
            return self._datetime <= self._get_datetime(other)
        except ValueError:
            return NotImplemented

    def between(self, dt1, dt2, equal=True):
        """
        Determines if the instance is between two others.

        :type dt1: Pendulum or datetime or str or int
        :type dt2: Pendulum or datetime or str or int

        :param equal: Indicates if a > and < comparison shoud be used or <= and >=

        :rtype: bool
        """
        if dt1 > dt2:
            dt1, dt2 = dt2, dt1

        if equal:
            return self >= dt1 and self <= dt2

        return self > dt1 and self < dt2

    def closest(self, dt1, dt2):
        """
        Get the closest date from the instance.

        :type dt1: Pendulum or datetime
        :type dt2: Pendulum or datetime

        :rtype: Pendulum
        """
        dt1 = self._get_datetime(dt1, True)
        dt2 = self._get_datetime(dt2, True)

        if self.diff(dt1).in_seconds() < self.diff(dt2).in_seconds():
            return dt1

        return dt2

    def farthest(self, dt1, dt2):
        """
        Get the farthest date from the instance.

        :type dt1: Pendulum or datetime
        :type dt2: Pendulum or datetime

        :rtype: Pendulum
        """
        dt1 = self._get_datetime(dt1, True)
        dt2 = self._get_datetime(dt2, True)

        if self.diff(dt1).in_seconds() > self.diff(dt2).in_seconds():
            return dt1

        return dt2

    def min_(self, dt=None):
        """
        Get the minimum instance between a given instance (default utcnow)
        and the current instance.

        :type dt: Pendulum or datetime or str or int

        :rtype: Pendulum
        """
        if dt is None:
            dt = Pendulum.now(self.timezone)

        if self < dt:
            return self

        return self._get_datetime(dt, True)

    def minimum(self, dt=None):
        """
        Get the minimum instance between a given instance (default now)
        and the current instance.

        :type dt: Pendulum or datetime or str or int

        :rtype: Pendulum
        """
        return self.min_(dt)

    def max_(self, dt=None):
        """
        Get the maximum instance between a given instance (default now)
        and the current instance.

        :type dt: Pendulum or datetime or str or int

        :rtype: Pendulum
        """
        if dt is None:
            dt = Pendulum.now(self.timezone)

        if self > dt:
            return self

        return self._get_datetime(dt, True)

    def maximum(self, dt=None):
        """
        Get the maximum instance between a given instance (default utcnow)
        and the current instance.

        :type dt: Pendulum or datetime or str or int

        :rtype: Pendulum
        """
        return self.max_(dt)

    def is_yesterday(self):
        """
        Determines if the instance is yesterday.

        :rtype: bool
        """
        return self.to_date_string() == self.yesterday(self._tz).to_date_string()

    def is_today(self):
        """
        Determines if the instance is today.

        :rtype: bool
        """
        return self.to_date_string() == self.now(self._tz).to_date_string()

    def is_tomorrow(self):
        """
        Determines if the instance is tomorrow.

        :rtype: bool
        """
        return self.to_date_string() == self.tomorrow(self._tz).to_date_string()

    def is_future(self):
        """
        Determines if the instance is in the future, ie. greater than now.

        :rtype: bool
        """
        return self > self.now(self.timezone)

    def is_past(self):
        """
        Determines if the instance is in the past, ie. less than now.

        :rtype: bool
        """
        return self < self.now(self.timezone)

    def is_long_year(self):
        """
        Determines if the instance is a long year

        See link `https://en.wikipedia.org/wiki/ISO_8601#Week_dates`_

        :rtype: bool
        """
        return Pendulum.create(self.year, 12, 28, 0, 0, 0, tz=self._tz).isocalendar()[1] == 53

    def is_same_day(self, dt):
        """
        Checks if the passed in date is the same day as the instance current day.

        :type dt: Pendulum or datetime or str or int

        :rtype: bool
        """
        dt = self._get_datetime(dt, True)

        return self.to_date_string() == dt.to_date_string()

    def is_birthday(self, dt=None):
        """
        Check if its the birthday. Compares the date/month values of the two dates.

        :rtype: bool
        """
        if dt is None:
            dt = Pendulum.now(self._tz)

        instance = self._get_datetime(dt, True)

        return (self.month, self.day) == (instance.month, instance.day)

    # ADDITIONS AND SUBSTRACTIONS

    def add(self, years=0, months=0, weeks=0, days=0,
            hours=0, minutes=0, seconds=0, microseconds=0):
        """
        Add duration to the instance.

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

        :rtype: Pendulum
        """
        dt = add_duration(
            self._datetime,
            years=years, months=months, weeks=weeks, days=days,
            hours=hours, minutes=minutes, seconds=seconds,
            microseconds=microseconds
        )

        if any([years, months, weeks, days]):
            # If we specified any of years, months, weeks or days
            # we will not apply the transition (if any)
            return self.__class__(
                dt.year, dt.month, dt.day,
                dt.hour, dt.minute, dt.second, dt.microsecond,
                tzinfo=self._tz,
                fold=1
            )

        # Else, we need to apply the transition properly (if any)
        dt = self._tz.convert(dt)

        return self.instance(dt)

    def subtract(self, years=0, months=0, weeks=0, days=0,
                 hours=0, minutes=0, seconds=0, microseconds=0):
        """
        Remove duration from the instance.

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

        :rtype: Pendulum
        """
        return self.add(
            years=-years, months=-months, weeks=-weeks, days=-days,
            hours=-hours, minutes=-minutes, seconds=-seconds,
            microseconds=-microseconds
        )

    def add_timedelta(self, delta):
        """
        Add timedelta duration to the instance.

        :param delta: The timedelta instance
        :type delta: datetime.timedelta

        :rtype: Pendulum
        """
        if isinstance(delta, Period):
            return self.add(
                years=delta.years, months=delta.months,
                weeks=delta.weeks, days=delta.remaining_days,
                hours=delta.hours, minutes=delta.minutes,
                seconds=delta.remaining_seconds, microseconds=delta.microseconds
            )

        return self.add(days=delta.days, seconds=delta.seconds,
                        microseconds=delta.microseconds)

    def subtract_timedelta(self, delta):
        """
        Remove timedelta duration from the instance.

        :param delta: The timedelta instance
        :type delta: datetime.timedelta

        :rtype: Pendulum
        """
        if isinstance(delta, Period):
            return self.subtract(
                years=delta.years, months=delta.months,
                weeks=delta.weeks, days=delta.remaining_days,
                hours=delta.hours, minutes=delta.minutes,
                seconds=delta.remaining_seconds, microseconds=delta.microseconds
            )

        return self.subtract(days=delta.days, seconds=delta.seconds,
                             microseconds=delta.microseconds)

    # DIFFERENCES

    def seconds_since_midnight(self):
        """
        The number of seconds since midnight.

        :rtype: int
        """
        return self.diff(self.start_of('day')).in_seconds()

    def seconds_until_end_of_day(self):
        """
        The number of seconds until 23:59:59.

        :rtype: int
        """
        return self.diff(self.end_of('day')).in_seconds()

    def diff(self, dt=None, abs=True):
        """
        Returns the difference between two Pendulum objects represented as a Interval.

        :type dt: Pendulum or None

        :param abs: Whether to return an absolute interval or not
        :type abs: bool

        :rtype: Period
        """
        if dt is None:
            dt = self.now(self._tz)

        return Period(self, self._get_datetime(dt, pendulum=True), absolute=abs)

    # Modifiers
    def start_of(self, unit):
        """
        Returns a copy of the instance with the time reset
        with the following rules:

        * second: microsecond set to 0
        * minute: second and microsecond set to 0
        * hour: minute, second and microsecond set to 0
        * day: time to 00:00:00
        * week: date to first day of the week and time to 00:00:00
        * month: date to first day of the month and time to 00:00:00
        * year: date to first day of the year and time to 00:00:00
        * decade: date to first day of the decade and time to 00:00:00
        * century: date to first day of century and time to 00:00:00

        :param unit: The unit to reset to
        :type unit: str

        :rtype: Pendulum
        """
        if unit not in self._MODIFIERS_VALID_UNITS:
            raise ValueError('Invalid unit "{}" for start_of()'.format(unit))

        return getattr(self, '_start_of_{}'.format(unit))()

    def end_of(self, unit):
        """
        Returns a copy of the instance with the time reset
        with the following rules:

        * second: microsecond set to 999999
        * minute: second set to 59 and microsecond set to 999999
        * hour: minute and second set to 59 and microsecond set to 999999
        * day: time to 23:59:59.999999
        * week: date to last day of the week and time to 23:59:59.999999
        * month: date to last day of the month and time to 23:59:59.999999
        * year: date to last day of the year and time to 23:59:59.999999
        * decade: date to last day of the decade and time to 23:59:59.999999
        * century: date to last day of century and time to 23:59:59.999999

        :param unit: The unit to reset to
        :type unit: str

        :rtype: Pendulum
        """
        if unit not in self._MODIFIERS_VALID_UNITS:
            raise ValueError('Invalid unit "%s" for end_of()' % unit)

        return getattr(self, '_end_of_%s' % unit)()

    def _start_of_second(self):
        """
        Reset microseconds to 0.

        :rtype: Pendulum
        """
        return self.microsecond_(0)

    def _end_of_second(self):
        """
        Set microseconds to 999999.

        :rtype: Pendulum
        """
        return self.microsecond_(999999)

    def _start_of_minute(self):
        """
        Reset seconds and microseconds to 0.

        :rtype: Pendulum
        """
        return self.replace(second=0, microsecond=0)

    def _end_of_minute(self):
        """
        Set seconds to 59 and microseconds to 999999.

        :rtype: Pendulum
        """
        return self.replace(second=59, microsecond=999999)

    def _start_of_hour(self):
        """
        Reset minutes, seconds and microseconds to 0.

        :rtype: Pendulum
        """
        return self.replace(minute=0, second=0, microsecond=0)

    def _end_of_hour(self):
        """
        Set minutes and seconds to 59 and microseconds to 999999.

        :rtype: Pendulum
        """
        return self.replace(minute=59, second=59, microsecond=999999)

    def _start_of_day(self):
        """
        Reset the time to 00:00:00

        :rtype: Pendulum
        """
        return self.at(0, 0, 0)

    def _end_of_day(self):
        """
        Reset the time to 23:59:59.999999

        :rtype: Pendulum
        """
        return self.at(23, 59, 59, 999999)

    def _start_of_month(self):
        """
        Reset the date to the first day of the month and the time to 00:00:00.

        :rtype: Pendulum
        """
        return self.with_date_time(self.year, self.month, 1, 0, 0, 0)

    def _end_of_month(self):
        """
        Reset the date to the last day of the month
        and the time to 23:59:59.999999.

        :rtype: Pendulum
        """
        return self.with_date_time(
            self.year, self.month, self.days_in_month, 23, 59, 59, 999999
        )

    def _start_of_year(self):
        """
        Reset the date to the first day of the year and the time to 00:00:00.

        :rtype: Pendulum
        """
        return self.with_date_time(self.year, 1, 1, 0, 0, 0)

    def _end_of_year(self):
        """
        Reset the date to the last day of the year
        and the time to 23:59:59.999999

        :rtype: Pendulum
        """
        return self.with_date_time(
            self.year, 12, 31, 23, 59, 59, 999999
        )

    def _start_of_decade(self):
        """
        Reset the date to the first day of the decade
        and the time to 00:00:00.

        :rtype: Pendulum
        """
        year = self.year - self.year % YEARS_PER_DECADE
        return self.with_date_time(year, 1, 1, 0, 0, 0)

    def _end_of_decade(self):
        """
        Reset the date to the last day of the decade
        and the time to 23:59:59.999999.

        :rtype: Pendulum
        """
        year = self.year - self.year % YEARS_PER_DECADE + YEARS_PER_DECADE - 1

        return self.with_date_time(
            year, 12, 31, 23, 59, 59, 999999
        )

    def _start_of_century(self):
        """
        Reset the date to the first day of the century
        and the time to 00:00:00.

        :rtype: Pendulum
        """
        year = self.year - 1 - (self.year - 1) % YEARS_PER_CENTURY + 1

        return self.with_date_time(year, 1, 1, 0, 0, 0)

    def _end_of_century(self):
        """
        Reset the date to the last day of the century
        and the time to 23:59:59.999999.

        :rtype: Pendulum
        """
        year = self.year - 1 - (self.year - 1) % YEARS_PER_CENTURY + YEARS_PER_CENTURY

        return self.with_date_time(
            year, 12, 31, 23, 59, 59, 999999
        )

    def _start_of_week(self):
        """
        Reset the date to the first day of the week
        and the time to 00:00:00.

        :rtype: Pendulum
        """
        dt = self

        if self.day_of_week != self._week_starts_at:
            dt = self.previous(self._week_starts_at)

        return dt.start_of('day')

    def _end_of_week(self):
        """
        Reset the date to the last day of the week
        and the time to 23:59:59.

        :rtype: Pendulum
        """
        dt = self

        if self.day_of_week != self._week_ends_at:
            dt = self.next(self._week_ends_at)

        return dt.end_of('day')

    def next(self, day_of_week=None, keep_time=False):
        """
        Modify to the next occurrence of a given day of the week.
        If no day_of_week is provided, modify to the next occurrence
        of the current day of the week.  Use the supplied consts
        to indicate the desired day_of_week, ex. Pendulum.MONDAY.

        :param day_of_week: The next day of week to reset to.
        :type day_of_week: int or None

        :param keep_time: Whether to keep the time information or not.
        :type keep_time: bool

        :rtype: Pendulum
        """
        if day_of_week is None:
            day_of_week = self.day_of_week

        if day_of_week < SUNDAY or day_of_week > SATURDAY:
            raise ValueError('Invalid day of week')

        if keep_time:
            dt = self
        else:
            dt = self.start_of('day')

        dt = dt.add(days=1)
        while dt.day_of_week != day_of_week:
            dt = dt.add(days=1)

        return dt

    def previous(self, day_of_week=None, keep_time=False):
        """
        Modify to the previous occurrence of a given day of the week.
        If no day_of_week is provided, modify to the previous occurrence
        of the current day of the week.  Use the supplied consts
        to indicate the desired day_of_week, ex. Pendulum.MONDAY.

        :param day_of_week: The previous day of week to reset to.
        :type day_of_week: int or None

        :param keep_time: Whether to keep the time information or not.
        :type keep_time: bool

        :rtype: Pendulum
        """
        if day_of_week is None:
            day_of_week = self.day_of_week

        if day_of_week < SUNDAY or day_of_week > SATURDAY:
            raise ValueError('Invalid day of week')

        if keep_time:
            dt = self
        else:
            dt = self.start_of('day')

        dt = dt.subtract(days=1)
        while dt.day_of_week != day_of_week:
            dt = dt.subtract(days=1)

        return dt

    def first_of(self, unit, day_of_week=None):
        """
        Returns an instance set to the first occurrence
        of a given day of the week in the current unit.
        If no day_of_week is provided, modify to the first day of the unit.
        Use the supplied consts to indicate the desired day_of_week, ex. Pendulum.MONDAY.

        Supported units are month, quarter and year.

        :param unit: The unit to use
        :type unit: str

        :type day_of_week: int or None

        :rtype: Pendulum
        """
        if unit not in ['month', 'quarter', 'year']:
            raise ValueError('Invalid unit "{}" for first_of()'.format(unit))

        return getattr(self, '_first_of_{}'.format(unit))(day_of_week)

    def last_of(self, unit, day_of_week=None):
        """
        Returns an instance set to the last occurrence
        of a given day of the week in the current unit.
        If no day_of_week is provided, modify to the last day of the unit.
        Use the supplied consts to indicate the desired day_of_week, ex. Pendulum.MONDAY.

        Supported units are month, quarter and year.

        :param unit: The unit to use
        :type unit: str

        :type day_of_week: int or None

        :rtype: Pendulum
        """
        if unit not in ['month', 'quarter', 'year']:
            raise ValueError('Invalid unit "{}" for first_of()'.format(unit))

        return getattr(self, '_last_of_{}'.format(unit))(day_of_week)

    def nth_of(self, unit, nth, day_of_week):
        """
        Returns a new instance set to the given occurrence
        of a given day of the week in the current unit.
        If the calculated occurrence is outside the scope of the current unit,
        then raise an error. Use the supplied consts
        to indicate the desired day_of_week, ex. Pendulum.MONDAY.

        Supported units are month, quarter and year.

        :param unit: The unit to use
        :type unit: str

        :type nth: int

        :type day_of_week: int or None

        :rtype: Pendulum
        """
        if unit not in ['month', 'quarter', 'year']:
            raise ValueError('Invalid unit "{}" for first_of()'.format(unit))

        dt = getattr(self, '_nth_of_{}'.format(unit))(nth, day_of_week)
        if dt is False:
            raise PendulumException('Unable to find occurence {} of {} in {}'.format(
                                     nth, self._days[day_of_week], unit))

        return dt

    def _first_of_month(self, day_of_week):
        """
        Modify to the first occurrence of a given day of the week
        in the current month. If no day_of_week is provided,
        modify to the first day of the month. Use the supplied consts
        to indicate the desired day_of_week, ex. Pendulum.MONDAY.

        :type day_of_week: int

        :rtype: Pendulum
        """
        dt = self.start_of('day')

        if day_of_week is None:
            return dt.day_(1)

        month = calendar.monthcalendar(dt.year, dt.month)

        calendar_day = (day_of_week - 1) % 7

        if month[0][calendar_day] > 0:
            day_of_month = month[0][calendar_day]
        else:
            day_of_month = month[1][calendar_day]

        return dt.day_(day_of_month)

    def _last_of_month(self, day_of_week=None):
        """
        Modify to the last occurrence of a given day of the week
        in the current month. If no day_of_week is provided,
        modify to the last day of the month. Use the supplied consts
        to indicate the desired day_of_week, ex. Pendulum.MONDAY.

        :type day_of_week: int or None

        :rtype: Pendulum
        """
        dt = self.start_of('day')

        if day_of_week is None:
            return dt.day_(self.days_in_month)

        month = calendar.monthcalendar(dt.year, dt.month)

        calendar_day = (day_of_week - 1) % 7

        if month[-1][calendar_day] > 0:
            day_of_month = month[-1][calendar_day]
        else:
            day_of_month = month[-2][calendar_day]

        return dt.day_(day_of_month)

    def _nth_of_month(self, nth, day_of_week):
        """
        Modify to the given occurrence of a given day of the week
        in the current month. If the calculated occurrence is outside,
        the scope of the current month, then return False and no
        modifications are made. Use the supplied consts
        to indicate the desired day_of_week, ex. Pendulum.MONDAY.

        :type nth: int

        :type day_of_week: int or None

        :rtype: Pendulum
        """
        if nth == 1:
            return self.first_of('month', day_of_week)

        dt = self.first_of('month')
        check = dt.format('%Y-%m')
        for i in range(nth - (1 if dt.day_of_week == day_of_week else 0)):
            dt = dt.next(day_of_week)

        if dt.format('%Y-%m') == check:
            return self.day_(dt.day).start_of('day')

        return False

    def _first_of_quarter(self, day_of_week=None):
        """
        Modify to the first occurrence of a given day of the week
        in the current quarter. If no day_of_week is provided,
        modify to the first day of the quarter. Use the supplied consts
        to indicate the desired day_of_week, ex. Pendulum.MONDAY.

        :type day_of_week: int or None

        :rtype: Pendulum
        """
        return self.on(self.year, self.quarter * 3 - 2, 1).first_of('month', day_of_week)

    def _last_of_quarter(self, day_of_week=None):
        """
        Modify to the last occurrence of a given day of the week
        in the current quarter. If no day_of_week is provided,
        modify to the last day of the quarter. Use the supplied consts
        to indicate the desired day_of_week, ex. Pendulum.MONDAY.

        :type day_of_week: int or None

        :rtype: Pendulum
        """
        return self.on(self.year, self.quarter * 3, 1).last_of('month', day_of_week)

    def _nth_of_quarter(self, nth, day_of_week):
        """
        Modify to the given occurrence of a given day of the week
        in the current quarter. If the calculated occurrence is outside,
        the scope of the current quarter, then return False and no
        modifications are made. Use the supplied consts
        to indicate the desired day_of_week, ex. Pendulum.MONDAY.

        :type nth: int

        :type day_of_week: int or None

        :rtype: Pendulum
        """
        if nth == 1:
            return self.first_of('quarter', day_of_week)

        dt = self.day_(1).month_(self.quarter * 3)
        last_month = dt.month
        year = dt.year
        dt = dt.first_of('quarter')
        for i in range(nth - (1 if dt.day_of_week == day_of_week else 0)):
            dt = dt.next(day_of_week)

        if last_month < dt.month or year != dt.year:
            return False

        return self.on(self.year, dt.month, dt.day).start_of('day')

    def _first_of_year(self, day_of_week=None):
        """
        Modify to the first occurrence of a given day of the week
        in the current year. If no day_of_week is provided,
        modify to the first day of the year. Use the supplied consts
        to indicate the desired day_of_week, ex. Pendulum.MONDAY.

        :type day_of_week: int or None

        :rtype: Pendulum
        """
        return self.month_(1).first_of('month', day_of_week)

    def _last_of_year(self, day_of_week=None):
        """
        Modify to the last occurrence of a given day of the week
        in the current year. If no day_of_week is provided,
        modify to the last day of the year. Use the supplied consts
        to indicate the desired day_of_week, ex. Pendulum.MONDAY.

        :type day_of_week: int or None

        :rtype: Pendulum
        """
        return self.month_(MONTHS_PER_YEAR).last_of('month', day_of_week)

    def _nth_of_year(self, nth, day_of_week):
        """
        Modify to the given occurrence of a given day of the week
        in the current year. If the calculated occurrence is outside,
        the scope of the current year, then return False and no
        modifications are made. Use the supplied consts
        to indicate the desired day_of_week, ex. Pendulum.MONDAY.

        :type nth: int

        :type day_of_week: int or None

        :rtype: Pendulum
        """
        if nth == 1:
            return self.first_of('year', day_of_week)

        dt = self.first_of('year')
        year = dt.year
        for i in range(nth - (1 if dt.day_of_week == day_of_week else 0)):
            dt = dt.next(day_of_week)

        if year != dt.year:
            return False

        return self.on(self.year, dt.month, dt.day).start_of('day')

    def average(self, dt=None):
        """
        Modify the current instance to the average
        of a given instance (default now) and the current instance.

        :type dt: Pendulum or datetime

        :rtype: Pendulum
        """
        if dt is None:
            dt = Pendulum.now(self._tz)

        return self.add(seconds=int(self.diff(dt, False).in_seconds() / 2))

    def _get_datetime(self, value, pendulum=False):
        """
        Gets a datetime from a given value.

        :param value: The value to get the datetime from.
        :type value: Pendulum or datetime or int or float or str.

        :param pendulum: Whether to return a Pendulum instance.
        :type pendulum: bool

        :rtype: datetime or Pendulum
        """
        if value is None:
            return None

        if isinstance(value, Pendulum):
            return value._datetime if not pendulum else value

        if isinstance(value, datetime.datetime):
            if value.tzinfo is None:
                value = self._tz.convert(value)

            return value if not pendulum else Pendulum.instance(value)

        raise ValueError('Invalid datetime "{}"'.format(value))

    def __sub__(self, other):
        if isinstance(other, datetime.timedelta):
            return self.subtract_timedelta(other)

        try:
            return self._get_datetime(other, True).diff(self, False)
        except ValueError:
            return NotImplemented

    def __rsub__(self, other):
        try:
            return self.diff(self._get_datetime(other, True), False)
        except ValueError:
            return NotImplemented

    def __add__(self, other):
        if not isinstance(other, datetime.timedelta):
            return NotImplemented

        return self.add_timedelta(other)

    def __radd__(self, other):
        return self.__add__(other)

    # Native methods override

    @classmethod
    def fromtimestamp(cls, t, tz=None):
        return cls.create_from_timestamp(t, tz)

    @classmethod
    def utcfromtimestamp(cls, t):
        return cls.create_from_timestamp(t)

    @classmethod
    def fromordinal(cls, n):
        return cls.instance(datetime.datetime.fromordinal(n))

    @classmethod
    def combine(cls, date, time):
        return cls.instance(datetime.datetime.combine(date, time))

    def timetuple(self):
        return self._datetime.timetuple()

    def utctimetuple(self):
        return self._datetime.utctimetuple()

    def replace(self, year=None, month=None, day=None, hour=None,
                minute=None, second=None, microsecond=None, tzinfo=True,
                fold=None):
        year = year if year is not None else self._year
        month = month if month is not None else self._month
        day = day if day is not None else self._day
        hour = hour if hour is not None else self._hour
        minute = minute if minute is not None else self._minute
        second = second if second is not None else self._second
        microsecond = microsecond if microsecond is not None else self._microsecond

        # Checking tzinfo
        if tzinfo is not None and tzinfo is not True:
            tzinfo = self._safe_create_datetime_zone(tzinfo)
        elif tzinfo is None:
            tzinfo = UTC
        else:
            tzinfo = self._tzinfo.tz

        return self.__class__(
            year, month, day,
            hour, minute, second, microsecond,
            tzinfo=tzinfo, fold=fold
        )

    def astimezone(self, tz=None):
        tz = self._safe_create_datetime_zone(tz)

        return self.instance(self._datetime.astimezone(tz))

    def isoformat(self, sep='T'):
        return self._datetime.isoformat(sep)

    def utcoffset(self):
        return self._tzinfo.utcoffset(self)

    def tzname(self):
        return self._datetime.tzname()

    def dst(self):
        return self._datetime.dst()

    def __hash__(self):
        return self._datetime.__hash__()

    def __getnewargs__(self):
        return(self, )

    def _getstate(self, protocol=3):
        tz = self.timezone_name

        # Fix for fixed timezones not being properly unpickled
        if isinstance(self.tz, FixedTimezone):
            tz = self.offset_hours

        return (
            self.year, self.month, self.day,
            self.hour, self.minute, self.second, self.microsecond,
            tz,
            self.fold
        )

    def __reduce__(self):
        return self.__reduce_ex__(2)

    def __reduce_ex__(self, protocol):
        return self.__class__, self._getstate(protocol)

Pendulum.min = Pendulum.instance(datetime.datetime.min.replace(tzinfo=UTC))
Pendulum.max = Pendulum.instance(datetime.datetime.max.replace(tzinfo=UTC))
Pendulum.EPOCH = Pendulum(1970, 1, 1)
