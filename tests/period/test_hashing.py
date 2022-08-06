from __future__ import annotations

import pendulum


def test_periods_with_same_duration_and_different_dates():
    day1 = pendulum.DateTime(2018, 1, 1)
    day2 = pendulum.DateTime(2018, 1, 2)
    day3 = pendulum.DateTime(2018, 1, 2)

    period1 = day2 - day1
    period2 = day3 - day2

    assert period1 != period2
    assert len({period1, period2}) == 2


def test_periods_with_same_dates():
    period1 = pendulum.DateTime(2018, 1, 2) - pendulum.DateTime(2018, 1, 1)
    period2 = pendulum.DateTime(2018, 1, 2) - pendulum.DateTime(2018, 1, 1)

    assert period1 == period2
    assert len({period1, period2}) == 1
