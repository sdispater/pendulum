from __future__ import annotations

import pickle

from datetime import time

import pytest

import pendulum

from pendulum import Time


@pytest.fixture()
def p():
    return pendulum.Time(12, 34, 56, 123456, tzinfo=pendulum.timezone("Europe/Paris"))


@pytest.fixture()
def d():
    return time(12, 34, 56, 123456, tzinfo=pendulum.timezone("Europe/Paris"))


def test_hash(p, d):
    assert hash(d) == hash(p)
    dt1 = Time(12, 34, 57, 123456)

    assert hash(p) != hash(dt1)


def test_pickle():
    dt1 = Time(12, 34, 56, 123456)
    s = pickle.dumps(dt1)
    dt2 = pickle.loads(s)

    assert dt2 == dt1


def test_utcoffset(p, d):
    assert d.utcoffset() == p.utcoffset()


def test_dst(p, d):
    assert d.dst() == p.dst()


def test_tzname(p, d):
    assert d.tzname() == p.tzname()
    assert Time(12, 34, 56, 123456).tzname() == time(12, 34, 56, 123456).tzname()
