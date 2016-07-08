# -*- coding: utf-8 -*-

from datetime import timedelta

from .translator import Translator


class Interval(timedelta):

    _y = None
    _m = None
    _w = None
    _d = None
    _h = None
    _i = None
    _s = None
    _invert = None

    _translator = None

    def __init__(self, days=0, seconds=0, microseconds=0,
                milliseconds=0, minutes=0, hours=0, weeks=0):
        total = self.total_seconds()
        m = 1
        if total < 0:
            m = -1

        self._microseconds = total - int(total)
        self._seconds = abs(int(total)) % 86400 * m
        self._days = abs(int(total)) // 86400 * m

    @classmethod
    def instance(cls, delta):
        """
        Creates a Interval from a timedelta

        :type delta: timedelta

        :rtype: Interval
        """
        return cls(days=delta.days, seconds=delta.seconds, microseconds=delta.microseconds)

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
        if not cls.translator().register_resource(locale):
            return False

        cls.translator().locale = locale

        return True

    def total_minutes(self):
        return self.total_seconds() / 60

    def total_hours(self):
        return self.total_seconds() / 3600

    def total_days(self):
        return self.total_seconds() / 86400

    def total_weeks(self):
        return self.total_days() / 7

    def total_months(self):
        return round(self.total_days() / 30.436875, 1)

    def total_years(self):
        return round(self.total_days() / 365.2425, 1)

    @property
    def years(self):
        if self._y is None:
            days = self._days
            self._y = int(round(abs(days) / 365, 1) * self._sign(days))

        return self._y

    @property
    def months(self):
        if self._m is None:
            days = self._days
            self._m = int(round(abs(days) / 30.436875, 1) % 12 * self._sign(days))

        return self._m

    @property
    def weeks(self):
        return self.days // 7

    @property
    def days(self):
        return self._days

    @property
    def days_exclude_weeks(self):
        return self._days % 7 * self._sign(self._days)

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
        if self._s is None:
            self._s = self._seconds
            self._s = self._s % 60 * self._sign(self._s)

        return self._s

    @property
    def invert(self):
        if self._invert is None:
            self._invert = self.total_seconds() < 0

        return self._invert

    def in_years(self):
        return int(self.total_years())

    def in_months(self):
        return int(self.total_months())

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

    def in_words(self, locale=None):
        """
        Get the current interval in words in the current locale.

        Ex: 6 jours 23 heures 58 minutes

        :rtype: str
        """
        periods = [
            ('week', self.weeks),
            ('day', self.days_exclude_weeks),
            ('hour', self.hours),
            ('minute', self.minutes),
            ('second', self.seconds)
        ]

        parts = []
        for period in periods:
            unit, count = period
            if abs(count) > 0:
                parts.append(
                    self.translator().transchoice(unit, count, {'count': count}, locale=locale)
                )

        return ' '.join(parts)

    def __str__(self):
        return self.in_words()

    def __repr__(self):
        return '<{0} [{1}]>'.format(self.__class__.__name__, str(self))

    def __add__(self, other):
        if isinstance(other, timedelta):
            return Interval(seconds=self.total_seconds() + other.total_seconds())

        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, timedelta):
            # for CPython compatibility, we cannot use
            # our __class__ here, but need a real timedelta
            return Interval(seconds=self.total_seconds() - other.total_seconds())

        return NotImplemented

    def __neg__(self):
        # for CPython compatibility, we cannot use
        # our __class__ here, but need a real timedelta
        return Interval(seconds=-self.total_seconds())


class AbsoluteInterval(Interval):

    def total_seconds(self):
        return abs(super(AbsoluteInterval, self).total_seconds())

    @property
    def weeks(self):
        return abs(super(AbsoluteInterval, self).weeks)

    @property
    def days(self):
        return abs(super(AbsoluteInterval, self).days)

    @property
    def hours(self):
        return abs(super(AbsoluteInterval, self).hours)

    @property
    def minutes(self):
        return abs(super(AbsoluteInterval, self).minutes)

    @property
    def seconds(self):
        return abs(super(AbsoluteInterval, self).seconds)

    @property
    def microseconds(self):
        return abs(super(AbsoluteInterval, self).microseconds)

    @property
    def invert(self):
        return super(AbsoluteInterval, self).total_seconds() < 0

    def _sign(self, value):
        return 1
