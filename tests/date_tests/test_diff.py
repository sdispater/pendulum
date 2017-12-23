from datetime import date
import pendulum
from pendulum import DateTime, Date


def test_diff_in_years_positive():
    dt = Date(2000, 1, 1)
    assert 1 ==  dt.diff(dt.add(years=1)).in_years()

def test_diff_in_years_negative_with_sign():
    dt = Date(2000, 1, 1)
    assert -1 ==  dt.diff(dt.subtract(years=1), False).in_years()

def test_diff_in_years_negative_no_sign():
    dt = Date(2000, 1, 1)
    assert 1 ==  dt.diff(dt.subtract(years=1)).in_years()

def test_diff_in_years_vs_default_now():
    assert 1 ==  Date.today().subtract(years=1).diff().in_years()

def test_diff_in_years_ensure_is_truncated():
    dt = Date(2000, 1, 1)
    assert 1 ==  dt.diff(dt.add(years=1).add(months=7)).in_years()

def test_diff_in_months_positive():
    dt = Date(2000, 1, 1)
    assert 13 ==  dt.diff(dt.add(years=1).add(months=1)).in_months()

def test_diff_in_months_negative_with_sign():
    dt = Date(2000, 1, 1)

    assert -11 ==  dt.diff(dt.subtract(years=1).add(months=1), False).in_months()

def test_diff_in_months_negative_no_sign():
    dt = Date(2000, 1, 1)
    assert 11 ==  dt.diff(dt.subtract(years=1).add(months=1)).in_months()

def test_diff_in_months_vs_default_now():
    assert 12 ==  Date.today().subtract(years=1).diff().in_months()

def test_diff_in_months_ensure_is_truncated():
    dt = Date(2000, 1, 1)
    assert 1 ==  dt.diff(dt.add(months=1).add(days=16)).in_months()

def test_diff_in_days_positive():
    dt = Date(2000, 1, 1)
    assert 366 ==  dt.diff(dt.add(years=1)).in_days()

def test_diff_in_days_negative_with_sign():
    dt = Date(2000, 1, 1)
    assert -365 ==  dt.diff(dt.subtract(years=1), False).in_days()

def test_diff_in_days_negative_no_sign():
    dt = Date(2000, 1, 1)
    assert 365 ==  dt.diff(dt.subtract(years=1)).in_days()

def test_diff_in_days_vs_default_now():
    assert 7 ==  Date.today().subtract(weeks=1).diff().in_days()

def test_diff_in_weeks_positive():
    dt = Date(2000, 1, 1)
    assert 52 ==  dt.diff(dt.add(years=1)).in_weeks()

def test_diff_in_weeks_negative_with_sign():
    dt = Date(2000, 1, 1)
    assert -52 ==  dt.diff(dt.subtract(years=1), False).in_weeks()

def test_diff_in_weeks_negative_no_sign():
    dt = Date(2000, 1, 1)
    assert 52 ==  dt.diff(dt.subtract(years=1)).in_weeks()

def test_diff_in_weeks_vs_default_now():
    assert 1 ==  Date.today().subtract(weeks=1).diff().in_weeks()

def test_diff_in_weeks_ensure_is_truncated():
    dt = Date(2000, 1, 1)
    assert 0 ==  dt.diff(dt.add(weeks=1).subtract(days=1)).in_weeks()

def test_diff_for_humans_now_and_day():
    assert '1 day ago' ==  Date.today().subtract(days=1).diff_for_humans()

def test_diff_for_humans_now_and_days():
    assert '2 days ago' ==  Date.today().subtract(days=2).diff_for_humans()

def test_diff_for_humans_now_and_nearly_week():
    assert '6 days ago' ==  Date.today().subtract(days=6).diff_for_humans()

def test_diff_for_humans_now_and_week():
    assert '1 week ago' ==  Date.today().subtract(weeks=1).diff_for_humans()

def test_diff_for_humans_now_and_weeks():
    assert '2 weeks ago' ==  Date.today().subtract(weeks=2).diff_for_humans()

def test_diff_for_humans_now_and_nearly_month():
    assert '3 weeks ago' ==  Date.today().subtract(weeks=3).diff_for_humans()

