from datetime import datetime

import pendulum
import pytest


def test_diff_in_years_positive():
    dt = pendulum.datetime(2000, 1, 1)
    assert 1 == dt.diff(dt.add(years=1)).in_years()


def test_diff_in_years_negative_with_sign():
    dt = pendulum.datetime(2000, 1, 1)
    assert -1 == dt.diff(dt.subtract(years=1), False).in_years()


def test_diff_in_years_negative_no_sign():
    dt = pendulum.datetime(2000, 1, 1)
    assert 1 == dt.diff(dt.subtract(years=1)).in_years()


def test_diff_in_years_vs_default_now():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert 1 == pendulum.now().subtract(years=1).diff().in_years()


def test_diff_in_years_ensure_is_truncated():
    dt = pendulum.datetime(2000, 1, 1)
    assert 1 == dt.diff(dt.add(years=1).add(months=7)).in_years()


def test_diff_in_months_positive():
    dt = pendulum.datetime(2000, 1, 1)
    assert 13 == dt.diff(dt.add(years=1).add(months=1)).in_months()


def test_diff_in_months_negative_with_sign():
    dt = pendulum.datetime(2000, 1, 1)
    assert -11 == dt.diff(dt.subtract(years=1).add(months=1), False).in_months()


def test_diff_in_months_negative_no_sign():
    dt = pendulum.datetime(2000, 1, 1)
    assert 11 == dt.diff(dt.subtract(years=1).add(months=1)).in_months()


def test_diff_in_months_vs_default_now():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert 12 == pendulum.now().subtract(years=1).diff().in_months()


def test_diff_in_months_ensure_is_truncated():
    dt = pendulum.datetime(2000, 1, 1)
    assert 1 == dt.diff(dt.add(months=1).add(days=16)).in_months()


def test_diff_in_days_positive():
    dt = pendulum.datetime(2000, 1, 1)
    assert 366 == dt.diff(dt.add(years=1)).in_days()


def test_diff_in_days_negative_with_sign():
    dt = pendulum.datetime(2000, 1, 1)
    assert -365 == dt.diff(dt.subtract(years=1), False).in_days()


def test_diff_in_days_negative_no_sign():
    dt = pendulum.datetime(2000, 1, 1)
    assert 365 == dt.diff(dt.subtract(years=1)).in_days()


def test_diff_in_days_vs_default_now():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert 7 == pendulum.now().subtract(weeks=1).diff().in_days()


def test_diff_in_days_ensure_is_truncated():
    dt = pendulum.datetime(2000, 1, 1)
    assert 1 == dt.diff(dt.add(days=1).add(hours=13)).in_days()


def test_diff_in_weeks_positive():
    dt = pendulum.datetime(2000, 1, 1)
    assert 52 == dt.diff(dt.add(years=1)).in_weeks()


def test_diff_in_weeks_negative_with_sign():
    dt = pendulum.datetime(2000, 1, 1)
    assert -52 == dt.diff(dt.subtract(years=1), False).in_weeks()


def test_diff_in_weeks_negative_no_sign():
    dt = pendulum.datetime(2000, 1, 1)
    assert 52 == dt.diff(dt.subtract(years=1)).in_weeks()


def test_diff_in_weeks_vs_default_now():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert 1 == pendulum.now().subtract(weeks=1).diff().in_weeks()


def test_diff_in_weeks_ensure_is_truncated():
    dt = pendulum.datetime(2000, 1, 1)
    assert 0 == dt.diff(dt.add(weeks=1).subtract(days=1)).in_weeks()


def test_diff_in_hours_positive():
    dt = pendulum.datetime(2000, 1, 1)
    assert 26 == dt.diff(dt.add(days=1).add(hours=2)).in_hours()


def test_diff_in_hours_negative_with_sign():
    dt = pendulum.datetime(2000, 1, 1)
    assert -22 == dt.diff(dt.subtract(days=1).add(hours=2), False).in_hours()


