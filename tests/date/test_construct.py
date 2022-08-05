from __future__ import annotations

from pendulum import Date
from tests.conftest import assert_date


def test_construct():
    d = Date(2016, 10, 20)

    assert_date(d, 2016, 10, 20)


def test_today():
    d = Date.today()

    assert isinstance(d, Date)
