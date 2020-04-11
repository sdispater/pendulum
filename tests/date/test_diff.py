from datetime import date

import pendulum
import pytest


@pytest.fixture
def today():
    return pendulum.today().date()


def test_diff_in_years_positive():
    dt = pendulum.date(2000, 1, 1)
    assert 1 == dt.diff(dt.add(years=1)).in_years()


def test_diff_in_years_negative_with_sign():
    dt = pendulum.date(2000, 1, 1)
    assert -1 == dt.diff(dt.subtract(years=1), False).in_years()


def test_diff_in_years_negative_no_sign():
    dt = pendulum.date(2000, 1, 1)
    assert 1 == dt.diff(dt.subtract(years=1)).in_years()


def test_diff_in_years_vs_default_now(today):
    assert 1 == today.subtract(years=1).diff().in_years()


def test_diff_in_years_ensure_is_truncated():
    dt = pendulum.date(2000, 1, 1)
    assert 1 == dt.diff(dt.add(years=1).add(months=7)).in_years()


def test_diff_in_months_positive():
    dt = pendulum.date(2000, 1, 1)
    assert 13 == dt.diff(dt.add(years=1).add(months=1)).in_months()


def test_diff_in_months_negative_with_sign():
    dt = pendulum.date(2000, 1, 1)

    assert -11 == dt.diff(dt.subtract(years=1).add(months=1), False).in_months()


def test_diff_in_months_negative_no_sign():
    dt = pendulum.date(2000, 1, 1)
    assert 11 == dt.diff(dt.subtract(years=1).add(months=1)).in_months()


def test_diff_in_months_vs_default_now(today):
    assert 12 == today.subtract(years=1).diff().in_months()


def test_diff_in_months_ensure_is_truncated():
    dt = pendulum.date(2000, 1, 1)
    assert 1 == dt.diff(dt.add(months=1).add(days=16)).in_months()


def test_diff_in_days_positive():
    dt = pendulum.date(2000, 1, 1)
    assert 366 == dt.diff(dt.add(years=1)).in_days()


def test_diff_in_days_negative_with_sign():
    dt = pendulum.date(2000, 1, 1)
    assert -365 == dt.diff(dt.subtract(years=1), False).in_days()


def test_diff_in_days_negative_no_sign():
    dt = pendulum.date(2000, 1, 1)
    assert 365 == dt.diff(dt.subtract(years=1)).in_days()


def test_diff_in_days_vs_default_now(today):
    assert 7 == today.subtract(weeks=1).diff().in_days()


def test_diff_in_weeks_positive():
    dt = pendulum.date(2000, 1, 1)
    assert 52 == dt.diff(dt.add(years=1)).in_weeks()


def test_diff_in_weeks_negative_with_sign():
    dt = pendulum.date(2000, 1, 1)
    assert -52 == dt.diff(dt.subtract(years=1), False).in_weeks()


def test_diff_in_weeks_negative_no_sign():
    dt = pendulum.date(2000, 1, 1)
    assert 52 == dt.diff(dt.subtract(years=1)).in_weeks()


def test_diff_in_weeks_vs_default_now(today):
    assert 1 == today.subtract(weeks=1).diff().in_weeks()


def test_diff_in_weeks_ensure_is_truncated():
    dt = pendulum.date(2000, 1, 1)
    assert 0 == dt.diff(dt.add(weeks=1).subtract(days=1)).in_weeks()


def test_diff_for_humans_now_and_day(today):
    assert "1 day ago" == today.subtract(days=1).diff_for_humans()


def test_diff_for_humans_now_and_days(today):
    assert "2 days ago" == today.subtract(days=2).diff_for_humans()


def test_diff_for_humans_now_and_nearly_week(today):
    assert "6 days ago" == today.subtract(days=6).diff_for_humans()


def test_diff_for_humans_now_and_week(today):
    assert "1 week ago" == today.subtract(weeks=1).diff_for_humans()


def test_diff_for_humans_now_and_weeks(today):
    assert "2 weeks ago" == today.subtract(weeks=2).diff_for_humans()


def test_diff_for_humans_now_and_nearly_month(today):
    assert "3 weeks ago" == today.subtract(weeks=3).diff_for_humans()


