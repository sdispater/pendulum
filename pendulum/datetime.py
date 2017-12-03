import calendar
import datetime
import pendulum

from .date import Date
from .time import Time
from .period import Period
from .exceptions import DateTimeException
from .tz import Timezone, UTC, FixedTimezone, local_timezone
from .tz.timezone_info import TimezoneInfo
from .helpers import add_duration
from .formatting import FORMATTERS
from .constants import (
    YEARS_PER_CENTURY, YEARS_PER_DECADE,
    MONTHS_PER_YEAR,
    MINUTES_PER_HOUR, SECONDS_PER_MINUTE,
    SECONDS_PER_DAY,
    SUNDAY, SATURDAY,
    ATOM, COOKIE, RFC822, RFC850, RFC1036, RFC1123, RFC2822, RSS, W3C
)


class DateTime(datetime.datetime, Date):

    # Formats

    _FORMATS = {
        'atom': ATOM,
        'cookie': COOKIE,
        'iso8601': lambda dt: dt.isoformat(),
        'rfc822': RFC822,
        'rfc850': RFC850,
        'rfc1036': RFC1036,
        'rfc1123': RFC1123,
        'rfc2822': RFC2822,
        'rfc3339': lambda dt: dt.isoformat(),
        'rss': RSS,
        'w3c': W3C
    }

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

            offset = obj.utcoffset(None)

            if offset is None:
                offset = datetime.timedelta(0)

            return FixedTimezone.load(offset.total_seconds())

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

    @classmethod
    def instance(cls, dt, tz=UTC):
        """
        Create a DateTime instance from a datetime one.

        :param dt: A datetime instance
        :type dt: datetime.datetime

        :param tz: The timezone
        :type tz: Timezone or TimeZoneInfo or str or None

        :rtype: DateTime
        """
        tz = dt.tzinfo or tz

        # Checking for pytz/tzinfo
        if (isinstance(tz, datetime.tzinfo)
            and not isinstance(tz, (Timezone, TimezoneInfo))):
            # pytz
            if hasattr(tz, 'localize') and tz.zone:
                tz = tz.zone
            else:
                # We have no sure way to figure out
                # the timezone name, we fallback
                # on a fixed offset
                tz = tz.utcoffset(dt).total_seconds() / 3600

        return cls.create(
            dt.year, dt.month, dt.day,
            dt.hour, dt.minute, dt.second, dt.microsecond,
            tz=tz
        )

    @classmethod
    def now(cls, tz=None):
        """
        Get a DateTime instance for the current date and time.

        :param tz: The timezone
        :type tz: Timezone or TimezoneInfo or str or int or None

        :rtype: DateTime
        """
        # If the class has a test now set and we are trying to create a now()
        # instance then override as required
        if pendulum.has_test_now():
            test_instance = pendulum.get_test_now()

            if tz is not None and tz != test_instance.timezone:
                test_instance = test_instance.in_timezone(tz)

            return test_instance

        if tz is None or tz == 'local':
            dt = datetime.datetime.now()
            tz = cls._local_timezone()
        elif tz is UTC or tz == 'UTC':
            dt = datetime.datetime.utcnow().replace(tzinfo=UTC)
        else:
            tz = cls._safe_create_datetime_zone(tz)
            dt = datetime.datetime.utcnow().replace(tzinfo=UTC)
            dt = tz.convert(dt)

        return cls.instance(dt, tz)

    @classmethod
    def utcnow(cls):
        """
        Get a DateTime instance for the current date and time in UTC.

        :param tz: The timezone
        :type tz: Timezone or TimezoneInfo or str or None

        :rtype: DateTime
        """
        return cls.now(UTC)

    @classmethod
    def today(cls, tz=None):
        """
        Create a DateTime instance for today.

        :param tz: The timezone
        :type tz: Timezone or TimezoneInfo or str or None

        :rtype: DateTime
        """
        return cls.now(tz).start_of('day')

    @classmethod
    def tomorrow(cls, tz=None):
        """
        Create a DateTime instance for tomorrow.

        :param tz: The timezone
        :type tz: Timezone or TimezoneInfo or str or None

        :rtype: DateTime
        """
        return cls.today(tz).add(days=1)

    @classmethod
    def yesterday(cls, tz=None):
        """
        Create a DateTime instance for yesterday.

        :param tz: The timezone
        :type tz: Timezone or TimezoneInfo or str or None

        :rtype: DateTime
        """
        return cls.today(tz).subtract(days=1)

    @classmethod
    def create(cls, year=None, month=None, day=None,
               hour=0, minute=0, second=0, microsecond=0,
               tz=UTC):
        """
        Create a new DateTime instance from a specific date and time.

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

        :rtype: DateTime
        """
        if tz is not None:
            tz = cls._safe_create_datetime_zone(tz)

        if any([year is None, month is None, day is None]):
            if tz is not None:
                if pendulum.has_test_now():
                    now = pendulum.get_test_now().in_tz(tz)
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
            year, month, day,
            hour, minute, second, microsecond,
            fold=1
        )
        if tz is not None:
            dt = tz.convert(dt)

        return cls(
            dt.year, dt.month, dt.day,
            dt.hour, dt.minute, dt.second, dt.microsecond,
            tzinfo=dt.tzinfo
        )

    @classmethod
    def from_format(cls, time, fmt, tz=UTC):
        """
        Create a DateTime instance from a specific format.

        :param fmt: The format
        :type fmt: str

        :param time: The time string
        :type time: str

        :param tz: The timezone
        :type tz: tzinfo or str or int or None

        :rtype: DateTime
        """
        formatter = FORMATTERS['alternative']

        parts = formatter.parse(time, fmt)
        actual_parts = {}

        # If timestamp has been specified
        # we use it and don't go any further
        if parts['timestamp'] is not None:
            return cls.create_from_timestamp(parts['timestamp'])

        if parts['quarter'] is not None:
            dt = pendulum.now().start_of('year')

            while dt.quarter != parts['quarter']:
                dt = dt.add(months=3)

            actual_parts['year'] = dt.year
            actual_parts['month'] = dt.month
            actual_parts['day'] = dt.day

        # If the date part has not been specified
        # we default to today
        if all([parts['year'] is None, parts['month'] is None, parts['day'] is None]):
            now = pendulum.now()

            parts['year'] = actual_parts['year'] = now.year
            parts['month'] = actual_parts['month'] = now.month
            parts['day'] = actual_parts['day'] = now.day

        # We replace any not set month/day value
        # with the first of each unit
        if any([parts['month'] is None, parts['day'] is None]):
            for part in ['month', 'day']:
                if parts[part] is None and actual_parts.get(part) is None:
                    actual_parts[part] = 1

        for part in ['year', 'month', 'day']:
            if parts[part] is not None:
                actual_parts[part] = parts[part]

        # If any of hour/minute/second/microsecond is not set
        # We assume start of corresponding value
        for part in ['hour', 'minute', 'second', 'microsecond']:
            if parts[part] is None:
                actual_parts[part] = 0
            else:
                actual_parts[part] = parts[part]

        if parts['day_of_year'] is not None:
            dt = pendulum.parse(f"{actual_parts['year']}-{parts['day_of_year']}")

            actual_parts['month'] = dt.month
            actual_parts['day'] = dt.day

        # Meridiem
        if parts['meridiem'] is not None:
            pass

        actual_parts['tz'] = parts['tz'] or tz

        return cls.create(**actual_parts)

    @classmethod
    def create_from_timestamp(cls, timestamp, tz=UTC):
        """
        Create a DateTime instance from a timestamp.

        :param timestamp: The timestamp
        :type timestamp: int or float

        :param tz: The timezone
        :type tz: Timezone or TimezoneInfo or str or int or None

        :rtype: DateTime
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
        return cls.instance(datetime.datetime.strptime(time, fmt))

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

        return self.tzinfo.tz.convert(self.replace(**kwargs))

    def timezone_(self, tz):
        return self.create(
            self.year, self.month, self.day,
            self.hour, self.minute, self.second, self.microsecond,
            tz=tz
        )

    def tz_(self, tz):
        return self.timezone_(tz)

    def timestamp_(self, timestamp, tz=UTC):
        return self.create_from_timestamp(timestamp, tz)

    @property
    def float_timestamp(self):
        return self.timestamp()

    @property
    def int_timestamp(self):
        # Workaround needed to avoid inaccuracy
        # for far into the future datetimes
        dt = datetime.datetime(
            self.year, self.month, self.day,
            self.hour, self.minute, self.second, self.microsecond,
            tzinfo=self.tzinfo
        )

        delta = dt - self._EPOCH

        return delta.days * SECONDS_PER_DAY + delta.seconds

    @property
    def offset(self):
        return self.get_offset()

    @property
    def offset_hours(self):
        return (self.get_offset()
                / SECONDS_PER_MINUTE
                / MINUTES_PER_HOUR)

    @property
    def timezone(self):
        if self.tzinfo is None:
            return None

        return self.tzinfo.tz

    @property
    def tz(self):
        return self.timezone

    @property
    def timezone_name(self):
        tz = self.timezone

        if self.timezone is None:
            return None

        return tz.name

    @property
    def age(self):
        return self.date().diff(self.now(self.tzinfo.tz).date()).in_years()

    def is_local(self):
        return self.offset == self.in_timezone(self._local_timezone()).offset

    def is_utc(self):
        return self.offset == 0

    def is_dst(self):
        return self.tzinfo.is_dst()

    def get_offset(self):
        return int(self.tzinfo.offset)

    def date(self):
        return Date.instance(super().date())

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

        :rtype: DateTime
        """
        return self.replace(
            year=int(year), month=int(month), day=int(day)
        )

    def at(self, hour, minute=0, second=0, microsecond=0):
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

        :rtype: DateTime
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

        :rtype: DateTime
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

        :rtype: DateTime
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

        :rtype: DateTime
        """
        tz = self._safe_create_datetime_zone(tz)

        return tz.convert(self)

    def in_tz(self, tz):
        """
        Set the instance's timezone from a string or object.

        :param value: The timezone
        :type value: Timezone or TimezoneInfo or str or int or None

        :rtype: DateTime
        """
        return self.in_timezone(tz)

    def with_timestamp(self, timestamp):
        """
        Set the date and time based on a Unix timestamp.

        :param timestamp: The timestamp
        :type timestamp: int or float
        :rtype: DateTime
        """
        dt = datetime.datetime.fromtimestamp(
            timestamp, UTC
        ).astimezone(self.tzinfo.tz)

        return self.instance(dt)

    # STRING FORMATTING

    def to_time_string(self):
        """
        Format the instance as time.

        :rtype: str
        """
        return self.format('HH:mm:ss')

    def to_datetime_string(self):
        """
        Format the instance as date and time.

        :rtype: str
        """
        return self.format('YYYY-MM-DD HH:mm:ss')

    def to_day_datetime_string(self):
        """
        Format the instance as day, date and time (in english).

        :rtype: str
        """
        return self.format('ddd, MMM D, YYYY h:mm A', locale='en')

    def to_atom_string(self):
        """
        Format the instance as ATOM.

        :rtype: str
        """
        return self._to_string('atom')

    def to_cookie_string(self):
        """
        Format the instance as COOKIE.

        :rtype: str
        """
        return self._to_string('cookie', locale='en')

    def to_iso8601_string(self):
        """
        Format the instance as ISO 8601.

        :rtype: str
        """
        return self._to_string('iso8601')

    def to_rfc822_string(self):
        """
        Format the instance as RFC 822.

        :rtype: str
        """
        return self._to_string('rfc822')

    def to_rfc850_string(self):
        """
        Format the instance as RFC 850.

        :rtype: str
        """
        return self._to_string('rfc850')

    def to_rfc1036_string(self):
        """
        Format the instance as RFC 1036.

        :rtype: str
        """
        return self._to_string('rfc1036')

    def to_rfc1123_string(self):
        """
        Format the instance as RFC 1123.

        :rtype: str
        """
        return self._to_string('rfc1123')

    def to_rfc2822_string(self):
        """
        Format the instance as RFC 2822.

        :rtype: str
        """
        return self._to_string('rfc2822')

    def to_rfc3339_string(self):
        """
        Format the instance as RFC 3339.

        :rtype: str
        """
        return self._to_string('rfc3339')

    def to_rss_string(self):
        """
        Format the instance as RSS.

        :rtype: str
        """
        return self._to_string('rss')

    def to_w3c_string(self):
        """
        Format the instance as W3C.

        :rtype: str
        """
        return self._to_string('w3c')

    def _to_string(self, fmt, locale=None):
        """
        Format the instance to a common string format.

        :param fmt: The name of the string format
        :type fmt: string

        :param locale: The locale to use
        :type locale: str or None

        :rtype: str
        """
        if fmt not in self._FORMATS:
            raise ValueError('Format [{}] is not supported'.format(fmt))

        fmt = self._FORMATS[fmt]
        if callable(fmt):
            return fmt(self)

        return self.format(fmt, locale=locale)

    def __str__(self):
        return self.isoformat('T')

    def __repr__(self):
        us = ''
        if self.microsecond:
            us = f', {self.microsecond}'

        repr_ = (
            f"{self.__class__.__name__}("
            f"{self.year}, {self.month}, {self.day}, "
            f"{self.hour}, {self.minute}, {self.second}{us}"
        )

        if self.tzinfo is not None:
            repr_ += f", tzinfo={self.tzinfo}"

        repr_ += f")"

        return repr_

    # Comparisons
    def between(self, dt1, dt2, equal=True):
        """
        Determines if the instance is between two others.

        :type dt1: datetime.datetime
        :type dt2: datetime.datetime

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

        :type dt1: DateTime or datetime
        :type dt2: DateTime or datetime

        :rtype: DateTime
        """
        if dt1 < dt2:
            return self.instance(dt1)

        return self.instance(dt2)

    def farthest(self, dt1, dt2):
        """
        Get the farthest date from the instance.

        :type dt1: datetime.datetime
        :type dt2: datetime.datetime

        :rtype: DateTime
        """
        dt1 = self.instance(dt1)
        dt2 = self.instance(dt2)

        if dt1 > dt2:
            return dt1

        return dt2

    def min_(self, dt=None):
        """
        Get the minimum instance between a given instance (default utcnow)
        and the current instance.

        :type dt: DateTime or datetime or str or int

        :rtype: DateTime
        """
        if dt is None:
            dt = self.now(self.timezone)

        if self < dt:
            return self

        return self.instance(dt)

    def minimum(self, dt=None):
        """
        Get the minimum instance between a given instance (default now)
        and the current instance.

        :type dt: DateTime or datetime or str or int

        :rtype: DateTime
        """
        return self.min_(dt)

    def max_(self, dt=None):
        """
        Get the maximum instance between a given instance (default now)
        and the current instance.

        :type dt: DateTime or datetime or str or int

        :rtype: DateTime
        """
        if dt is None:
            dt = self.now(self.timezone)

        if self > dt:
            return self

        return self.instance(dt)

    def maximum(self, dt=None):
        """
        Get the maximum instance between a given instance (default utcnow)
        and the current instance.

        :type dt: DateTime or datetime or str or int

        :rtype: DateTime
        """
        return self.max_(dt)

    def is_yesterday(self):
        """
        Determines if the instance is yesterday.

        :rtype: bool
        """
        return self.to_date_string() == self.yesterday(self.tzinfo.tz).to_date_string()

    def is_today(self):
        """
        Determines if the instance is today.

        :rtype: bool
        """
        return self.to_date_string() == self.now(self.tzinfo.tz).to_date_string()

    def is_tomorrow(self):
        """
        Determines if the instance is tomorrow.

        :rtype: bool
        """
        return self.to_date_string() == self.tomorrow(self.tzinfo.tz).to_date_string()

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
        return self.create(
            self.year, 12, 28, 0, 0, 0, tz=self.tzinfo.tz
        ).isocalendar()[1] == 53

    def is_same_day(self, dt):
        """
        Checks if the passed in date is the same day as the instance current day.

        :type dt: DateTime or datetime or str or int

        :rtype: bool
        """
        dt = self.instance(dt)

        return self.to_date_string() == dt.to_date_string()

    def is_birthday(self, dt=None):
        """
        Check if its the birthday. Compares the date/month values of the two dates.

        :rtype: bool
        """
        if dt is None:
            dt = self.now(self.tzinfo.tz)

        instance = self.instance(dt)

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

        :rtype: DateTime
        """
        dt = datetime.datetime(
            self.year, self.month, self.day,
            self.hour, self.minute, self.second, self.microsecond,
            tzinfo=self.tzinfo
        )
        dt = add_duration(
            dt,
            years=years, months=months, weeks=weeks, days=days,
            hours=hours, minutes=minutes, seconds=seconds,
            microseconds=microseconds
        )

        if dt.tzinfo is None:
            return self.instance(dt, tz=None)

        if any([years, months, weeks, days]):
            # If we specified any of years, months, weeks or days
            # we will not apply the transition (if any)
            return self.create(
                dt.year, dt.month, dt.day,
                dt.hour, dt.minute, dt.second, dt.microsecond,
                tz=self.tzinfo
            )

        # Else, we need to apply the transition properly (if any)
        dt = self.tzinfo.tz.convert(dt)

        return self.__class__(
            dt.year, dt.month, dt.day,
            dt.hour, dt.minute, dt.second, dt.microsecond,
            tzinfo=dt.tzinfo
        )

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

        :rtype: DateTime
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
        :type delta: pendulum.Duration or datetime.timedelta

        :rtype: DateTime
        """
        if isinstance(delta, (pendulum.duration, pendulum.period)):
            return self.add(
                years=delta.years,
                months=delta.months,
                weeks=delta.weeks,
                days=delta.remaining_days,
                hours=delta.hours,
                minutes=delta.minutes,
                seconds=delta.remaining_seconds,
                microseconds=delta.microseconds
            )

        return self.add(days=delta.days, seconds=delta.seconds,
                        microseconds=delta.microseconds)

    def subtract_timedelta(self, delta):
        """
        Remove timedelta duration from the instance.

        :param delta: The timedelta instance
        :type delta: pendulum.Duration or datetime.timedelta

        :rtype: DateTime
        """
        if isinstance(delta, (pendulum.duration, pendulum.period)):
            return self.subtract(
                years=delta.years,
                months=delta.months,
                weeks=delta.weeks,
                days=delta.remaining_days,
                hours=delta.hours,
                minutes=delta.minutes,
                seconds=delta.remaining_seconds,
                microseconds=delta.microseconds
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
        Returns the difference between two DateTime objects represented as a Duration.

        :type dt: DateTime or None

        :param abs: Whether to return an absolute interval or not
        :type abs: bool

        :rtype: Period
        """
        if dt is None:
            dt = self.now(self.tzinfo.tz)

        return Period(self, self.instance(dt), absolute=abs)

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

        :rtype: DateTime
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

        :rtype: DateTime
        """
        if unit not in self._MODIFIERS_VALID_UNITS:
            raise ValueError('Invalid unit "%s" for end_of()' % unit)

        return getattr(self, '_end_of_%s' % unit)()

    def _start_of_second(self):
        """
        Reset microseconds to 0.

        :rtype: DateTime
        """
        return self.microsecond_(0)

    def _end_of_second(self):
        """
        Set microseconds to 999999.

        :rtype: DateTime
        """
        return self.microsecond_(999999)

    def _start_of_minute(self):
        """
        Reset seconds and microseconds to 0.

        :rtype: DateTime
        """
        return self.replace(second=0, microsecond=0)

    def _end_of_minute(self):
        """
        Set seconds to 59 and microseconds to 999999.

        :rtype: DateTime
        """
        return self.replace(second=59, microsecond=999999)

    def _start_of_hour(self):
        """
        Reset minutes, seconds and microseconds to 0.

        :rtype: DateTime
        """
        return self.replace(minute=0, second=0, microsecond=0)

    def _end_of_hour(self):
        """
        Set minutes and seconds to 59 and microseconds to 999999.

        :rtype: DateTime
        """
        return self.replace(minute=59, second=59, microsecond=999999)

    def _start_of_day(self):
        """
        Reset the time to 00:00:00

        :rtype: DateTime
        """
        return self.at(0, 0, 0)

    def _end_of_day(self):
        """
        Reset the time to 23:59:59.999999

        :rtype: DateTime
        """
        return self.at(23, 59, 59, 999999)

    def _start_of_month(self):
        """
        Reset the date to the first day of the month and the time to 00:00:00.

        :rtype: DateTime
        """
        return self.with_date_time(self.year, self.month, 1, 0, 0, 0)

    def _end_of_month(self):
        """
        Reset the date to the last day of the month
        and the time to 23:59:59.999999.

        :rtype: DateTime
        """
        return self.with_date_time(
            self.year, self.month, self.days_in_month, 23, 59, 59, 999999
        )

    def _start_of_year(self):
        """
        Reset the date to the first day of the year and the time to 00:00:00.

        :rtype: DateTime
        """
        return self.with_date_time(self.year, 1, 1, 0, 0, 0)

    def _end_of_year(self):
        """
        Reset the date to the last day of the year
        and the time to 23:59:59.999999

        :rtype: DateTime
        """
        return self.with_date_time(
            self.year, 12, 31, 23, 59, 59, 999999
        )

    def _start_of_decade(self):
        """
        Reset the date to the first day of the decade
        and the time to 00:00:00.

        :rtype: DateTime
        """
        year = self.year - self.year % YEARS_PER_DECADE
        return self.with_date_time(year, 1, 1, 0, 0, 0)

    def _end_of_decade(self):
        """
        Reset the date to the last day of the decade
        and the time to 23:59:59.999999.

        :rtype: DateTime
        """
        year = self.year - self.year % YEARS_PER_DECADE + YEARS_PER_DECADE - 1

        return self.with_date_time(
            year, 12, 31, 23, 59, 59, 999999
        )

    def _start_of_century(self):
        """
        Reset the date to the first day of the century
        and the time to 00:00:00.

        :rtype: DateTime
        """
        year = self.year - 1 - (self.year - 1) % YEARS_PER_CENTURY + 1

        return self.with_date_time(year, 1, 1, 0, 0, 0)

    def _end_of_century(self):
        """
        Reset the date to the last day of the century
        and the time to 23:59:59.999999.

        :rtype: DateTime
        """
        year = self.year - 1 - (self.year - 1) % YEARS_PER_CENTURY + YEARS_PER_CENTURY

        return self.with_date_time(
            year, 12, 31, 23, 59, 59, 999999
        )

    def _start_of_week(self):
        """
        Reset the date to the first day of the week
        and the time to 00:00:00.

        :rtype: DateTime
        """
        dt = self

        if self.day_of_week != self._week_starts_at:
            dt = self.previous(self._week_starts_at)

        return dt.start_of('day')

    def _end_of_week(self):
        """
        Reset the date to the last day of the week
        and the time to 23:59:59.

        :rtype: DateTime
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
        to indicate the desired day_of_week, ex. DateTime.MONDAY.

        :param day_of_week: The next day of week to reset to.
        :type day_of_week: int or None

        :param keep_time: Whether to keep the time information or not.
        :type keep_time: bool

        :rtype: DateTime
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
        to indicate the desired day_of_week, ex. DateTime.MONDAY.

        :param day_of_week: The previous day of week to reset to.
        :type day_of_week: int or None

        :param keep_time: Whether to keep the time information or not.
        :type keep_time: bool

        :rtype: DateTime
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
        Use the supplied consts to indicate the desired day_of_week, ex. DateTime.MONDAY.

        Supported units are month, quarter and year.

        :param unit: The unit to use
        :type unit: str

        :type day_of_week: int or None

        :rtype: DateTime
        """
        if unit not in ['month', 'quarter', 'year']:
            raise ValueError('Invalid unit "{}" for first_of()'.format(unit))

        return getattr(self, '_first_of_{}'.format(unit))(day_of_week)

    def last_of(self, unit, day_of_week=None):
        """
        Returns an instance set to the last occurrence
        of a given day of the week in the current unit.
        If no day_of_week is provided, modify to the last day of the unit.
        Use the supplied consts to indicate the desired day_of_week, ex. DateTime.MONDAY.

        Supported units are month, quarter and year.

        :param unit: The unit to use
        :type unit: str

        :type day_of_week: int or None

        :rtype: DateTime
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
        to indicate the desired day_of_week, ex. DateTime.MONDAY.

        Supported units are month, quarter and year.

        :param unit: The unit to use
        :type unit: str

        :type nth: int

        :type day_of_week: int or None

        :rtype: DateTime
        """
        if unit not in ['month', 'quarter', 'year']:
            raise ValueError('Invalid unit "{}" for first_of()'.format(unit))

        dt = getattr(self, '_nth_of_{}'.format(unit))(nth, day_of_week)
        if dt is False:
            raise DateTimeException('Unable to find occurence {} of {} in {}'.format(
                                     nth, self._days[day_of_week], unit))

        return dt

    def _first_of_month(self, day_of_week):
        """
        Modify to the first occurrence of a given day of the week
        in the current month. If no day_of_week is provided,
        modify to the first day of the month. Use the supplied consts
        to indicate the desired day_of_week, ex. DateTime.MONDAY.

        :type day_of_week: int

        :rtype: DateTime
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
        to indicate the desired day_of_week, ex. DateTime.MONDAY.

        :type day_of_week: int or None

        :rtype: DateTime
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
        to indicate the desired day_of_week, ex. DateTime.MONDAY.

        :type nth: int

        :type day_of_week: int or None

        :rtype: DateTime
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
        to indicate the desired day_of_week, ex. DateTime.MONDAY.

        :type day_of_week: int or None

        :rtype: DateTime
        """
        return self.on(self.year, self.quarter * 3 - 2, 1).first_of('month', day_of_week)

    def _last_of_quarter(self, day_of_week=None):
        """
        Modify to the last occurrence of a given day of the week
        in the current quarter. If no day_of_week is provided,
        modify to the last day of the quarter. Use the supplied consts
        to indicate the desired day_of_week, ex. DateTime.MONDAY.

        :type day_of_week: int or None

        :rtype: DateTime
        """
        return self.on(self.year, self.quarter * 3, 1).last_of('month', day_of_week)

    def _nth_of_quarter(self, nth, day_of_week):
        """
        Modify to the given occurrence of a given day of the week
        in the current quarter. If the calculated occurrence is outside,
        the scope of the current quarter, then return False and no
        modifications are made. Use the supplied consts
        to indicate the desired day_of_week, ex. DateTime.MONDAY.

        :type nth: int

        :type day_of_week: int or None

        :rtype: DateTime
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
        to indicate the desired day_of_week, ex. DateTime.MONDAY.

        :type day_of_week: int or None

        :rtype: DateTime
        """
        return self.month_(1).first_of('month', day_of_week)

    def _last_of_year(self, day_of_week=None):
        """
        Modify to the last occurrence of a given day of the week
        in the current year. If no day_of_week is provided,
        modify to the last day of the year. Use the supplied consts
        to indicate the desired day_of_week, ex. DateTime.MONDAY.

        :type day_of_week: int or None

        :rtype: DateTime
        """
        return self.month_(MONTHS_PER_YEAR).last_of('month', day_of_week)

    def _nth_of_year(self, nth, day_of_week):
        """
        Modify to the given occurrence of a given day of the week
        in the current year. If the calculated occurrence is outside,
        the scope of the current year, then return False and no
        modifications are made. Use the supplied consts
        to indicate the desired day_of_week, ex. DateTime.MONDAY.

        :type nth: int

        :type day_of_week: int or None

        :rtype: DateTime
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

        :type dt: DateTime or datetime

        :rtype: DateTime
        """
        if dt is None:
            dt = self.now(self.tzinfo.tz)

        diff = self.diff(dt, False)
        return self.add(microseconds=(diff.in_seconds() * 1000000 + diff.microseconds) // 2)

    def __sub__(self, other):
        if isinstance(other, datetime.timedelta):
            return self.subtract_timedelta(other)

        if not isinstance(other, datetime.datetime):
            return NotImplemented

        return self.instance(other).diff(self, False)

    def __rsub__(self, other):
        if not isinstance(other, datetime.datetime):
            return NotImplemented

        return self.diff(self.instance(other), False)

    def __add__(self, other):
        if not isinstance(other, datetime.timedelta):
            return NotImplemented

        return self.add_timedelta(other)

    def __radd__(self, other):
        return self.__add__(other)

    # Native methods override

    @classmethod
    def fromtimestamp(cls, t, tz=None):
        return cls.instance(datetime.datetime.fromtimestamp(t, tz=tz), tz=tz)

    @classmethod
    def utcfromtimestamp(cls, t):
        return cls.instance(datetime.datetime.utcfromtimestamp(t), tz=None)

    @classmethod
    def fromordinal(cls, n):
        return cls.instance(datetime.datetime.fromordinal(n), tz=None)

    @classmethod
    def combine(cls, date, time):
        return cls.instance(datetime.datetime.combine(date, time), tz=None)

    def astimezone(self, tz=None):
        return self.instance(super().astimezone(tz))

    def replace(self, year=None, month=None, day=None, hour=None,
                minute=None, second=None, microsecond=None, tzinfo=True,
                fold=None):
        if year is None:
            year = self.year
        if month is None:
            month = self.month
        if day is None:
            day = self.day
        if hour is None:
            hour = self.hour
        if minute is None:
            minute = self.minute
        if second is None:
            second = self.second
        if microsecond is None:
            microsecond = self.microsecond
        if tzinfo is True:
            tzinfo = self.tzinfo
        if fold is None:
            fold = self.fold

        return self.instance(
            super().replace(
                year=year, month=month, day=day,
                hour=hour, minute=minute, second=second,
                microsecond=microsecond,
                tzinfo=tzinfo,
                fold=fold
            )
        )

    def __getnewargs__(self):
        return(self, )

    def _getstate(self, protocol=3):
        return (
            self.year, self.month, self.day,
            self.hour, self.minute, self.second, self.microsecond,
            self.tzinfo
        )

    def __reduce__(self):
        return self.__reduce_ex__(2)

    def __reduce_ex__(self, protocol):
        return self.__class__, self._getstate(protocol)


DateTime.min = DateTime.instance(datetime.datetime.min.replace(tzinfo=UTC))
DateTime.max = DateTime.instance(datetime.datetime.max.replace(tzinfo=UTC))
DateTime.EPOCH = DateTime(1970, 1, 1)
