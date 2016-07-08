# -*- coding: utf-8 -*-

from datetime import timedelta
from pendulum import PendulumInterval
from pendulum.pendulum_interval import AbsolutePendulumInterval

from .. import AbstractTestCase


class ConstructTest(AbstractTestCase):

    def test_defaults(self):
        pi = PendulumInterval()
        self.assertIsInstanceOfInterval(pi)
        self.assertInterval(pi, 0, 0, 0, 0, 0)

    def test_weeks(self):
        pi = PendulumInterval(days=365)
        self.assertInterval(pi, 52)

        pi = PendulumInterval(days=13)
        self.assertInterval(pi, 1)

    def test_days(self):
        pi = PendulumInterval(days=6)
        self.assertInterval(pi, 0, 6, 0, 0, 0)

        pi = PendulumInterval(days=16)
        self.assertInterval(pi, 2, 2, 0, 0, 0)

    def test_hours(self):
        pi = PendulumInterval(seconds=3600 * 3)
        self.assertInterval(pi, 0, 0, 3, 0, 0)

    def test_minutes(self):
        pi = PendulumInterval(seconds=60 * 3)
        self.assertInterval(pi, 0, 0, 0, 3, 0)

        pi = PendulumInterval(seconds=60 * 3 + 12)
        self.assertInterval(pi, 0, 0, 0, 3, 12)

    def test_all(self):
        pi = PendulumInterval(days=1177, seconds=7284, microseconds=1000000)
        self.assertInterval(pi, 168, 1, 2, 1, 25)

    def test_instance(self):
        pi = PendulumInterval.instance(timedelta(days=1177, seconds=7284, microseconds=1000000))
        self.assertInterval(pi, 168, 1, 2, 1, 25)

    def test_absolute_interval(self):
        pi = AbsolutePendulumInterval(days=-1177, seconds=-7284, microseconds=-1000001)
        self.assertInterval(pi, 168, 1, 2, 1, 25)
        self.assertEqual(999999, pi.microseconds)

    def test_invert(self):
        pi = PendulumInterval(days=1177, seconds=7284, microseconds=1000000)
        self.assertFalse(pi.invert)

        pi = PendulumInterval(days=-1177, seconds=-7284, microseconds=-1000000)
        self.assertTrue(pi.invert)
