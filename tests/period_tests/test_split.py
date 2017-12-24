# -*- coding: utf-8 -*-

from datetime import datetime
from pendulum import Period, Pendulum, Date

from .. import AbstractTestCase


class SplitTest(AbstractTestCase):

    def test_split(self):
        dt1 = Pendulum(2000, 1, 1, 12, 45, 37)
        dt2 = Pendulum(2000, 1, 31, 12, 45, 37)

        p = Period(dt1, dt2)
        spl = p.split('days')
        self.assertEqual(31, len(spl))
        self.assertPendulum(spl[0].start, 2000, 1, 1, 12, 45, 37)
        self.assertPendulum(spl[-1].end, 2000, 1, 31, 12, 45, 37)

    def test_split_hours(self):
        dt1 = Pendulum(2000, 1, 1, 12, 45, 37)
        dt2 = Pendulum(2000, 1, 31, 12, 45, 37)

        p = Period(dt1, dt2)
        spl = p.split('hours',5)
        self.assertEqual(145, len(spl))
        self.assertPendulum(spl[0].start, 2000, 1, 1, 12, 45, 37)
        self.assertPendulum(spl[-1].end, 2000, 1, 31, 12, 45, 37)

    def test_split_no_overflow(self):
        dt1 = Pendulum(2000, 1, 1, 12, 45, 37)
        dt2 = Pendulum(2000, 1, 31, 11, 45, 37)

        p = Period(dt1, dt2)
        spl = p.split('days')
        self.assertEqual(30, len(spl))
        self.assertPendulum(spl[0].start, 2000, 1, 1, 12, 45, 37)
        self.assertPendulum(spl[-1].end, 2000, 1, 31, 11, 45, 37)

    def test_split_inverted(self):
        dt1 = Pendulum(2000, 1, 1, 12, 45, 37)
        dt2 = Pendulum(2000, 1, 31, 12, 45, 37)

        p = Period(dt2, dt1)
        spl = p.split('days')
        self.assertEqual(31, len(spl))
        self.assertPendulum(spl[-1].end, 2000, 1, 1, 12, 45, 37)
        self.assertPendulum(spl[0].start, 2000, 1, 31, 12, 45, 37)

    def test_iter(self):
        dt1 = Pendulum(2000, 1, 1, 12, 45, 37)
        dt2 = Pendulum(2000, 1, 31, 12, 45, 37)

        p = Period(dt1, dt2)
        spl = p.split('days', 1)
        i = 0
        for s in spl:
            self.assertIsInstanceOfPeriod(s)
            i += 1

        self.assertEqual(31, i)

    def test_contained_exactly_once(self):
        dt1 = Pendulum(2000, 1, 1, 12, 45, 37)
        dt2 = Pendulum(2000, 1, 31, 12, 45, 37)

        p = Period(dt1, dt2)
        spl = p.split('days', 3)
        for dt in p:
            self.assertEqual(1, sum(dt in p for p in spl))

    def test_contained_exactly_once_hours(self):
        dt1 = Pendulum(2000, 1, 1, 12, 45, 37)
        dt2 = Pendulum(2000, 1, 31, 12, 45, 37)

        p = Period(dt1, dt2)
        spl = p.split('hours', 3)
        for dt in p:
            self.assertEqual(1, sum(dt in p for p in spl))

    def test_contained_exactly_once_boundary(self):
        dt1 = Pendulum(2000, 1, 1)
        dt2 = Pendulum(2000, 1, 31)

        p = Period(dt1, dt2)
        spl = p.split('days', 3)
        for dt in p:
            self.assertEqual(1, sum(dt in p for p in spl))

    def test_contains_exactly_once_datetime(self):
        dt1 = Pendulum(2000, 1, 1, 12, 45, 37)
        dt2 = Pendulum(2000, 1, 31, 12, 45, 37)

        p = Period(dt1, dt2)
        spl = p.split('days', 3)
        dt = datetime(2000, 1, 7)
        self.assertEqual(1, sum(dt in p for p in spl))

    def test_split_months_overflow(self):
        dt1 = Pendulum(2016, 1, 30, tzinfo='America/Sao_Paulo')
        dt2 = dt1.add(months=4)

        p = Period(dt1, dt2)
        spl = p.split('months')
        self.assertPendulum(spl[0].start, 2016, 1, 30, 0, 0, 0)
        self.assertPendulum(spl[-1].end, 2016, 5, 30, 0, 0, 0)

    def test_split_with_dst(self):
        dt1 = Pendulum(2016, 10, 14, tzinfo='America/Sao_Paulo')
        dt2 = dt1.add(weeks=1)

        p = Period(dt1, dt2)
        spl = p.split('days')
        self.assertPendulum(spl[0].start, 2016, 10, 14, 0, 0, 0)
        self.assertPendulum(spl[2].start, 2016, 10, 16, 1, 0, 0)
        self.assertPendulum(spl[-1].end, 2016, 10, 21, 0, 0, 0)

    def test_split_amount(self):
        dt1 = Pendulum(2016, 10, 14, tzinfo='America/Sao_Paulo')
        dt2 = dt1.add(weeks=1)

        p = Period(dt1, dt2)
        spl = p.split('days', 2)

        self.assertEqual(len(spl), 4)
        self.assertPendulum(spl[0].start, 2016, 10, 14, 0, 0, 0)
        self.assertPendulum(spl[1].start, 2016, 10, 16, 1, 0, 0)
        self.assertPendulum(spl[2].start, 2016, 10, 18, 0, 0, 0)
        self.assertPendulum(spl[3].start, 2016, 10, 20, 0, 0, 0)
        self.assertPendulum(spl[3].end, 2016, 10, 21, 0, 0, 0)
