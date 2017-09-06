# -*- coding: utf-8 -*-

import pytest

import pendulum
from pendulum import Date
from pendulum.exceptions import PendulumException

from .. import AbstractTestCase


class DayOfWeekModifiersTest(AbstractTestCase):

    def test_get_weekend_days(self):
        self.assertEqual(
            [pendulum.SATURDAY, pendulum.SUNDAY],
            Date.get_weekend_days()
        )
        Date.set_weekend_days([pendulum.FRIDAY, pendulum.SATURDAY])
        self.assertEqual(
            [pendulum.FRIDAY, pendulum.SATURDAY],
            Date.get_weekend_days()
        )
        Date.set_weekend_days([pendulum.SATURDAY, pendulum.SUNDAY])

    def test_get_week_ends_at(self):
        Date.set_week_ends_at(pendulum.SATURDAY)
        self.assertEqual(Date.get_week_ends_at(), pendulum.SATURDAY)
        Date.set_week_ends_at(pendulum.SUNDAY)

    def test_get_week_starts_at(self):
        Date.set_week_starts_at(pendulum.TUESDAY)
        self.assertEqual(Date.get_week_starts_at(), pendulum.TUESDAY)
        Date.set_week_starts_at(pendulum.MONDAY)

    def test_start_of_week(self):
        d = Date(1980, 8, 7).start_of('week')
        self.assertDate(d, 1980, 8, 4)

    def test_start_of_week_from_week_start(self):
        d = Date(1980, 8, 4).start_of('week')
        self.assertDate(d, 1980, 8, 4)

    def test_start_of_week_crossing_year_boundary(self):
        d = Date(2014, 1, 1).start_of('week')
        self.assertDate(d, 2013, 12, 30)

    def test_end_of_week(self):
        d = Date(1980, 8, 7).end_of('week')
        self.assertDate(d, 1980, 8, 10)

    def test_end_of_week_from_week_end(self):
        d = Date(1980, 8, 10).end_of('week')
        self.assertDate(d, 1980, 8, 10)

    def test_end_of_week_crossing_year_boundary(self):
        d = Date(2013, 12, 31).end_of('week')
        self.assertDate(d, 2014, 1, 5)

    def test_next(self):
        d = Date(1975, 5, 21).next()
        self.assertDate(d, 1975, 5, 28)

    def test_next_monday(self):
        d = Date(1975, 5, 21).next(pendulum.MONDAY)
        self.assertDate(d, 1975, 5, 26)

    def test_next_saturday(self):
        d = Date(1975, 5, 21).next(6)
        self.assertDate(d, 1975, 5, 24)

    def test_next_invalid(self):
        dt = pendulum.date(1975, 5, 21)

        with pytest.raises(ValueError):
            dt.next(7)

    def test_previous(self):
        d = Date(1975, 5, 21).previous()
        self.assertDate(d, 1975, 5, 14)

    def test_previous_monday(self):
        d = Date(1975, 5, 21).previous(pendulum.MONDAY)
        self.assertDate(d, 1975, 5, 19)

    def test_previous_saturday(self):
        d = Date(1975, 5, 21).previous(6)
        self.assertDate(d, 1975, 5, 17)

    def test_previous_invalid(self):
        dt = pendulum.date(1975, 5, 21)

        with pytest.raises(ValueError):
            dt.previous(7)

    def test_first_day_of_month(self):
        d = Date(1975, 11, 21).first_of('month', )
        self.assertDate(d, 1975, 11, 1)

    def test_first_wednesday_of_month(self):
        d = Date(1975, 11, 21).first_of('month', pendulum.WEDNESDAY)
        self.assertDate(d, 1975, 11, 5)

    def test_first_friday_of_month(self):
        d = Date(1975, 11, 21).first_of('month', 5)
        self.assertDate(d, 1975, 11, 7)

    def test_last_day_of_month(self):
        d = Date(1975, 12, 5).last_of('month', )
        self.assertDate(d, 1975, 12, 31)

    def test_last_tuesday_of_month(self):
        d = Date(1975, 12, 1).last_of('month', pendulum.TUESDAY)
        self.assertDate(d, 1975, 12, 30)

    def test_last_friday_of_month(self):
        d = Date(1975, 12, 5).last_of('month', 5)
        self.assertDate(d, 1975, 12, 26)

    def test_nth_of_month_outside_scope(self):
        d = Date(1975, 12, 5)

        self.assertRaises(PendulumException, d.nth_of, 'month', 6, pendulum.MONDAY)

    def test_nth_of_month_outside_year(self):
        d = Date(1975, 12, 5)

        self.assertRaises(PendulumException, d.nth_of, 'month', 55, pendulum.MONDAY)

    def test_nth_of_month_first(self):
        d = Date(1975, 12, 5).nth_of('month', 1, pendulum.MONDAY)

        self.assertDate(d, 1975, 12, 1)

    def test_2nd_monday_of_month(self):
        d = Date(1975, 12, 5).nth_of('month', 2, pendulum.MONDAY)

        self.assertDate(d, 1975, 12, 8)

    def test_3rd_wednesday_of_month(self):
        d = Date(1975, 12, 5).nth_of('month', 3, 3)

        self.assertDate(d, 1975, 12, 17)

    def test_first_day_of_quarter(self):
        d = Date(1975, 11, 21).first_of('quarter', )
        self.assertDate(d, 1975, 10, 1)

    def test_first_wednesday_of_quarter(self):
        d = Date(1975, 11, 21).first_of('quarter', pendulum.WEDNESDAY)
        self.assertDate(d, 1975, 10, 1)

    def test_first_friday_of_quarter(self):
        d = Date(1975, 11, 21).first_of('quarter', 5)
        self.assertDate(d, 1975, 10, 3)

    def test_first_of_quarter_from_a_day_that_will_not_exist_in_the_first_month(self):
        d = Date(2014, 5, 31).first_of('quarter')
        self.assertDate(d, 2014, 4, 1)

    def test_last_day_of_quarter(self):
        d = Date(1975, 8, 5).last_of('quarter')
        self.assertDate(d, 1975, 9, 30)

    def test_last_tuesday_of_quarter(self):
        d = Date(1975, 8, 5).last_of('quarter', pendulum.TUESDAY)
        self.assertDate(d, 1975, 9, 30)

    def test_last_friday_of_quarter(self):
        d = Date(1975, 8, 5).last_of('quarter', pendulum.FRIDAY)
        self.assertDate(d, 1975, 9, 26)

    def test_last_day_of_quarter_that_will_not_exist_in_the_last_month(self):
        d = Date(2014, 5, 31).last_of('quarter', )
        self.assertDate(d, 2014, 6, 30)

    def test_nth_of_quarter_outside_scope(self):
        d = Date(1975, 1, 5)

        self.assertRaises(PendulumException, d.nth_of, 'quarter', 20, pendulum.MONDAY)

    def test_nth_of_quarter_outside_year(self):
        d = Date(1975, 1, 5)

        self.assertRaises(PendulumException, d.nth_of, 'quarter', 55, pendulum.MONDAY)

    def test_nth_of_quarter_first(self):
        d = Date(1975, 12, 5).nth_of('quarter', 1, pendulum.MONDAY)

        self.assertDate(d, 1975, 10, 6)

    def test_nth_of_quarter_from_a_day_that_will_not_exist_in_the_first_month(self):
        d = Date(2014, 5, 31).nth_of('quarter', 2, pendulum.MONDAY)
        self.assertDate(d, 2014, 4, 14)

    def test_2nd_monday_of_quarter(self):
        d = Date(1975, 8, 5).nth_of('quarter', 2, pendulum.MONDAY)
        self.assertDate(d, 1975, 7, 14)

    def test_3rd_wednesday_of_quarter(self):
        d = Date(1975, 8, 5).nth_of('quarter', 3, 3)
        self.assertDate(d, 1975, 7, 16)

    def test_first_day_of_year(self):
        d = Date(1975, 11, 21).first_of('year')
        self.assertDate(d, 1975, 1, 1)

    def test_first_wednesday_of_year(self):
        d = Date(1975, 11, 21).first_of('year', pendulum.WEDNESDAY)
        self.assertDate(d, 1975, 1, 1)

    def test_first_friday_of_year(self):
        d = Date(1975, 11, 21).first_of('year', 5)
        self.assertDate(d, 1975, 1, 3)

    def test_last_day_of_year(self):
        d = Date(1975, 8, 5).last_of('year')
        self.assertDate(d, 1975, 12, 31)

    def test_last_tuesday_of_year(self):
        d = Date(1975, 8, 5).last_of('year', pendulum.TUESDAY)
        self.assertDate(d, 1975, 12, 30)

    def test_last_friday_of_year(self):
        d = Date(1975, 8, 5).last_of('year', 5)
        self.assertDate(d, 1975, 12, 26)

    def test_nth_of_year_outside_scope(self):
        d = Date(1975, 1, 5)

        self.assertRaises(PendulumException, d.nth_of, 'year', 55, pendulum.MONDAY)

    def test_nth_of_year_first(self):
        d = Date(1975, 12, 5).nth_of('year', 1, pendulum.MONDAY)

        self.assertDate(d, 1975, 1, 6)

    def test_2nd_monday_of_year(self):
        d = Date(1975, 8, 5).nth_of('year', 2, pendulum.MONDAY)
        self.assertDate(d, 1975, 1, 13)

    def test_2rd_wednesday_of_year(self):
        d = Date(1975, 8, 5).nth_of('year', 3, pendulum.WEDNESDAY)
        self.assertDate(d, 1975, 1, 15)

    def test_7th_thursday_of_year(self):
        d = Date(1975, 8, 31).nth_of('year', 7, pendulum.THURSDAY)
        self.assertDate(d, 1975, 2, 13)

    def test_first_of_invalid_unit(self):
        d = Date.create(1975, 8, 5)

        self.assertRaises(ValueError, d.first_of, 'invalid')

    def test_last_of_invalid_unit(self):
        d = Date.create(1975, 8, 5)

        self.assertRaises(ValueError, d.last_of, 'invalid')

    def test_nth_of_invalid_unit(self):
        d = Date.create(1975, 8, 5)

        self.assertRaises(ValueError, d.nth_of, 'invalid', 3, pendulum.MONDAY)