def test_diff_in_hours_negative_no_sign():
    dt = pendulum.datetime(2000, 1, 1)
    assert 22 == dt.diff(dt.subtract(days=1).add(hours=2)).in_hours()


def test_diff_in_hours_vs_default_now():
    with pendulum.test(pendulum.datetime(2012, 1, 15)):
        assert 48 == pendulum.now().subtract(days=2).diff().in_hours()


def test_diff_in_hours_ensure_is_truncated():
    dt = pendulum.datetime(2000, 1, 1)
    assert 1 == dt.diff(dt.add(hours=1).add(minutes=31)).in_hours()


def test_diff_in_minutes_positive():
    dt = pendulum.datetime(2000, 1, 1)
    assert 62 == dt.diff(dt.add(hours=1).add(minutes=2)).in_minutes()


def test_diff_in_minutes_positive_big():
    dt = pendulum.datetime(2000, 1, 1)
    assert 1502 == dt.diff(dt.add(hours=25).add(minutes=2)).in_minutes()


def test_diff_in_minutes_negative_with_sign():
    dt = pendulum.datetime(2000, 1, 1)
    assert -58 == dt.diff(dt.subtract(hours=1).add(minutes=2), False).in_minutes()


def test_diff_in_minutes_negative_no_sign():
    dt = pendulum.datetime(2000, 1, 1)
    assert 58 == dt.diff(dt.subtract(hours=1).add(minutes=2)).in_minutes()


def test_diff_in_minutes_vs_default_now():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert 60 == pendulum.now().subtract(hours=1).diff().in_minutes()


def test_diff_in_minutes_ensure_is_truncated():
    dt = pendulum.datetime(2000, 1, 1)
    assert 1 == dt.diff(dt.add(minutes=1).add(seconds=59)).in_minutes()


def test_diff_in_seconds_positive():
    dt = pendulum.datetime(2000, 1, 1)
    assert 62 == dt.diff(dt.add(minutes=1).add(seconds=2)).in_seconds()


def test_diff_in_seconds_positive_big():
    dt = pendulum.datetime(2000, 1, 1)
    assert 7202 == dt.diff(dt.add(hours=2).add(seconds=2)).in_seconds()


def test_diff_in_seconds_negative_with_sign():
    dt = pendulum.datetime(2000, 1, 1)
    assert -58 == dt.diff(dt.subtract(minutes=1).add(seconds=2), False).in_seconds()


def test_diff_in_seconds_negative_no_sign():
    dt = pendulum.datetime(2000, 1, 1)
    assert 58 == dt.diff(dt.subtract(minutes=1).add(seconds=2)).in_seconds()


def test_diff_in_seconds_vs_default_now():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert 3600 == pendulum.now().subtract(hours=1).diff().in_seconds()


def test_diff_in_seconds_ensure_is_truncated():
    dt = pendulum.datetime(2000, 1, 1)
    assert 1 == dt.diff(dt.add(seconds=1.9)).in_seconds()


def test_diff_in_seconds_with_timezones():
    dt_ottawa = pendulum.datetime(2000, 1, 1, 13, tz="America/Toronto")
    dt_vancouver = pendulum.datetime(2000, 1, 1, 13, tz="America/Vancouver")
    assert 3 * 60 * 60 == dt_ottawa.diff(dt_vancouver).in_seconds()


def test_diff_for_humans_now_and_second():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "a few seconds ago" == pendulum.now().diff_for_humans()


def test_diff_for_humans_now_and_second_with_timezone():
    van_now = pendulum.now("America/Vancouver")
    here_now = van_now.in_timezone(pendulum.now().timezone)

    with pendulum.test(here_now):
        assert "a few seconds ago" == here_now.diff_for_humans()


def test_diff_for_humans_now_and_seconds():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert (
            "a few seconds ago" == pendulum.now().subtract(seconds=2).diff_for_humans()
        )


def test_diff_for_humans_now_and_nearly_minute():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "59 seconds ago" == pendulum.now().subtract(seconds=59).diff_for_humans()


