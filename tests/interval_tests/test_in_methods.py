# -*- coding: utf-8 -*-

from pendulum.pendulum_interval import PendulumInterval

from .. import AbstractTestCase


class InMethodsTest(AbstractTestCase):

    def test_in_years(self):
        it = PendulumInterval(days=365)
        self.assertEqual(1, it.in_years())

    def test_in_months(self):
        it = PendulumInterval(days=75)
        self.assertEqual(2, it.in_months())

    def test_in_weeks(self):
        it = PendulumInterval(days=17)
        self.assertEqual(2, it.in_weeks())

    def test_in_days(self):
        it = PendulumInterval(days=3)
        self.assertEqual(3, it.in_days())

    def test_in_hours(self):
        it = PendulumInterval(days=3, minutes=72)
        self.assertEqual(73, it.in_hours())

    def test_in_minutes(self):
        it = PendulumInterval(minutes=6, seconds=72)
        self.assertEqual(7, it.in_minutes())

    def test_in_seconds(self):
        it = PendulumInterval(seconds=72)
        self.assertEqual(72, it.in_seconds())
