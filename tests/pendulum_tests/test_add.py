# -*- coding: utf-8 -*-

from .. import AbstractTestCase

import pendulum
from datetime import timedelta
from pendulum import Pendulum


class AddTest(AbstractTestCase):

    def test_add_years_positive(self):
        self.assertEqual(1976, Pendulum.create(1975).add(years=1).year)

    def test_add_years_zero(self):
        self.assertEqual(1975, Pendulum.create(1975).add(years=0).year)

    def test_add_years_negative(self):
        self.assertEqual(1974, Pendulum.create(1975).add(years=-1).year)

    def test_add_months_positive(self):
        self.assertEqual(1, Pendulum.create(1975, 12).add(months=1).month)

    def test_add_months_zero(self):
        self.assertEqual(12, Pendulum.create(1975, 12).add(months=0).month)

    def test_add_months_negative(self):
        self.assertEqual(11, Pendulum.create(1975, 12).add(months=-1).month)

    def test_add_month_with_overflow(self):
        self.assertEqual(2, Pendulum(2012, 1, 31).add(months=1).month)

    def test_add_days_positive(self):
        self.assertEqual(1, Pendulum(1975, 5, 31).add(days=1).day)

    def test_add_days_zero(self):
        self.assertEqual(31, Pendulum(1975, 5, 31).add(days=0).day)

    def test_add_days_negative(self):
        self.assertEqual(30, Pendulum(1975, 5, 31).add(days=-1).day)

    def test_add_weeks_positive(self):
        self.assertEqual(28, Pendulum(1975, 5, 21).add(weeks=1).day)

    def test_add_weeks_zero(self):
        self.assertEqual(21, Pendulum(1975, 5, 21).add(weeks=0).day)

    def test_add_weeks_negative(self):
        self.assertEqual(14, Pendulum(1975, 5, 21).add(weeks=-1).day)

    def test_add_hours_positive(self):
        self.assertEqual(1, Pendulum(1975, 5, 21, 0, 0, 0).add(hours=1).hour)

    def test_add_hours_zero(self):
        self.assertEqual(0, Pendulum(1975, 5, 21, 0, 0, 0).add(hours=0).hour)

    def test_add_hours_negative(self):
        self.assertEqual(23, Pendulum(1975, 5, 21, 0, 0, 0).add(hours=-1).hour)

    def test_add_minutes_positive(self):
        self.assertEqual(1, Pendulum(1975, 5, 21, 0, 0, 0).add(minutes=1).minute)

    def test_add_minutes_zero(self):
        self.assertEqual(0, Pendulum(1975, 5, 21, 0, 0, 0).add(minutes=0).minute)

    def test_add_minutes_negative(self):
        self.assertEqual(59, Pendulum(1975, 5, 21, 0, 0, 0).add(minutes=-1).minute)

    def test_add_seconds_positive(self):
        self.assertEqual(1, Pendulum(1975, 5, 21, 0, 0, 0).add(seconds=1).second)

    def test_add_seconds_zero(self):
        self.assertEqual(0, Pendulum(1975, 5, 21, 0, 0, 0).add(seconds=0).second)

    def test_add_seconds_negative(self):
        self.assertEqual(59, Pendulum(1975, 5, 21, 0, 0, 0).add(seconds=-1).second)

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

    def test_addition_invalid_type(self):
        d = Pendulum.create(2015, 3, 14, 3, 12, 15, 654321)

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

    def test_add_to_fixed_timezones(self):
        dt = pendulum.parse('2015-03-08T01:00:00-06:00')
        dt = dt.add(weeks=1)

        self.assertPendulum(dt, 2015, 3, 15, 1, 0, 0)
        self.assertEqual('-06:00', dt.timezone_name)
        self.assertEqual(-6 * 3600, dt.offset)

    def test_add_time_to_new_transition_skipped(self):
        dt = pendulum.create(2013, 3, 31, 1, 59, 59, 999999, 'Europe/Paris')

        self.assertPendulum(dt, 2013, 3, 31, 1, 59, 59, 999999)
        self.assertEqual('Europe/Paris', dt.timezone_name)
        self.assertEqual(3600, dt.offset)
        self.assertFalse(dt.is_dst)

        dt = dt.add(microseconds=1)

        self.assertPendulum(dt, 2013, 3, 31, 3, 0, 0, 0)
        self.assertEqual('Europe/Paris', dt.timezone_name)
        self.assertEqual(7200, dt.offset)
        self.assertTrue(dt.is_dst)

        dt = pendulum.create(2013, 3, 10, 1, 59, 59, 999999, 'America/New_York')

        self.assertPendulum(dt, 2013, 3, 10, 1, 59, 59, 999999)
        self.assertEqual('America/New_York', dt.timezone_name)
        self.assertEqual(-5 * 3600, dt.offset)
        self.assertFalse(dt.is_dst)

        dt = dt.add(microseconds=1)

        self.assertPendulum(dt, 2013, 3, 10, 3, 0, 0, 0)
        self.assertEqual('America/New_York', dt.timezone_name)
        self.assertEqual(- 4 * 3600, dt.offset)
        self.assertTrue(dt.is_dst)

        dt = pendulum.create(1957, 4, 28, 1, 59, 59, 999999, 'America/New_York')

        self.assertPendulum(dt, 1957, 4, 28, 1, 59, 59, 999999)
        self.assertEqual('America/New_York', dt.timezone_name)
        self.assertEqual(-5 * 3600, dt.offset)
        self.assertFalse(dt.is_dst)

        dt = dt.add(microseconds=1)

        self.assertPendulum(dt, 1957, 4, 28, 3, 0, 0, 0)
        self.assertEqual('America/New_York', dt.timezone_name)
        self.assertEqual(- 4 * 3600, dt.offset)
        self.assertTrue(dt.is_dst)

    def test_add_time_to_new_transition_skipped_big(self):
        dt = pendulum.create(2013, 3, 31, 1, tz='Europe/Paris')

        self.assertPendulum(dt, 2013, 3, 31, 1, 0, 0, 0)
        self.assertEqual('Europe/Paris', dt.timezone_name)
        self.assertEqual(3600, dt.offset)
        self.assertFalse(dt.is_dst)

        dt = dt.add(weeks=1)

        self.assertPendulum(dt, 2013, 4, 7, 1, 0, 0, 0)
        self.assertEqual('Europe/Paris', dt.timezone_name)
        self.assertEqual(7200, dt.offset)
        self.assertTrue(dt.is_dst)

    def test_add_time_to_new_transition_repeated(self):
        dt = pendulum.create(2013, 10, 27, 1, 59, 59, 999999, 'Europe/Paris')
        dt = dt.add(hours=1)

        self.assertPendulum(dt, 2013, 10, 27, 2, 59, 59, 999999)
        self.assertEqual('Europe/Paris', dt.timezone_name)
        self.assertEqual(7200, dt.offset)
        self.assertTrue(dt.is_dst)

        dt = dt.add(microseconds=1)

        self.assertPendulum(dt, 2013, 10, 27, 2, 0, 0, 0)
        self.assertEqual('Europe/Paris', dt.timezone_name)
        self.assertEqual(3600, dt.offset)
        self.assertFalse(dt.is_dst)


        dt = pendulum.create(2013, 11, 3, 0, 59, 59, 999999, 'America/New_York')
        dt = dt.add(hours=1)

        self.assertPendulum(dt, 2013, 11, 3, 1, 59, 59, 999999)
        self.assertEqual('America/New_York', dt.timezone_name)
        self.assertEqual(-4 * 3600, dt.offset)
        self.assertTrue(dt.is_dst)

        dt = dt.add(microseconds=1)

        self.assertPendulum(dt, 2013, 11, 3, 1, 0, 0, 0)
        self.assertEqual('America/New_York', dt.timezone_name)
        self.assertEqual(-5 * 3600, dt.offset)
        self.assertFalse(dt.is_dst)

    def test_add_time_to_new_transition_repeated_big(self):
        dt = pendulum.create(2013, 10, 27, 1, tz='Europe/Paris')

        self.assertPendulum(dt, 2013, 10, 27, 1, 0, 0, 0)
        self.assertEqual('Europe/Paris', dt.timezone_name)
        self.assertEqual(7200, dt.offset)
        self.assertTrue(dt.is_dst)

        dt = dt.add(weeks=1)

        self.assertPendulum(dt, 2013, 11, 3, 1, 0, 0, 0)
        self.assertEqual('Europe/Paris', dt.timezone_name)
        self.assertEqual(3600, dt.offset)
        self.assertFalse(dt.is_dst)

    def test_add_time_to_new_transition_does_not_use_transition_rule(self):
        pendulum.set_transition_rule(pendulum.TRANSITION_ERROR)
        dt = pendulum.create(2013, 3, 31, 1, 59, 59, 999999, 'Europe/Paris')

        self.assertPendulum(dt, 2013, 3, 31, 1, 59, 59, 999999)
        self.assertEqual('Europe/Paris', dt.timezone_name)
        self.assertEqual(3600, dt.offset)
        self.assertFalse(dt.is_dst)

        dt = dt.add(microseconds=1)

        self.assertPendulum(dt, 2013, 3, 31, 3, 0, 0, 0)
        self.assertEqual('Europe/Paris', dt.timezone_name)
        self.assertEqual(7200, dt.offset)
        self.assertTrue(dt.is_dst)
