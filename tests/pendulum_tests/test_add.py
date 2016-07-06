# -*- coding: utf-8 -*-

from .. import AbstractTestCase

from datetime import timedelta
from pendulum import Pendulum


class AddTest(AbstractTestCase):

    def test_add_years_positive(self):
        self.assertEqual(1976, Pendulum(1975).add_years(1).year)

    def test_add_years_zero(self):
        self.assertEqual(1975, Pendulum(1975).add_years(0).year)

    def test_add_years_negative(self):
        self.assertEqual(1974, Pendulum(1975).add_years(-1).year)

    def test_add_year(self):
        self.assertEqual(1976, Pendulum(1975).add_year().year)

    def test_add_months_positive(self):
        self.assertEqual(1, Pendulum(1975, 12).add_months(1).month)

    def test_add_months_zero(self):
        self.assertEqual(12, Pendulum(1975, 12).add_months(0).month)

    def test_add_months_negative(self):
        self.assertEqual(11, Pendulum(1975, 12).add_months(-1).month)

    def test_add_month(self):
        self.assertEqual(1, Pendulum(1975, 12).add_month().month)

    def test_add_month_with_overflow(self):
        self.assertEqual(2, Pendulum(2012, 1, 31).add_month().month)

    def test_add_days_positive(self):
        self.assertEqual(1, Pendulum(1975, 5, 31).add_days(1).day)

    def test_add_days_zero(self):
        self.assertEqual(31, Pendulum(1975, 5, 31).add_days(0).day)

    def test_add_days_negative(self):
        self.assertEqual(30, Pendulum(1975, 5, 31).add_days(-1).day)

    def test_add_day(self):
        self.assertEqual(1, Pendulum(1975, 3, 31).add_day().day)

    def test_add_weeks_positive(self):
        self.assertEqual(28, Pendulum(1975, 5, 21).add_weeks(1).day)

    def test_add_weeks_zero(self):
        self.assertEqual(21, Pendulum(1975, 5, 21).add_weeks(0).day)

    def test_add_weeks_negative(self):
        self.assertEqual(14, Pendulum(1975, 5, 21).add_weeks(-1).day)

    def test_add_week(self):
        self.assertEqual(28, Pendulum(1975, 3, 21).add_week().day)

    def test_add_hours_positive(self):
        self.assertEqual(1, Pendulum(1975, 5, 21, 0, 0, 0).add_hours(1).hour)

    def test_add_hours_zero(self):
        self.assertEqual(0, Pendulum(1975, 5, 21, 0, 0, 0).add_hours(0).hour)

    def test_add_hours_negative(self):
        self.assertEqual(23, Pendulum(1975, 5, 21, 0, 0, 0).add_hours(-1).hour)

    def test_add_hour(self):
        self.assertEqual(1, Pendulum(1975, 5, 21, 0, 0, 0).add_hour().hour)

    def test_add_minutes_positive(self):
        self.assertEqual(1, Pendulum(1975, 5, 21, 0, 0, 0).add_minutes(1).minute)

    def test_add_minutes_zero(self):
        self.assertEqual(0, Pendulum(1975, 5, 21, 0, 0, 0).add_minutes(0).minute)

    def test_add_minutes_negative(self):
        self.assertEqual(59, Pendulum(1975, 5, 21, 0, 0, 0).add_minutes(-1).minute)

    def test_add_minute(self):
        self.assertEqual(1, Pendulum(1975, 5, 21, 0, 0, 0).add_minute().minute)

    def test_add_seconds_positive(self):
        self.assertEqual(1, Pendulum(1975, 5, 21, 0, 0, 0).add_seconds(1).second)

    def test_add_seconds_zero(self):
        self.assertEqual(0, Pendulum(1975, 5, 21, 0, 0, 0).add_seconds(0).second)

    def test_add_seconds_negative(self):
        self.assertEqual(59, Pendulum(1975, 5, 21, 0, 0, 0).add_seconds(-1).second)

    def test_add_second(self):
        self.assertEqual(1, Pendulum(1975, 5, 21, 0, 0, 0).add_second().second)

    def test_add_timedelta(self):
        delta = timedelta(days=6, seconds=45, microseconds=123456)
        d = Pendulum.create(2015, 3, 14, 3, 12, 15, 654321)

        d = d.add_timedelta(delta)
        self.assertEqual(20, d.day)
        self.assertEqual(13, d.minute)
        self.assertEqual(0, d.second)
        self.assertEqual(777777, d.microsecond)

        d = Pendulum.create(2015, 3, 14, 3, 12, 15, 654321)

        d = d + delta
        self.assertEqual(20, d.day)
        self.assertEqual(13, d.minute)
        self.assertEqual(0, d.second)
        self.assertEqual(777777, d.microsecond)


