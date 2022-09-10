from __future__ import annotations

import pytest

import pendulum

from pendulum import Date
from tests.conftest import assert_date


def test_start_of_day():
    d = Date.today()
    new = d.start_of("day")
    assert isinstance(new, Date)
    assert_date(new, d.year, d.month, d.day)


def test_end_of_day():
    d = Date.today()
    new = d.end_of("day")
    assert isinstance(new, Date)
    assert_date(new, d.year, d.month, d.day)


def test_start_of_week():
    d = Date(2016, 10, 20)
    new = d.start_of("week")
    assert isinstance(new, Date)
    assert_date(new, d.year, d.month, 17)


def test_end_of_week():
    d = Date(2016, 10, 20)
    new = d.end_of("week")
    assert isinstance(new, Date)
    assert_date(new, d.year, d.month, 23)


def test_start_of_month_is_fluid():
    d = Date.today()
    assert isinstance(d.start_of("month"), Date)


def test_start_of_month_from_now():
    d = Date.today()
    new = d.start_of("month")
    assert_date(new, d.year, d.month, 1)


def test_start_of_month_from_last_day():
    d = Date(2000, 1, 31)
    new = d.start_of("month")
    assert_date(new, 2000, 1, 1)


def test_start_of_year_is_fluid():
    d = Date.today()
    new = d.start_of("year")
    assert isinstance(new, Date)


def test_start_of_year_from_now():
    d = Date.today()
    new = d.start_of("year")
    assert_date(new, d.year, 1, 1)


def test_start_of_year_from_first_day():
    d = Date(2000, 1, 1)
    new = d.start_of("year")
    assert_date(new, 2000, 1, 1)


def test_start_of_year_from_last_day():
    d = Date(2000, 12, 31)
    new = d.start_of("year")
    assert_date(new, 2000, 1, 1)


def test_end_of_month_is_fluid():
    d = Date.today()
    assert isinstance(d.end_of("month"), Date)


def test_end_of_month_from_now():
    d = Date.today().start_of("month")
    new = d.start_of("month")
    assert_date(new, d.year, d.month, 1)


def test_end_of_month():
    d = Date(2000, 1, 1).end_of("month")
    new = d.end_of("month")
    assert_date(new, 2000, 1, 31)


def test_end_of_month_from_last_day():
    d = Date(2000, 1, 31)
    new = d.end_of("month")
    assert_date(new, 2000, 1, 31)


def test_end_of_year_is_fluid():
    d = Date.today()
    assert isinstance(d.end_of("year"), Date)


def test_end_of_year_from_now():
    d = Date.today().end_of("year")
    new = d.end_of("year")
    assert_date(new, d.year, 12, 31)


def test_end_of_year_from_first_day():
    d = Date(2000, 1, 1)
    new = d.end_of("year")
    assert_date(new, 2000, 12, 31)


def test_end_of_year_from_last_day():
    d = Date(2000, 12, 31)
    new = d.end_of("year")
    assert_date(new, 2000, 12, 31)


def test_start_of_decade_is_fluid():
    d = Date.today()
    assert isinstance(d.start_of("decade"), Date)


def test_start_of_decade_from_now():
    d = Date.today()
    new = d.start_of("decade")
    assert_date(new, d.year - d.year % 10, 1, 1)


def test_start_of_decade_from_first_day():
    d = Date(2000, 1, 1)
    new = d.start_of("decade")
    assert_date(new, 2000, 1, 1)


def test_start_of_decade_from_last_day():
    d = Date(2009, 12, 31)
    new = d.start_of("decade")
    assert_date(new, 2000, 1, 1)


def test_end_of_decade_is_fluid():
    d = Date.today()
    assert isinstance(d.end_of("decade"), Date)


def test_end_of_decade_from_now():
    d = Date.today()
    new = d.end_of("decade")
    assert_date(new, d.year - d.year % 10 + 9, 12, 31)


def test_end_of_decade_from_first_day():
    d = Date(2000, 1, 1)
    new = d.end_of("decade")
    assert_date(new, 2009, 12, 31)


def test_end_of_decade_from_last_day():
    d = Date(2009, 12, 31)
    new = d.end_of("decade")
    assert_date(new, 2009, 12, 31)


def test_start_of_century_is_fluid():
    d = Date.today()
    assert isinstance(d.start_of("century"), Date)


def test_start_of_century_from_now():
    d = Date.today()
    new = d.start_of("century")
    assert_date(new, d.year - d.year % 100 + 1, 1, 1)


def test_start_of_century_from_first_day():
    d = Date(2001, 1, 1)
    new = d.start_of("century")
    assert_date(new, 2001, 1, 1)


def test_start_of_century_from_last_day():
    d = Date(2100, 12, 31)
    new = d.start_of("century")
    assert_date(new, 2001, 1, 1)


def test_end_of_century_is_fluid():
    d = Date.today()
    assert isinstance(d.end_of("century"), Date)


def test_end_of_century_from_now():
    now = Date.today()
    d = now.end_of("century")
    assert_date(d, now.year - now.year % 100 + 100, 12, 31)


def test_end_of_century_from_first_day():
    d = Date(2001, 1, 1)
    new = d.end_of("century")
    assert_date(new, 2100, 12, 31)


def test_end_of_century_from_last_day():
    d = Date(2100, 12, 31)
    new = d.end_of("century")
    assert_date(new, 2100, 12, 31)


def test_average_is_fluid():
    d = Date.today().average()
    assert isinstance(d, Date)


def test_average_from_same():
    d1 = pendulum.date(2000, 1, 31)
    d2 = pendulum.date(2000, 1, 31).average(d1)
    assert_date(d2, 2000, 1, 31)


def test_average_from_greater():
    d1 = pendulum.date(2000, 1, 1)
    d2 = pendulum.date(2009, 12, 31).average(d1)
    assert_date(d2, 2004, 12, 31)


def test_average_from_lower():
    d1 = pendulum.date(2009, 12, 31)
    d2 = pendulum.date(2000, 1, 1).average(d1)
    assert_date(d2, 2004, 12, 31)


def test_start_of():
    d = pendulum.date(2013, 3, 31)

    with pytest.raises(ValueError):
        d.start_of("invalid")


def test_end_of_invalid_unit():
    d = pendulum.date(2013, 3, 31)

    with pytest.raises(ValueError):
        d.end_of("invalid")
