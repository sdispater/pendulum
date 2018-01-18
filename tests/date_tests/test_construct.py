from datetime import date
from pendulum import Date

from ..conftest import assert_date


def test_construct():
    d = Date(2016, 10, 20)

    assert_date(d, 2016, 10, 20)


def test_today():
    d = Date.today()

    assert isinstance(d, Date)


def test_instance():
    d = Date.instance(date(2016, 10, 20))

    assert isinstance(d, Date)
    assert_date(d, 2016, 10, 20)


def test_create():
    d = Date.create(2016, 10, 20)

    assert isinstance(d, Date)
    assert_date(d, 2016, 10, 20)


def test_create_empty_values():
    now = Date.today()
    d = Date.create()

    assert isinstance(d, Date)
    assert_date(d, now.year, now.month, now.day)
