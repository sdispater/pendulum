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
    _invert = None

    @classmethod
    def instance(cls, delta):
        """
        Creates a PendulumInterval from a timedelta

        :type delta: timedelta

        :rtype: PendulumInterval
        """
        return cls(days=delta.days, seconds=delta.seconds, microseconds=delta.microseconds)

    def total_minutes(self):
        return int(math.floor(round(self.total_seconds() / 60, 1)))

    def total_hours(self):
        return int(math.floor(round(self.total_minutes() / 60, 1)))

    def total_days(self):
        return int(math.floor(round(self.total_hours() / 24, 1)))

    def total_months(self):
        return int(math.floor(round(self.total_days() / 30.436875, 1)))

    def total_years(self):
        return int(math.floor(round(self.total_days() / 365.2425, 1)))

    @property
    def y(self):
        if self._y is None:
            self._y = self.total_years()

        return self._y

    @property
    def m(self):
        if self._m is None:
            if self.invert:
                self._m = int(round(self.total_months()))
            else:
                self._m = int(self.total_months())

        return self._m

    @property
    def d(self):
        if self._d is None:
            if self.invert:
                self._d = int(round(self.s / (60 * 60 * 24), 2))
            else:
                self._d = int(self.s / (60 * 60 * 24))

        return self._d

    @property
    def h(self):
        if self._h is None:
            if self.invert:
                self._h = int(round(self.s / 3600, 2))
            else:
                self._h = int(self.s / 3600)

        return self._h

    @property
    def i(self):
        if self._i is None:
            if self.invert:
                self._i = int(round(self.s / 60, 2))
            else:
                self._i = int(self.s / 60)

        return self._i

    @property
    def s(self):
        if self._s is None:
            if self.invert:
                self._s = int(round(self.total_seconds()))
            else:
                self._s = int(self.total_seconds())

        return self._s

    @property
    def invert(self):
        if self._invert is None:
            self._invert = self.total_seconds() < 0

        return self._invert


class AbsolutePendulumInterval(PendulumInterval):
    
    def total_seconds(self):
        return abs(super(AbsolutePendulumInterval, self).total_seconds())

    @property
    def invert(self):
        return super(AbsolutePendulumInterval, self).total_seconds() < 0
