from __future__ import annotations

import pendulum

from tests.conftest import assert_time


def test_init():
    t = pendulum.time(12, 34, 56, 123456)

    assert_time(t, 12, 34, 56, 123456)


def test_init_with_missing_values():
    t = pendulum.time(12, 34, 56)
    assert_time(t, 12, 34, 56, 0)

    t = pendulum.time(12, 34)
    assert_time(t, 12, 34, 0, 0)

    t = pendulum.time(12)
    assert_time(t, 12, 0, 0, 0)
