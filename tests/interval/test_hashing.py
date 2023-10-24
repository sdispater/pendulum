from __future__ import annotations

import pendulum


def test_intervals_with_same_duration_and_different_dates():
    day1 = pendulum.DateTime(2018, 1, 1)
    day2 = pendulum.DateTime(2018, 1, 2)
    day3 = pendulum.DateTime(2018, 1, 2)

    interval1 = day2 - day1
    interval2 = day3 - day2

    assert interval1 != interval2
    assert len({interval1, interval2}) == 2


def test_intervals_with_same_dates():
    interval1 = pendulum.DateTime(2018, 1, 2) - pendulum.DateTime(2018, 1, 1)
    interval2 = pendulum.DateTime(2018, 1, 2) - pendulum.DateTime(2018, 1, 1)

    assert interval1 == interval2
    assert len({interval1, interval2}) == 1
