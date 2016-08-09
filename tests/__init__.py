# -*- coding: utf-8 -*-

from unittest import TestCase
from contextlib import contextmanager

from pendulum import Pendulum, Interval
from pendulum.tz import LocalTimezone, timezone


class AbstractTestCase(TestCase):

    def setUp(self):
        self._save_tz = LocalTimezone.get

        LocalTimezone.get = classmethod(lambda _: timezone('America/Toronto'))

        super(AbstractTestCase, self).setUp()

    def tearDown(self):
        LocalTimezone.get = self._save_tz
        Pendulum.reset_to_string_format()

    def assertPendulum(self, d, year, month, day, hour=None, minute=None, second=None):
        self.assertEqual(year, d.year)
        self.assertEqual(month, d.month)
        self.assertEqual(day, d.day)

        if hour is not None:
            self.assertEqual(hour, d.hour)

        if minute is not None:
            self.assertEqual(minute, d.minute)

        if second is not None:
            self.assertEqual(second, d.second)

    def assertInterval(self, pi, weeks, days=None,
                       hours=None, minutes=None, seconds=None):
        expected = {'weeks': pi.weeks}
        actual = {'weeks': weeks}

        if days is not None:
            expected['days'] = pi.days_exclude_weeks
            actual['days'] = days

        if hours is not None:
            expected['hours'] = pi.hours
            actual['hours'] = hours

        if minutes is not None:
            expected['minutes'] = pi.minutes
            actual['minutes'] = minutes

        if seconds is not None:
            expected['seconds'] = pi.seconds
            actual['seconds'] = seconds

        self.assertEqual(expected, actual)

    def assertIsInstanceOfPendulum(self, d):
        self.assertIsInstance(d, Pendulum)

    def assertIsInstanceOfInterval(self, d):
        self.assertIsInstance(d, Interval)

    @contextmanager
    def wrap_with_test_now(self, dt=None):
        Pendulum.set_test_now(dt or Pendulum.now())

        yield

        Pendulum.set_test_now()
