# -*- coding: utf-8 -*-

from datetime import timedelta
from pendulum import Date

from .. import AbstractTestCase


class AddTest(AbstractTestCase):

    def test_add_years_positive(self):
        self.assertEqual(1976, Date.create(1975).add(years=1).year)

    def test_add_years_zero(self):
        self.assertEqual(1975, Date.create(1975).add(years=0).year)

    def test_add_years_negative(self):
        self.assertEqual(1974, Date.create(1975).add(years=-1).year)

    def test_add_months_positive(self):
        self.assertEqual(1, Date.create(1975, 12).add(months=1).month)

    def test_add_months_zero(self):
        self.assertEqual(12, Date.create(1975, 12).add(months=0).month)

    def test_add_months_negative(self):
        self.assertEqual(11, Date.create(1975, 12).add(months=-1).month)

    def test_add_month_with_overflow(self):
        self.assertEqual(2, Date(2012, 1, 31).add(months=1).month)

    def test_add_days_positive(self):
        self.assertEqual(1, Date(1975, 5, 31).add(days=1).day)

    def test_add_days_zero(self):
        self.assertEqual(31, Date(1975, 5, 31).add(days=0).day)

    def test_add_days_negative(self):
        self.assertEqual(30, Date(1975, 5, 31).add(days=-1).day)

    def test_add_weeks_positive(self):
        self.assertEqual(28, Date(1975, 5, 21).add(weeks=1).day)

    def test_add_weeks_zero(self):
        self.assertEqual(21, Date(1975, 5, 21).add(weeks=0).day)

    def test_add_weeks_negative(self):
        self.assertEqual(14, Date(1975, 5, 21).add(weeks=-1).day)

    def test_add_timedelta(self):
        delta = timedelta(days=18)
        d = Date.create(2015, 3, 14)

        new = d.add_timedelta(delta)
        self.assertIsInstanceOfDate(new)
        self.assertDate(new, 2015, 4, 1)

        new = d + delta
        self.assertIsInstanceOfDate(new)
        self.assertDate(new, 2015, 4, 1)

    def test_addition_invalid_type(self):
        d = Date.create(2015, 3, 14)

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