def test_diff_for_humans_now_and_month():
    with pendulum.test(pendulum.datetime(2016, 3, 1)):
        today = pendulum.today().date()

        assert "4 weeks ago" == today.subtract(weeks=4).diff_for_humans()
        assert "1 month ago" == today.subtract(months=1).diff_for_humans()

    with pendulum.test(pendulum.datetime(2017, 2, 28)):
        today = pendulum.today().date()

        assert "1 month ago" == today.subtract(weeks=4).diff_for_humans()


def test_diff_for_humans_now_and_months(today):
    assert "2 months ago" == today.subtract(months=2).diff_for_humans()


def test_diff_for_humans_now_and_nearly_year(today):
    assert "11 months ago" == today.subtract(months=11).diff_for_humans()


def test_diff_for_humans_now_and_year(today):
    assert "1 year ago" == today.subtract(years=1).diff_for_humans()


def test_diff_for_humans_now_and_years(today):
    assert "2 years ago" == today.subtract(years=2).diff_for_humans()


def test_diff_for_humans_now_and_future_day(today):
    assert "in 1 day" == today.add(days=1).diff_for_humans()


def test_diff_for_humans_now_and_future_days(today):
    assert "in 2 days" == today.add(days=2).diff_for_humans()


def test_diff_for_humans_now_and_nearly_future_week(today):
    assert "in 6 days" == today.add(days=6).diff_for_humans()


def test_diff_for_humans_now_and_future_week(today):
    assert "in 1 week" == today.add(weeks=1).diff_for_humans()


def test_diff_for_humans_now_and_future_weeks(today):
    assert "in 2 weeks" == today.add(weeks=2).diff_for_humans()


def test_diff_for_humans_now_and_nearly_future_month(today):
    assert "in 3 weeks" == today.add(weeks=3).diff_for_humans()


def test_diff_for_humans_now_and_future_month():
    with pendulum.test(pendulum.datetime(2016, 3, 1)):
        today = pendulum.today().date()

        assert "in 4 weeks" == today.add(weeks=4).diff_for_humans()
        assert "in 1 month" == today.add(months=1).diff_for_humans()

    with pendulum.test(pendulum.datetime(2017, 3, 31)):
        today = pendulum.today().date()

        assert "in 1 month" == today.add(months=1).diff_for_humans()

    with pendulum.test(pendulum.datetime(2017, 4, 30)):
        today = pendulum.today().date()

        assert "in 1 month" == today.add(months=1).diff_for_humans()

    with pendulum.test(pendulum.datetime(2017, 1, 31)):
        today = pendulum.today().date()

        assert "in 1 month" == today.add(weeks=4).diff_for_humans()


def test_diff_for_humans_now_and_future_months(today):
    assert "in 2 months" == today.add(months=2).diff_for_humans()


def test_diff_for_humans_now_and_nearly_future_year(today):
    assert "in 11 months" == today.add(months=11).diff_for_humans()


def test_diff_for_humans_now_and_future_year(today):
    assert "in 1 year" == today.add(years=1).diff_for_humans()


def test_diff_for_humans_now_and_future_years(today):
    assert "in 2 years" == today.add(years=2).diff_for_humans()


def test_diff_for_humans_other_and_day(today):
    assert "1 day before" == today.diff_for_humans(today.add(days=1))


def test_diff_for_humans_other_and_days(today):
    assert "2 days before" == today.diff_for_humans(today.add(days=2))


def test_diff_for_humans_other_and_nearly_week(today):
    assert "6 days before" == today.diff_for_humans(today.add(days=6))


def test_diff_for_humans_other_and_week(today):
    assert "1 week before" == today.diff_for_humans(today.add(weeks=1))


def test_diff_for_humans_other_and_weeks(today):
    assert "2 weeks before" == today.diff_for_humans(today.add(weeks=2))


def test_diff_for_humans_other_and_nearly_month(today):
    assert "3 weeks before" == today.diff_for_humans(today.add(weeks=3))


