# -*- coding: utf-8 -*-

import pytz
from datetime import timedelta, time
from pendulum import Time

from .. import AbstractTestCase


class SubTest(AbstractTestCase):

    def test_sub_hours_positive(self):
        self.assertEqual(23, Time(0, 0, 0).subtract(hours=1).hour)

    def test_sub_hours_zero(self):
        self.assertEqual(0, Time(0, 0, 0).subtract(hours=0).hour)

    def test_sub_hours_negative(self):
        self.assertEqual(1, Time(0, 0, 0).subtract(hours=-1).hour)

    def test_sub_minutes_positive(self):
        self.assertEqual(59, Time(0, 0, 0).subtract(minutes=1).minute)

    def test_sub_minutes_zero(self):
        self.assertEqual(0, Time(0, 0, 0).subtract(minutes=0).minute)

    def test_sub_minutes_negative(self):
        self.assertEqual(1, Time(0, 0, 0).subtract(minutes=-1).minute)

    def test_sub_seconds_positive(self):
        self.assertEqual(59, Time(0, 0, 0).subtract(seconds=1).second)

    def test_sub_seconds_zero(self):
        self.assertEqual(0, Time(0, 0, 0).subtract(seconds=0).second)

    def test_sub_seconds_negative(self):
        self.assertEqual(1, Time(0, 0, 0).subtract(seconds=-1).second)

    def test_subtract_timedelta(self):
        delta = timedelta(seconds=16, microseconds=654321)
        d = Time(3, 12, 15, 777777)

        d = d.subtract_timedelta(delta)
        self.assertEqual(11, d.minute)
        self.assertEqual(59, d.second)
        self.assertEqual(123456, d.microsecond)

        d = Time(3, 12, 15, 777777)

        d = d - delta
        self.assertEqual(11, d.minute)
        self.assertEqual(59, d.second)
        self.assertEqual(123456, d.microsecond)

    def test_add_timedelta_with_days(self):
        delta = timedelta(days=3, seconds=45, microseconds=123456)
        d = Time(3, 12, 15, 654321)

        self.assertRaises(TypeError, d.subtract_timedelta, delta)

    def test_subtract_invalid_type(self):
        d = Time(0, 0, 0)

        try:
            d - 'ab'
            self.fail()
        except TypeError:
            pass

        try:
            'ab' - d
            self.fail()
        except TypeError:
            pass

    def test_subtract_time(self):
        t = Time(12, 34, 56)
        t1 = Time(1, 1, 1)
        t2 = time(1, 1, 1)
        t3 = time(1, 1, 1, tzinfo=pytz.timezone('Europe/Paris'))

        diff = t - t1
        self.assertIsInstanceOfInterval(diff)
        self.assertInterval(diff, 0, hours=11, minutes=33, seconds=55)

        diff = t1 - t
        self.assertIsInstanceOfInterval(diff)
        self.assertInterval(diff, 0, hours=-11, minutes=-33, seconds=-55)

        diff = t - t2
        self.assertIsInstanceOfInterval(diff)
        self.assertInterval(diff, 0, hours=11, minutes=33, seconds=55)

        diff = t2 - t
        self.assertIsInstanceOfInterval(diff)
        self.assertInterval(diff, 0, hours=-11, minutes=-33, seconds=-55)

        self.assertRaises(TypeError, t.__sub__, t3)
        self.assertRaises(TypeError, t.__rsub__, t3)
