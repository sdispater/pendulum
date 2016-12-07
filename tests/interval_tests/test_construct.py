# -*- coding: utf-8 -*-

from datetime import timedelta
from pendulum import Interval
from pendulum.interval import AbsoluteInterval

from .. import AbstractTestCase


class ConstructTest(AbstractTestCase):

    def test_defaults(self):
        pi = Interval()
        self.assertIsInstanceOfInterval(pi)
        self.assertInterval(pi, 0, 0, 0, 0, 0)

    def test_weeks(self):
        pi = Interval(days=365)
        self.assertInterval(pi, 52)

        pi = Interval(days=13)
        self.assertInterval(pi, 1)

    def test_days(self):
        pi = Interval(days=6)
        self.assertInterval(pi, 0, 6, 0, 0, 0)

        pi = Interval(days=16)
        self.assertInterval(pi, 2, 2, 0, 0, 0)

    def test_hours(self):
        pi = Interval(seconds=3600 * 3)
        self.assertInterval(pi, 0, 0, 3, 0, 0)

    def test_minutes(self):
        pi = Interval(seconds=60 * 3)
        self.assertInterval(pi, 0, 0, 0, 3, 0)

        pi = Interval(seconds=60 * 3 + 12)
        self.assertInterval(pi, 0, 0, 0, 3, 12)

    def test_all(self):
        pi = Interval(days=1177, seconds=7284, microseconds=1000000)
        self.assertInterval(pi, 168, 1, 2, 1, 25)
        self.assertEqual(1177, pi.days)
        self.assertEqual(7285, pi.seconds)

    def test_instance(self):
        pi = Interval.instance(timedelta(days=1177, seconds=7284, microseconds=1000000))
        self.assertInterval(pi, 168, 1, 2, 1, 25)

    def test_absolute_interval(self):
        pi = AbsoluteInterval(days=-1177, seconds=-7284, microseconds=-1000001)
        self.assertInterval(pi, 168, 1, 2, 1, 25)
        self.assertEqual(1, pi.microseconds)
        self.assertTrue(pi.invert)

    def test_invert(self):
        pi = Interval(days=1177, seconds=7284, microseconds=1000000)
        self.assertFalse(pi.invert)

        pi = Interval(days=-1177, seconds=-7284, microseconds=-1000000)
        self.assertTrue(pi.invert)

    def test_as_timedelta(self):
        pi = Interval(seconds=3456.123456)
        self.assertInterval(pi, 0, 0, 0, 57, 36, 123456)
        delta = pi.as_timedelta()
        self.assertIsInstance(delta, timedelta)
        self.assertEqual(3456.123456, delta.total_seconds())
        self.assertEqual(3456, delta.seconds)
