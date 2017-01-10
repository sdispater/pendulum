# -*- coding: utf-8 -*-

from datetime import timedelta

from .mixins.interval import (
    WordableIntervalMixin
)

from .constants import (
    SECONDS_PER_DAY, SECONDS_PER_HOUR,
    SECONDS_PER_MINUTE
)


def _divide_and_round(a, b):
    """divide a by b and round result to the nearest integer

    When the ratio is exactly half-way between two integers,
    the even integer is returned.
    """
    # Based on the reference implementation for divmod_near
    # in Objects/longobject.c.
    q, r = divmod(a, b)
    # round up if either r / b > 0.5, or r / b == 0.5 and q is odd.
    # The expression r / b > 0.5 is equivalent to 2 * r > b if b is
    # positive, 2 * r < b if b negative.
    r *= 2
    greater_than_half = r > b if b > 0 else r < b
    if greater_than_half or r == b and q % 2 == 1:
        q += 1

    return q


class BaseInterval(timedelta):
    """
    Base class for all inherited interval classes.
    """

    _y = None
    _m = None
    _w = None
    _d = None
    _h = None
    _i = None
    _s = None
    _invert = None

    def __new__(cls, days=0, seconds=0, microseconds=0,
                milliseconds=0, minutes=0, hours=0, weeks=0):
        self = timedelta.__new__(
            cls, days, seconds, microseconds,
            milliseconds, minutes, hours, weeks
        )

        # Intuitive normalization
        total = self.total_seconds()

        m = 1
        if total < 0:
            m = -1

        self._microseconds = abs(round(total % 1 * 1e6)) * m
        self._seconds = abs(int(total)) % SECONDS_PER_DAY * m
        self._days = abs(int(total)) // SECONDS_PER_DAY * m

        return self

    def total_minutes(self):
        return self.total_seconds() / SECONDS_PER_MINUTE

    def total_hours(self):
        return self.total_seconds() / SECONDS_PER_HOUR

    def total_days(self):
        return self.total_seconds() / SECONDS_PER_DAY

    def total_weeks(self):
        return self.total_days() / 7

    @property
    def weeks(self):
        return abs(self.days) // 7 * self._sign(self._days)

    @property
    def days(self):
        return self._days

    @property
    def remaining_days(self):
        return abs(self._days) % 7 * self._sign(self._days)

    @property
    def hours(self):
        if self._h is None:
            seconds = self._seconds
            self._h = 0
            if abs(seconds) >= 3600:
                self._h = (abs(seconds) // 3600 % 24) * self._sign(seconds)

        return self._h

    @property
    def minutes(self):
        if self._i is None:
            seconds = self._seconds
            self._i = 0
            if abs(seconds) >= 60:
                self._i = (abs(seconds) // 60 % 60) * self._sign(seconds)

        return self._i

    @property
    def seconds(self):
        return self._seconds

    @property
    def remaining_seconds(self):
        if self._s is None:
            self._s = self._seconds
            self._s = abs(self._s) % 60 * self._sign(self._s)

        return self._s

    @property
    def microseconds(self):
        return self._microseconds

    @property
    def invert(self):
        if self._invert is None:
            self._invert = self.total_seconds() < 0

        return self._invert

    def in_weeks(self):
        return int(self.total_weeks())

    def in_days(self):
        return int(self.total_days())

    def in_hours(self):
        return int(self.total_hours())

    def in_minutes(self):
        return int(self.total_minutes())

    def in_seconds(self):
        return int(self.total_seconds())

    def _sign(self, value):
        if value < 0:
            return -1

        return 1

    def as_timedelta(self):
        """
        Return the interval as a native timedelta.

        :rtype: timedelta
        """
        return timedelta(seconds=self.total_seconds())


class Interval(WordableIntervalMixin, BaseInterval):
    """
    Replacement for the standard timedelta class.

    Provides several improvements over the base class.
    """

    @classmethod
    def instance(cls, delta):
        """
        Creates a Interval from a timedelta

        :type delta: timedelta

        :rtype: Interval
        """
        return cls(days=delta.days, seconds=delta.seconds, microseconds=delta.microseconds)

    def __add__(self, other):
        if isinstance(other, timedelta):
            return self.__class__(seconds=self.total_seconds() + other.total_seconds())

        return NotImplemented

    __radd__ = __add__

    def __sub__(self, other):
        if isinstance(other, timedelta):
            return self.__class__(seconds=self.total_seconds() - other.total_seconds())

        return NotImplemented

    def __neg__(self):
        return self.__class__(seconds=-self.total_seconds())

    def _to_microseconds(self):
        return ((self._days * (24*3600) + self._seconds) * 1000000 +
                self._microseconds)

    def __mul__(self, other):
        if isinstance(other, int):
            return self.__class__(seconds=self.total_seconds() * other)

        if isinstance(other, float):
            usec = self._to_microseconds()
            a, b = other.as_integer_ratio()

            return self.__class__(0, 0, _divide_and_round(usec * a, b))

        return NotImplemented

    __rmul__ = __mul__

    def __floordiv__(self, other):
        if not isinstance(other, (int, timedelta)):
            return NotImplemented

        usec = self._to_microseconds()
        if isinstance(other, timedelta):
            return usec // other._to_microseconds()

        if isinstance(other, int):
            return self.__class__(0, 0, usec // other)

    def __truediv__(self, other):
        if not isinstance(other, (int, float, timedelta)):
            return NotImplemented

        usec = self._to_microseconds()
        if isinstance(other, timedelta):
            return usec / other._to_microseconds()

        if isinstance(other, int):
            return self.__class__(0, 0, _divide_and_round(usec, other))

        if isinstance(other, float):
            a, b = other.as_integer_ratio()

            return self.__class__(0, 0, _divide_and_round(b * usec, a))

    __div__ = __floordiv__

    def __mod__(self, other):
        if isinstance(other, timedelta):
            r = self._to_microseconds() % other._to_microseconds()

            return self.__class__(0, 0, r)

        return NotImplemented

    def __divmod__(self, other):
        if isinstance(other, timedelta):
            q, r = divmod(self._to_microseconds(),
                          other._to_microseconds())

            return q, self.__class__(0, 0, r)

        return NotImplemented

Interval.min = Interval(-999999999)
Interval.max = Interval(days=999999999, hours=23,
                        minutes=59, seconds=59,
                        microseconds=999999)
Interval.resolution = Interval(microseconds=1)


class AbsoluteInterval(Interval):
    """
    Interval that expresses a time difference in absolute values.
    """

    def __new__(cls, days=0, seconds=0, microseconds=0,
                milliseconds=0, minutes=0, hours=0, weeks=0):
        self = timedelta.__new__(
            cls, days, seconds, microseconds,
            milliseconds, minutes, hours, weeks
        )

        # We need to compute the total_seconds() value
        # on a native timedelta object
        delta = timedelta(
            days, seconds, microseconds,
            milliseconds, minutes, hours, weeks
        )

        # Intuitive normalization
        self._total = delta.total_seconds()
        total = abs(self._total)

        self._microseconds = round(total % 1 * 1e6)
        self._seconds = int(total) % SECONDS_PER_DAY
        self._days = int(total) // SECONDS_PER_DAY

        return self

    def total_seconds(self):
        return abs(self._total)

    @property
    def invert(self):
        if self._invert is None:
            self._invert = self._total < 0

        return self._invert
