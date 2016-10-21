# -*- coding: utf-8 -*-

from pendulum import Date

from .. import AbstractTestCase


class FluentSettersTest(AbstractTestCase):

    def test_fluid_year_setter(self):
        d = Date(2016, 10, 20)
        new = d.year_(1995)
        self.assertIsInstanceOfDate(new)
        self.assertDate(new, 1995, 10, 20)
        self.assertEqual(1995, new.year)

    def test_fluid_month_setter(self):
        d = Date(2016, 7, 2)
        new = d.month_(11)
        self.assertIsInstanceOfDate(new)
        self.assertEqual(11, new.month)
        self.assertEqual(7, d.month)

    def test_fluid_day_setter(self):
        d = Date(2016, 7, 2)
        new = d.day_(9)
        self.assertIsInstanceOfDate(new)
        self.assertEqual(9, new.day)
        self.assertEqual(2, d.day)
