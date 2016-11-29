# -*- coding: utf-8 -*-

import sys
import pendulum
import struct

from unittest import TestCase
from contextlib import contextmanager

from pendulum import Pendulum, Date, Time, Interval
from pendulum.tz import LocalTimezone, timezone, Timezone

PY36 = sys.version_info >= (3, 6)


class AbstractTestCase(TestCase):

    def setUp(self):
        LocalTimezone.set_local_timezone(timezone('America/Toronto'))

        super(AbstractTestCase, self).setUp()

    def tearDown(self):
        pendulum.set_test_now()
        pendulum.set_formatter()
        pendulum.set_locale('en')
        LocalTimezone.set_local_timezone()
        Pendulum.reset_to_string_format()
        Date.reset_to_string_format()
        Time.reset_to_string_format()
        Pendulum.set_transition_rule(Timezone.POST_TRANSITION)

    def assertPendulum(self, d, year, month, day,
                       hour=None, minute=None, second=None, microsecond=None):
        self.assertEqual(year, d.year)
        self.assertEqual(month, d.month)
        self.assertEqual(day, d.day)

        if hour is not None:
            self.assertEqual(hour, d.hour)

        if minute is not None:
            self.assertEqual(minute, d.minute)

        if second is not None:
            self.assertEqual(second, d.second)

        if microsecond is not None:
            self.assertEqual(microsecond, d.microsecond)

    def assertDate(self, d, year, month, day):
        self.assertEqual(year, d.year)
        self.assertEqual(month, d.month)
        self.assertEqual(day, d.day)

    def assertTime(self, t, hour, minute, second, microsecond=None):
        self.assertEqual(hour, t.hour)
        self.assertEqual(minute, t.minute)
        self.assertEqual(second, t.second)

        if microsecond is not None:
            self.assertEqual(microsecond, t.microsecond)

    def assertInterval(self, pi, weeks, days=None,
                       hours=None, minutes=None, seconds=None,
                       microseconds=None):
        expected = {'weeks': pi.weeks}
        actual = {'weeks': weeks}

        if days is not None:
            expected['days'] = pi.remaining_days
            actual['days'] = days

        if hours is not None:
            expected['hours'] = pi.hours
            actual['hours'] = hours

        if minutes is not None:
            expected['minutes'] = pi.minutes
            actual['minutes'] = minutes

        if seconds is not None:
            expected['seconds'] = pi.remaining_seconds
            actual['seconds'] = seconds

        if microseconds is not None:
            expected['microseconds'] = pi.microseconds
            actual['microseconds'] = microseconds

        self.assertEqual(expected, actual)

    def assertIsInstanceOfPendulum(self, d):
        self.assertIsInstance(d, Pendulum)

    def assertIsInstanceOfDate(self, d):
        self.assertIsInstance(d, Date)

    def assertIsInstanceOfTime(self, t):
        self.assertIsInstance(t, Time)

    def assertIsInstanceOfInterval(self, d):
        self.assertIsInstance(d, Interval)

    @contextmanager
    def wrap_with_test_now(self, dt=None):
        pendulum.set_test_now(dt or Pendulum.now())

        yield

        pendulum.set_test_now()

    def skip_if_not_36(self):
        if not PY36:
            self.skipTest('Tests only available for Python 3.6')

    def skip_if_36(self):
        if PY36:
            self.skipTest('Tests only available for Python <= 3.5')

    def skip_if_32bit(self):
        if struct.calcsize("P") * 8 == 32:
            self.skipTest('Tests only available for 64bit systems')

    def skip_if_windows(self):
        if sys.platform == 'win32':
            self.skipTest('Tests only available for UNIX systems')
