# -*- coding: utf-8 -*-

import re
import math
from datetime import timedelta


class PendulumInterval(timedelta):

    _CUSTOM_FORMATTERS = ['P']
    _FORMATTERS_REGEX = re.compile('%%(%s)' % '|'.join(_CUSTOM_FORMATTERS))

    _y = None
    _m = None
    _d = None
    _h = None
    _i = None
    _s = None

    @classmethod
    def instance(cls, delta):
        """
        Creates a PendulumInterval from a timedelta

        :type delta: timedelta

        :rtype: PendulumInterval
        """
        return cls(days=delta.days, seconds=delta.seconds, microseconds=delta.microseconds)

    def total_minutes(self):
        return math.floor(round(self.total_seconds() / 60, 1))

    def total_hours(self):
        return math.floor(round(self.total_minutes() / 60, 1))

    def total_days(self):
        return math.floor(round(self.total_hours() / 24, 1))

    def total_months(self):
        return math.floor(round(self.total_days() / 30.436875, 1))

    def total_years(self):
        return math.floor(round(self.total_days() / 365.2425, 1))

    @property
    def y(self):
        if self._y is None:
            self._y = self.total_years()

        return self._y

    @property
    def m(self):
        if self._m is None:
            self._m = self.total_months()

        return self._m

    @property
    def d(self):
        if self._d is None:
            self._d = self.total_days()

        return self._d

    @property
    def h(self):
        if self._h is None:
            self._h = self.total_hours()

        return self._h

    @property
    def i(self):
        if self._i is None:
            self._i = self.total_minutes()

        return self._i

    @property
    def s(self):
        if self._s is None:
            self._s = self.total_seconds()

        return self._s


class AbsolutePendulumInterval(PendulumInterval):
    
    def total_seconds(self):
        return abs(super(AbsolutePendulumInterval, self).total_seconds())
