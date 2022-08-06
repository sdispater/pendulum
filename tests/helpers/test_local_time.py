from __future__ import annotations

import pendulum

from pendulum.helpers import local_time


def test_local_time_positive_integer():
    d = pendulum.datetime(2016, 8, 7, 12, 34, 56, 123456)

    t = local_time(d.int_timestamp, 0, d.microsecond)
    assert d.year == t[0]
    assert d.month == t[1]
    assert d.day == t[2]
    assert d.hour == t[3]
    assert d.minute == t[4]
    assert d.second == t[5]
    assert d.microsecond == t[6]


def test_local_time_negative_integer():
    d = pendulum.datetime(1951, 8, 7, 12, 34, 56, 123456)

    t = local_time(d.int_timestamp, 0, d.microsecond)
    assert d.year == t[0]
    assert d.month == t[1]
    assert d.day == t[2]
    assert d.hour == t[3]
    assert d.minute == t[4]
    assert d.second == t[5]
    assert d.microsecond == t[6]