def test_diff_for_humans_now_and_minute():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "1 minute ago" == pendulum.now().subtract(minutes=1).diff_for_humans()


def test_diff_for_humans_now_and_minutes():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "2 minutes ago" == pendulum.now().subtract(minutes=2).diff_for_humans()


def test_diff_for_humans_now_and_nearly_hour():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "59 minutes ago" == pendulum.now().subtract(minutes=59).diff_for_humans()


def test_diff_for_humans_now_and_hour():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "1 hour ago" == pendulum.now().subtract(hours=1).diff_for_humans()


def test_diff_for_humans_now_and_hours():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "2 hours ago" == pendulum.now().subtract(hours=2).diff_for_humans()


def test_diff_for_humans_now_and_nearly_day():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "23 hours ago" == pendulum.now().subtract(hours=23).diff_for_humans()


def test_diff_for_humans_now_and_day():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "1 day ago" == pendulum.now().subtract(days=1).diff_for_humans()


def test_diff_for_humans_now_and_days():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "2 days ago" == pendulum.now().subtract(days=2).diff_for_humans()


def test_diff_for_humans_now_and_nearly_week():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "6 days ago" == pendulum.now().subtract(days=6).diff_for_humans()


def test_diff_for_humans_now_and_week():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "1 week ago" == pendulum.now().subtract(weeks=1).diff_for_humans()


def test_diff_for_humans_now_and_weeks():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "2 weeks ago" == pendulum.now().subtract(weeks=2).diff_for_humans()


def test_diff_for_humans_now_and_nearly_month():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "3 weeks ago" == pendulum.now().subtract(weeks=3).diff_for_humans()


def test_diff_for_humans_now_and_month():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "4 weeks ago" == pendulum.now().subtract(weeks=4).diff_for_humans()
        assert "1 month ago" == pendulum.now().subtract(months=1).diff_for_humans()


def test_diff_for_humans_now_and_months():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "2 months ago" == pendulum.now().subtract(months=2).diff_for_humans()


def test_diff_for_humans_now_and_nearly_year():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "11 months ago" == pendulum.now().subtract(months=11).diff_for_humans()


def test_diff_for_humans_now_and_year():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "1 year ago" == pendulum.now().subtract(years=1).diff_for_humans()


def test_diff_for_humans_now_and_years():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "2 years ago" == pendulum.now().subtract(years=2).diff_for_humans()


def test_diff_for_humans_now_and_future_second():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "in a few seconds" == pendulum.now().add(seconds=1).diff_for_humans()


def test_diff_for_humans_now_and_future_seconds():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "in a few seconds" == pendulum.now().add(seconds=2).diff_for_humans()


def test_diff_for_humans_now_and_nearly_future_minute():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "in 59 seconds" == pendulum.now().add(seconds=59).diff_for_humans()


def test_diff_for_humans_now_and_future_minute():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "in 1 minute" == pendulum.now().add(minutes=1).diff_for_humans()


def test_diff_for_humans_now_and_future_minutes():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "in 2 minutes" == pendulum.now().add(minutes=2).diff_for_humans()


def test_diff_for_humans_now_and_nearly_future_hour():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "in 59 minutes" == pendulum.now().add(minutes=59).diff_for_humans()


def test_diff_for_humans_now_and_future_hour():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "in 1 hour" == pendulum.now().add(hours=1).diff_for_humans()


def test_diff_for_humans_now_and_future_hours():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "in 2 hours" == pendulum.now().add(hours=2).diff_for_humans()


def test_diff_for_humans_now_and_nearly_future_day():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "in 23 hours" == pendulum.now().add(hours=23).diff_for_humans()


def test_diff_for_humans_now_and_future_day():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "in 1 day" == pendulum.now().add(days=1).diff_for_humans()


def test_diff_for_humans_now_and_future_days():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "in 2 days" == pendulum.now().add(days=2).diff_for_humans()


def test_diff_for_humans_now_and_nearly_future_week():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "in 6 days" == pendulum.now().add(days=6).diff_for_humans()


