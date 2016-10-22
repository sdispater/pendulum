# -*- coding: utf-8 -*-

import pendulum
from datetime import timedelta
from pendulum import Pendulum

from .. import AbstractTestCase


class SubTest(AbstractTestCase):

    def test_sub_years_positive(self):
        self.assertEqual(1974, Pendulum.create(1975).subtract(years=1).year)

    def test_sub_years_zero(self):
        self.assertEqual(1975, Pendulum.create(1975).subtract(years=0).year)

    def test_sub_years_negative(self):
        self.assertEqual(1976, Pendulum.create(1975).subtract(years=-1).year)

    def test_sub_months_positive(self):
        self.assertEqual(11, Pendulum.create(1975, 12).subtract(months=1).month)

    def test_sub_months_zero(self):
        self.assertEqual(12, Pendulum.create(1975, 12).subtract(months=0).month)

    def test_sub_months_negative(self):
        self.assertEqual(1, Pendulum.create(1975, 12).subtract(months=-1).month)

    def test_sub_days_positive(self):
        self.assertEqual(30, Pendulum(1975, 5, 31).subtract(days=1).day)

    def test_sub_days_zero(self):
        self.assertEqual(31, Pendulum(1975, 5, 31).subtract(days=0).day)

    def test_sub_days_negative(self):
        self.assertEqual(1, Pendulum(1975, 5, 31).subtract(days=-1).day)

    def test_sub_weeks_positive(self):
        self.assertEqual(14, Pendulum(1975, 5, 21).subtract(weeks=1).day)

    def test_sub_weeks_zero(self):
        self.assertEqual(21, Pendulum(1975, 5, 21).subtract(weeks=0).day)

    def test_sub_weeks_negative(self):
        self.assertEqual(28, Pendulum(1975, 5, 21).subtract(weeks=-1).day)

    def test_sub_hours_positive(self):
        self.assertEqual(23, Pendulum(1975, 5, 21, 0, 0, 0).subtract(hours=1).hour)

    def test_sub_hours_zero(self):
        self.assertEqual(0, Pendulum(1975, 5, 21, 0, 0, 0).subtract(hours=0).hour)

    def test_sub_hours_negative(self):
        self.assertEqual(1, Pendulum(1975, 5, 21, 0, 0, 0).subtract(hours=-1).hour)

    def test_sub_minutes_positive(self):
        self.assertEqual(59, Pendulum(1975, 5, 21, 0, 0, 0).subtract(minutes=1).minute)

    def test_sub_minutes_zero(self):
        self.assertEqual(0, Pendulum(1975, 5, 21, 0, 0, 0).subtract(minutes=0).minute)

    def test_sub_minutes_negative(self):
        self.assertEqual(1, Pendulum(1975, 5, 21, 0, 0, 0).subtract(minutes=-1).minute)

    def test_sub_seconds_positive(self):
        self.assertEqual(59, Pendulum(1975, 5, 21, 0, 0, 0).subtract(seconds=1).second)

    def test_sub_seconds_zero(self):
        self.assertEqual(0, Pendulum(1975, 5, 21, 0, 0, 0).subtract(seconds=0).second)

    def test_sub_seconds_negative(self):
        self.assertEqual(1, Pendulum(1975, 5, 21, 0, 0, 0).subtract(seconds=-1).second)

    def test_subtract_timedelta(self):
        delta = timedelta(days=6, seconds=16, microseconds=654321)
        d = Pendulum.create(2015, 3, 14, 3, 12, 15, 777777)

        d = d.subtract_timedelta(delta)
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

    def test_subtract_time_to_new_transition_skipped(self):
        dt = pendulum.create(2013, 3, 31, 3, 0, 0, 0, 'Europe/Paris')

        self.assertPendulum(dt, 2013, 3, 31, 3, 0, 0, 0)
        self.assertEqual('Europe/Paris', dt.timezone_name)
        self.assertEqual(7200, dt.offset)
        self.assertTrue(dt.is_dst)

        dt = dt.subtract(microseconds=1)

        self.assertPendulum(dt, 2013, 3, 31, 1, 59, 59, 999999)
        self.assertEqual('Europe/Paris', dt.timezone_name)
        self.assertEqual(3600, dt.offset)
        self.assertFalse(dt.is_dst)

        dt = pendulum.create(2013, 3, 10, 3, 0, 0, 0, 'America/New_York')

        self.assertPendulum(dt, 2013, 3, 10, 3, 0, 0, 0)
        self.assertEqual('America/New_York', dt.timezone_name)
        self.assertEqual(-4 * 3600, dt.offset)
        self.assertTrue(dt.is_dst)

        dt = dt.subtract(microseconds=1)

        self.assertPendulum(dt, 2013, 3, 10, 1, 59, 59, 999999)
        self.assertEqual('America/New_York', dt.timezone_name)
        self.assertEqual(-5 * 3600, dt.offset)
        self.assertFalse(dt.is_dst)

        dt = pendulum.create(1957, 4, 28, 3, 0, 0, 0, 'America/New_York')

        self.assertPendulum(dt, 1957, 4, 28, 3, 0, 0, 0)
        self.assertEqual('America/New_York', dt.timezone_name)
        self.assertEqual(-4 * 3600, dt.offset)
        self.assertTrue(dt.is_dst)

        dt = dt.subtract(microseconds=1)

        self.assertPendulum(dt, 1957, 4, 28, 1, 59, 59, 999999)
        self.assertEqual('America/New_York', dt.timezone_name)
        self.assertEqual(-5 * 3600, dt.offset)
        self.assertFalse(dt.is_dst)

    def test_subtract_time_to_new_transition_skipped_big(self):
        dt = pendulum.create(2013, 3, 31, 3, 0, 0, 0, 'Europe/Paris')

        self.assertPendulum(dt, 2013, 3, 31, 3, 0, 0, 0)
        self.assertEqual('Europe/Paris', dt.timezone_name)
        self.assertEqual(7200, dt.offset)
        self.assertTrue(dt.is_dst)

        dt = dt.subtract(days=1)

        self.assertPendulum(dt, 2013, 3, 30, 3, 0, 0, 0)
        self.assertEqual('Europe/Paris', dt.timezone_name)
        self.assertEqual(3600, dt.offset)
        self.assertFalse(dt.is_dst)

    def test_subtract_time_to_new_transition_repeated(self):
        dt = pendulum.create(2013, 10, 27, 2, 0, 0, 0, 'Europe/Paris')

        self.assertPendulum(dt, 2013, 10, 27, 2, 0, 0, 0)
        self.assertEqual('Europe/Paris', dt.timezone_name)
        self.assertEqual(3600, dt.offset)
        self.assertFalse(dt.is_dst)

        dt = dt.subtract(microseconds=1)

        self.assertPendulum(dt, 2013, 10, 27, 2, 59, 59, 999999)
        self.assertEqual('Europe/Paris', dt.timezone_name)
        self.assertEqual(7200, dt.offset)
        self.assertTrue(dt.is_dst)

        dt = pendulum.create(2013, 11, 3, 1, 0, 0, 0, 'America/New_York')

        self.assertPendulum(dt, 2013, 11, 3, 1, 0, 0, 0)
        self.assertEqual('America/New_York', dt.timezone_name)
        self.assertEqual(-5 * 3600, dt.offset)
        self.assertFalse(dt.is_dst)

        dt = dt.subtract(microseconds=1)

        self.assertPendulum(dt, 2013, 11, 3, 1, 59, 59, 999999)
        self.assertEqual('America/New_York', dt.timezone_name)
        self.assertEqual(-4 * 3600, dt.offset)
        self.assertTrue(dt.is_dst)

    def test_subtract_time_to_new_transition_repeated_big(self):
        dt = pendulum.create(2013, 10, 27, 2, 0, 0, 0, 'Europe/Paris')

        self.assertPendulum(dt, 2013, 10, 27, 2, 0, 0, 0)
        self.assertEqual('Europe/Paris', dt.timezone_name)
        self.assertEqual(3600, dt.offset)
        self.assertFalse(dt.is_dst)

        dt = dt.subtract(days=1)

        self.assertPendulum(dt, 2013, 10, 26, 2, 0, 0, 0)
        self.assertEqual('Europe/Paris', dt.timezone_name)
        self.assertEqual(7200, dt.offset)
        self.assertTrue(dt.is_dst)

    def test_subtract_invalid_type(self):
        d = Pendulum(1975, 5, 21, 0, 0, 0)

        try:
            d - 'ab'
            self.fail()
        except TypeError:
            pass

        try:
            'ab' - d
            self.fail()
        except TypeError:
            pass
