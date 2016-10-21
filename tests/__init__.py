# -*- coding: utf-8 -*-

from unittest import TestCase
from contextlib import contextmanager

from pendulum import Pendulum, Date, Interval
from pendulum.tz import LocalTimezone, timezone, Timezone


class AbstractTestCase(TestCase):

    def setUp(self):
        LocalTimezone.set_local_timezone(timezone('America/Toronto'))

        super(AbstractTestCase, self).setUp()

    def tearDown(self):
        LocalTimezone.set_local_timezone()
        Pendulum.reset_to_string_format()
        Date.reset_to_string_format()
        Pendulum.set_transition_rule(Timezone.POST_TRANSITION)
        Pendulum.set_formatter()
        Date.set_formatter()

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

    def assertInterval(self, pi, weeks, days=None,
                       hours=None, minutes=None, seconds=None,
                       microseconds=None):
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

        if microseconds is not None:
            expected['microseconds'] = pi.microseconds
            actual['microseconds'] = microseconds

        self.assertEqual(expected, actual)

    def assertIsInstanceOfPendulum(self, d):
        self.assertIsInstance(d, Pendulum)

    def assertIsInstanceOfDate(self, d):
        self.assertIsInstance(d, Date)

    def assertIsInstanceOfInterval(self, d):
        self.assertIsInstance(d, Interval)

    @contextmanager
    def wrap_with_test_now(self, dt=None):
        Pendulum.set_test_now(dt or Pendulum.now())

        yield

        Pendulum.set_test_now()
