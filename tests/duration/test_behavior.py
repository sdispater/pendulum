from __future__ import annotations

import pickle

from copy import deepcopy
from datetime import timedelta

import pendulum

from tests.conftest import assert_duration


def test_pickle() -> None:
    it = pendulum.duration(days=3, seconds=2456, microseconds=123456)
    s = pickle.dumps(it)
    it2 = pickle.loads(s)

    assert it == it2


def test_comparison_to_timedelta() -> None:
    duration = pendulum.duration(days=3)

    assert duration < timedelta(days=4)


def test_deepcopy() -> None:
    duration = pendulum.duration(months=1)
    copied_duration = deepcopy(duration)

    assert copied_duration == duration
    assert_duration(copied_duration, months=1)
