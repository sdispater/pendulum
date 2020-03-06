import pickle

from datetime import date

import pendulum
import pytest


@pytest.fixture()
def p():
    return pendulum.Date(2016, 8, 27)


@pytest.fixture()
def d():
    return date(2016, 8, 27)


def test_timetuple(p, d):
    assert p.timetuple() == d.timetuple()


def test_ctime(p, d):
    assert p.ctime() == d.ctime()


def test_isoformat(p, d):
    assert p.isoformat() == d.isoformat()


def test_toordinal(p, d):
    assert p.toordinal() == d.toordinal()


def test_weekday(p, d):
    assert p.weekday() == d.weekday()


def test_isoweekday(p, d):
    assert p.isoweekday() == d.isoweekday()


def test_isocalendar(p, d):
    assert p.isocalendar() == d.isocalendar()


def test_fromtimestamp():
    assert pendulum.Date.fromtimestamp(0) == date.fromtimestamp(0)


def test_fromordinal():
    assert pendulum.Date.fromordinal(730120) == date.fromordinal(730120)


def test_hash():
    d1 = pendulum.Date(2016, 8, 27)
    d2 = pendulum.Date(2016, 8, 27)
    d3 = pendulum.Date(2016, 8, 28)

    assert hash(d2) == hash(d1)
    assert hash(d1) != hash(d3)


def test_pickle():
    d1 = pendulum.Date(2016, 8, 27)
    s = pickle.dumps(d1)
    d2 = pickle.loads(s)

    assert isinstance(d2, pendulum.Date)
    assert d2 == d1
