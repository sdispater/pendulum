from datetime import time

import pendulum

from ..conftest import assert_time


def test_equal_to_true():
    t1 = pendulum.time(1, 2, 3)
    t2 = pendulum.time(1, 2, 3)
    t3 = time(1, 2, 3)

    assert t1 == t2
    assert t1 == t3


def test_equal_to_false():
    t1 = pendulum.time(1, 2, 3)
    t2 = pendulum.time(1, 2, 4)
    t3 = time(1, 2, 4)

    assert t1 != t2
    assert t1 != t3


def test_not_equal_to_none():
    t1 = pendulum.time(1, 2, 3)

    assert t1 != None  # noqa


def test_greater_than_true():
    t1 = pendulum.time(1, 2, 3)
    t2 = pendulum.time(1, 2, 2)
    t3 = time(1, 2, 2)

    assert t1 > t2
    assert t1 > t3


def test_greater_than_false():
    t1 = pendulum.time(1, 2, 2)
    t2 = pendulum.time(1, 2, 3)
    t3 = time(1, 2, 3)

    assert not t1 > t2
    assert not t1 > t3


def test_greater_than_or_equal_true():
    t1 = pendulum.time(1, 2, 3)
    t2 = pendulum.time(1, 2, 2)
    t3 = time(1, 2, 2)

    assert t1 >= t2
    assert t1 >= t3


def test_greater_than_or_equal_true_equal():
    t1 = pendulum.time(1, 2, 3)
    t2 = pendulum.time(1, 2, 3)
    t3 = time(1, 2, 3)

    assert t1 >= t2
    assert t1 >= t3


def test_greater_than_or_equal_false():
    t1 = pendulum.time(1, 2, 2)
    t2 = pendulum.time(1, 2, 3)
    t3 = time(1, 2, 3)

    assert not t1 >= t2
    assert not t1 >= t3


def test_less_than_true():
    t1 = pendulum.time(1, 2, 2)
    t2 = pendulum.time(1, 2, 3)
    t3 = time(1, 2, 3)

    assert t1 < t2
    assert t1 < t3


def test_less_than_false():
    t1 = pendulum.time(1, 2, 3)
    t2 = pendulum.time(1, 2, 2)
    t3 = time(1, 2, 2)

    assert not t1 < t2
    assert not t1 < t3


def test_less_than_or_equal_true():
    t1 = pendulum.time(1, 2, 2)
    t2 = pendulum.time(1, 2, 3)
    t3 = time(1, 2, 3)

    assert t1 <= t2
    assert t1 <= t3


def test_less_than_or_equal_true_equal():
    t1 = pendulum.time(1, 2, 3)
    t2 = pendulum.time(1, 2, 3)
    t3 = time(1, 2, 3)

    assert t1 <= t2
    assert t1 <= t3


def test_less_than_or_equal_false():
    t1 = pendulum.time(1, 2, 3)
    t2 = pendulum.time(1, 2, 2)
    t3 = time(1, 2, 2)

    assert not t1 <= t2
    assert not t1 <= t3


def test_closest():
    instance = pendulum.time(12, 34, 56)
    t1 = pendulum.time(12, 34, 54)
    t2 = pendulum.time(12, 34, 59)
    closest = instance.closest(t1, t2)
    assert t1 == closest

    closest = instance.closest(t2, t1)
    assert t1 == closest


def test_closest_with_time():
    instance = pendulum.time(12, 34, 56)
    t1 = pendulum.time(12, 34, 54)
    t2 = pendulum.time(12, 34, 59)
    closest = instance.closest(t1, t2)

    assert_time(closest, 12, 34, 54)


def test_closest_with_equals():
    instance = pendulum.time(12, 34, 56)
    t1 = pendulum.time(12, 34, 56)
    t2 = pendulum.time(12, 34, 59)
    closest = instance.closest(t1, t2)
    assert t1 == closest


def test_farthest():
    instance = pendulum.time(12, 34, 56)
    t1 = pendulum.time(12, 34, 54)
    t2 = pendulum.time(12, 34, 59)
    farthest = instance.farthest(t1, t2)
    assert t2 == farthest

    farthest = instance.farthest(t2, t1)
    assert t2 == farthest


def test_farthest_with_time():
    instance = pendulum.time(12, 34, 56)
    t1 = pendulum.time(12, 34, 54)
    t2 = pendulum.time(12, 34, 59)
    farthest = instance.farthest(t1, t2)

    assert_time(farthest, 12, 34, 59)


def test_farthest_with_equals():
    instance = pendulum.time(12, 34, 56)
    t1 = pendulum.time(12, 34, 56)
    t2 = pendulum.time(12, 34, 59)

    farthest = instance.farthest(t1, t2)
    assert t2 == farthest


def test_comparison_to_unsupported():
    t1 = pendulum.now().time()

    assert t1 != "test"
    assert t1 not in ["test"]
