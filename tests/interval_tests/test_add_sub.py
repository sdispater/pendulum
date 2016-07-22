# -*- coding: utf-8 -*-

from datetime import timedelta
from pendulum import Interval

from .. import AbstractTestCase


class AddSubTestCase(AbstractTestCase):

    def test_add_interval(self):
        p1 = Interval(days=23, seconds=32)
        p2 = Interval(days=12, seconds=30)

        p = p1 + p2
        self.assertInterval(p, 5, 0, 0, 1, 2)

    def test_add_timedelta(self):
        p1 = Interval(days=23, seconds=32)
        p2 = timedelta(days=12, seconds=30)

        p = p1 + p2
        self.assertInterval(p, 5, 0, 0, 1, 2)

    def test_add_unsupported(self):
        p = Interval(days=23, seconds=32)
        self.assertEqual(NotImplemented, p.__add__(5))

    def test_sub_interval(self):
        p1 = Interval(days=23, seconds=32)
        p2 = Interval(days=12, seconds=28)

        p = p1 - p2
        self.assertInterval(p, 1, 4, 0, 0, 4)

    def test_sub_timedelta(self):
        p1 = Interval(days=23, seconds=32)
        p2 = timedelta(days=12, seconds=28)

        p = p1 - p2
        self.assertInterval(p, 1, 4, 0, 0, 4)

    def test_sub_unsupported(self):
        p = Interval(days=23, seconds=32)
        self.assertEqual(NotImplemented, p.__sub__(5))

    def test_neg(self):
        p = Interval(days=23, seconds=32)
        self.assertInterval(-p, -3, -2, 0, 0, -32)
