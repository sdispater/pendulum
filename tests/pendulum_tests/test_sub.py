# -*- coding: utf-8 -*-

from datetime import timedelta
from pendulum import Pendulum

from .. import AbstractTestCase


class SubTest(AbstractTestCase):

    def test_sub_years_positive(self):
        self.assertEqual(1974, Pendulum(1975).sub_years(1).year)

    def test_sub_years_zero(self):
        self.assertEqual(1975, Pendulum(1975).sub_years(0).year)

    def test_sub_years_negative(self):
        self.assertEqual(1976, Pendulum(1975).sub_years(-1).year)

    def test_sub_year(self):
        self.assertEqual(1974, Pendulum(1975).sub_year().year)

    def test_sub_months_positive(self):
        self.assertEqual(11, Pendulum(1975, 12).sub_months(1).month)

    def test_sub_months_zero(self):
        self.assertEqual(12, Pendulum(1975, 12).sub_months(0).month)

    def test_sub_months_negative(self):
        self.assertEqual(1, Pendulum(1975, 12).sub_months(-1).month)

    def test_sub_month(self):
        self.assertEqual(11, Pendulum(1975, 12).sub_month().month)

    def test_sub_days_positive(self):
        self.assertEqual(30, Pendulum(1975, 5, 31).sub_days(1).day)

    def test_sub_days_zero(self):
        self.assertEqual(31, Pendulum(1975, 5, 31).sub_days(0).day)

    def test_sub_days_negative(self):
        self.assertEqual(1, Pendulum(1975, 5, 31).sub_days(-1).day)

    def test_sub_day(self):
        self.assertEqual(30, Pendulum(1975, 3, 31).sub_day().day)

    def test_sub_weeks_positive(self):
        self.assertEqual(14, Pendulum(1975, 5, 21).sub_weeks(1).day)

    def test_sub_weeks_zero(self):
        self.assertEqual(21, Pendulum(1975, 5, 21).sub_weeks(0).day)

    def test_sub_weeks_negative(self):
        self.assertEqual(28, Pendulum(1975, 5, 21).sub_weeks(-1).day)

    def test_sub_week(self):
        self.assertEqual(14, Pendulum(1975, 3, 21).sub_week().day)

    def test_sub_hours_positive(self):
        self.assertEqual(23, Pendulum(1975, 5, 21, 0, 0, 0).sub_hours(1).hour)

    def test_sub_hours_zero(self):
        self.assertEqual(0, Pendulum(1975, 5, 21, 0, 0, 0).sub_hours(0).hour)

    def test_sub_hours_negative(self):
        self.assertEqual(1, Pendulum(1975, 5, 21, 0, 0, 0).sub_hours(-1).hour)

    def test_sub_hour(self):
        self.assertEqual(23, Pendulum(1975, 5, 21, 0, 0, 0).sub_hour().hour)

    def test_sub_minutes_positive(self):
        self.assertEqual(59, Pendulum(1975, 5, 21, 0, 0, 0).sub_minutes(1).minute)

    def test_sub_minutes_zero(self):
        self.assertEqual(0, Pendulum(1975, 5, 21, 0, 0, 0).sub_minutes(0).minute)

    def test_sub_minutes_negative(self):
        self.assertEqual(1, Pendulum(1975, 5, 21, 0, 0, 0).sub_minutes(-1).minute)

    def test_sub_minute(self):
        self.assertEqual(59, Pendulum(1975, 5, 21, 0, 0, 0).sub_minute().minute)

    def test_sub_seconds_positive(self):
        self.assertEqual(59, Pendulum(1975, 5, 21, 0, 0, 0).sub_seconds(1).second)

    def test_sub_seconds_zero(self):
        self.assertEqual(0, Pendulum(1975, 5, 21, 0, 0, 0).sub_seconds(0).second)

    def test_sub_seconds_negative(self):
        self.assertEqual(1, Pendulum(1975, 5, 21, 0, 0, 0).sub_seconds(-1).second)

    def test_sub_second(self):
        self.assertEqual(59, Pendulum(1975, 5, 21, 0, 0, 0).sub_second().second)

    def test_sub_timedelta(self):
        delta = timedelta(days=6, seconds=16, microseconds=654321)
        d = Pendulum.create(2015, 3, 14, 3, 12, 15, 777777)

        d.sub_timedelta(delta)
        self.assertEqual(8, d.day)
        self.assertEqual(11, d.minute)
        self.assertEqual(59, d.second)
        self.assertEqual(123456, d.microsecond)

        d = Pendulum.create(2015, 3, 14, 3, 12, 15, 777777)

        d = d - delta
        self.assertEqual(8, d.day)
        self.assertEqual(11, d.minute)
        self.assertEqual(59, d.second)
        self.assertEqual(123456, d.microsecond)
