from datetime import timedelta
from pendulum import Duration
from pendulum.duration import AbsoluteDuration

from .. import AbstractTestCase


class ConstructTest(AbstractTestCase):

    def test_defaults(self):
        pi = Duration()
        self.assertIsInstanceOfDuration(pi)
        self.assertDuration(pi, 0, 0, 0, 0, 0)

    def test_weeks(self):
        pi = Duration(days=365)
        self.assertDuration(pi, 52)

        pi = Duration(days=13)
        self.assertDuration(pi, 1)

    def test_days(self):
        pi = Duration(days=6)
        self.assertDuration(pi, 0, 6, 0, 0, 0)

        pi = Duration(days=16)
        self.assertDuration(pi, 2, 2, 0, 0, 0)

    def test_hours(self):
        pi = Duration(seconds=3600 * 3)
        self.assertDuration(pi, 0, 0, 3, 0, 0)

    def test_minutes(self):
        pi = Duration(seconds=60 * 3)
        self.assertDuration(pi, 0, 0, 0, 3, 0)

        pi = Duration(seconds=60 * 3 + 12)
        self.assertDuration(pi, 0, 0, 0, 3, 12)

    def test_all(self):
        pi = Duration(days=1177, seconds=7284, microseconds=1000000)
        self.assertDuration(pi, 168, 1, 2, 1, 25)
        self.assertEqual(1177, pi.days)
        self.assertEqual(7285, pi.seconds)

    def test_instance(self):
        pi = Duration.instance(timedelta(days=1177, seconds=7284, microseconds=1000000))
        self.assertDuration(pi, 168, 1, 2, 1, 25)

    def test_absolute_interval(self):
        pi = AbsoluteDuration(days=-1177, seconds=-7284, microseconds=-1000001)
        self.assertDuration(pi, 168, 1, 2, 1, 25)
        self.assertEqual(1, pi.microseconds)
        self.assertTrue(pi.invert)

    def test_invert(self):
        pi = Duration(days=1177, seconds=7284, microseconds=1000000)
        self.assertFalse(pi.invert)

        pi = Duration(days=-1177, seconds=-7284, microseconds=-1000000)
        self.assertTrue(pi.invert)

    def test_as_timedelta(self):
        pi = Duration(seconds=3456.123456)
        self.assertDuration(pi, 0, 0, 0, 57, 36, 123456)
        delta = pi.as_timedelta()
        self.assertIsInstance(delta, timedelta)
        self.assertEqual(3456.123456, delta.total_seconds())
        self.assertEqual(3456, delta.seconds)
