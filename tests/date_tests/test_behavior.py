# -*- coding: utf-8 -*-

import pickle
from datetime import date
from pendulum import Date
from .. import AbstractTestCase


class BehaviorTest(AbstractTestCase):

    def setUp(self):
        super(BehaviorTest, self).setUp()

        self.p = Date(2016, 8, 27)
        self.d = date(2016, 8, 27)

    def test_timetuple(self):
        self.assertEqual(self.d.timetuple(), self.p.timetuple())

    def test_ctime(self):
        self.assertEqual(self.d.ctime(), self.p.ctime())

    def test_isoformat(self):
        self.assertEqual(self.d.isoformat(), self.p.isoformat())

    def test_toordinal(self):
        self.assertEqual(self.d.toordinal(), self.p.toordinal())

    def test_weekday(self):
        self.assertEqual(self.d.weekday(), self.p.weekday())

    def test_isoweekday(self):
        self.assertEqual(self.d.isoweekday(), self.p.isoweekday())

    def test_isocalendar(self):
        self.assertEqual(self.d.isocalendar(), self.p.isocalendar())

    def test_fromtimestamp(self):
        self.assertEqual(
            date.fromtimestamp(0),
            Date.fromtimestamp(0)
        )

    def test_fromordinal(self):
        self.assertEqual(date.fromordinal(730120), Date.fromordinal(730120))

    def test_hash(self):
        d1 = Date(2016, 8, 27)
        d2 = Date(2016, 8, 27)
        d3 = Date(2016, 8, 28)

        self.assertEqual(hash(d1), hash(d2))
        self.assertNotEqual(hash(d1), hash(d3))

    def test_pickle(self):
        d1 = Date(2016, 8, 27)
        s = pickle.dumps(d1)
        d2 = pickle.loads(s)

        self.assertIsInstanceOfDate(d2)
        self.assertEqual(d1, d2)
