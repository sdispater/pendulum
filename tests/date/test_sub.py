from __future__ import annotations

from datetime import datetime
from datetime import timedelta

import pytest

import pendulum

from tests.conftest import assert_date


def test_subtract_years_positive():
    assert pendulum.date(1975, 1, 1).subtract(years=1).year == 1974


def test_subtract_years_zero():
    assert pendulum.date(1975, 1, 1).subtract(years=0).year == 1975


def test_subtract_years_negative():
    assert pendulum.date(1975, 1, 1).subtract(years=-1).year == 1976


def test_subtract_months_positive():
    assert pendulum.date(1975, 1, 1).subtract(months=1).month == 12


def test_subtract_months_zero():
    assert pendulum.date(1975, 12, 1).subtract(months=0).month == 12


def test_subtract_months_negative():
    assert pendulum.date(1975, 11, 1).subtract(months=-1).month == 12


def test_subtract_days_positive():
    assert pendulum.Date(1975, 6, 1).subtract(days=1).day == 31


def test_subtract_days_zero():
    assert pendulum.Date(1975, 5, 31).subtract(days=0).day == 31


def test_subtract_days_negative():
    assert pendulum.Date(1975, 5, 30).subtract(days=-1).day == 31


def test_subtract_days_max():
    delta = pendulum.now() - pendulum.instance(datetime.min)
    assert pendulum.now().subtract(days=delta.days - 1).year == 1


def test_subtract_weeks_positive():
    assert pendulum.Date(1975, 5, 28).subtract(weeks=1).day == 21


def test_subtract_weeks_zero():
    assert pendulum.Date(1975, 5, 21).subtract(weeks=0).day == 21


def test_subtract_weeks_negative():
    assert pendulum.Date(1975, 5, 14).subtract(weeks=-1).day == 21


def test_subtract_timedelta():
    delta = timedelta(days=18)
    d = pendulum.date(2015, 3, 14)

    new = d - delta
    assert isinstance(new, pendulum.Date)
    assert_date(new, 2015, 2, 24)


def test_subtract_duration():
    delta = pendulum.duration(years=2, months=3, days=18)
    d = pendulum.date(2015, 3, 14)

    new = d - delta
    assert_date(new, 2012, 11, 26)


def test_addition_invalid_type():
    d = pendulum.date(2015, 3, 14)

    with pytest.raises(TypeError):
        d - "ab"

    with pytest.raises(TypeError):
        "ab" - d
