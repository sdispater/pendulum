from __future__ import annotations

import pendulum


def test_dst_add():
    start = pendulum.datetime(2017, 3, 7, tz="America/Toronto")
    end = start.add(days=6)
    period = end - start
    new_end = start + period

    assert new_end == end


def test_dst_add_non_variable_units():
    start = pendulum.datetime(2013, 3, 31, 1, 30, tz="Europe/Paris")
    end = start.add(hours=1)
    period = end - start
    new_end = start + period

    assert new_end == end


def test_dst_subtract():
    start = pendulum.datetime(2017, 3, 7, tz="America/Toronto")
    end = start.add(days=6)
    period = end - start
    new_start = end - period

    assert new_start == start


def test_naive_subtract():
    start = pendulum.naive(2013, 3, 31, 1, 30)
    end = start.add(hours=1)
    period = end - start
    new_end = start + period

    assert new_end == end


def test_negative_difference_subtract():
    start = pendulum.datetime(2018, 5, 28, 12, 34, 56, 123456)
    end = pendulum.datetime(2018, 1, 1)

    period = end - start
    new_end = start + period

    assert new_end == end