def test_diff_for_humans_other_and_month():
    with pendulum.test(pendulum.datetime(2016, 3, 1)):
        today = pendulum.today().date()

        assert "4 weeks before" == today.diff_for_humans(today.add(weeks=4))
        assert "1 month before" == today.diff_for_humans(today.add(months=1))

    with pendulum.test(pendulum.datetime(2017, 3, 31)):
        today = pendulum.today().date()

        assert "1 month before" == today.diff_for_humans(today.add(months=1))

    with pendulum.test(pendulum.datetime(2017, 4, 30)):
        today = pendulum.today().date()

        assert "1 month before" == today.diff_for_humans(today.add(months=1))

    with pendulum.test(pendulum.datetime(2017, 1, 31)):
        today = pendulum.today().date()

        assert "1 month before" == today.diff_for_humans(today.add(weeks=4))


def test_diff_for_humans_other_and_months(today):
    assert "2 months before" == today.diff_for_humans(today.add(months=2))


def test_diff_for_humans_other_and_nearly_year(today):
    assert "11 months before" == today.diff_for_humans(today.add(months=11))


def test_diff_for_humans_other_and_year(today):
    assert "1 year before" == today.diff_for_humans(today.add(years=1))


def test_diff_for_humans_other_and_years(today):
    assert "2 years before" == today.diff_for_humans(today.add(years=2))


def test_diff_for_humans_other_and_future_day(today):
    assert "1 day after" == today.diff_for_humans(today.subtract(days=1))


def test_diff_for_humans_other_and_future_days(today):
    assert "2 days after" == today.diff_for_humans(today.subtract(days=2))


def test_diff_for_humans_other_and_nearly_future_week(today):
    assert "6 days after" == today.diff_for_humans(today.subtract(days=6))


def test_diff_for_humans_other_and_future_week(today):
    assert "1 week after" == today.diff_for_humans(today.subtract(weeks=1))


def test_diff_for_humans_other_and_future_weeks(today):
    assert "2 weeks after" == today.diff_for_humans(today.subtract(weeks=2))


def test_diff_for_humans_other_and_nearly_future_month(today):
    assert "3 weeks after" == today.diff_for_humans(today.subtract(weeks=3))


def test_diff_for_humans_other_and_future_month():
    with pendulum.test(pendulum.datetime(2016, 3, 1)):
        today = pendulum.today().date()

        assert "4 weeks after" == today.diff_for_humans(today.subtract(weeks=4))
        assert "1 month after" == today.diff_for_humans(today.subtract(months=1))

    with pendulum.test(pendulum.datetime(2017, 2, 28)):
        today = pendulum.today().date()

        assert "1 month after" == today.diff_for_humans(today.subtract(weeks=4))


def test_diff_for_humans_other_and_future_months(today):
    assert "2 months after" == today.diff_for_humans(today.subtract(months=2))


def test_diff_for_humans_other_and_nearly_future_year(today):
    assert "11 months after" == today.diff_for_humans(today.subtract(months=11))


def test_diff_for_humans_other_and_future_year(today):
    assert "1 year after" == today.diff_for_humans(today.subtract(years=1))


def test_diff_for_humans_other_and_future_years(today):
    assert "2 years after" == today.diff_for_humans(today.subtract(years=2))


def test_diff_for_humans_absolute_days(today):
    assert "2 days" == today.diff_for_humans(today.subtract(days=2), True)
    assert "2 days" == today.diff_for_humans(today.add(days=2), True)


def test_diff_for_humans_absolute_weeks(today):
    assert "2 weeks" == today.diff_for_humans(today.subtract(weeks=2), True)
    assert "2 weeks" == today.diff_for_humans(today.add(weeks=2), True)


def test_diff_for_humans_absolute_months(today):
    assert "2 months" == today.diff_for_humans(today.subtract(months=2), True)
    assert "2 months" == today.diff_for_humans(today.add(months=2), True)


def test_diff_for_humans_absolute_years(today):
    assert "1 year" == today.diff_for_humans(today.subtract(years=1), True)
    assert "1 year" == today.diff_for_humans(today.add(years=1), True)


def test_subtraction():
    d = pendulum.date(2016, 7, 5)
    future_dt = date(2016, 7, 6)
    future = d.add(days=1)

    assert 86400 == (future - d).total_seconds()
    assert 86400 == (future_dt - d).total_seconds()
