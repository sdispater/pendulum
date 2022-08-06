from __future__ import annotations

from datetime import date

import pendulum

from tests.conftest import assert_date


def test_equal_to_true():
    d1 = pendulum.Date(2000, 1, 1)
    d2 = pendulum.Date(2000, 1, 1)
    d3 = date(2000, 1, 1)

    assert d2 == d1
    assert d3 == d1


def test_equal_to_false():
    d1 = pendulum.Date(2000, 1, 1)
    d2 = pendulum.Date(2000, 1, 2)
    d3 = date(2000, 1, 2)

    assert d1 != d2
    assert d1 != d3


def test_not_equal_to_true():
    d1 = pendulum.Date(2000, 1, 1)
    d2 = pendulum.Date(2000, 1, 2)
    d3 = date(2000, 1, 2)

    assert d1 != d2
    assert d1 != d3


def test_not_equal_to_false():
    d1 = pendulum.Date(2000, 1, 1)
    d2 = pendulum.Date(2000, 1, 1)
    d3 = date(2000, 1, 1)

    assert d2 == d1
    assert d3 == d1


def test_not_equal_to_none():
    d1 = pendulum.Date(2000, 1, 1)

    assert d1 != None  # noqa


def test_greater_than_true():
    d1 = pendulum.Date(2000, 1, 1)
    d2 = pendulum.Date(1999, 12, 31)
    d3 = date(1999, 12, 31)

    assert d1 > d2
    assert d1 > d3


def test_greater_than_false():
    d1 = pendulum.Date(2000, 1, 1)
    d2 = pendulum.Date(2000, 1, 2)
    d3 = date(2000, 1, 2)

    assert not d1 > d2
    assert not d1 > d3


def test_greater_than_or_equal_true():
    d1 = pendulum.Date(2000, 1, 1)
    d2 = pendulum.Date(1999, 12, 31)
    d3 = date(1999, 12, 31)

    assert d1 >= d2
    assert d1 >= d3


def test_greater_than_or_equal_true_equal():
    d1 = pendulum.Date(2000, 1, 1)
    d2 = pendulum.Date(2000, 1, 1)
    d3 = date(2000, 1, 1)

    assert d1 >= d2
    assert d1 >= d3


def test_greater_than_or_equal_false():
    d1 = pendulum.Date(2000, 1, 1)
    d2 = pendulum.Date(2000, 1, 2)
    d3 = date(2000, 1, 2)

    assert not d1 >= d2
    assert not d1 >= d3


def test_less_than_true():
    d1 = pendulum.Date(2000, 1, 1)
    d2 = pendulum.Date(2000, 1, 2)
    d3 = date(2000, 1, 2)

    assert d1 < d2
    assert d1 < d3


def test_less_than_false():
    d1 = pendulum.Date(2000, 1, 2)
    d2 = pendulum.Date(2000, 1, 1)
    d3 = date(2000, 1, 1)

    assert not d1 < d2
    assert not d1 < d3


def test_less_than_or_equal_true():
    d1 = pendulum.Date(2000, 1, 1)
    d2 = pendulum.Date(2000, 1, 2)
    d3 = date(2000, 1, 2)

    assert d1 <= d2
    assert d1 <= d3


def test_less_than_or_equal_true_equal():
    d1 = pendulum.Date(2000, 1, 1)
    d2 = pendulum.Date(2000, 1, 1)
    d3 = date(2000, 1, 1)

    assert d1 <= d2
    assert d1 <= d3


def test_less_than_or_equal_false():
    d1 = pendulum.Date(2000, 1, 2)
    d2 = pendulum.Date(2000, 1, 1)
    d3 = date(2000, 1, 1)

    assert not d1 <= d2
    assert not d1 <= d3


def test_is_anniversary():
    d = pendulum.Date.today()
    an_anniversary = d.subtract(years=1)
    assert an_anniversary.is_anniversary()
    not_an_anniversary = d.subtract(days=1)
    assert not not_an_anniversary.is_anniversary()
    also_not_an_anniversary = d.add(days=2)
    assert not also_not_an_anniversary.is_anniversary()

    d1 = pendulum.Date(1987, 4, 23)
    d2 = pendulum.Date(2014, 9, 26)
    d3 = pendulum.Date(2014, 4, 23)
    assert not d2.is_anniversary(d1)
    assert d3.is_anniversary(d1)


def test_is_birthday():  # backward compatibility
    d = pendulum.Date.today()
    an_anniversary = d.subtract(years=1)
    assert an_anniversary.is_birthday()
    not_an_anniversary = d.subtract(days=1)
    assert not not_an_anniversary.is_birthday()
    also_not_an_anniversary = d.add(days=2)
    assert not also_not_an_anniversary.is_birthday()

    d1 = pendulum.Date(1987, 4, 23)
    d2 = pendulum.Date(2014, 9, 26)
    d3 = pendulum.Date(2014, 4, 23)
    assert not d2.is_birthday(d1)
    assert d3.is_birthday(d1)


def test_closest():
    instance = pendulum.Date(2015, 5, 28)
    dt1 = pendulum.Date(2015, 5, 27)
    dt2 = pendulum.Date(2015, 5, 30)
    closest = instance.closest(dt1, dt2)
    assert closest == dt1

    closest = instance.closest(dt2, dt1)
    assert closest == dt1


def test_closest_with_date():
    instance = pendulum.Date(2015, 5, 28)
    dt1 = date(2015, 5, 27)
    dt2 = date(2015, 5, 30)
    closest = instance.closest(dt1, dt2)
    assert isinstance(closest, pendulum.Date)
    assert_date(closest, 2015, 5, 27)


def test_closest_with_equals():
    instance = pendulum.Date(2015, 5, 28)
    dt1 = pendulum.Date(2015, 5, 28)
    dt2 = pendulum.Date(2015, 5, 30)
    closest = instance.closest(dt1, dt2)
    assert closest == dt1


def test_farthest():
    instance = pendulum.Date(2015, 5, 28)
    dt1 = pendulum.Date(2015, 5, 27)
    dt2 = pendulum.Date(2015, 5, 30)
    closest = instance.farthest(dt1, dt2)
    assert closest == dt2

    closest = instance.farthest(dt2, dt1)
    assert closest == dt2


def test_farthest_with_date():
    instance = pendulum.Date(2015, 5, 28)
    dt1 = date(2015, 5, 27)
    dt2 = date(2015, 5, 30)
    closest = instance.farthest(dt1, dt2)
    assert isinstance(closest, pendulum.Date)
    assert_date(closest, 2015, 5, 30)


def test_farthest_with_equals():
    instance = pendulum.Date(2015, 5, 28)
    dt1 = pendulum.Date(2015, 5, 28)
    dt2 = pendulum.Date(2015, 5, 30)
    closest = instance.farthest(dt1, dt2)
    assert closest == dt2


def test_is_same_day():
    dt1 = pendulum.Date(2015, 5, 28)
    dt2 = pendulum.Date(2015, 5, 29)
    dt3 = pendulum.Date(2015, 5, 28)
    dt4 = date(2015, 5, 28)
    dt5 = date(2015, 5, 29)

    assert not dt1.is_same_day(dt2)
    assert dt1.is_same_day(dt3)
    assert dt1.is_same_day(dt4)
    assert not dt1.is_same_day(dt5)


def test_comparison_to_unsupported():
    dt1 = pendulum.Date.today()

    assert dt1 != "test"
    assert dt1 not in ["test"]
