# -*- coding: utf-8 -*-

from contextlib import contextmanager
from pendulum import Pendulum

from . import AbstractTestCase


class DiffTest(AbstractTestCase):

    @contextmanager
    def wrap_with_test_now(self, dt=None):
        yield super(DiffTest, self).wrap_with_test_now(dt or Pendulum.create_from_date(2012, 1, 1))

    def test_diff_in_years_positive(self):
        dt = Pendulum.create_from_date(2000, 1, 1)
        self.assertEqual(1, dt.diff_in_years(dt.copy().add_year()))

    def test_diff_in_years_negative_with_sign(self):
        dt = Pendulum.create_from_date(2000, 1, 1)
        self.assertEqual(-1, dt.diff_in_years(dt.copy().sub_year(), False))

    def test_diff_in_years_negative_no_sign(self):
        dt = Pendulum.create_from_date(2000, 1, 1)
        self.assertEqual(1, dt.diff_in_years(dt.copy().sub_year()))

    def test_diff_in_years_vs_default_now(self):
        with self.wrap_with_test_now():
            self.assertEqual(1, Pendulum.now().sub_year().diff_in_years())

    def test_diff_in_years_ensure_is_truncated(self):
        dt = Pendulum.create_from_date(2000, 1, 1)
        self.assertEqual(1, dt.diff_in_years(dt.copy().add_year().add_months(7)))

    def test_diff_in_months_positive(self):
        dt = Pendulum.create_from_date(2000, 1, 1)
        self.assertEqual(13, dt.diff_in_months(dt.copy().add_year().add_month()))

    def test_diff_in_months_negative_with_sign(self):
        dt = Pendulum.create_from_date(2000, 1, 1)
        self.assertEqual(-11, dt.diff_in_months(dt.copy().sub_year().add_month(), False))

    def test_diff_in_months_negative_no_sign(self):
        dt = Pendulum.create_from_date(2000, 1, 1)
        self.assertEqual(11, dt.diff_in_months(dt.copy().sub_year().add_month()))

    def test_diff_in_months_vs_default_now(self):
        with self.wrap_with_test_now():
            self.assertEqual(12, Pendulum.now().sub_year().diff_in_months())

    def test_diff_in_months_ensure_is_truncated(self):
        dt = Pendulum.create_from_date(2000, 1, 1)
        self.assertEqual(1, dt.diff_in_months(dt.copy().add_month().add_days(16)))

    def test_diff_in_days_positive(self):
        dt = Pendulum.create_from_date(2000, 1, 1)
        self.assertEqual(366, dt.diff_in_days(dt.copy().add_year()))

    def test_diff_in_days_negative_with_sign(self):
        dt = Pendulum.create_from_date(2000, 1, 1)
        self.assertEqual(-365, dt.diff_in_days(dt.copy().sub_year(), False))

    def test_diff_in_days_negative_no_sign(self):
        dt = Pendulum.create_from_date(2000, 1, 1)
        self.assertEqual(365, dt.diff_in_days(dt.copy().sub_year()))

    def test_diff_in_days_vs_default_now(self):
        with self.wrap_with_test_now():
            self.assertEqual(7, Pendulum.now().sub_week().diff_in_days())

    def test_diff_in_days_ensure_is_truncated(self):
        dt = Pendulum.create_from_date(2000, 1, 1)
        self.assertEqual(1, dt.diff_in_days(dt.copy().add_day().add_hours(13)))

    def test_diff_in_weeks_positive(self):
        dt = Pendulum.create_from_date(2000, 1, 1)
        self.assertEqual(52, dt.diff_in_weeks(dt.copy().add_year()))

    def test_diff_in_weeks_negative_with_sign(self):
        dt = Pendulum.create_from_date(2000, 1, 1)
        self.assertEqual(-52, dt.diff_in_weeks(dt.copy().sub_year(), False))

    def test_diff_in_weeks_negative_no_sign(self):
        dt = Pendulum.create_from_date(2000, 1, 1)
        self.assertEqual(52, dt.diff_in_weeks(dt.copy().sub_year()))

    def test_diff_in_weeks_vs_default_now(self):
        with self.wrap_with_test_now():
            self.assertEqual(1, Pendulum.now().sub_week().diff_in_weeks())

    def test_diff_in_weeks_ensure_is_truncated(self):
        dt = Pendulum.create_from_date(2000, 1, 1)
        self.assertEqual(0, dt.diff_in_weeks(dt.copy().add_week().sub_day()))

    def test_diff_in_hours_positive(self):
        dt = Pendulum.create_from_date(2000, 1, 1)
        self.assertEqual(26, dt.diff_in_hours(dt.copy().add_day().add_hours(2)))

    def test_diff_in_hours_negative_with_sign(self):
        dt = Pendulum.create_from_date(2000, 1, 1)
        self.assertEqual(-22, dt.diff_in_hours(dt.copy().sub_day().add_hours(2), False))

    def test_diff_in_hours_negative_no_sign(self):
        dt = Pendulum.create_from_date(2000, 1, 1)
        self.assertEqual(22, dt.diff_in_hours(dt.copy().sub_day().add_hours(2)))

    def test_diff_in_hours_vs_default_now(self):
        with self.wrap_with_test_now(Pendulum.create_from_date(2012, 1, 15)):
            self.assertEqual(48, Pendulum.now().sub_days(2).diff_in_hours())

    def test_diff_in_hours_ensure_is_truncated(self):
        dt = Pendulum.create_from_date(2000, 1, 1)
        self.assertEqual(1, dt.diff_in_hours(dt.copy().add_hour().add_minutes(31)))

    def test_diff_in_minutes_positive(self):
        dt = Pendulum.create_from_date(2000, 1, 1)
        self.assertEqual(62, dt.diff_in_minutes(dt.copy().add_hour().add_minutes(2)))

    def test_diff_in_minutes_positive_big(self):
        dt = Pendulum.create_from_date(2000, 1, 1)
        self.assertEqual(1502, dt.diff_in_minutes(dt.copy().add_hours(25).add_minutes(2)))

    def test_diff_in_minutes_negative_with_sign(self):
        dt = Pendulum.create_from_date(2000, 1, 1)
        self.assertEqual(-58, dt.diff_in_minutes(dt.copy().sub_hour().add_minutes(2), False))

    def test_diff_in_minutes_negative_no_sign(self):
        dt = Pendulum.create_from_date(2000, 1, 1)
        self.assertEqual(58, dt.diff_in_minutes(dt.copy().sub_hour().add_minutes(2)))

    def test_diff_in_minutes_vs_default_now(self):
        with self.wrap_with_test_now():
            self.assertEqual(60, Pendulum.now().sub_hour().diff_in_minutes())

    def test_diff_in_minutes_ensure_is_truncated(self):
        dt = Pendulum.create_from_date(2000, 1, 1)
        self.assertEqual(1, dt.diff_in_minutes(dt.copy().add_minute().add_seconds(31)))

    def test_diff_in_seconds_positive(self):
        dt = Pendulum.create_from_date(2000, 1, 1)
        self.assertEqual(62, dt.diff_in_seconds(dt.copy().add_minute().add_seconds(2)))

    def test_diff_in_seconds_positive_big(self):
        dt = Pendulum.create_from_date(2000, 1, 1)
        self.assertEqual(7202, dt.diff_in_seconds(dt.copy().add_hours(2).add_seconds(2)))

    def test_diff_in_seconds_negative_with_sign(self):
        dt = Pendulum.create_from_date(2000, 1, 1)
        self.assertEqual(-58, dt.diff_in_seconds(dt.copy().sub_minute().add_seconds(2), False))

    def test_diff_in_seconds_negative_no_sign(self):
        dt = Pendulum.create_from_date(2000, 1, 1)
        self.assertEqual(58, dt.diff_in_seconds(dt.copy().sub_minute().add_seconds(2)))

    def test_diff_in_seconds_vs_default_now(self):
        with self.wrap_with_test_now():
            self.assertEqual(3600, Pendulum.now().sub_hour().diff_in_seconds())

    def test_diff_in_seconds_ensure_is_truncated(self):
        dt = Pendulum.create_from_date(2000, 1, 1)
        self.assertEqual(1, dt.diff_in_seconds(dt.copy().add_seconds(1.9)))

    def test_diff_in_seconds_with_timezones(self):
        dt_ottawa = Pendulum(2000, 1, 1, 13, tzinfo='America/Toronto')
        dt_vancouver = Pendulum(2000, 1, 1, 13, tzinfo='America/Vancouver')
        self.assertEqual(3 * 60 * 60, dt_ottawa.diff_in_seconds(dt_vancouver))

    # TODO: Diff for humans
