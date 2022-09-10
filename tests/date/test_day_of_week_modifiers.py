from __future__ import annotations

import pytest

import pendulum

from pendulum.exceptions import PendulumException
from tests.conftest import assert_date


def test_start_of_week():
    d = pendulum.date(1980, 8, 7).start_of("week")
    assert_date(d, 1980, 8, 4)


def test_start_of_week_from_week_start():
    d = pendulum.date(1980, 8, 4).start_of("week")
    assert_date(d, 1980, 8, 4)


def test_start_of_week_crossing_year_boundary():
    d = pendulum.date(2014, 1, 1).start_of("week")
    assert_date(d, 2013, 12, 30)


def test_end_of_week():
    d = pendulum.date(1980, 8, 7).end_of("week")
    assert_date(d, 1980, 8, 10)


def test_end_of_week_from_week_end():
    d = pendulum.date(1980, 8, 10).end_of("week")
    assert_date(d, 1980, 8, 10)


def test_end_of_week_crossing_year_boundary():
    d = pendulum.date(2013, 12, 31).end_of("week")
    assert_date(d, 2014, 1, 5)


def test_next():
    d = pendulum.date(1975, 5, 21).next()
    assert_date(d, 1975, 5, 28)


def test_next_monday():
    d = pendulum.date(1975, 5, 21).next(pendulum.MONDAY)
    assert_date(d, 1975, 5, 26)


def test_next_saturday():
    d = pendulum.date(1975, 5, 21).next(6)
    assert_date(d, 1975, 5, 24)


def test_next_invalid():
    dt = pendulum.date(1975, 5, 21)

    with pytest.raises(ValueError):
        dt.next(7)


def test_previous():
    d = pendulum.date(1975, 5, 21).previous()
    assert_date(d, 1975, 5, 14)


def test_previous_monday():
    d = pendulum.date(1975, 5, 21).previous(pendulum.MONDAY)
    assert_date(d, 1975, 5, 19)


def test_previous_saturday():
    d = pendulum.date(1975, 5, 21).previous(6)
    assert_date(d, 1975, 5, 17)


def test_previous_invalid():
    dt = pendulum.date(1975, 5, 21)

    with pytest.raises(ValueError):
        dt.previous(7)


def test_first_day_of_month():
    d = pendulum.date(1975, 11, 21).first_of("month")
    assert_date(d, 1975, 11, 1)


def test_first_wednesday_of_month():
    d = pendulum.date(1975, 11, 21).first_of("month", pendulum.WEDNESDAY)
    assert_date(d, 1975, 11, 5)


def test_first_friday_of_month():
    d = pendulum.date(1975, 11, 21).first_of("month", 5)
    assert_date(d, 1975, 11, 7)


def test_last_day_of_month():
    d = pendulum.date(1975, 12, 5).last_of("month")
    assert_date(d, 1975, 12, 31)


def test_last_tuesday_of_month():
    d = pendulum.date(1975, 12, 1).last_of("month", pendulum.TUESDAY)
    assert_date(d, 1975, 12, 30)


def test_last_friday_of_month():
    d = pendulum.date(1975, 12, 5).last_of("month", 5)
    assert_date(d, 1975, 12, 26)


def test_nth_of_month_outside_scope():
    d = pendulum.date(1975, 6, 5)

    with pytest.raises(PendulumException):
        d.nth_of("month", 6, pendulum.MONDAY)


def test_nth_of_month_outside_year():
    d = pendulum.date(1975, 12, 5)

    with pytest.raises(PendulumException):
        d.nth_of("month", 55, pendulum.MONDAY)


def test_nth_of_month_first():
    d = pendulum.date(1975, 12, 5).nth_of("month", 1, pendulum.MONDAY)

    assert_date(d, 1975, 12, 1)


def test_2nd_monday_of_month():
    d = pendulum.date(1975, 12, 5).nth_of("month", 2, pendulum.MONDAY)

    assert_date(d, 1975, 12, 8)


def test_3rd_wednesday_of_month():
    d = pendulum.date(1975, 12, 5).nth_of("month", 3, 3)

    assert_date(d, 1975, 12, 17)


def test_first_day_of_quarter():
    d = pendulum.date(1975, 11, 21).first_of("quarter")
    assert_date(d, 1975, 10, 1)


def test_first_wednesday_of_quarter():
    d = pendulum.date(1975, 11, 21).first_of("quarter", pendulum.WEDNESDAY)
    assert_date(d, 1975, 10, 1)


def test_first_friday_of_quarter():
    d = pendulum.date(1975, 11, 21).first_of("quarter", 5)
    assert_date(d, 1975, 10, 3)