def test_diff_for_humans_now_and_month():
    with pendulum.test(DateTime.create(2016, 3, 1)):
        assert '4 weeks ago' ==  Date.today().subtract(weeks=4).diff_for_humans()
        assert '1 month ago' ==  Date.today().subtract(months=1).diff_for_humans()

    with pendulum.test(DateTime.create(2017, 2, 28)):
        assert '1 month ago' ==  Date.today().subtract(weeks=4).diff_for_humans()

def test_diff_for_humans_now_and_months():
    assert '2 months ago' ==  Date.today().subtract(months=2).diff_for_humans()

def test_diff_for_humans_now_and_nearly_year():
    assert '11 months ago' ==  Date.today().subtract(months=11).diff_for_humans()

def test_diff_for_humans_now_and_year():
    assert '1 year ago' ==  Date.today().subtract(years=1).diff_for_humans()

def test_diff_for_humans_now_and_years():
    assert '2 years ago' ==  Date.today().subtract(years=2).diff_for_humans()

def test_diff_for_humans_now_and_future_day():
    assert '1 day from now' ==  Date.today().add(days=1).diff_for_humans()

def test_diff_for_humans_now_and_future_days():
    assert '2 days from now' ==  Date.today().add(days=2).diff_for_humans()

def test_diff_for_humans_now_and_nearly_future_week():
    assert '6 days from now' ==  Date.today().add(days=6).diff_for_humans()

def test_diff_for_humans_now_and_future_week():
    assert '1 week from now' ==  Date.today().add(weeks=1).diff_for_humans()

def test_diff_for_humans_now_and_future_weeks():
    assert '2 weeks from now' ==  Date.today().add(weeks=2).diff_for_humans()

def test_diff_for_humans_now_and_nearly_future_month():
    assert '3 weeks from now' ==  Date.today().add(weeks=3).diff_for_humans()

def test_diff_for_humans_now_and_future_month():
    with pendulum.test(DateTime.create(2016, 3, 1)):
        assert '4 weeks from now' ==  Date.today().add(weeks=4).diff_for_humans()
        assert '1 month from now' ==  Date.today().add(months=1).diff_for_humans()

    with pendulum.test(DateTime.create(2017, 3, 31)):
        assert '1 month from now' ==  Date.today().add(months=1).diff_for_humans()

    with pendulum.test(DateTime.create(2017, 4, 30)):
        assert '1 month from now' ==  Date.today().add(months=1).diff_for_humans()

    with pendulum.test(DateTime.create(2017, 1, 31)):
        assert '1 month from now' ==  Date.today().add(weeks=4).diff_for_humans()

def test_diff_for_humans_now_and_future_months():
    assert '2 months from now' ==  Date.today().add(months=2).diff_for_humans()

def test_diff_for_humans_now_and_nearly_future_year():
    assert '11 months from now' ==  Date.today().add(months=11).diff_for_humans()

def test_diff_for_humans_now_and_future_year():
    assert '1 year from now' ==  Date.today().add(years=1).diff_for_humans()

def test_diff_for_humans_now_and_future_years():
    assert '2 years from now' ==  Date.today().add(years=2).diff_for_humans()

def test_diff_for_humans_other_and_day():
    assert '1 day before' ==  Date.today().diff_for_humans(Date.today().add(days=1))

def test_diff_for_humans_other_and_days():
    assert '2 days before' ==  Date.today().diff_for_humans(Date.today().add(days=2))

def test_diff_for_humans_other_and_nearly_week():
    assert '6 days before' ==  Date.today().diff_for_humans(Date.today().add(days=6))

def test_diff_for_humans_other_and_week():
    assert '1 week before' ==  Date.today().diff_for_humans(Date.today().add(weeks=1))

def test_diff_for_humans_other_and_weeks():
    assert '2 weeks before' ==  Date.today().diff_for_humans(Date.today().add(weeks=2))

def test_diff_for_humans_other_and_nearly_month():
    assert '3 weeks before' ==  Date.today().diff_for_humans(Date.today().add(weeks=3))

