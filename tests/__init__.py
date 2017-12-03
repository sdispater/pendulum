import sys
import pendulum
import struct

from unittest import TestCase
from contextlib import contextmanager

from pendulum import DateTime, Date, Time, Duration
from pendulum.tz import timezone, Timezone


class AbstractTestCase(TestCase):

    def setUp(self):
        pendulum.set_local_timezone(timezone('America/Toronto'))

        super(AbstractTestCase, self).setUp()

    def tearDown(self):
        pendulum.set_test_now()
        pendulum.set_formatter()
        pendulum.set_locale('en')
        pendulum.set_local_timezone()

    def assertDateTime(self, d, year, month, day,
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

    def assertDuration(self, pi, weeks, days=None,
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

    def assertIsInstanceOfDateTime(self, d):
        self.assertIsInstance(d, DateTime)

    def assertIsInstanceOfDate(self, d):
        self.assertIsInstance(d, Date)

    def assertIsInstanceOfTime(self, t):
        self.assertIsInstance(t, Time)

    def assertIsInstanceOfDuration(self, d):
        self.assertIsInstance(d, Duration)

    @contextmanager
    def wrap_with_test_now(self, dt=None):
        pendulum.set_test_now(dt or DateTime.now())

        yield

        pendulum.set_test_now()

    def skip_if_32bit(self):
        if struct.calcsize("P") * 8 == 32:
            self.skipTest('Tests only available for 64bit systems')

    def skip_if_windows(self):
        if sys.platform == 'win32':
            self.skipTest('Tests only available for UNIX systems')
