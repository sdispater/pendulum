from datetime import timedelta

import pendulum

from ..conftest import assert_duration


def test_add_interval():
    p1 = pendulum.duration(days=23, seconds=32)
    p2 = pendulum.duration(days=12, seconds=30)

    p = p1 + p2
    assert_duration(p, 0, 0, 5, 0, 0, 1, 2)


def test_add_timedelta():
    p1 = pendulum.duration(days=23, seconds=32)
    p2 = timedelta(days=12, seconds=30)

    p = p1 + p2
    assert_duration(p, 0, 0, 5, 0, 0, 1, 2)


def test_add_unsupported():
    p = pendulum.duration(days=23, seconds=32)
    assert NotImplemented == p.__add__(5)


def test_sub_interval():
    p1 = pendulum.duration(days=23, seconds=32)
    p2 = pendulum.duration(days=12, seconds=28)

    p = p1 - p2
    assert_duration(p, 0, 0, 1, 4, 0, 0, 4)


def test_sub_timedelta():
    p1 = pendulum.duration(days=23, seconds=32)
    p2 = timedelta(days=12, seconds=28)

    p = p1 - p2
    assert_duration(p, 0, 0, 1, 4, 0, 0, 4)


def test_sub_unsupported():
    p = pendulum.duration(days=23, seconds=32)
    assert NotImplemented == p.__sub__(5)


def test_neg():
    p = pendulum.duration(days=23, seconds=32)
    assert_duration(-p, 0, 0, -3, -2, 0, 0, -32)
