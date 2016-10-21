# -*- coding: utf-8 -*-

from pendulum import Date

from .. import AbstractTestCase


class StartEndOfTest(AbstractTestCase):

    def test_start_of_day(self):
        d = Date.today()
        new = d.start_of('day')
        self.assertIsInstanceOfDate(new)
        self.assertDate(new, d.year, d.month, d.day)

    def test_end_of_day(self):
        d = Date.today()
        new = d.end_of('day')
        self.assertIsInstanceOfDate(new)
        self.assertDate(new, d.year, d.month, d.day)

    def test_start_of_week(self):
        d = Date(2016, 10, 20)
        new = d.start_of('week')
        self.assertIsInstanceOfDate(new)
        self.assertDate(new, d.year, d.month, 17)

    def test_end_of_week(self):
        d = Date(2016, 10, 20)
        new = d.end_of('week')
        self.assertIsInstanceOfDate(new)
        self.assertDate(new, d.year, d.month, 23)

    def test_start_of_month_is_fluid(self):
        d = Date.today()
        self.assertIsInstanceOfDate(d.start_of('month'))

    def test_start_of_month_from_now(self):
        d = Date.today()
        new = d.start_of('month')
        self.assertDate(new, d.year, d.month, 1)

    def test_start_of_month_from_last_day(self):
        d = Date(2000, 1, 31)
        new = d.start_of('month')
        self.assertDate(new, 2000, 1, 1)

    def test_start_of_year_is_fluid(self):
        d = Date.today()
        new = d.start_of('year')
        self.assertIsInstanceOfDate(new)

    def test_start_of_year_from_now(self):
        d = Date.today()
        new = d.start_of('year')
        self.assertDate(new, d.year, 1, 1)

    def test_start_of_year_from_first_day(self):
        d = Date(2000, 1, 1)
        new = d.start_of('year')
        self.assertDate(new, 2000, 1, 1)

    def test_start_of_year_from_last_day(self):
        d = Date(2000, 12, 31)
        new = d.start_of('year')
        self.assertDate(new, 2000, 1, 1)

    def test_end_of_month_is_fluid(self):
        d = Date.today()
        self.assertIsInstanceOfDate(d.end_of('month'))

    def test_end_of_month_from_now(self):
        d = Date.today().start_of('month')
        new = d.start_of('month')
        self.assertDate(new, d.year, d.month, 1)

    def test_end_of_month(self):
        d = Date(2000, 1, 1).end_of('month')
        new = d.end_of('month')
        self.assertDate(new, 2000, 1, 31)

    def test_end_of_month_from_last_day(self):
        d = Date(2000, 1, 31)
        new = d.end_of('month')
        self.assertDate(new, 2000, 1, 31)

    def test_end_of_year_is_fluid(self):
        d = Date.today()
        self.assertIsInstanceOfDate(d.end_of('year'))

    def test_end_of_year_from_now(self):
        d = Date.today().end_of('year')
        new = d.end_of('year')
        self.assertDate(new, d.year, 12, 31)

    def test_end_of_year_from_first_day(self):
        d = Date(2000, 1, 1)
        new = d.end_of('year')
        self.assertDate(new, 2000, 12, 31)

    def test_end_of_year_from_last_day(self):
        d = Date(2000, 12, 31)
        new = d.end_of('year')
        self.assertDate(new, 2000, 12, 31)

    def test_start_of_decade_is_fluid(self):
        d = Date.today()
        self.assertIsInstanceOfDate(d.start_of('decade'))

    def test_start_of_decade_from_now(self):
        d = Date.today()
        new = d.start_of('decade')
        self.assertDate(new, d.year - d.year % 10, 1, 1)

    def test_start_of_decade_from_first_day(self):
        d = Date(2000, 1, 1)
        new = d.start_of('decade')
        self.assertDate(new, 2000, 1, 1)

    def test_start_of_decade_from_last_day(self):
        d = Date(2009, 12, 31)
        new = d.start_of('decade')
        self.assertDate(new, 2000, 1, 1)

    def test_end_of_decade_is_fluid(self):
        d = Date.today()
        self.assertIsInstanceOfDate(d.end_of('decade'))

    def test_end_of_decade_from_now(self):
        d = Date.today()
        new  = d.end_of('decade')
        self.assertDate(new, d.year - d.year % 10 + 9, 12, 31)

    def test_end_of_decade_from_first_day(self):
        d = Date(2000, 1, 1)
        new = d.end_of('decade')
        self.assertDate(new, 2009, 12, 31)

    def test_end_of_decade_from_last_day(self):
        d = Date(2009, 12, 31)
        new = d.end_of('decade')
        self.assertDate(new, 2009, 12, 31)

    def test_start_of_century_is_fluid(self):
        d = Date.today()
        self.assertIsInstanceOfDate(d.start_of('century'))

    def test_start_of_century_from_now(self):
        d = Date.today()
        new = d.start_of('century')
        self.assertDate(new, d.year - d.year % 100 + 1, 1, 1)

    def test_start_of_century_from_first_day(self):
        d = Date(2001, 1, 1)
        new = d.start_of('century')
        self.assertDate(new, 2001, 1, 1)

    def test_start_of_century_from_last_day(self):
        d = Date(2100, 12, 31)
        new = d.start_of('century')
        self.assertDate(new, 2001, 1, 1)

    def test_end_of_century_is_fluid(self):
        d = Date.today()
        self.assertIsInstanceOfDate(d.end_of('century'))

    def test_end_of_century_from_now(self):
        now = Date.today()
        d = now.end_of('century')
        self.assertDate(d, now.year - now.year % 100 + 100, 12, 31)

    def test_end_of_century_from_first_day(self):
        d = Date(2001, 1, 1)
        new = d.end_of('century')
        self.assertDate(new, 2100, 12, 31)

    def test_end_of_century_from_last_day(self):
        d = Date(2100, 12, 31)
        new = d.end_of('century')
        self.assertDate(new, 2100, 12, 31)

    def test_average_is_fluid(self):
        d = Date.today().average()
        self.assertIsInstanceOfDate(d)

    def test_average_from_same(self):
        d1 = Date.create(2000, 1, 31)
        d2 = Date.create(2000, 1, 31).average(d1)
        self.assertDate(d2, 2000, 1, 31)

    def test_average_from_greater(self):
        d1 = Date.create(2000, 1, 1)
        d2 = Date.create(2009, 12, 31).average(d1)
        self.assertDate(d2, 2004, 12, 31)

    def test_average_from_lower(self):
        d1 = Date.create(2009, 12, 31)
        d2 = Date.create(2000, 1, 1).average(d1)
        self.assertDate(d2, 2004, 12, 31)

    def start_of_with_invalid_unit(self):
        self.assertRaises(ValueError, Date.today().start_of('invalid'))

    def end_of_with_invalid_unit(self):
        self.assertRaises(ValueError, Date.today().end_of('invalid'))

    def test_start_of(self):
        d = Date(2013, 3, 31)

        self.assertRaises(ValueError, d.start_of, 'invalid')

    def test_end_of_invalid_unit(self):
        d = Date(2013, 3, 31)

        self.assertRaises(ValueError, d.end_of, 'invalid')
