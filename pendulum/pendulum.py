# -*- coding: utf-8 -*-

from __future__ import division

import re
import os
import time as _time
import math
import calendar
import pytz
import tzlocal
import datetime

from pytz.tzinfo import BaseTzInfo, tzinfo
from dateutil.relativedelta import relativedelta
from dateutil import parser as dateparser

from .translator import Translator

from .pendulum_interval import PendulumInterval, AbsolutePendulumInterval
from .exceptions import PendulumException
from ._compat import PY33, basestring


class Pendulum(object):

    # The day constants
    SUNDAY = 0
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6

    # Names of days of the week
    _days = {
        SUNDAY: 'Sunday',
        MONDAY: 'Monday',
        TUESDAY: 'Tuesday',
        WEDNESDAY: 'Wednesday',
        THURSDAY: 'Thursday',
        FRIDAY: 'Friday',
        SATURDAY: 'Saturday'
    }

    # Number of X in Y.
    YEARS_PER_CENTURY = 100
    YEARS_PER_DECADE = 10
    MONTHS_PER_YEAR = 12
    WEEKS_PER_YEAR = 52
    DAYS_PER_WEEK = 7
    HOURS_PER_DAY = 24
    MINUTES_PER_HOUR = 60
    SECONDS_PER_MINUTE = 60

    # Formats
    ATOM = '%Y-%m-%dT%H:%M:%S%P'
    COOKIE = '%A, %d-%b-%Y %H:%M:%S %Z'
    ISO8601 = '%Y-%m-%dT%H:%M:%S%P'
    ISO8601_EXTENDED = '%Y-%m-%dT%H:%M:%S.%f%P'
    RFC822 = '%a, %d %b %y %H:%M:%S %z'
    RFC850 = '%A, %d-%b-%y %H:%M:%S %Z'
    RFC1036 = '%a, %d %b %y %H:%M:%S %z'
    RFC1123 = '%a, %d %b %Y %H:%M:%S %z'
    RFC2822 = '%a, %d %b %Y %H:%M:%S %z'
    RFC3339 = '%Y-%m-%dT%H:%M:%S%P'
    RFC3339_EXTENDED = '%Y-%m-%dT%H:%M:%S.%f%P'
    RSS = '%a, %d %b %Y %H:%M:%S %z'
    W3C = '%Y-%m-%dT%H:%M:%S%P'

    # Default format to use for __str__ method when type juggling occurs.
    DEFAULT_TO_STRING_FORMAT = None

    _to_string_format = DEFAULT_TO_STRING_FORMAT

    # First day of week
    _week_starts_at = MONDAY

    # Last day of week
    _week_ends_at = SUNDAY

    # Weekend days
    _weekend_days = [
        SATURDAY,
        SUNDAY
    ]

    # A test Pendulum instance to be returned when now instances are created.
    _test_now = None

    # Transaltor
    _translator = None

    _EPOCH = datetime.datetime(1970, 1, 1, tzinfo=pytz.UTC)

    _CUSTOM_FORMATTERS = ['P', 't']
    _FORMATTERS_REGEX = re.compile('%%(%s)' % '|'.join(_CUSTOM_FORMATTERS))

    @classmethod
    def _safe_create_datetime_zone(cls, obj):
        """
        Creates a timezone from a string, BaseTzInfo or integer offset.

        :param obj: str or tzinfo or int or None

        :rtype: BaseTzInfo
        """
        if obj is None or obj == 'local':
            return cls._local_timezone()

        if isinstance(obj, tzinfo):
            return obj

        if isinstance(obj, (int, float)):
            timezone_offset = obj * 60

            return pytz.FixedOffset(timezone_offset)

        tz = pytz.timezone(obj)

        return tz

    @classmethod
    def _local_timezone(cls):
        """
        Returns the local timezone using tzlocal.get_localzone
        or the TZ environment variable.

        :rtype: tzinfo
        """
        if os.getenv('TZ'):
            return pytz.timezone(os.environ['TZ'])

        return tzlocal.get_localzone()

    def __init__(self, year=None, month=None, day=None,
                 hour=None, minute=None, second=None, microsecond=None,
                 tzinfo=pytz.UTC):
        """
        Constructor.

        :type tz: BaseTzInfo or str or None
        """
        # If the class has a test now set and we are trying to create a now()
        # instance then override as required
        if (self.has_test_now()
            and all([year is None, month is None, day is None, hour is None,
                     minute is None, second is None, microsecond is None])):
            test_instance = self._test_now.copy()

            if tzinfo is not None and tzinfo != self._test_now.timezone:
                test_instance.to(tzinfo)
            else:
                tzinfo = test_instance.timezone

            year, month, day = test_instance.year, test_instance.month, test_instance.day
            hour, minute, second = test_instance.hour, test_instance.minute, test_instance.second
            microsecond = test_instance.microsecond

        self._tz = self._safe_create_datetime_zone(tzinfo)

        # Default datetime behavior
        if year is not None and month is not None and day is not None:
            hour = 0 if hour is None else hour
            minute = 0 if minute is None else minute
            second = 0 if second is None else second
            microsecond = 0 if microsecond is None else microsecond

        self._datetime = self._create_datetime(
            self._tz, year, month, day,
            hour, minute, second, microsecond
        )

    @classmethod
    def instance(cls, dt):
        """
        Create a Carbon instance from a datetime one.

        :param dt: A datetime instance
        :type dt: datetime.datetime

        :rtype: Pendulum
        """
        return cls(
            dt.year, dt.month, dt.day,
            dt.hour, dt.minute, dt.second, dt.microsecond,
            tzinfo=dt.tzinfo
        )

    @classmethod
    def parse(cls, time=None, tz=pytz.UTC):
        """
        Create a Pendulum instance from a string.

        :param time: The time string
        :type time: str

        :param tz: The timezone
        :type tz: BaseTzInfo or str or None

        :rtype: Pendulum
        """
        if time is None:
            return cls.now(tz)

        if time == 'now':
            return cls.now(None)

        dt = dateparser.parse(time)

        if not dt:
            raise PendulumException('Invalid time string "%s"' % time)

        return cls(
            dt.year, dt.month, dt.day,
            dt.hour, dt.minute, dt.second, dt.microsecond,
            tzinfo=tz
        )

    @classmethod
    def now(cls, tz=None):
        """
        Get a Pendulum instance for the current date and time.

        :param tz: The timezone
        :type tz: BaseTzInfo or str or None

        :rtype: Pendulum
        """
        return cls(tzinfo=tz)

    @classmethod
    def utcnow(cls):
        """
        Get a Pendulum instance for the current date and time in UTC.

        :param tz: The timezone
        :type tz: BaseTzInfo or str or None

        :rtype: Pendulum
        """
        return cls.now(pytz.UTC)

    @classmethod
    def today(cls, tz=None):
        """
        Create a Pendulum instance for today.

        :param tz: The timezone
        :type tz: BaseTzInfo or str or None

        :rtype: Pendulum
        """
        return cls.now(tz).start_of_day()

    @classmethod
    def tomorrow(cls, tz=None):
        """
        Create a Pendulum instance for tomorrow.

        :param tz: The timezone
        :type tz: BaseTzInfo or str or None

        :rtype: Pendulum
        """
        return cls.today(tz).add_day()

    @classmethod
    def yesterday(cls, tz=None):
        """
        Create a Pendulum instance for yesterday.

        :param tz: The timezone
        :type tz: BaseTzInfo or str or None

        :rtype: Pendulum
        """
        return cls.today(tz).sub_day()

    @classmethod
    def _create_datetime(cls, tz, year=None, month=None, day=None,
                         hour=None, minute=None, second=None, microsecond=None):
        now = (datetime.datetime.utcnow()
               .replace(tzinfo=pytz.UTC)
               .astimezone(tz))

        if year is None:
            year = now.year

        if month is None:
            month = now.month

        if day is None:
            day = now.day

        if hour is None:
            hour = now.hour
            minute = now.minute if minute is None else minute
            second = now.second if second is None else second
            microsecond = now.microsecond if microsecond is None else microsecond
        else:
            minute = 0 if minute is None else minute
            second = 0 if second is None else second
            microsecond = 0 if microsecond is None else microsecond

        return tz.localize(datetime.datetime(
            year, month, day,
            hour, minute, second, microsecond,
            tzinfo=None
        ))

    @classmethod
    def create(cls, year=None, month=None, day=None,
               hour=None, minute=None, second=None, microsecond=None,
               tz=pytz.UTC):
        """
        Create a new Carbon instance from a specific date and time.

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

        self = cls()
        self._tz = tz
        self._datetime = cls._create_datetime(
            tz, year, month, day,
            hour, minute, second, microsecond
        )

        return self

    @classmethod
    def create_from_date(cls, year=None, month=None, day=None, tz=pytz.UTC):
        """
        Create a Pendulum instance from just a date.
        The time portion is set to now.

        :type year: int
        :type month: int
        :type day: int
        :type tz: tzinfo or str or None

        :rtype: Pendulum
        """
        return cls.create(year, month, day, tz=tz)

    @classmethod
    def create_from_time(cls, hour=None, minute=None, second=None,
                         microsecond=None, tz=pytz.UTC):
        """
        Create a Pendulum instance from just a time.
        The date portion is set to today.

        :type hour: int
        :type minute: int
        :type second: int
        :type microsecond: int
        :type tz: tzinfo or str or int or None

        :rtype: Pendulum
        """
        return cls.create(hour=hour, minute=minute, second=second,
                          microsecond=microsecond, tz=tz)

    @classmethod
    def create_from_format(cls, time, fmt, tz=pytz.UTC):
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
        dt = (datetime.datetime.strptime(time, fmt)
              .replace(tzinfo=cls._safe_create_datetime_zone(tz)))

        return cls.instance(dt)

    @classmethod
    def create_from_timestamp(cls, timestamp, tz=pytz.UTC):
        """
        Create a Pendulum instance from a timestamp.

        :param timestamp: The timestamp
        :type timestamp: int or float

        :param tz: The timezone
        :type tz: tzinfo or str or int or None

        :rtype: Pendulum
        """
        return cls.now(tz).set_timestamp(timestamp)

    @classmethod
    def strptime(cls, time, fmt):
        return cls.create_from_format(time, fmt)

    def copy(self):
        """
        Get a copy of the instance.

        :rtype: Pendulum
        """
        return self.instance(self._datetime)

    ### Getters/Setters

    def year_(self, year):
        return self.set_year(year)

    def set_year(self, year):
        self._datetime = self._datetime.replace(year=year)

        return self

    def month_(self, month):
        return self.set_month(month)

    def set_month(self, month):
        self._datetime = self._datetime.replace(month=month)

        return self

    def day_(self, day):
        return self.set_day(day)

    def set_day(self, day):
        self._datetime = self._datetime.replace(day=day)

        return self

    def hour_(self, hour):
        return self.set_hour(hour)

    def set_hour(self, hour):
        self._datetime = self._datetime.replace(hour=hour)

        return self

    def minute_(self, minute):
        return self.set_minute(minute)

    def set_minute(self, minute):
        self._datetime = self._datetime.replace(minute=minute)

        return self

    def second_(self, second):
        return self.set_second(second)

    def set_second(self, second):
        self._datetime = self._datetime.replace(second=second)

        return self

    def microsecond_(self, microsecond):
        return self.set_microsecond(microsecond)

    def set_microsecond(self, microsecond):
        self._datetime = self._datetime.replace(microsecond=microsecond)

        return self

    def timezone_(self, tz):
        return self.set_timezone(tz)

    def tz_(self, tz):
        return self.set_timezone(tz)

    def timestamp_(self, timestamp):
        return self.set_timestamp(timestamp)

    @property
    def day_of_week(self):
        return int(self.format('%w'))

    @property
    def day_of_year(self):
        return int(self.format('%-j'))

    @property
    def week_of_year(self):
        return self.isocalendar()[1]

    @property
    def days_in_month(self):
        return calendar.monthrange(self.year, self.month)[1]

    @property
    def timestamp(self):
        return int(self.float_timestamp - self._datetime.microsecond / 1e6)

    @property
    def float_timestamp(self):
        # If Python > 3.3 we use the native function
        # else we emulate it
        if PY33:
            return self._datetime.timestamp()

        if self._datetime.tzinfo is None:
            return _time.mktime((self.year, self.month, self.day,
                                 self.hour, self.minute, self.second,
                                 -1, -1, -1)) + self.microsecond / 1e6

        else:
            return (self._datetime - self._EPOCH).total_seconds()

    @property
    def week_of_month(self):
        return math.ceil(self.day / self.DAYS_PER_WEEK)

    @property
    def age(self):
        return self.diff_in_years()

    @property
    def quarter(self):
        return int(math.ceil(self.month / 3))

    @property
    def offset(self):
        return self.get_offset()

    @property
    def offset_hours(self):
        return int(self.get_offset()
                   / self.SECONDS_PER_MINUTE
                   / self.MINUTES_PER_HOUR)

    @property
    def local(self):
        return self.offset == self.copy().set_timezone(self._local_timezone()).offset

    @property
    def utc(self):
        return self.offset == 0

    @property
    def is_dst(self):
        dst = self._datetime.dst()

        return dst.total_seconds() != 0

    @property
    def timezone(self):
        return self.get_timezone()

    @property
    def tz(self):
        return self.get_timezone()

    @property
    def timezone_name(self):
        return self.timezone.zone

    def get_timezone(self):
        return self._tz

    def get_offset(self):
        return int(self._datetime.utcoffset().total_seconds())

    def set_date(self, year, month, day):
        """
        Sets the current date to a different date.

        :param year: The year
        :type year: int

        :param month: The month
        :type month: int

        :param day: The day
        :type day: int

        :rtype: Pendulum
        """
        self._datetime = self._datetime.replace(
            year=int(year), month=int(month), day=int(day)
        )

        return self

    def set_time(self, hour, minute, second, microsecond=0):
        """
        Sets the current time to a different time.

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
        self._datetime = self._datetime.replace(
            hour=int(hour), minute=int(minute), second=int(second),
            microsecond=microsecond
        )

        return self

    def set_date_time(self, year, month, day, hour, minute, second=0):
        """
        Set the date and time all together.

        :type year: int
        :type month: int
        :type day: int
        :type hour: int
        :type minute: int
        :type second: int

        :rtype: Pendulum
        """
        return self.set_date(year, month, day).set_time(hour, minute, second)

    def set_time_from_string(self, time):
        """
        Set the time by time string.

        :param time: The time string
        :type time: str

        :rtype: Pendulum
        """
        time = time.split(':')

        hour = time[0]
        minute = time[1] if len(time) > 1 else 0
        second = time[2] if len(time) > 2 else 0

        return self.set_time(hour, minute, second)

    def set_timezone(self, value):
        """
        Set the instance's timezone from a string or object.

        :param value: The timezone
        :type value: BaseTzInfo or str or None

        :rtype: Pendulum
        """
        self._tz = self._safe_create_datetime_zone(value)
        self._datetime = self._datetime.astimezone(self._tz)

        return self

    def to(self, tz):
        """
        Set the instance's timezone from a string or object.

        :param value: The timezone
        :type value: BaseTzInfo or str or None

        :rtype: Pendulum
        """
        return self.set_timezone(tz)

    def set_timestamp(self, timestamp):
        """
        Set the date and time based on a Unix timestamp.

        :param timestamp: The timestamp
        :type timestamp: int or float

        :rtype: Pendulum
        """
        self._datetime = datetime.datetime.fromtimestamp(timestamp, pytz.UTC).astimezone(self._tz)

        return self

    ### Special week days

    @classmethod
    def get_week_starts_at(cls):
        """
        Get the first day of the week.

        :rtype: int
        """
        return cls._week_starts_at

    @classmethod
    def set_week_starts_at(cls, value):
        """
        Set the first day of the week.

        :type value: int
        """
        cls._week_starts_at = value

    @classmethod
    def get_week_ends_at(cls):
        """
        Get the last day of the week.

        :rtype: int
        """
        return cls._week_ends_at

    @classmethod
    def set_week_ends_at(cls, value):
        """
        Set the last day of the week.

        :type value: int
        """
        cls._week_ends_at = value

    @classmethod
    def get_weekend_days(cls):
        """
        Get weekend days.

        :rtype: list
        """
        return cls._weekend_days

    @classmethod
    def set_weekend_days(cls, value):
        """
        Set weekend days.

        :type value: list
        """
        cls._weekend_days = value

    # Testing aids

    @classmethod
    def set_test_now(cls, test_now=None):
        """
        Set a Pendulum instance (real or mock) to be returned when a "now"
        instance is created.  The provided instance will be returned
        specifically under the following conditions:
            - A call to the classmethod now() method, ex. Pendulum.now()
            - When nothing is passed to the constructor or parse(), ex. Pendulum()
            - When the string "now" is passed to parse(), ex. Pendulum.parse('now')

        Note the timezone parameter was left out of the examples above and
        has no affect as the mock value will be returned regardless of its value.

        To clear the test instance call this method using the default
        parameter of null.

        :type test_now: Pendulum or None
        """
        cls._test_now = test_now

    @classmethod
    def get_test_now(cls):
        """
        Get the Carbon instance (real or mock) to be returned when a "now"
        instance is created.

        :rtype: Pendulum or None
        """
        return cls._test_now

    @classmethod
    def has_test_now(cls):
        return cls.get_test_now() is not None

    # Localization

    @classmethod
    def translator(cls):
        """
        Initialize the translator instance if necessary.

        :rtype: Translator
        """
        if cls._translator is None:
            cls._translator = Translator('en')
            cls.set_locale('en')

        return cls._translator

    @classmethod
    def set_translator(cls, translator):
        """
        Set the translator instance to use.

        :param translator: The translator
        :type translator: Translator
        """
        cls._translator = translator

    @classmethod
    def get_locale(cls):
        """
        Get the current translator locale.

        :rtype: str
        :rtype: str
        """
        return cls.translator().locale

    @classmethod
    def set_locale(cls, locale):
        """
        Set the current translator locale and
        indicate if the source locale file exists.

        :type locale: str

        :rtype: bool
        """
        locale = cls.format_locale(locale)
        if not cls.translator().register_resource(locale):
            return False

        cls.translator().locale = locale

        return True

    @classmethod
    def format_locale(cls, locale):
        """
        Properly format locale.

        :param locale: The locale
        :type locale: str

        :rtype: str
        """
        m = re.match('([a-z]{2})[-_]([a-z]{2})', locale, re.I)
        if m:
            return '%s_%s' % (m.group(1).lower(), m.group(2).lower())
        else:
            return locale.lower()

    # String Formatting

    @classmethod
    def reset_to_string_format(cls):
        """
        Reset the format used to the default
        when type juggling a Pendulum instance to a string.
        """
        cls.set_to_string_format(cls.DEFAULT_TO_STRING_FORMAT)

    @classmethod
    def set_to_string_format(cls, fmt):
        """
        Set the default format used
        when type juggling a Pendulum instance to a string

        :type fmt: str
        """
        cls._to_string_format = fmt

    def format(self, fmt):
        """
        Formats the Pendulum instance using the given format.

        :param fmt: The format to use
        :type fmt: str

        :rtype: str
        """
        return self.strftime(fmt)

    def strftime(self, fmt):
        """
        Formats the Pendulum instance using the given format.

        :param fmt: The format to use
        :type fmt: str

        :rtype: str
        """
        # Checking for custom formatters
        fmt = self._FORMATTERS_REGEX.sub(self._strftime, fmt)

        return self._datetime.strftime(fmt)

    def _strftime(self, m):
        """
        Handles custom formatters in format string.

        :return: str
        """
        fmt = m.group(1)

        if fmt == 'P':
            offset = self._datetime.utcoffset() or datetime.timedelta()
            minutes = offset.total_seconds() / 60

            if minutes >= 0:
                sign = '+'
            else:
                sign = '-'

            hour, minute = divmod(abs(int(minutes)), 60)

            return '{0}{1:02d}:{2:02d}'.format(sign, hour, minute)
        elif fmt == 't':
            if 10 <= self.day % 100 < 20:
                return 'th'
            else:
                return {1: 'st', 2: 'nd', 3: 'rd'}.get(self.day % 10, "th")

        raise PendulumException('Unknown formatter %%%s' % fmt)

    def __str__(self):
        if self._to_string_format is None:
            return self._datetime.isoformat()

        return self.format(self._to_string_format)

    def __repr__(self):
        return self.__str__()

    def to_date_string(self):
        """
        Format the instance as date.

        :rtype: str
        """
        return self.format('%Y-%m-%d')

    def to_formatted_date_string(self):
        """
        Format the instance as a readable date.

        :rtype: str
        """
        return self.format('%b %d, %Y')

    def to_time_string(self):
        """
        Format the instance as time.

        :rtype: str
        """
        return self.format('%H:%M:%S')

    def to_datetime_string(self):
        """
        Format the instance as date and time.

        :rtype: str
        """
        return self.format('%Y-%m-%d %H:%M:%S')

    def to_day_datetime_string(self):
        """
        Format the instance as day, date and time.

        :rtype: str
        """
        return self.format('%a, %b %d, %Y %-I:%M %p')

    def to_atom_string(self):
        """
        Format the instance as ATOM.

        :rtype: str
        """
        return self.format(self.ATOM)

    def to_cookie_string(self):
        """
        Format the instance as COOKIE.

        :rtype: str
        """
        return self.format(self.COOKIE)

    def to_iso8601_string(self, extended=False):
        """
        Format the instance as ISO8601.

        :rtype: str
        """
        fmt = self.ISO8601
        if extended:
            fmt = self.ISO8601_EXTENDED

        return self.format(fmt)

    def to_rfc822_string(self):
        """
        Format the instance as RFC822.

        :rtype: str
        """
        return self.format(self.RFC822)

    def to_rfc850_string(self):
        """
        Format the instance as RFC850.

        :rtype: str
        """
        return self.format(self.RFC850)

    def to_rfc1036_string(self):
        """
        Format the instance as RFC1036.

        :rtype: str
        """
        return self.format(self.RFC1036)

    def to_rfc1123_string(self):
        """
        Format the instance as RFC1123.

        :rtype: str
        """
        return self.format(self.RFC1123)

    def to_rfc2822_string(self):
        """
        Format the instance as RFC2822.

        :rtype: str
        """
        return self.format(self.RFC2822)

    def to_rfc3339_string(self, extended=False):
        """
        Format the instance as RFC3339.

        :rtype: str
        """
        fmt = self.RFC3339
        if extended:
            fmt = self.RFC3339_EXTENDED

        return self.format(fmt)

    def to_rss_string(self):
        """
        Format the instance as RSS.

        :rtype: str
        """
        return self.format(self.RSS)

    def to_w3c_string(self):
        """
        Format the instance as W3C.

        :rtype: str
        """
        return self.format(self.W3C)

    # Comparisons

    def eq(self, other):
        """
        Determines if the instance is equal to another.

        :param other: The other instance
        :type other: Pendulum or datetime or str or int

        :rtype: bool
        """
        return self._datetime == self._get_datetime(other)

    def equal_to(self, other):
        """
        Determines if the instance is equal to another.

        :param other: The other instance
        :type other: Pendulum or datetime or str or int

        :rtype: bool
        """
        return  self.eq(other)

    def __eq__(self, other):
        return self.eq(other)

    def ne(self, other):
        """
        Determines if the instance is not equal to another.

        :param other: The other instance
        :type other: Pendulum or datetime or str or int

        :rtype: bool
        """
        return self._datetime != self._get_datetime(other)

    def not_equal_to(self, other):
        """
        Determines if the instance is not equal to another.

        :param other: The other instance
        :type other: Pendulum or datetime or str or int

        :rtype: bool
        """
        return self.ne(other)

    def __ne__(self, other):
        return self.ne(other)

    def gt(self, other):
        """
        Determines if the instance is greater (after) than another.

        :param other: The other instance
        :type other: Pendulum or datetime or str or int

        :rtype: bool
        """
        return self._datetime > self._get_datetime(other)

    def greater_than(self, other):
        """
        Determines if the instance is greater (after) than another.

        :param other: The other instance
        :type other: Pendulum or datetime or str or int

        :rtype: bool
        """
        return self.gt(other)

    def __gt__(self, other):
        return self.gt(other)

    def gte(self, other):
        """
        Determines if the instance is greater (after) than
        or equal to another.

        :param other: The other instance
        :type other: Pendulum or datetime or str or int

        :rtype: bool
        """
        return self._datetime >= self._get_datetime(other)

    def greater_than_or_equal_to(self, other):
        """
        Determines if the instance is greater (after) than
        or equal to another.

        :param other: The other instance
        :type other: Pendulum or datetime or str or int

        :rtype: bool
        """
        return self.gte(other)

    def __ge__(self, other):
        return self.gte(other)

    def lt(self, other):
        """
        Determines if the instance is less (before) than another.

        :param other: The other instance
        :type other: Pendulum or datetime or str or int

        :rtype: bool
        """
        return self._datetime < self._get_datetime(other)

    def less_than(self, other):
        """
        Determines if the instance is less (before) than another.

        :param other: The other instance
        :type other: Pendulum or datetime or str or int

        :rtype: bool
        """
        return self.lt(other)

    def __lt__(self, other):
        return self.lt(other)

    def lte(self, other):
        """
        Determines if the instance is less (before) than
        or equal to another.

        :param other: The other instance
        :type other: Pendulum or datetime or str or int

        :rtype: bool
        """
        return self._datetime <= self._get_datetime(other)

    def less_than_or_equal_to(self, other):
        """
        Determines if the instance is less (before) than
        or equal to another.

        :param other: The other instance
        :type other: Pendulum or datetime or str or int

        :rtype: bool
        """
        return self.lte(other)

    def __le__(self, other):
        return self.lte(other)

    def between(self, dt1, dt2, equal=True):
        """
        Determines if the instance is between two others.

        :type dt1: Pendulum or datetime or str or int
        :type dt2: Pendulum or datetime or str or int

        :param equal: Indicates if a > and < comparison shoud be used or <= and >=

        :rtype: bool
        """
        dt1 = self._get_datetime(dt1)
        dt2 = self._get_datetime(dt2)

        if dt1 > dt2:
            dt1, dt2 = dt2, dt1

        if equal:
            return self.gte(dt1) and self.lte(dt2)

        return self.gt(dt1) and self.lt(dt2)

    def closest(self, dt1, dt2):
        """
        Get the closest date from the instance.

        :type dt1: Pendulum or datetime
        :type dt2: Pendulum or datetime

        :rtype: Pendulum
        """
        dt1 = self._get_datetime(dt1, True)
        dt2 = self._get_datetime(dt2, True)

        if self.diff_in_seconds(dt1) < self.diff_in_seconds(dt2):
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

        if self.diff_in_seconds(dt1) > self.diff_in_seconds(dt2):
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

        if self.lt(dt):
            return self

        return self._get_datetime(dt, True)

    def minimum(self, dt=None):
        """
        Get the minimum instance between a given instance (default now)
        and the current instance.

        :type dt: Pendulum or datetime or str or int

        :rtype: Pendulum
        """
        return self.min(dt)

    def max_(self, dt=None):
        """
        Get the maximum instance between a given instance (default now)
        and the current instance.

        :type dt: Pendulum or datetime or str or int

        :rtype: Pendulum
        """
        if dt is None:
            dt = Pendulum.now(self.timezone)

        if self.gt(dt):
            return self

        return self._get_datetime(dt, True)

    def maximum(self, dt=None):
        """
        Get the maximum instance between a given instance (default utcnow)
        and the current instance.

        :type dt: Pendulum or datetime or str or int

        :rtype: Pendulum
        """
        return self.max(dt)

    def is_week_day(self):
        """
        Determines if the instance is a weekday.

        :rtype: bool
        """
        return not self.is_weekend()

    def is_weekend(self):
        """
        Determines if the instance is a weekend day.

        :rtype: bool
        """
        return self.day_of_week in self._weekend_days

    def is_yesterday(self):
        """
        Determines if the instance is yesterday.

        :rtype: bool
        """
        return self.to_date_string() == self.yesterday(self.timezone).to_date_string()

    def is_today(self):
        """
        Determines if the instance is today.

        :rtype: bool
        """
        return self.to_date_string() == self.now(self.timezone).to_date_string()

    def is_tomorrow(self):
        """
        Determines if the instance is tomorrow.

        :rtype: bool
        """
        return self.to_date_string() == self.tomorrow(self.timezone).to_date_string()

    def is_future(self):
        """
        Determines if the instance is in the future, ie. greater than now.

        :rtype: bool
        """
        return self.gt(self.now(self.tz))

    def is_past(self):
        """
        Determines if the instance is in the past, ie. less than now.

        :rtype: bool
        """
        return self.lt(self.now(self.tz))

    def is_leap_year(self):
        """
        Determines if the instance is a leap year.

        :rtype: bool
        """
        return calendar.isleap(self.year)

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

    def is_sunday(self):
        """
        Checks if this day is a sunday.

        :rtype: bool
        """
        return self.day_of_week == self.SUNDAY

    def is_monday(self):
        """
        Checks if this day is a monday.

        :rtype: bool
        """
        return self.day_of_week == self.MONDAY

    def is_tuesday(self):
        """
        Checks if this day is a tuesday.

        :rtype: bool
        """
        return self.day_of_week == self.TUESDAY

    def is_wednesday(self):
        """
        Checks if this day is a wednesday.

        :rtype: bool
        """
        return self.day_of_week == self.WEDNESDAY

    def is_thursday(self):
        """
        Checks if this day is a thursday.

        :rtype: bool
        """
        return self.day_of_week == self.THURSDAY

    def is_friday(self):
        """
        Checks if this day is a friday.

        :rtype: bool
        """
        return self.day_of_week == self.FRIDAY

    def is_saturday(self):
        """
        Checks if this day is a saturday.

        :rtype: bool
        """
        return self.day_of_week == self.SATURDAY

    def is_birthday(self, dt=None):
        """
        Check if its the birthday. Compares the date/month values of the two dates.

        :rtype: bool
        """
        if dt is None:
            dt = Pendulum.now(self.timezone)

        return self.format('%m%d') == self._get_datetime(dt, True).format('%m%d')

    # ADDITIONS AND SUBSTRACTIONS

    def add_years(self, value):
        """
        Add years to the instance. Positive $value travel forward while
        negative $value travel into the past.

        :param value: The number of years
        :type value: int

        :rtype: Pendulum
        """
        return self.add(years=value)

    def add_year(self, value=1):
        """
        Add a year to the instance.

        :param value: The number of years
        :type value: int

        :rtype: Pendulum
        """
        return self.add_years(value)

    def sub_years(self, value):
        """
        Remove years from the instance.

        :param value: The number of years
        :type value: int

        :rtype: Pendulum
        """
        return self.sub(years=value)

    def sub_year(self, value=1):
        """
        Remove a year from the instance.

        :param value: The number of years
        :type value: int

        :rtype: Pendulum
        """
        return self.sub_years(value)

    def add_months(self, value):
        """
        Add months to the instance. Positive $value travel forward while
        negative $value travel into the past.

        :param value: The number of months
        :type value: int

        :rtype: Pendulum
        """
        return self.add(months=value)

    def add_month(self, value=1):
        """
        Add a month to the instance.

        :param value: The number of month
        :type value: int

        :rtype: Pendulum
        """
        return self.add_months(value)

    def sub_months(self, value):
        """
        Remove months from the instance.

        :param value: The number of months
        :type value: int

        :rtype: Pendulum
        """
        return self.sub(months=value)

    def sub_month(self, value=1):
        """
        Remove a month from the instance.

        :param value: The number of months
        :type value: int

        :rtype: Pendulum
        """
        return self.sub_months(value)

    def add_days(self, value):
        """
        Add days to the instance. Positive $value travel forward while
        negative $value travel into the past.

        :param value: The number of days
        :type value: int

        :rtype: Pendulum
        """
        return self.add(days=value)

    def add_day(self, value=1):
        """
        Add a day to the instance.

        :param value: The number of days
        :type value: int

        :rtype: Pendulum
        """
        return self.add_days(value)

    def sub_days(self, value):
        """
        Remove days from the instance.

        :param value: The number of days
        :type value: int

        :rtype: Pendulum
        """
        return self.sub(days=value)

    def sub_day(self, value=1):
        """
        Remove a day from the instance.

        :param value: The number of days
        :type value: int

        :rtype: Pendulum
        """
        return self.sub_days(value)

    def add_weeks(self, value):
        """
        Add weeks to the instance. Positive $value travel forward while
        negative $value travel into the past.

        :param value: The number of weeks
        :type value: int

        :rtype: Pendulum
        """
        return self.add(weeks=value)

    def add_week(self, value=1):
        """
        Add a week to the instance.

        :param value: The number of weeks
        :type value: int

        :rtype: Pendulum
        """
        return self.add_weeks(value)

    def sub_weeks(self, value):
        """
        Remove weeks from the instance.

        :param value: The number of weeks
        :type value: int

        :rtype: Pendulum
        """
        return self.sub(weeks=value)

    def sub_week(self, value=1):
        """
        Remove a week from the instance.

        :param value: The number of weeks
        :type value: int

        :rtype: Pendulum
        """
        return self.sub_weeks(value)

    def add_hours(self, value):
        """
        Add hours to the instance. Positive $value travel forward while
        negative $value travel into the past.

        :param value: The number of hours
        :type value: int

        :rtype: Pendulum
        """
        return self.add(hours=value)

    def add_hour(self, value=1):
        """
        Add a hour to the instance.

        :param value: The number of hours
        :type value: int

        :rtype: Pendulum
        """
        return self.add_hours(value)

    def sub_hours(self, value):
        """
        Remove hours from the instance.

        :param value: The number of hours
        :type value: int

        :rtype: Pendulum
        """
        return self.sub(hours=value)

    def sub_hour(self, value=1):
        """
        Remove a hour from the instance.

        :param value: The number of hours
        :type value: int

        :rtype: Pendulum
        """
        return self.sub_hours(value)

    def add_minutes(self, value):
        """
        Add minutes to the instance. Positive $value travel forward while
        negative $value travel into the past.

        :param value: The number of minutes
        :type value: int

        :rtype: Pendulum
        """
        return self.add(minutes=value)

    def add_minute(self, value=1):
        """
        Add a minute to the instance.

        :param value: The number of minutes
        :type value: int

        :rtype: Pendulum
        """
        return self.add_minutes(value)

    def sub_minutes(self, value):
        """
        Remove minutes from the instance.

        :param value: The number of minutes
        :type value: int

        :rtype: Pendulum
        """
        return self.sub(minutes=value)

    def sub_minute(self, value=1):
        """
        Remove a minute from the instance.

        :param value: The number of minutes
        :type value: int

        :rtype: Pendulum
        """
        return self.sub_minutes(value)

    def add_seconds(self, value):
        """
        Add seconds to the instance. Positive $value travel forward while
        negative $value travel into the past.

        :param value: The number of seconds
        :type value: int

        :rtype: Pendulum
        """
        return self.add(seconds=value)

    def add_second(self, value=1):
        """
        Add a second to the instance.

        :param value: The number of seconds
        :type value: int

        :rtype: Pendulum
        """
        return self.add_seconds(value)

    def sub_seconds(self, value):
        """
        Remove seconds from the instance.

        :param value: The number of seconds
        :type value: int

        :rtype: Pendulum
        """
        return self.sub(seconds=value)

    def sub_second(self, value=1):
        """
        Remove a second from the instance.

        :param value: The number of seconds
        :type value: int

        :rtype: Pendulum
        """
        return self.sub_seconds(value)

    def add(self, years=0, months=0, weeks=0, days=0,
            hours=0, minutes=0, seconds=0, microseconds=0,
            weekdays=None):
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
        delta = relativedelta(
            years=years, months=months, weeks=weeks, days=days,
            hours=hours, minutes=minutes, seconds=seconds,
            microseconds=microseconds, weekday=weekdays
        )
        self._datetime = self._datetime + delta

        return self

    def sub(self, years=0, months=0, weeks=0, days=0,
            hours=0, minutes=0, seconds=0, microseconds=0,
            weekdays=None):
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
        delta = relativedelta(
            years=years, months=months, weeks=weeks, days=days,
            hours=hours, minutes=minutes, seconds=seconds,
            microseconds=microseconds, weekday=weekdays
        )
        self._datetime = self._datetime - delta

        return self

    def add_timedelta(self, delta):
        """
        Add timedelta duration to the instance.

        :param delta: The timedelta instance
        :type delta: datetime.timedelta

        :rtype: Pendulum
        """
        return self.add(days=delta.days, seconds=delta.seconds,
                        microseconds=delta.microseconds)

    def sub_timedelta(self, delta):
        """
        Remove timedelta duration from the instance.

        :param delta: The timedelta instance
        :type delta: datetime.timedelta

        :rtype: Pendulum
        """
        return self.sub(days=delta.days, seconds=delta.seconds,
                        microseconds=delta.microseconds)

    # DIFFERENCES

    def diff_in_years(self, dt=None, abs=True):
        """
        Get the difference in years.

        :type dt: Pendulum

        :param: Get the absolute of the difference
        :type abs: bool

        :rtype: int
        """
        if dt is None:
            dt = self.now(self._tz)

        return int(self.diff(dt, abs).total_years())

    def diff_in_months(self, dt=None, abs=True):
        """
        Get the difference in months.

        :type dt: Pendulum

        :param: Get the absolute of the difference
        :type abs: bool

        :rtype: int
        """
        if dt is None:
            dt = self.now(self._tz)

        return int(self.diff(dt, abs).total_months())

    def diff_in_days(self, dt=None, abs=True):
        """
        Get the difference in days.

        :type dt: Pendulum

        :param: Get the absolute of the difference
        :type abs: bool

        :rtype: int
        """
        if dt is None:
            dt = self.now(self._tz)

        return int(self.diff(dt, abs).total_days())

    def diff_in_hours(self, dt=None, abs=True):
        """
        Get the difference in hours.

        :type dt: Pendulum

        :param: Get the absolute of the difference
        :type abs: bool

        :rtype: int
        """
        if dt is None:
            dt = self.now(self._tz)

        return int(self.diff(dt, abs).total_hours())

    def diff_in_minutes(self, dt=None, abs=True):
        """
        Get the difference in minutes.

        :type dt: Pendulum

        :param: Get the absolute of the difference
        :type abs: bool

        :rtype: int
        """
        if dt is None:
            dt = self.now(self._tz)

        return int(self.diff(dt, abs).total_minutes())

    def diff_in_seconds(self, dt=None, abs=True):
        """
        Get the difference in seconds.

        :type dt: Pendulum

        :param: Get the absolute of the difference
        :type abs: bool

        :rtype: int
        """
        if dt is None:
            dt = self.now(self._tz)

        return int(self.diff(dt, abs).total_seconds())

    def diff_in_weeks(self, dt=None, abs=True):
        """
        Get the difference in weeks.

        :type dt: Pendulum

        :param: Get the absolute of the difference
        :type abs: bool

        :rtype: int
        """
        return int(self.diff_in_days(dt, abs) / self.DAYS_PER_WEEK)

    def seconds_since_midnight(self):
        """
        The number of seconds since midnight.

        :rtype: int
        """
        return self.diff_in_seconds(self.copy().start_of_day())

    def seconds_until_end_of_days(self):
        """
        The number of seconds until 23:59:59.

        :rtype: int
        """
        return self.diff_in_seconds(self.copy().end_of_day())

    def diff(self, dt, abs=True):
        """
        Returns the difference between two Pendulum objects represented as a PendulumInterval.

        :type dt: Pendulum

        :rtype: PendulumInterval
        """
        delta = self._get_datetime(dt) - self._datetime

        if abs:
            return AbsolutePendulumInterval.instance(delta)

        return PendulumInterval.instance(delta)

    def diff_for_humans(self, other=None, absolute=False, locale=None):
        """
        Get the difference in a human readable format in the current locale.

        When comparing a value in the past to default now:
        1 hour ago
        5 months ago

        When comparing a value in the future to default now:
        1 hour from now
        5 months from now

        When comparing a value in the past to another value:
        1 hour before
        5 months before

        When comparing a value in the future to another value:
        1 hour after
        5 months after

        :type other: Pendulum

        :param absolute: removes time difference modifiers ago, after, etc
        :type absolute: bool

        :param locale: The locale to use for localization
        :type locale: str

        :rtype: str
        """
        is_now = other is None

        if is_now:
            other = self.now(self.timezone)

        diff = self.diff(other)

        if diff.years > 0:
            unit = 'year'
            count = diff.years
        elif diff.months > 0:
            unit = 'month'
            count = diff.months
        elif diff.weeks > 0:
            unit = 'week'
            count = diff.weeks
        elif diff.days > 0:
            unit = 'day'
            count = diff.days
        elif diff.hours > 0:
            unit = 'hour'
            count = diff.hours
        elif diff.minutes > 0:
            unit = 'minute'
            count = diff.minutes
        else:
            unit = 'second'
            count = diff.seconds

        if count == 0:
            count = 1

        if locale:
            locale = self.format_locale(locale)

        time = self.translator().transchoice(unit, count, {'count': count}, locale=locale)

        if absolute:
            return time

        is_future = diff.invert

        if is_now:
            trans_id = 'from_now' if is_future else 'ago'
        else:
            trans_id = 'after' if is_future else 'before'

        # Some langs have special pluralization for past and future tense
        try_key_exists = '%s_%s' % (unit, trans_id)
        if try_key_exists != self.translator().transchoice(try_key_exists, count, locale=locale):
            time = self.translator().transchoice(try_key_exists, count, {'count': count}, locale=locale)

        return self.translator().trans(trans_id, {'time': time}, locale=locale)

    # Modifiers

    def start_of_day(self):
        """
        Reset the time to 00:00:00

        :rtype: Pendulum
        """
        return self.set_time(0, 0, 0)

    def end_of_day(self):
        """
        Reset the time to 23:59:59

        :rtype: Pendulum
        """
        return self.set_time(23, 59, 59)

    def start_of_month(self):
        """
        Reset the date to the first day of the month and the time to 00:00:00.

        :rtype: Pendulum
        """
        return self.set_date_time(self.year, self.month, 1, 0, 0, 0)

    def end_of_month(self):
        """
        Reset the date to the last day of the month and the time to 23:59:59.

        :rtype: Pendulum
        """
        return self.set_date_time(
            self.year, self.month, self.days_in_month, 23, 59, 59
        )

    def start_of_year(self):
        """
        Reset the date to the first day of the year and the time to 00:00:00.

        :rtype: Pendulum
        """
        return self.set_date_time(self.year, 1, 1, 0, 0, 0)

    def end_of_year(self):
        """
        Reset the date to the last day of the year and the time to 23:59:59.

        :rtype: Pendulum
        """
        return self.set_date_time(
            self.year, 12, 31, 23, 59, 59
        )

    def start_of_decade(self):
        """
        Reset the date to the first day of the decade
        and the time to 00:00:00.

        :rtype: Pendulum
        """
        year = self.year - self.year % self.YEARS_PER_DECADE
        return self.set_date_time(year, 1, 1, 0, 0, 0)

    def end_of_decade(self):
        """
        Reset the date to the last day of the decade
        and the time to 23:59:59.

        :rtype: Pendulum
        """
        year = self.year - self.year % self.YEARS_PER_DECADE + self.YEARS_PER_DECADE - 1

        return self.set_date_time(
            year, 12, 31, 23, 59, 59
        )

    def start_of_century(self):
        """
        Reset the date to the first day of the century
        and the time to 00:00:00.

        :rtype: Pendulum
        """
        year = self.year - 1 - (self.year - 1) % self.YEARS_PER_CENTURY + 1
        return self.set_date_time(year, 1, 1, 0, 0, 0)

    def end_of_century(self):
        """
        Reset the date to the last day of the century
        and the time to 23:59:59.

        :rtype: Pendulum
        """
        year = self.year - 1 - (self.year - 1) % self.YEARS_PER_CENTURY + self.YEARS_PER_CENTURY

        return self.set_date_time(
            year, 12, 31, 23, 59, 59
        )

    def start_of_week(self):
        """
        Reset the date to the first day of the week
        and the time to 00:00:00.

        :rtype: Pendulum
        """
        if self.day_of_week != self._week_starts_at:
            self.previous(self._week_starts_at)

        return self.start_of_day()

    def end_of_week(self):
        """
        Reset the date to the last day of the week
        and the time to 23:59:59.

        :rtype: Pendulum
        """
        if self.day_of_week != self._week_ends_at:
            self.next(self._week_ends_at)

        return self.end_of_day()

    def next(self, day_of_week=None):
        """
        Modify to the next occurrence of a given day of the week.
        If no day_of_week is provided, modify to the next occurrence
        of the current day of the week.  Use the supplied consts
        to indicate the desired day_of_week, ex. Pendulum.MONDAY.

        :param day_of_week: The next day of week to reset to.
        :type day_of_week: int or None

        :rtype: Pendulum
        """
        if day_of_week is None:
            day_of_week = self.day_of_week

        dt = self.start_of_day().add_day()
        while dt.day_of_week != day_of_week:
            dt.add_day()

        return dt

    def previous(self, day_of_week=None):
        """
        Modify to the previous occurrence of a given day of the week.
        If no day_of_week is provided, modify to the previous occurrence
        of the current day of the week.  Use the supplied consts
        to indicate the desired day_of_week, ex. Pendulum.MONDAY.

        :param day_of_week: The previous day of week to reset to.
        :type day_of_week: int or None

        :rtype: Pendulum
        """
        if day_of_week is None:
            day_of_week = self.day_of_week

        dt = self.start_of_day().sub_day()
        while dt.day_of_week != day_of_week:
            dt.sub_day()

        return dt

    def first_of_month(self, day_of_week=None):
        """
        Modify to the first occurrence of a given day of the week
        in the current month. If no day_of_week is provided,
        modify to the first day of the month. Use the supplied consts
        to indicate the desired day_of_week, ex. Pendulum.MONDAY.

        :type day_of_week: int or None

        :rtype: Pendulum
        """
        self.start_of_day()

        if day_of_week is None:
            return self.day_(1)

        month = calendar.monthcalendar(self.year, self.month)

        calendar_day = (day_of_week - 1) % 7

        if month[0][calendar_day] > 0:
            day_of_month = month[0][calendar_day]
        else:
            day_of_month = month[1][calendar_day]

        return self.day_(day_of_month)

    def last_of_month(self, day_of_week=None):
        """
        Modify to the last occurrence of a given day of the week
        in the current month. If no day_of_week is provided,
        modify to the last day of the month. Use the supplied consts
        to indicate the desired day_of_week, ex. Pendulum.MONDAY.

        :type day_of_week: int or None

        :rtype: Pendulum
        """
        self.start_of_day()

        if day_of_week is None:
            return self.day_(self.days_in_month)

        month = calendar.monthcalendar(self.year, self.month)

        calendar_day = (day_of_week - 1) % 7

        if month[-1][calendar_day] > 0:
            day_of_month = month[-1][calendar_day]
        else:
            day_of_month = month[-2][calendar_day]

        return self.day_(day_of_month)

    def nth_of_month(self, nth, day_of_week):
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
            return self.first_of_month(day_of_week)

        dt = self.copy().first_of_month()
        check = dt.format('%Y-%m')
        for i in range(nth - (1 if dt.day_of_week == day_of_week else 0)):
            dt.next(day_of_week)

        if dt.format('%Y-%m') == check:
            return self.day_(dt.day).start_of_day()

        return False

    def first_of_quarter(self, day_of_week=None):
        """
        Modify to the first occurrence of a given day of the week
        in the current quarter. If no day_of_week is provided,
        modify to the first day of the quarter. Use the supplied consts
        to indicate the desired day_of_week, ex. Pendulum.MONDAY.

        :type day_of_week: int or None

        :rtype: Pendulum
        """
        return self.set_date(self.year, self.quarter * 3 - 2, 1).first_of_month(day_of_week)

    def last_of_quarter(self, day_of_week=None):
        """
        Modify to the last occurrence of a given day of the week
        in the current quarter. If no day_of_week is provided,
        modify to the last day of the quarter. Use the supplied consts
        to indicate the desired day_of_week, ex. Pendulum.MONDAY.

        :type day_of_week: int or None

        :rtype: Pendulum
        """
        return self.set_date(self.year, self.quarter * 3, 1).last_of_month(day_of_week)

    def nth_of_quarter(self, nth, day_of_week):
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
            return self.first_of_quarter(day_of_week)

        dt = self.copy().day_(1).month_(self.quarter * 3)
        last_month = dt.month
        year = dt.year
        dt.first_of_quarter()
        for i in range(nth - (1 if dt.day_of_week == day_of_week else 0)):
            dt.next(day_of_week)

        if last_month < dt.month or year != dt.year:
            return False

        return self.set_date(self.year, dt.month, dt.day).start_of_day()

    def first_of_year(self, day_of_week=None):
        """
        Modify to the first occurrence of a given day of the week
        in the current year. If no day_of_week is provided,
        modify to the first day of the year. Use the supplied consts
        to indicate the desired day_of_week, ex. Pendulum.MONDAY.

        :type day_of_week: int or None

        :rtype: Pendulum
        """
        return self.month_(1).first_of_month(day_of_week)

    def last_of_year(self, day_of_week=None):
        """
        Modify to the last occurrence of a given day of the week
        in the current year. If no day_of_week is provided,
        modify to the last day of the year. Use the supplied consts
        to indicate the desired day_of_week, ex. Pendulum.MONDAY.

        :type day_of_week: int or None

        :rtype: Pendulum
        """
        return self.month_(self.MONTHS_PER_YEAR).last_of_month(day_of_week)

    def nth_of_year(self, nth, day_of_week):
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
            return self.first_of_year(day_of_week)

        dt = self.copy().first_of_year()
        year = dt.year
        for i in range(nth - (1 if dt.day_of_week == day_of_week else 0)):
            dt.next(day_of_week)

        if year != dt.year:
            return False

        return self.set_date(self.year, dt.month, dt.day).start_of_day()

    def average(self, dt=None):
        """
        Modify the current instance to the average
        of a given instance (default now) and the current instance.

        :type dt: Pendulum or datetime

        :rtype: Pendulum
        """
        if dt is None:
            dt = Pendulum.now(self._tz)

        return self.add_seconds(int(self.diff_in_seconds(dt, False) / 2))

    def _get_datetime(self, value, pendulum=False):
        """
        Gets a datetime from a given value.

        :param value: The value to get the datetime from.
        :type value: Pendulum or datetime or int or float or str.

        :param pendulum: Whether to return a Pendulum instance.
        :type pendulum: bool

        :rtype: datetime or Pendulum
        """
        if isinstance(value, Pendulum):
            return value._datetime if not pendulum else value

        if isinstance(value, datetime.datetime):
            if value.tzinfo is None:
                value = self._tz.localize(value)

            return value if not pendulum else Pendulum.instance(value)

        if isinstance(value, (int, float)):
            d = Pendulum.create_from_timestamp(value, self.timezone)
            if pendulum:
                return d

            return d._datetime

        if isinstance(value, basestring):
            d = Pendulum.parse(value, tz=self.timezone)
            if pendulum:
                return d

            return d._datetime

        raise ValueError('Invalid datetime "%s"' % value)

    def for_json(self):
        """
        Methods for automatic json serialization by simplejson

        :rtype: str
        """
        return str(self)

    def __getattr__(self, item):
        result = getattr(self._datetime, item)

        if isinstance(result, datetime.datetime):
            return Pendulum.instance(result)

        return result

    def __sub__(self, other):
        if isinstance(other, datetime.timedelta):
            return self.copy().sub_timedelta(other)

        return self._get_datetime(other, True).diff(self, False)

    def __add__(self, other):
        if isinstance(other, datetime.timedelta):
            return self.copy().add_timedelta(other)

        result = self._datetime + other

        if isinstance(result, datetime.datetime):
            return Pendulum.instance(result)

        return result


Pendulum.min = Pendulum.instance(datetime.datetime.min.replace(tzinfo=pytz.UTC))
Pendulum.max = Pendulum.instance(datetime.datetime.max.replace(tzinfo=pytz.UTC))
