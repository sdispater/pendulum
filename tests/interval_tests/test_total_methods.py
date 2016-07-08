# -*- coding: utf-8 -*-

from pendulum.pendulum_interval import PendulumInterval

from .. import AbstractTestCase


class TotalMethodsTest(AbstractTestCase):

    def test_total_years(self):
        it = PendulumInterval(days=365)
        self.assertEqual(1, it.total_years())

    def test_in_months(self):
        it = PendulumInterval(days=75)
        self.assertEqual(2.5, it.total_months())

    def test_in_weeks(self):
        it = PendulumInterval(days=17)
        self.assertEqual(2.43, round(it.total_weeks(), 2))

    def test_in_days(self):
        it = PendulumInterval(days=3)
        self.assertEqual(3, it.total_days())

    def test_in_hours(self):
        it = PendulumInterval(days=3, minutes=72)
        self.assertEqual(73.2, it.total_hours())

    def test_in_minutes(self):
        it = PendulumInterval(minutes=6, seconds=72)
        self.assertEqual(7.2, it.total_minutes())

    def test_in_seconds(self):
        it = PendulumInterval(seconds=72, microseconds=123456)
        self.assertEqual(72.123456, it.total_seconds())
