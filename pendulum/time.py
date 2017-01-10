# -*- coding: utf-8 -*-

from datetime import time, datetime, timedelta

from .interval import Interval, AbsoluteInterval
from .mixins.default import TranslatableMixin, FormattableMixing, TestableMixin
from .constants import (
    USECS_PER_SEC, SECS_PER_HOUR, SECS_PER_MIN
)


class Time(TranslatableMixin, FormattableMixing, TestableMixin, time):
    """
    Represents a time instance as hour, minute, second, microsecond.
    """

    def __init__(self, hour, minute=0, second=0, microsecond=0,
                 tzinfo=None, fold=0):
        """
        Constructor.

        :param hour: The hour.
        :type hour: int

        :param minute: The minute.
        :type minute: int

        :param second: The second
        :type second: int

        :param microsecond: The microsecond
        :type microsecond: int

        :param tzinfo: The timezone info (not used)
        :type tzinfo: tzinfo or None
        """
        self._hour = hour
        self._minute = minute
        self._second = second
        self._microsecond = microsecond
        self._tzinfo = tzinfo
        self._time = time(hour, minute, second, microsecond, tzinfo)
        self._fold = fold

    @classmethod
    def instance(cls, t, copy=True):
        """
        Creates a Time instance from a time object.

        It will raise a TypeError exception if the time
        is timezone aware.

        :param t: The time object
        :type t: time

        :param copy: Whether to return a copy of the instance or not.
        :type copy: bool

        :rtype: Time

        :raises: TypeError
        """
        if isinstance(t, Time) and not copy:
            return t

        return cls(t.hour, t.minute, t.second, t.microsecond, t.tzinfo)

    @classmethod
    def now(cls, with_microseconds=True):
        """
        Return a Time instance corresponding to the current time.

        It will return your local time.

        By default, it will include microseconds.
        Just set ``with_microseconds`` to ``False`` to exclude them.

        :param with_microseconds: Whether to include microseconds or not.
        :type with_microseconds: bool

        :rtype: Time
        """
        if cls.has_test_now():
            if not with_microseconds:
                return cls.get_test_now().replace(microsecond=0)

            return cls.get_test_now()

        now = datetime.now()

        microsecond = now.microsecond if with_microseconds else 0

        return cls(now.hour, now.minute, now.second, microsecond)

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

    # Comparisons

    def between(self, dt1, dt2, equal=True):
        """
        Determines if the instance is between two others.

        :type dt1: Time or time
        :type dt2: Time or time

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
        Get the closest time from the instance.

        :type dt1: Time or time
        :type dt2: Time or time

        :rtype: Time
        """
        dt1 = self.instance(dt1, False)
        dt2 = self.instance(dt2, False)

        if self.diff(dt1).in_seconds() < self.diff(dt2).in_seconds():
            return dt1

        return dt2

    def farthest(self, dt1, dt2):
        """
        Get the farthest time from the instance.

        :type dt1: Time or time
        :type dt2: Time or time

        :rtype: Time
        """
        dt1 = self.instance(dt1, False)
        dt2 = self.instance(dt2, False)

        if self.diff(dt1).in_seconds() > self.diff(dt2).in_seconds():
            return dt1

        return dt2

    def min_(self, dt=None):
        """
        Get the minimum instance between a given instance (default now)
        and the current instance.

        :type dt: Time or time

        :rtype: Time
        """
        if dt is None:
            dt = Time.now()

        if self < dt:
            return self

        return self.instance(dt, False)

    def minimum(self, dt=None):
        """
        Get the minimum instance between a given instance (default now)
        and the current instance.

        :type dt: Time or time

        :rtype: Time
        """
        return self.min_(dt)

    def max_(self, dt=None):
        """
        Get the maximum instance between a given instance (default now)
        and the current instance.

        :type dt: Time or time

        :rtype: Time
        """
        if dt is None:
            dt = Time.now()

        if self > dt:
            return self

        return self.instance(dt, False)

    def maximum(self, dt=None):
        """
        Get the maximum instance between a given instance (default now)
        and the current instance.

        :type dt: Time or time

        :rtype: Time
        """
        return self.max_(dt)

    def __hash__(self):
        return self._time.__hash__()

    # ADDITIONS AND SUBSTRACTIONS

    def add(self, hours=0, minutes=0, seconds=0, microseconds=0):
        """
        Add duration to the instance.

        :param hours: The number of hours
        :type hours: int

        :param minutes: The number of minutes
        :type minutes: int

        :param seconds: The number of seconds
        :type seconds: int

        :param microseconds: The number of microseconds
        :type microseconds: int

        :rtype: Time
        """
        from .pendulum import Pendulum

        return Pendulum.EPOCH.at(
            self._hour, self._minute, self._second, self._microsecond
        ).add(
            hours=hours,
            minutes=minutes,
            seconds=seconds,
            microseconds=microseconds
        ).time()

    def subtract(self, hours=0, minutes=0, seconds=0, microseconds=0):
        """
        Add duration to the instance.

        :param hours: The number of hours
        :type hours: int

        :param minutes: The number of minutes
        :type minutes: int

        :param seconds: The number of seconds
        :type seconds: int

        :param microseconds: The number of microseconds
        :type microseconds: int

        :rtype: Time
        """
        from .pendulum import Pendulum

        return Pendulum.EPOCH.at(
            self._hour, self._minute, self._second, self._microsecond
        ).subtract(
            hours=hours,
            minutes=minutes,
            seconds=seconds,
            microseconds=microseconds
        ).time()

    def add_timedelta(self, delta):
        """
        Add timedelta duration to the instance.

        :param delta: The timedelta instance
        :type delta: datetime.timedelta

        :rtype: Time
        """
        if delta.days:
            raise TypeError('Cannot timedelta with days to Time.')

        return self.add(
            seconds=delta.seconds,
            microseconds=delta.microseconds
        )

    def subtract_timedelta(self, delta):
        """
        Remove timedelta duration from the instance.

        :param delta: The timedelta instance
        :type delta: datetime.timedelta

        :rtype: Time
        """
        if delta.days:
            raise TypeError('Cannot timedelta with days to Time.')

        return self.subtract(
            seconds=delta.seconds,
            microseconds=delta.microseconds
        )

    def __add__(self, other):
        if not isinstance(other, timedelta):
            return NotImplemented

        return self.add_timedelta(other)

    def __sub__(self, other):
        if not isinstance(other, (Time, time, timedelta)):
            return NotImplemented

        if isinstance(other, timedelta):
            return self.subtract_timedelta(other)

        if isinstance(other, time):
            if other.tzinfo is not None:
                raise TypeError('Cannot subtract aware times to or from Time.')

            other = self.instance(other)

        return other.diff(self, False)

    def __rsub__(self, other):
        if not isinstance(other, (Time, time)):
            return NotImplemented

        if isinstance(other, time):
            if other.tzinfo is not None:
                raise TypeError('Cannot subtract aware times to or from Time.')

            other = self.instance(other)

        return other.__sub__(self)

    # DIFFERENCES

    def diff(self, dt=None, abs=True):
        """
        Returns the difference between two Time objects as an Interval.

        :type dt: Time or None

        :param abs: Whether to return an absolute interval or not
        :type abs: bool

        :rtype: Interval
        """
        if dt is None:
            dt = self.now()
        else:
            dt = self.instance(dt, False)

        us1 = (
            self.hour * SECS_PER_HOUR
            + self.minute * SECS_PER_MIN
            + self.second
        ) * USECS_PER_SEC

        us2 = (
            dt.hour * SECS_PER_HOUR
            + dt.minute * SECS_PER_MIN
            + dt.second
        ) * USECS_PER_SEC

        klass = Interval
        if abs:
            klass = AbsoluteInterval

        return klass(microseconds=us2 - us1)

    def diff_for_humans(self, other=None, absolute=False, locale=None):
        """
        Get the difference in a human readable format in the current locale.

        :type other: Time or time

        :param absolute: removes time difference modifiers ago, after, etc
        :type absolute: bool

        :param locale: The locale to use for localization
        :type locale: str

        :rtype: str
        """
        is_now = other is None

        if is_now:
            other = self.now()

        diff = self.diff(other)

        if diff.hours > 0:
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

    # String formatting

    def isoformat(self):
        return self._time.isoformat()

    # Testing aids

    @classmethod
    def set_test_now(cls, test_now=None):
        """
        Set a Time instance (real or mock) to be returned when a "now"
        instance is created.  The provided instance will be returned
        specifically under the following conditions:
            - A call to the classmethod now() method, ex. Time.now()

        To clear the test instance call this method using the default
        parameter of None.

        :type test_now: Date or Pendulum or None
        """
        from .pendulum import Pendulum

        if test_now is not None and not isinstance(test_now, (Pendulum, Time)):
            raise TypeError(
                'Time.set_test_now() only accepts a Time instance, '
                'a Pendulum instance or None.'
            )

        cls._test_now = test_now

    @classmethod
    def get_test_now(cls):
        if cls._test_now is None:
            return None

        if isinstance(cls._test_now, Time):
            return cls._test_now

        return cls._test_now.time()

    # Compatibility methods

    def replace(self, hour=None, minute=None, second=None, microsecond=None,
                tzinfo=True):
        if tzinfo is True:
            tzinfo = self._tzinfo

        hour = hour if hour is not None else self._hour
        minute = minute if minute is not None else self._minute
        second = second if second is not None else self._second
        microsecond = microsecond if microsecond is not None else self._microsecond

        return self.instance(
            self._time.replace(
                hour, minute, second, microsecond,
                tzinfo=tzinfo
            )
        )

    def utcoffset(self):
        return self._time.utcoffset()

    def dst(self):
        return self._time.dst()

    def tzname(self):
        if self._tzinfo is None:
            return None

        return self._time.tzname()

    def _getstate(self, protocol=3):
        tz = self.tzinfo

        return (
            self.hour, self.minute, self.second, self.microsecond,
            tz
        )

    def __reduce__(self):
        return self.__reduce_ex__(2)

    def __reduce_ex__(self, protocol):
        return self.__class__, self._getstate(protocol)

Time.min = Time(0, 0, 0)
Time.max = Time(23, 59, 59, 999999)
Time.resolution = Interval(microseconds=1)
