# -*- coding: utf-8 -*-

import operator

from .interval import BaseInterval, Interval
from .mixins.interval import WordableIntervalMixin


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

    def range(self, unit):
        return list(self.xrange(unit))

    def xrange(self, unit):
        method = 'add'
        op = operator.le
        if not self._absolute and self.invert:
            method = 'subtract'
            op = operator.ge

        start, end = self.start, self.end
        while op(start, end):
            yield start

            start = getattr(start, method)(**{unit: 1})

    def as_interval(self):
        """
        Return the Period as an Interval.

        :rtype: Interval
        """
        return Interval(seconds=self.total_seconds())

    def exclude_from(self, *periods):
        """Exclude a period from the list of periods and return the list."""

        excluded_periods = []
        periods = list(periods)

        for period in periods:
            excluded_period = self._exclude(other=period)
            if excluded_period is not None:
                excluded_periods += excluded_period

        return excluded_periods

    def _exclude(self, other):
        excluded_periods = []
        if self.end > other.start:
            if self.start <= other.start:
                if self.end < other.end:
                    other = Period(
                        start=self.end,
                        end=other.end
                    )
                else:
                    # Do not add it (remove it)
                    return None
            elif self.start < other.end:
                if self.end < other.end:
                    # Insert a period before new one, the self splits
                    # a period in two periods.
                    excluded_periods.append(
                        Period(
                            start=self.end,
                            end=other.end
                        )
                    )
                    other = Period(
                        start=other.start,
                        end=self.start
                    )
                else:
                    other = Period(
                        start=other.start,
                        end=self.start
                    )
        excluded_periods.append(other)
        return excluded_periods

    def merge(self, *periods):
        periods = list(periods)
        periods.append(self)
        periods.sort()

        period = periods[0]
        merged_periods = []

        for i in range(1, len(periods)):
            next_period = periods[i]

            if next_period.start <= period.end:
                if next_period.end > period.end:
                    period = Period(
                        start=period.start,
                        end=next_period.end
                    )
                continue
            else:
                merged_periods.append(
                    period
                )
                period = next_period

        merged_periods.append(
            period
        )
        return merged_periods

    def __iter__(self):
        return self.xrange('days')

    def __contains__(self, item):
        from .pendulum import Pendulum

        if not isinstance(item, Pendulum):
            item = Pendulum.instance(item)

        return item.between(self.start, self.end)

    def __add__(self, other):
        return self.as_interval().__add__(other)

    __radd__ = __add__

    def __sub__(self, other):
        return self.as_interval().__sub__(other)

    def __neg__(self):
        return self.__class__(self.end, self.start, self._absolute)

    def __mul__(self, other):
        return self.as_interval().__mul__(other)

    __rmul__ = __mul__

    def __floordiv__(self, other):
        return self.as_interval().__floordiv__(other)

    def __truediv__(self, other):
        return self.as_interval().__truediv__(other)

    __div__ = __floordiv__

    def __mod__(self, other):
        return self.as_interval().__mod__(other)

    def __divmod__(self, other):
        return self.as_interval().__divmod__(other)

    def __abs__(self):
        return self.__class__(self.start, self.end, True)

    def __repr__(self):
        return '<Period [{} -> {}]>'.format(
            self._start, self._end
        )

    def __lt__(self, other):
        if self.start == other.start:
            return self.end < other.end
        return self.start < other.start
