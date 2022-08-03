from __future__ import annotations

import pendulum


def test_in_weeks():
    it = pendulum.duration(days=17)
    assert it.in_weeks() == 2


def test_in_days():
    it = pendulum.duration(days=3)
    assert it.in_days() == 3


def test_in_hours():
    it = pendulum.duration(days=3, minutes=72)
    assert it.in_hours() == 73


def test_in_minutes():
    it = pendulum.duration(minutes=6, seconds=72)
    assert it.in_minutes() == 7


def test_in_seconds():
    it = pendulum.duration(seconds=72)
    assert it.in_seconds() == 72
