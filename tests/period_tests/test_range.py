# -*- coding: utf-8 -*-

from datetime import datetime
from pendulum import Period, Pendulum

from .. import AbstractTestCase


class RangeTest(AbstractTestCase):

    def test_range(self):
        dt1 = Pendulum(2000, 1, 1, 12, 45, 37)
        dt2 = Pendulum(2000, 1, 31, 12, 45, 37)

        p = Period(dt1, dt2)
        r = p.range('days')
        self.assertEqual(31, len(r))
        self.assertPendulum(r[0], 2000, 1, 1, 12, 45, 37)
        self.assertPendulum(r[-1], 2000, 1, 31, 12, 45, 37)

    def test_range_no_overflow(self):
        dt1 = Pendulum(2000, 1, 1, 12, 45, 37)
        dt2 = Pendulum(2000, 1, 31, 11, 45, 37)

        p = Period(dt1, dt2)
        r = p.range('days')
        self.assertEqual(30, len(r))
        self.assertPendulum(r[0], 2000, 1, 1, 12, 45, 37)
        self.assertPendulum(r[-1], 2000, 1, 30, 12, 45, 37)

    def test_range_inverted(self):
        dt1 = Pendulum(2000, 1, 1, 12, 45, 37)
        dt2 = Pendulum(2000, 1, 31, 12, 45, 37)

        p = Period(dt2, dt1)
        r = p.range('days')
        self.assertEqual(31, len(r))
        self.assertPendulum(r[-1], 2000, 1, 1, 12, 45, 37)
        self.assertPendulum(r[0], 2000, 1, 31, 12, 45, 37)

    def test_iter(self):
        dt1 = Pendulum(2000, 1, 1, 12, 45, 37)
        dt2 = Pendulum(2000, 1, 31, 12, 45, 37)

        p = Period(dt1, dt2)
        i = 0
        for dt in p:
            self.assertIsInstanceOfPendulum(dt)
            i += 1

        self.assertEqual(31, i)

    def test_contains(self):
        dt1 = Pendulum(2000, 1, 1, 12, 45, 37)
        dt2 = Pendulum(2000, 1, 31, 12, 45, 37)

        p = Period(dt1, dt2)
        dt = Pendulum(2000, 1, 7)
        self.assertTrue(dt in p)

    def test_not_contains(self):
        dt1 = Pendulum(2000, 1, 1, 12, 45, 37)
        dt2 = Pendulum(2000, 1, 31, 12, 45, 37)

        p = Period(dt1, dt2)
        dt = Pendulum(2000, 1, 1, 11, 45, 37)
        self.assertFalse(dt in p)

    def test_contains_with_datetime(self):
        dt1 = Pendulum(2000, 1, 1, 12, 45, 37)
        dt2 = Pendulum(2000, 1, 31, 12, 45, 37)

        p = Period(dt1, dt2)
        dt = datetime(2000, 1, 7)
        self.assertTrue(dt in p)
