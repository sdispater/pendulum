# -*- coding: utf-8 -*-

from pendulum.interval import Interval

from .. import AbstractTestCase


class TotalMethodsTest(AbstractTestCase):

    def test_in_weeks(self):
        it = Interval(days=17)
        self.assertEqual(2.43, round(it.total_weeks(), 2))

    def test_in_days(self):
        it = Interval(days=3)
        self.assertEqual(3, it.total_days())

    def test_in_hours(self):
        it = Interval(days=3, minutes=72)
        self.assertEqual(73.2, it.total_hours())

    def test_in_minutes(self):
        it = Interval(minutes=6, seconds=72)
        self.assertEqual(7.2, it.total_minutes())

    def test_in_seconds(self):
        it = Interval(seconds=72, microseconds=123456)
        self.assertEqual(72.123456, it.total_seconds())
