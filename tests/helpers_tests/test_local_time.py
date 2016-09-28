# -*- coding: utf-8 -*-

from pendulum.helpers import local_time
from pendulum import Pendulum
from .. import AbstractTestCase


class LocalTimeTest(AbstractTestCase):

    def test_local_time_positive_integer(self):
        d = Pendulum(2016, 8, 7, 12, 34, 56)

        t = local_time(d.timestamp, 0)
        self.assertEqual(d.year, t[0])
        self.assertEqual(d.month, t[1])
        self.assertEqual(d.day, t[2])
        self.assertEqual(d.hour, t[3])
        self.assertEqual(d.minute, t[4])
        self.assertEqual(d.second, t[5])
