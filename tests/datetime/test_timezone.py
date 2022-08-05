from __future__ import annotations

import pendulum

from tests.conftest import assert_datetime


def test_in_timezone():
    d = pendulum.datetime(2015, 1, 15, 18, 15, 34)
    now = pendulum.datetime(2015, 1, 15, 18, 15, 34)
    assert d.timezone_name == "UTC"
    assert_datetime(d, now.year, now.month, now.day, now.hour, now.minute)

    d = d.in_timezone("Europe/Paris")
    assert d.timezone_name == "Europe/Paris"
    assert_datetime(d, now.year, now.month, now.day, now.hour + 1, now.minute)


def test_in_tz():
    d = pendulum.datetime(2015, 1, 15, 18, 15, 34)
    now = pendulum.datetime(2015, 1, 15, 18, 15, 34)
    assert d.timezone_name == "UTC"
    assert_datetime(d, now.year, now.month, now.day, now.hour, now.minute)

    d = d.in_tz("Europe/Paris")
    assert d.timezone_name == "Europe/Paris"
    assert_datetime(d, now.year, now.month, now.day, now.hour + 1, now.minute)


def test_astimezone():
    d = pendulum.datetime(2015, 1, 15, 18, 15, 34)
    now = pendulum.datetime(2015, 1, 15, 18, 15, 34)
    assert d.timezone_name == "UTC"
    assert_datetime(d, now.year, now.month, now.day, now.hour, now.minute)

    d = d.astimezone(pendulum.timezone("Europe/Paris"))
    assert d.timezone_name == "Europe/Paris"
    assert_datetime(d, now.year, now.month, now.day, now.hour + 1, now.minute)