def test_diff_for_humans_now_and_future_week():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "in 1 week" == pendulum.now().add(weeks=1).diff_for_humans()


def test_diff_for_humans_now_and_future_weeks():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "in 2 weeks" == pendulum.now().add(weeks=2).diff_for_humans()


def test_diff_for_humans_now_and_nearly_future_month():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "in 3 weeks" == pendulum.now().add(weeks=3).diff_for_humans()


def test_diff_for_humans_now_and_future_month():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "in 4 weeks" == pendulum.now().add(weeks=4).diff_for_humans()
        assert "in 1 month" == pendulum.now().add(months=1).diff_for_humans()


def test_diff_for_humans_now_and_future_months():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "in 2 months" == pendulum.now().add(months=2).diff_for_humans()


def test_diff_for_humans_now_and_nearly_future_year():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "in 11 months" == pendulum.now().add(months=11).diff_for_humans()


def test_diff_for_humans_now_and_future_year():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "in 1 year" == pendulum.now().add(years=1).diff_for_humans()


def test_diff_for_humans_now_and_future_years():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "in 2 years" == pendulum.now().add(years=2).diff_for_humans()


def test_diff_for_humans_other_and_second():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "a few seconds before" == pendulum.now().diff_for_humans(
            pendulum.now().add(seconds=1)
        )


def test_diff_for_humans_other_and_seconds():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "a few seconds before" == pendulum.now().diff_for_humans(
            pendulum.now().add(seconds=2)
        )


def test_diff_for_humans_other_and_nearly_minute():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "59 seconds before" == pendulum.now().diff_for_humans(
            pendulum.now().add(seconds=59)
        )


def test_diff_for_humans_other_and_minute():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "1 minute before" == pendulum.now().diff_for_humans(
            pendulum.now().add(minutes=1)
        )


def test_diff_for_humans_other_and_minutes():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "2 minutes before" == pendulum.now().diff_for_humans(
            pendulum.now().add(minutes=2)
        )


def test_diff_for_humans_other_and_nearly_hour():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "59 minutes before" == pendulum.now().diff_for_humans(
            pendulum.now().add(minutes=59)
        )


def test_diff_for_humans_other_and_hour():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "1 hour before" == pendulum.now().diff_for_humans(
            pendulum.now().add(hours=1)
        )


def test_diff_for_humans_other_and_hours():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "2 hours before" == pendulum.now().diff_for_humans(
            pendulum.now().add(hours=2)
        )


def test_diff_for_humans_other_and_nearly_day():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "23 hours before" == pendulum.now().diff_for_humans(
            pendulum.now().add(hours=23)
        )


def test_diff_for_humans_other_and_day():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "1 day before" == pendulum.now().diff_for_humans(
            pendulum.now().add(days=1)
        )


def test_diff_for_humans_other_and_days():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "2 days before" == pendulum.now().diff_for_humans(
            pendulum.now().add(days=2)
        )


def test_diff_for_humans_other_and_nearly_week():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "6 days before" == pendulum.now().diff_for_humans(
            pendulum.now().add(days=6)
        )


def test_diff_for_humans_other_and_week():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "1 week before" == pendulum.now().diff_for_humans(
            pendulum.now().add(weeks=1)
        )


def test_diff_for_humans_other_and_weeks():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "2 weeks before" == pendulum.now().diff_for_humans(
            pendulum.now().add(weeks=2)
        )


def test_diff_for_humans_other_and_nearly_month():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "3 weeks before" == pendulum.now().diff_for_humans(
            pendulum.now().add(weeks=3)
        )


def test_diff_for_humans_other_and_month():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "4 weeks before" == pendulum.now().diff_for_humans(
            pendulum.now().add(weeks=4)
        )
        assert "1 month before" == pendulum.now().diff_for_humans(
            pendulum.now().add(months=1)
        )


def test_diff_for_humans_other_and_months():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "2 months before" == pendulum.now().diff_for_humans(
            pendulum.now().add(months=2)
        )


