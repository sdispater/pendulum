from datetime import timedelta

import pendulum
import pytest


def test_add_hours_positive():
    assert pendulum.time(12, 34, 56).add(hours=1).hour == 13


def test_add_hours_zero():
    assert pendulum.time(12, 34, 56).add(hours=0).hour == 12


def test_add_hours_negative():
    assert pendulum.time(12, 34, 56).add(hours=-1).hour == 11


def test_add_minutes_positive():
    assert pendulum.time(12, 34, 56).add(minutes=1).minute == 35


def test_add_minutes_zero():
    assert pendulum.time(12, 34, 56).add(minutes=0).minute == 34


def test_add_minutes_negative():
    assert pendulum.time(12, 34, 56).add(minutes=-1).minute == 33


def test_add_seconds_positive():
    assert pendulum.time(12, 34, 56).add(seconds=1).second == 57


def test_add_seconds_zero():
    assert pendulum.time(12, 34, 56).add(seconds=0).second == 56


def test_add_seconds_negative():
    assert pendulum.time(12, 34, 56).add(seconds=-1).second == 55


def test_add_timedelta():
    delta = timedelta(seconds=45, microseconds=123456)
    d = pendulum.time(3, 12, 15, 654321)

    d = d.add_timedelta(delta)
    assert d.minute == 13
    assert d.second == 0
    assert d.microsecond == 777777

    d = pendulum.time(3, 12, 15, 654321)

    d = d + delta
    assert d.minute == 13
    assert d.second == 0
    assert d.microsecond == 777777


def test_add_timedelta_with_days():
    delta = timedelta(days=3, seconds=45, microseconds=123456)
    d = pendulum.time(3, 12, 15, 654321)

    with pytest.raises(TypeError):
        d.add_timedelta(delta)


def test_addition_invalid_type():
    d = pendulum.time(3, 12, 15, 654321)

    with pytest.raises(TypeError):
        d + 3

    with pytest.raises(TypeError):
        3 + d
