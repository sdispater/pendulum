# -*- coding: utf-8 -*-

from datetime import datetime
from pendulum import Period, Pendulum

from .. import AbstractTestCase


class ConstructTest(AbstractTestCase):

    def test_with_datetimes(self):
        dt1 = datetime(2000, 1, 1)
        dt2 = datetime(2000, 1, 31)

        p = Period(dt1, dt2)
        self.assertIsInstanceOfPendulum(p.start)
        self.assertIsInstanceOfPendulum(p.end)
        self.assertPendulum(p.start, 2000, 1, 1)
        self.assertPendulum(p.end, 2000, 1, 31)

    def test_with_pendulum(self):
        dt1 = Pendulum(2000, 1, 1)
        dt2 = Pendulum(2000, 1, 31)

        p = Period(dt1, dt2)
        self.assertIsInstanceOfPendulum(p.start)
        self.assertIsInstanceOfPendulum(p.end)
        self.assertPendulum(p.start, 2000, 1, 1)
        self.assertPendulum(p.end, 2000, 1, 31)

    def test_inverted(self):
        dt1 = Pendulum(2000, 1, 1)
        dt2 = Pendulum(2000, 1, 31)

        p = Period(dt2, dt1)
        self.assertIsInstanceOfPendulum(p.start)
        self.assertIsInstanceOfPendulum(p.end)
        self.assertPendulum(p.start, 2000, 1, 31)
        self.assertPendulum(p.end, 2000, 1, 1)

    def test_inverted_and_absolute(self):
        dt1 = Pendulum(2000, 1, 1)
        dt2 = Pendulum(2000, 1, 31)

        p = Period(dt2, dt1, True)
        self.assertIsInstanceOfPendulum(p.start)
        self.assertIsInstanceOfPendulum(p.end)
        self.assertPendulum(p.start, 2000, 1, 1)
        self.assertPendulum(p.end, 2000, 1, 31)