def test_first_of_quarter_from_a_day_that_will_not_exist_in_the_first_month():
    d = pendulum.date(2014, 5, 31).first_of("quarter")
    assert_date(d, 2014, 4, 1)


def test_last_day_of_quarter():
    d = pendulum.date(1975, 8, 5).last_of("quarter")
    assert_date(d, 1975, 9, 30)


def test_last_tuesday_of_quarter():
    d = pendulum.date(1975, 8, 5).last_of("quarter", pendulum.TUESDAY)
    assert_date(d, 1975, 9, 30)


def test_last_friday_of_quarter():
    d = pendulum.date(1975, 8, 5).last_of("quarter", pendulum.FRIDAY)
    assert_date(d, 1975, 9, 26)


def test_last_day_of_quarter_that_will_not_exist_in_the_last_month():
    d = pendulum.date(2014, 5, 31).last_of("quarter")
    assert_date(d, 2014, 6, 30)


def test_nth_of_quarter_outside_scope():
    d = pendulum.date(1975, 1, 5)

    with pytest.raises(PendulumException):
        d.nth_of("quarter", 20, pendulum.MONDAY)


def test_nth_of_quarter_outside_year():
    d = pendulum.date(1975, 1, 5)

    with pytest.raises(PendulumException):
        d.nth_of("quarter", 55, pendulum.MONDAY)


def test_nth_of_quarter_first():
    d = pendulum.date(1975, 12, 5).nth_of("quarter", 1, pendulum.MONDAY)

    assert_date(d, 1975, 10, 6)


def test_nth_of_quarter_from_a_day_that_will_not_exist_in_the_first_month():
    d = pendulum.date(2014, 5, 31).nth_of("quarter", 2, pendulum.MONDAY)
    assert_date(d, 2014, 4, 14)


def test_2nd_monday_of_quarter():
    d = pendulum.date(1975, 8, 5).nth_of("quarter", 2, pendulum.MONDAY)
    assert_date(d, 1975, 7, 14)


def test_3rd_wednesday_of_quarter():
    d = pendulum.date(1975, 8, 5).nth_of("quarter", 3, 3)
    assert_date(d, 1975, 7, 16)


def test_first_day_of_year():
    d = pendulum.date(1975, 11, 21).first_of("year")
    assert_date(d, 1975, 1, 1)


def test_first_wednesday_of_year():
    d = pendulum.date(1975, 11, 21).first_of("year", pendulum.WEDNESDAY)
    assert_date(d, 1975, 1, 1)


def test_first_friday_of_year():
    d = pendulum.date(1975, 11, 21).first_of("year", 5)
    assert_date(d, 1975, 1, 3)


def test_last_day_of_year():
    d = pendulum.date(1975, 8, 5).last_of("year")
    assert_date(d, 1975, 12, 31)


def test_last_tuesday_of_year():
    d = pendulum.date(1975, 8, 5).last_of("year", pendulum.TUESDAY)
    assert_date(d, 1975, 12, 30)


def test_last_friday_of_year():
    d = pendulum.date(1975, 8, 5).last_of("year", 5)
    assert_date(d, 1975, 12, 26)


def test_nth_of_year_outside_scope():
    d = pendulum.date(1975, 1, 5)

    with pytest.raises(PendulumException):
        d.nth_of("year", 55, pendulum.MONDAY)


def test_nth_of_year_first():
    d = pendulum.date(1975, 12, 5).nth_of("year", 1, pendulum.MONDAY)

    assert_date(d, 1975, 1, 6)


def test_2nd_monday_of_year():
    d = pendulum.date(1975, 8, 5).nth_of("year", 2, pendulum.MONDAY)
    assert_date(d, 1975, 1, 13)


def test_2rd_wednesday_of_year():
    d = pendulum.date(1975, 8, 5).nth_of("year", 3, pendulum.WEDNESDAY)
    assert_date(d, 1975, 1, 15)


def test_7th_thursday_of_year():
    d = pendulum.date(1975, 8, 31).nth_of("year", 7, pendulum.THURSDAY)
    assert_date(d, 1975, 2, 13)


def test_first_of_invalid_unit():
    d = pendulum.date(1975, 8, 5)

    with pytest.raises(ValueError):
        d.first_of("invalid", 3)


def test_last_of_invalid_unit():
    d = pendulum.date(1975, 8, 5)

    with pytest.raises(ValueError):
        d.last_of("invalid", 3)


def test_nth_of_invalid_unit():
    d = pendulum.date(1975, 8, 5)

    with pytest.raises(ValueError):
        d.nth_of("invalid", 3, pendulum.MONDAY)
