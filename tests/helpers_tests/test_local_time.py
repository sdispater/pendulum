# -*- coding: utf-8 -*-

from pendulum.helpers import local_time
from pendulum import Pendulum
from .. import AbstractTestCase


class LocalTimeTest(AbstractTestCase):

    def test_local_time_positive_integer(self):
        d = Pendulum(2016, 8, 7, 12, 34, 56, 123456)

        t = local_time(d.int_timestamp, 0, d.microsecond)
        self.assertEqual(d.year, t[0])
        self.assertEqual(d.month, t[1])
        self.assertEqual(d.day, t[2])
        self.assertEqual(d.hour, t[3])
        self.assertEqual(d.minute, t[4])
        self.assertEqual(d.second, t[5])
        self.assertEqual(d.microsecond, t[6])

    def test_local_time_negative_integer(self):
        d = Pendulum(1951, 8, 7, 12, 34, 56, 123456)

        t = local_time(d.int_timestamp, 0, d.microsecond)
        self.assertEqual(d.year, t[0])
        self.assertEqual(d.month, t[1])
        self.assertEqual(d.day, t[2])
        self.assertEqual(d.hour, t[3])
        self.assertEqual(d.minute, t[4])
        self.assertEqual(d.second, t[5])
        self.assertEqual(d.microsecond, t[6])