def test_diff_for_humans_other_and_nearly_year():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "11 months before" == pendulum.now().diff_for_humans(
            pendulum.now().add(months=11)
        )


def test_diff_for_humans_other_and_year():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "1 year before" == pendulum.now().diff_for_humans(
            pendulum.now().add(years=1)
        )


def test_diff_for_humans_other_and_years():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "2 years before" == pendulum.now().diff_for_humans(
            pendulum.now().add(years=2)
        )


def test_diff_for_humans_other_and_future_second():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "a few seconds after" == pendulum.now().diff_for_humans(
            pendulum.now().subtract(seconds=1)
        )


def test_diff_for_humans_other_and_future_seconds():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "a few seconds after" == pendulum.now().diff_for_humans(
            pendulum.now().subtract(seconds=2)
        )


def test_diff_for_humans_other_and_nearly_future_minute():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "59 seconds after" == pendulum.now().diff_for_humans(
            pendulum.now().subtract(seconds=59)
        )


def test_diff_for_humans_other_and_future_minute():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "1 minute after" == pendulum.now().diff_for_humans(
            pendulum.now().subtract(minutes=1)
        )


def test_diff_for_humans_other_and_future_minutes():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "2 minutes after" == pendulum.now().diff_for_humans(
            pendulum.now().subtract(minutes=2)
        )


def test_diff_for_humans_other_and_nearly_future_hour():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "59 minutes after" == pendulum.now().diff_for_humans(
            pendulum.now().subtract(minutes=59)
        )


def test_diff_for_humans_other_and_future_hour():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "1 hour after" == pendulum.now().diff_for_humans(
            pendulum.now().subtract(hours=1)
        )


def test_diff_for_humans_other_and_future_hours():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "2 hours after" == pendulum.now().diff_for_humans(
            pendulum.now().subtract(hours=2)
        )


def test_diff_for_humans_other_and_nearly_future_day():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "23 hours after" == pendulum.now().diff_for_humans(
            pendulum.now().subtract(hours=23)
        )


def test_diff_for_humans_other_and_future_day():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "1 day after" == pendulum.now().diff_for_humans(
            pendulum.now().subtract(days=1)
        )


def test_diff_for_humans_other_and_future_days():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "2 days after" == pendulum.now().diff_for_humans(
            pendulum.now().subtract(days=2)
        )


def test_diff_for_humans_other_and_nearly_future_week():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "6 days after" == pendulum.now().diff_for_humans(
            pendulum.now().subtract(days=6)
        )


def test_diff_for_humans_other_and_future_week():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "1 week after" == pendulum.now().diff_for_humans(
            pendulum.now().subtract(weeks=1)
        )


def test_diff_for_humans_other_and_future_weeks():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "2 weeks after" == pendulum.now().diff_for_humans(
            pendulum.now().subtract(weeks=2)
        )


def test_diff_for_humans_other_and_nearly_future_month():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "3 weeks after" == pendulum.now().diff_for_humans(
            pendulum.now().subtract(weeks=3)
        )


def test_diff_for_humans_other_and_future_month():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "4 weeks after" == pendulum.now().diff_for_humans(
            pendulum.now().subtract(weeks=4)
        )
        assert "1 month after" == pendulum.now().diff_for_humans(
            pendulum.now().subtract(months=1)
        )


def test_diff_for_humans_other_and_future_months():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "2 months after" == pendulum.now().diff_for_humans(
            pendulum.now().subtract(months=2)
        )


def test_diff_for_humans_other_and_nearly_future_year():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "11 months after" == pendulum.now().diff_for_humans(
            pendulum.now().subtract(months=11)
        )


def test_diff_for_humans_other_and_future_year():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "1 year after" == pendulum.now().diff_for_humans(
            pendulum.now().subtract(years=1)
        )


def test_diff_for_humans_other_and_future_years():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "2 years after" == pendulum.now().diff_for_humans(
            pendulum.now().subtract(years=2)
        )