def test_diff_for_humans_other_and_month():
    with pendulum.test(DateTime.create(2016, 3, 1)):
        assert '4 weeks before' ==  Date.today().diff_for_humans(Date.today().add(weeks=4))
        assert '1 month before' ==  Date.today().diff_for_humans(Date.today().add(months=1))

    with pendulum.test(DateTime.create(2017, 3, 31)):
        assert '1 month before' ==  Date.today().diff_for_humans(Date.today().add(months=1))

    with pendulum.test(DateTime.create(2017, 4, 30)):
        assert '1 month before' ==  Date.today().diff_for_humans(Date.today().add(months=1))

    with pendulum.test(DateTime.create(2017, 1, 31)):
        assert '1 month before' ==  Date.today().diff_for_humans(Date.today().add(weeks=4))

def test_diff_for_humans_other_and_months():
    assert '2 months before' ==  Date.today().diff_for_humans(Date.today().add(months=2))

def test_diff_for_humans_other_and_nearly_year():
    assert '11 months before' ==  Date.today().diff_for_humans(Date.today().add(months=11))

def test_diff_for_humans_other_and_year():
    assert '1 year before' ==  Date.today().diff_for_humans(Date.today().add(years=1))

def test_diff_for_humans_other_and_years():
    assert '2 years before' ==  Date.today().diff_for_humans(Date.today().add(years=2))

def test_diff_for_humans_other_and_future_day():
    assert '1 day after' ==  Date.today().diff_for_humans(Date.today().subtract(days=1))

def test_diff_for_humans_other_and_future_days():
    assert '2 days after' ==  Date.today().diff_for_humans(Date.today().subtract(days=2))

def test_diff_for_humans_other_and_nearly_future_week():
    assert '6 days after' ==  Date.today().diff_for_humans(Date.today().subtract(days=6))

def test_diff_for_humans_other_and_future_week():
    assert '1 week after' ==  Date.today().diff_for_humans(Date.today().subtract(weeks=1))

def test_diff_for_humans_other_and_future_weeks():
    assert '2 weeks after' ==  Date.today().diff_for_humans(Date.today().subtract(weeks=2))

def test_diff_for_humans_other_and_nearly_future_month():
    assert '3 weeks after' ==  Date.today().diff_for_humans(Date.today().subtract(weeks=3))

def test_diff_for_humans_other_and_future_month():
    with pendulum.test(DateTime.create(2016, 3, 1)):
        assert '4 weeks after' ==  Date.today().diff_for_humans(Date.today().subtract(weeks=4))
        assert '1 month after' ==  Date.today().diff_for_humans(Date.today().subtract(months=1))

    with pendulum.test(DateTime.create(2017, 2, 28)):
        assert '1 month after' ==  Date.today().diff_for_humans(Date.today().subtract(weeks=4))

def test_diff_for_humans_other_and_future_months():
    assert '2 months after' ==  Date.today().diff_for_humans(Date.today().subtract(months=2))

def test_diff_for_humans_other_and_nearly_future_year():
    assert '11 months after' ==  Date.today().diff_for_humans(Date.today().subtract(months=11))

def test_diff_for_humans_other_and_future_year():
    assert '1 year after' ==  Date.today().diff_for_humans(Date.today().subtract(years=1))

def test_diff_for_humans_other_and_future_years():
    assert '2 years after' ==  Date.today().diff_for_humans(Date.today().subtract(years=2))

def test_diff_for_humans_absolute_days():
    assert '2 days' ==  Date.today().diff_for_humans(Date.today().subtract(days=2), True)
    assert '2 days' ==  Date.today().diff_for_humans(Date.today().add(days=2), True)

def test_diff_for_humans_absolute_weeks():
    assert '2 weeks' ==  Date.today().diff_for_humans(Date.today().subtract(weeks=2), True)
    assert '2 weeks' ==  Date.today().diff_for_humans(Date.today().add(weeks=2), True)

def test_diff_for_humans_absolute_months():
    assert '2 months' ==  Date.today().diff_for_humans(Date.today().subtract(months=2), True)
    assert '2 months' ==  Date.today().diff_for_humans(Date.today().add(months=2), True)

def test_diff_for_humans_absolute_years():
    assert '1 year' ==  Date.today().diff_for_humans(Date.today().subtract(years=1), True)
    assert '1 year' ==  Date.today().diff_for_humans(Date.today().add(years=1), True)

def test_subtraction():
    d = Date(2016, 7, 5)
    future_dt = date(2016, 7, 6)
    future = d.add(days=1)

    assert 86400 ==  (future - d).total_seconds()
    assert 86400 ==  (future_dt - d).total_seconds()
