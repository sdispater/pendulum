# -*- coding: utf-8 -*-

from .. import AbstractTestCase

import pendulum
from datetime import timedelta
from pendulum import Time


class AddTest(AbstractTestCase):

    def test_add_hours_positive(self):
        self.assertEqual(13, Time(12, 34, 56).add(hours=1).hour)

    def test_add_hours_zero(self):
        self.assertEqual(12, Time(12, 34, 56).add(hours=0).hour)

    def test_add_hours_negative(self):
        self.assertEqual(11, Time(12, 34, 56).add(hours=-1).hour)

    def test_add_minutes_positive(self):
        self.assertEqual(35, Time(12, 34, 56).add(minutes=1).minute)

    def test_add_minutes_zero(self):
        self.assertEqual(34, Time(12, 34, 56).add(minutes=0).minute)

    def test_add_minutes_negative(self):
        self.assertEqual(33, Time(12, 34, 56).add(minutes=-1).minute)

    def test_add_seconds_positive(self):
        self.assertEqual(57, Time(12, 34, 56).add(seconds=1).second)

    def test_add_seconds_zero(self):
        self.assertEqual(56, Time(12, 34, 56).add(seconds=0).second)

    def test_add_seconds_negative(self):
        self.assertEqual(55, Time(12, 34, 56).add(seconds=-1).second)

    def test_add_timedelta(self):
        delta = timedelta(seconds=45, microseconds=123456)
        d = Time(3, 12, 15, 654321)

        d = d.add_timedelta(delta)
        self.assertEqual(13, d.minute)
        self.assertEqual(0, d.second)
        self.assertEqual(777777, d.microsecond)

        d = Time(3, 12, 15, 654321)

        d = d + delta
        self.assertEqual(13, d.minute)
        self.assertEqual(0, d.second)
        self.assertEqual(777777, d.microsecond)

    def test_add_timedelta_with_days(self):
        delta = timedelta(days=3, seconds=45, microseconds=123456)
        d = Time(3, 12, 15, 654321)

        self.assertRaises(TypeError, d.add_timedelta, delta)

    def test_addition_invalid_type(self):
        d = Time(3, 12, 15, 654321)

        try:
            d + 3
            self.fail()
        except TypeError:
            pass

        try:
            3 + d
            self.fail()
        except TypeError:
            pass
