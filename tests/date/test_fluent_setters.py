from __future__ import annotations

import pendulum

from tests.conftest import assert_date


def test_fluid_year_setter():
    d = pendulum.Date(2016, 10, 20)
    new = d.set(year=1995)

    assert_date(new, 1995, 10, 20)
    assert new.year == 1995


def test_fluid_month_setter():
    d = pendulum.Date(2016, 7, 2)
    new = d.set(month=11)

    assert new.month == 11
    assert d.month == 7


def test_fluid_day_setter():
    d = pendulum.Date(2016, 7, 2)
    new = d.set(day=9)

    assert new.day == 9
    assert d.day == 2
