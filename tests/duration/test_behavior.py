from __future__ import annotations

import pickle

from datetime import timedelta

import pendulum


def test_pickle():
    it = pendulum.duration(days=3, seconds=2456, microseconds=123456)
    s = pickle.dumps(it)
    it2 = pickle.loads(s)

    assert it == it2


def test_comparison_to_timedelta():
    duration = pendulum.duration(days=3)

    assert duration < timedelta(days=4)
