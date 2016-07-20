# -*- coding: utf-8 -*-

from .mixins.interval import WordableIntervalMixin
from .interval import BaseInterval


class Period(WordableIntervalMixin, BaseInterval):
    """
    Interval class that is aware of the datetimes that generated the
    time difference.
    """

    def __new__(cls, start, end, absolute=False):
        from .pendulum import Pendulum

        if absolute and start > end:
            end, start = start, end

        if isinstance(start, Pendulum):
            start = start._datetime

        if isinstance(end, Pendulum):
            end = end._datetime

        delta = end - start

        return super(Period, cls).__new__(
            cls, seconds=delta.total_seconds()
        )

    def __init__(self, start, end, absolute=False):
        from .pendulum import Pendulum

        super(Period, self).__init__()

        if not isinstance(start, Pendulum):
            start = Pendulum.instance(start)

        if not isinstance(end, Pendulum):
            end = Pendulum.instance(end)

        self._invert = False
        if start > end:
            self._invert = True

            if absolute:
                end, start = start, end

        self._absolute = absolute
        self._start = start
        self._end = end

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    def in_weekdays(self):
        start, end = self.start.start_of('day'), self.end.start_of('day')
        if not self._absolute and self.invert:
            start, end = self.end.start_of('day'), self.start.start_of('day')

        days = 0
        while start <= end:
            if start.is_weekday():
                days += 1

            start = start.add(days=1)

        return days * (-1 if not self._absolute and self.invert else 1)

    def in_weekend_days(self):
        start, end = self.start.start_of('day'), self.end.start_of('day')
        if not self._absolute and self.invert:
            start, end = self.end.start_of('day'), self.start.start_of('day')

        days = 0
        while start <= end:
            if start.is_weekend():
                days += 1

            start = start.add(days=1)

        return days * (-1 if not self._absolute and self.invert else 1)


