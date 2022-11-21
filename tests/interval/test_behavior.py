from __future__ import annotations

import pickle

from datetime import timedelta

import pendulum


def test_pickle():
    dt1 = pendulum.datetime(2016, 11, 18)
    dt2 = pendulum.datetime(2016, 11, 20)

    p = pendulum.interval(dt1, dt2)
    s = pickle.dumps(p)
    p2 = pickle.loads(s)

    assert p.start == p2.start
    assert p.end == p2.end
    assert p.invert == p2.invert

    p = pendulum.interval(dt2, dt1)
    s = pickle.dumps(p)
    p2 = pickle.loads(s)

    assert p.start == p2.start
    assert p.end == p2.end
    assert p.invert == p2.invert

    p = pendulum.interval(dt2, dt1, True)
    s = pickle.dumps(p)
    p2 = pickle.loads(s)

    assert p.start == p2.start
    assert p.end == p2.end
    assert p.invert == p2.invert


def test_comparison_to_timedelta():
    dt1 = pendulum.datetime(2016, 11, 18)
    dt2 = pendulum.datetime(2016, 11, 20)

    period = dt2 - dt1

    assert period < timedelta(days=4)


def test_equality_to_timedelta():
    dt1 = pendulum.datetime(2016, 11, 18)
    dt2 = pendulum.datetime(2016, 11, 20)

    period = dt2 - dt1

    assert period == timedelta(days=2)
