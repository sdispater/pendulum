# -*- coding: utf-8 -*-

from datetime import date
from pendulum import Pendulum, Date

from .. import AbstractTestCase


class DiffTest(AbstractTestCase):

    def test_diff_in_years_positive(self):
        dt = Date(2000, 1, 1)
        self.assertEqual(1, dt.diff(dt.add(years=1)).in_years())

    def test_diff_in_years_negative_with_sign(self):
        dt = Date(2000, 1, 1)
        self.assertEqual(-1, dt.diff(dt.subtract(years=1), False).in_years())

    def test_diff_in_years_negative_no_sign(self):
        dt = Date(2000, 1, 1)
        self.assertEqual(1, dt.diff(dt.subtract(years=1)).in_years())

    def test_diff_in_years_vs_default_now(self):
        self.assertEqual(1, Date.today().subtract(years=1).diff().in_years())

    def test_diff_in_years_ensure_is_truncated(self):
        dt = Date(2000, 1, 1)
        self.assertEqual(1, dt.diff(dt.add(years=1).add(months=7)).in_years())

    def test_diff_in_months_positive(self):
        dt = Date(2000, 1, 1)
        self.assertEqual(13, dt.diff(dt.add(years=1).add(months=1)).in_months())

    def test_diff_in_months_negative_with_sign(self):
        dt = Date(2000, 1, 1)
        self.assertEqual(-11, dt.diff(dt.subtract(years=1).add(months=1), False).in_months())

    def test_diff_in_months_negative_no_sign(self):
        dt = Date(2000, 1, 1)
        self.assertEqual(11, dt.diff(dt.subtract(years=1).add(months=1)).in_months())

    def test_diff_in_months_vs_default_now(self):
        self.assertEqual(12, Date.today().subtract(years=1).diff().in_months())

    def test_diff_in_months_ensure_is_truncated(self):
        dt = Date(2000, 1, 1)
        self.assertEqual(1, dt.diff(dt.add(months=1).add(days=16)).in_months())

    def test_diff_in_days_positive(self):
        dt = Date(2000, 1, 1)
        self.assertEqual(366, dt.diff(dt.add(years=1)).in_days())

    def test_diff_in_days_negative_with_sign(self):
        dt = Date(2000, 1, 1)
        self.assertEqual(-365, dt.diff(dt.subtract(years=1), False).in_days())

    def test_diff_in_days_negative_no_sign(self):
        dt = Date(2000, 1, 1)
        self.assertEqual(365, dt.diff(dt.subtract(years=1)).in_days())

    def test_diff_in_days_vs_default_now(self):
        self.assertEqual(7, Date.today().subtract(weeks=1).diff().in_days())

    def test_diff_in_weekdays_positive(self):
        dt = Date(2000, 1, 1)
        self.assertEqual(21, dt.diff(dt.end_of('month')).in_weekdays())

    def test_diff_in_weekdays_negative_no_sign(self):
        dt = Date(2000, 1, 31)
        self.assertEqual(21, dt.diff(dt.start_of('month')).in_weekdays())

    def test_diff_in_weekdays_negative_with_sign(self):
        dt = Date(2000, 1, 31)
        self.assertEqual(-21, dt.diff(dt.start_of('month'), False).in_weekdays())

    def test_diff_in_weekend_days_positive(self):
        dt = Date(2000, 1, 1)
        self.assertEqual(10, dt.diff(dt.end_of('month')).in_weekend_days())

    def test_diff_in_weekend_days_negative_no_sign(self):
        dt = Date(2000, 1, 31)
        self.assertEqual(10, dt.diff(dt.start_of('month')).in_weekend_days())

    def test_diff_in_weekend_days_negative_with_sign(self):
        dt = Date(2000, 1, 31)
        self.assertEqual(-10, dt.diff(dt.start_of('month'), False).in_weekend_days())

    def test_diff_in_weeks_positive(self):
        dt = Date(2000, 1, 1)
        self.assertEqual(52, dt.diff(dt.add(years=1)).in_weeks())

    def test_diff_in_weeks_negative_with_sign(self):
        dt = Date(2000, 1, 1)
        self.assertEqual(-52, dt.diff(dt.subtract(years=1), False).in_weeks())

    def test_diff_in_weeks_negative_no_sign(self):
        dt = Date(2000, 1, 1)
        self.assertEqual(52, dt.diff(dt.subtract(years=1)).in_weeks())

    def test_diff_in_weeks_vs_default_now(self):
        self.assertEqual(1, Date.today().subtract(weeks=1).diff().in_weeks())

    def test_diff_in_weeks_ensure_is_truncated(self):
        dt = Date(2000, 1, 1)
        self.assertEqual(0, dt.diff(dt.add(weeks=1).subtract(days=1)).in_weeks())

    def test_diff_for_humans_now_and_day(self):
        self.assertEqual('1 day ago', Date.today().subtract(days=1).diff_for_humans())

    def test_diff_for_humans_now_and_days(self):
        self.assertEqual('2 days ago', Date.today().subtract(days=2).diff_for_humans())

    def test_diff_for_humans_now_and_nearly_week(self):
        self.assertEqual('6 days ago', Date.today().subtract(days=6).diff_for_humans())

    def test_diff_for_humans_now_and_week(self):
        self.assertEqual('1 week ago', Date.today().subtract(weeks=1).diff_for_humans())

    def test_diff_for_humans_now_and_weeks(self):
        self.assertEqual('2 weeks ago', Date.today().subtract(weeks=2).diff_for_humans())

    def test_diff_for_humans_now_and_nearly_month(self):
        self.assertEqual('3 weeks ago', Date.today().subtract(weeks=3).diff_for_humans())

    def test_diff_for_humans_now_and_month(self):
        with self.wrap_with_test_now(Pendulum.create(2016, 3, 1)):
            self.assertEqual('4 weeks ago', Date.today().subtract(weeks=4).diff_for_humans())
            self.assertEqual('1 month ago', Date.today().subtract(months=1).diff_for_humans())

        with self.wrap_with_test_now(Pendulum.create(2017, 2, 28)):
            self.assertEqual('1 month ago', Date.today().subtract(weeks=4).diff_for_humans())

    def test_diff_for_humans_now_and_months(self):
        self.assertEqual('2 months ago', Date.today().subtract(months=2).diff_for_humans())

    def test_diff_for_humans_now_and_nearly_year(self):
        self.assertEqual('11 months ago', Date.today().subtract(months=11).diff_for_humans())

    def test_diff_for_humans_now_and_year(self):
        self.assertEqual('1 year ago', Date.today().subtract(years=1).diff_for_humans())

    def test_diff_for_humans_now_and_years(self):
        self.assertEqual('2 years ago', Date.today().subtract(years=2).diff_for_humans())

    def test_diff_for_humans_now_and_future_day(self):
        self.assertEqual('1 day from now', Date.today().add(days=1).diff_for_humans())

    def test_diff_for_humans_now_and_future_days(self):
        self.assertEqual('2 days from now', Date.today().add(days=2).diff_for_humans())

    def test_diff_for_humans_now_and_nearly_future_week(self):
        self.assertEqual('6 days from now', Date.today().add(days=6).diff_for_humans())

    def test_diff_for_humans_now_and_future_week(self):
        self.assertEqual('1 week from now', Date.today().add(weeks=1).diff_for_humans())

    def test_diff_for_humans_now_and_future_weeks(self):
        self.assertEqual('2 weeks from now', Date.today().add(weeks=2).diff_for_humans())

    def test_diff_for_humans_now_and_nearly_future_month(self):
        self.assertEqual('3 weeks from now', Date.today().add(weeks=3).diff_for_humans())

    def test_diff_for_humans_now_and_future_month(self):
        with self.wrap_with_test_now(Pendulum.create(2016, 3, 1)):
            self.assertEqual('4 weeks from now', Date.today().add(weeks=4).diff_for_humans())
            self.assertEqual('1 month from now', Date.today().add(months=1).diff_for_humans())

        with self.wrap_with_test_now(Pendulum.create(2017, 3, 31)):
            self.assertEqual('1 month from now', Date.today().add(months=1).diff_for_humans())

        with self.wrap_with_test_now(Pendulum.create(2017, 4, 30)):
            self.assertEqual('1 month from now', Date.today().add(months=1).diff_for_humans())

        with self.wrap_with_test_now(Pendulum.create(2017, 1, 31)):
            self.assertEqual('1 month from now', Date.today().add(weeks=4).diff_for_humans())

    def test_diff_for_humans_now_and_future_months(self):
        self.assertEqual('2 months from now', Date.today().add(months=2).diff_for_humans())

    def test_diff_for_humans_now_and_nearly_future_year(self):
        self.assertEqual('11 months from now', Date.today().add(months=11).diff_for_humans())

    def test_diff_for_humans_now_and_future_year(self):
        self.assertEqual('1 year from now', Date.today().add(years=1).diff_for_humans())

    def test_diff_for_humans_now_and_future_years(self):
        self.assertEqual('2 years from now', Date.today().add(years=2).diff_for_humans())

    def test_diff_for_humans_other_and_day(self):
        self.assertEqual('1 day before', Date.today().diff_for_humans(Date.today().add(days=1)))

    def test_diff_for_humans_other_and_days(self):
        self.assertEqual('2 days before', Date.today().diff_for_humans(Date.today().add(days=2)))

    def test_diff_for_humans_other_and_nearly_week(self):
        self.assertEqual('6 days before', Date.today().diff_for_humans(Date.today().add(days=6)))

    def test_diff_for_humans_other_and_week(self):
        self.assertEqual('1 week before', Date.today().diff_for_humans(Date.today().add(weeks=1)))

    def test_diff_for_humans_other_and_weeks(self):
        self.assertEqual('2 weeks before', Date.today().diff_for_humans(Date.today().add(weeks=2)))

    def test_diff_for_humans_other_and_nearly_month(self):
        self.assertEqual('3 weeks before', Date.today().diff_for_humans(Date.today().add(weeks=3)))

    def test_diff_for_humans_other_and_month(self):
        with self.wrap_with_test_now(Pendulum.create(2016, 3, 1)):
            self.assertEqual('4 weeks before', Date.today().diff_for_humans(Date.today().add(weeks=4)))
            self.assertEqual('1 month before', Date.today().diff_for_humans(Date.today().add(months=1)))

        with self.wrap_with_test_now(Pendulum.create(2017, 3, 31)):
            self.assertEqual('1 month before', Date.today().diff_for_humans(Date.today().add(months=1)))

        with self.wrap_with_test_now(Pendulum.create(2017, 4, 30)):
            self.assertEqual('1 month before', Date.today().diff_for_humans(Date.today().add(months=1)))

        with self.wrap_with_test_now(Pendulum.create(2017, 1, 31)):
            self.assertEqual('1 month before', Date.today().diff_for_humans(Date.today().add(weeks=4)))

    def test_diff_for_humans_other_and_months(self):
        self.assertEqual('2 months before', Date.today().diff_for_humans(Date.today().add(months=2)))

    def test_diff_for_humans_other_and_nearly_year(self):
        self.assertEqual('11 months before', Date.today().diff_for_humans(Date.today().add(months=11)))

    def test_diff_for_humans_other_and_year(self):
        self.assertEqual('1 year before', Date.today().diff_for_humans(Date.today().add(years=1)))

    def test_diff_for_humans_other_and_years(self):
        self.assertEqual('2 years before', Date.today().diff_for_humans(Date.today().add(years=2)))

    def test_diff_for_humans_other_and_future_day(self):
        self.assertEqual('1 day after', Date.today().diff_for_humans(Date.today().subtract(days=1)))

    def test_diff_for_humans_other_and_future_days(self):
        self.assertEqual('2 days after', Date.today().diff_for_humans(Date.today().subtract(days=2)))

    def test_diff_for_humans_other_and_nearly_future_week(self):
        self.assertEqual('6 days after', Date.today().diff_for_humans(Date.today().subtract(days=6)))

    def test_diff_for_humans_other_and_future_week(self):
        self.assertEqual('1 week after', Date.today().diff_for_humans(Date.today().subtract(weeks=1)))

    def test_diff_for_humans_other_and_future_weeks(self):
        self.assertEqual('2 weeks after', Date.today().diff_for_humans(Date.today().subtract(weeks=2)))

    def test_diff_for_humans_other_and_nearly_future_month(self):
        self.assertEqual('3 weeks after', Date.today().diff_for_humans(Date.today().subtract(weeks=3)))

    def test_diff_for_humans_other_and_future_month(self):
        with self.wrap_with_test_now(Pendulum.create(2016, 3, 1)):
            self.assertEqual('4 weeks after', Date.today().diff_for_humans(Date.today().subtract(weeks=4)))
            self.assertEqual('1 month after', Date.today().diff_for_humans(Date.today().subtract(months=1)))

        with self.wrap_with_test_now(Pendulum.create(2017, 2, 28)):
            self.assertEqual('1 month after', Date.today().diff_for_humans(Date.today().subtract(weeks=4)))

    def test_diff_for_humans_other_and_future_months(self):
        self.assertEqual('2 months after', Date.today().diff_for_humans(Date.today().subtract(months=2)))

    def test_diff_for_humans_other_and_nearly_future_year(self):
        self.assertEqual('11 months after', Date.today().diff_for_humans(Date.today().subtract(months=11)))

    def test_diff_for_humans_other_and_future_year(self):
        self.assertEqual('1 year after', Date.today().diff_for_humans(Date.today().subtract(years=1)))

    def test_diff_for_humans_other_and_future_years(self):
        self.assertEqual('2 years after', Date.today().diff_for_humans(Date.today().subtract(years=2)))

    def test_diff_for_humans_absolute_days(self):
        self.assertEqual('2 days', Date.today().diff_for_humans(Date.today().subtract(days=2), True))
        self.assertEqual('2 days', Date.today().diff_for_humans(Date.today().add(days=2), True))

    def test_diff_for_humans_absolute_weeks(self):
        self.assertEqual('2 weeks', Date.today().diff_for_humans(Date.today().subtract(weeks=2), True))
        self.assertEqual('2 weeks', Date.today().diff_for_humans(Date.today().add(weeks=2), True))

    def test_diff_for_humans_absolute_months(self):
        self.assertEqual('2 months', Date.today().diff_for_humans(Date.today().subtract(months=2), True))
        self.assertEqual('2 months', Date.today().diff_for_humans(Date.today().add(months=2), True))

    def test_diff_for_humans_absolute_years(self):
        self.assertEqual('1 year', Date.today().diff_for_humans(Date.today().subtract(years=1), True))
        self.assertEqual('1 year', Date.today().diff_for_humans(Date.today().add(years=1), True))

    def test_diff_accuracy(self):
        # DST
        today = Pendulum.create(2017, 3, 7, tz='America/Toronto')

        with self.wrap_with_test_now(today):
            diff = today.add(days=6).diff(today, abs=True)
            self.assertEqual(5, diff.days)
            self.assertEqual(6, diff.remaining_days)
            self.assertEqual(0, diff.hours)
            self.assertEqual('6 days', diff.in_words())

    def test_diff_for_humans_accuracy(self):
        today = Pendulum.today()

        with self.wrap_with_test_now(today.add(days=1)):
            self.assertEqual('1 year', today.add(years=1).diff_for_humans(absolute=True))

        with self.wrap_with_test_now(today):
            self.assertEqual('6 days', today.add(days=6).diff_for_humans(absolute=True))
            self.assertEqual('1 week', today.add(days=7).diff_for_humans(absolute=True))
            self.assertEqual('3 weeks', today.add(days=20).diff_for_humans(absolute=True))
            self.assertEqual('2 weeks', today.add(days=14).diff_for_humans(absolute=True))
            self.assertEqual('2 weeks', today.add(days=13).diff_for_humans(absolute=True))

        # DST
        today = Pendulum.create(2017, 3, 7, tz='America/Toronto')
        with self.wrap_with_test_now(today):
            self.assertEqual('6 days', today.add(days=6).diff_for_humans(absolute=True))

    def test_subtraction(self):
        d = Date(2016, 7, 5)
        future_dt = date(2016, 7, 6)
        future = d.add(days=1)

        self.assertEqual(86400, (future - d).total_seconds())
        self.assertEqual(86400, (future_dt - d).total_seconds())
