from __future__ import annotations

import pendulum


def test_year():
    d = pendulum.Date(1234, 5, 6)
    assert d.year == 1234


def test_month():
    d = pendulum.Date(1234, 5, 6)
    assert d.month == 5


def test_day():
    d = pendulum.Date(1234, 5, 6)
    assert d.day == 6


def test_day_of_week():
    d = pendulum.Date(2012, 5, 7)
    assert d.day_of_week == pendulum.MONDAY


def test_day_of_year():
    d = pendulum.Date(2015, 12, 31)
    assert d.day_of_year == 365
    d = pendulum.Date(2016, 12, 31)
    assert d.day_of_year == 366


def test_days_in_month():
    d = pendulum.Date(2012, 5, 7)
    assert d.days_in_month == 31


def test_age():
    d = pendulum.Date.today()
    assert d.age == 0
    assert d.add(years=1).age == -1
    assert d.subtract(years=1).age == 1


def test_is_leap_year():
    assert pendulum.Date(2012, 1, 1).is_leap_year()
    assert not pendulum.Date(2011, 1, 1).is_leap_year()


def test_is_long_year():
    assert pendulum.Date(2015, 1, 1).is_long_year()
    assert not pendulum.Date(2016, 1, 1).is_long_year()


def test_week_of_month():
    assert pendulum.Date(2012, 9, 30).week_of_month == 5
    assert pendulum.Date(2012, 9, 28).week_of_month == 5
    assert pendulum.Date(2012, 9, 20).week_of_month == 4
    assert pendulum.Date(2012, 9, 8).week_of_month == 2
    assert pendulum.Date(2012, 9, 1).week_of_month == 1
    assert pendulum.date(2020, 1, 1).week_of_month == 1
    assert pendulum.date(2020, 1, 7).week_of_month == 2
    assert pendulum.date(2020, 1, 14).week_of_month == 3


def test_week_of_year_first_week():
    assert pendulum.Date(2012, 1, 1).week_of_year == 52
    assert pendulum.Date(2012, 1, 2).week_of_year == 1


def test_week_of_year_last_week():
    assert pendulum.Date(2012, 12, 30).week_of_year == 52
    assert pendulum.Date(2012, 12, 31).week_of_year == 1


def test_is_future():
    d = pendulum.Date.today()
    assert not d.is_future()
    d = d.add(days=1)
    assert d.is_future()


def test_is_past():
    d = pendulum.Date.today()
    assert not d.is_past()
    d = d.subtract(days=1)
    assert d.is_past()