def test_diff_for_humans_absolute_seconds():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "59 seconds" == pendulum.now().diff_for_humans(
            pendulum.now().subtract(seconds=59), True
        )
        assert "59 seconds" == pendulum.now().diff_for_humans(
            pendulum.now().add(seconds=59), True
        )


def test_diff_for_humans_absolute_minutes():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "30 minutes" == pendulum.now().diff_for_humans(
            pendulum.now().subtract(minutes=30), True
        )
        assert "30 minutes" == pendulum.now().diff_for_humans(
            pendulum.now().add(minutes=30), True
        )


def test_diff_for_humans_absolute_hours():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "3 hours" == pendulum.now().diff_for_humans(
            pendulum.now().subtract(hours=3), True
        )
        assert "3 hours" == pendulum.now().diff_for_humans(
            pendulum.now().add(hours=3), True
        )


def test_diff_for_humans_absolute_days():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "2 days" == pendulum.now().diff_for_humans(
            pendulum.now().subtract(days=2), True
        )
        assert "2 days" == pendulum.now().diff_for_humans(
            pendulum.now().add(days=2), True
        )


def test_diff_for_humans_absolute_weeks():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "2 weeks" == pendulum.now().diff_for_humans(
            pendulum.now().subtract(weeks=2), True
        )
        assert "2 weeks" == pendulum.now().diff_for_humans(
            pendulum.now().add(weeks=2), True
        )


def test_diff_for_humans_absolute_months():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "2 months" == pendulum.now().diff_for_humans(
            pendulum.now().subtract(months=2), True
        )
        assert "2 months" == pendulum.now().diff_for_humans(
            pendulum.now().add(months=2), True
        )


def test_diff_for_humans_absolute_years():
    with pendulum.test(pendulum.datetime(2012, 1, 1, 1, 2, 3)):
        assert "1 year" == pendulum.now().diff_for_humans(
            pendulum.now().subtract(years=1), True
        )
        assert "1 year" == pendulum.now().diff_for_humans(
            pendulum.now().add(years=1), True
        )


def test_diff_for_humans_accuracy():
    now = pendulum.now("utc")

    with pendulum.test(now.add(microseconds=200)):
        assert "1 year" == now.add(years=1).diff_for_humans(absolute=True)
        assert "11 months" == now.add(months=11).diff_for_humans(absolute=True)
        assert "4 weeks" == now.add(days=27).diff_for_humans(absolute=True)
        assert "1 year" == now.add(years=1, months=3).diff_for_humans(absolute=True)
        assert "2 years" == now.add(years=1, months=8).diff_for_humans(absolute=True)

    # DST
    now = pendulum.datetime(2017, 3, 7, tz="America/Toronto")
    with pendulum.test(now):
        assert "6 days" == now.add(days=6).diff_for_humans(absolute=True)


def test_subtraction():
    d = pendulum.naive(2016, 7, 5, 12, 32, 25, 0)
    future_dt = datetime(2016, 7, 5, 13, 32, 25, 0)
    future = d.add(hours=1)

    assert 3600 == (future - d).total_seconds()
    assert 3600 == (future_dt - d).total_seconds()


def test_subtraction_aware_naive():
    dt = pendulum.datetime(2016, 7, 5, 12, 32, 25, 0)
    future_dt = datetime(2016, 7, 5, 13, 32, 25, 0)

    with pytest.raises(TypeError):
        future_dt - dt

    future_dt = pendulum.naive(2016, 7, 5, 13, 32, 25, 0)

    with pytest.raises(TypeError):
        future_dt - dt


def test_subtraction_with_timezone():
    dt = pendulum.datetime(2013, 3, 31, 1, 59, 59, 999999, tz="Europe/Paris")
    post = dt.add(microseconds=1)

    assert (post - dt).total_seconds() == 1e-06

    dt = pendulum.datetime(
        2013,
        10,
        27,
        2,
        59,
        59,
        999999,
        tz="Europe/Paris",
        dst_rule=pendulum.PRE_TRANSITION,
    )
    post = dt.add(microseconds=1)

    assert (post - dt).total_seconds() == 1e-06
