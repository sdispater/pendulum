import sys
from datetime import timedelta, timezone

import pendulum

from ..conftest import assert_datetime


def test_in_timezone():
    d = pendulum.create(2015, 1, 15, 18, 15, 34)
    now = pendulum.create(2015, 1, 15, 18, 15, 34)
    assert d.timezone_name == 'UTC'
    assert_datetime(d, now.year, now.month, now.day, now.hour, now.minute)

    d = d.in_timezone('Europe/Paris')
    assert d.timezone_name == 'Europe/Paris'
    assert_datetime(d, now.year, now.month, now.day, now.hour + 1, now.minute)


def test_in_tz():
    d = pendulum.create(2015, 1, 15, 18, 15, 34)
    now = pendulum.create(2015, 1, 15, 18, 15, 34)
    assert d.timezone_name == 'UTC'
    assert_datetime(d, now.year, now.month, now.day, now.hour, now.minute)

    d = d.in_tz('Europe/Paris')
    assert d.timezone_name == 'Europe/Paris'
    assert_datetime(d, now.year, now.month, now.day, now.hour + 1, now.minute)


def test_astimezone():
    d = pendulum.create(2015, 1, 15, 18, 15, 34)
    now = pendulum.create(2015, 1, 15, 18, 15, 34)
    assert d.timezone_name == 'UTC'
    assert_datetime(d, now.year, now.month, now.day, now.hour, now.minute)

    d = d.astimezone(pendulum.timezone('Europe/Paris'))
    assert d.timezone_name == 'Europe/Paris'
    assert_datetime(d, now.year, now.month, now.day, now.hour + 1, now.minute)

    d = d.astimezone(timezone.utc)
    assert d.timezone_name == '+00:00'
    assert_datetime(d, now.year, now.month, now.day, now.hour, now.minute)

    d = d.astimezone(timezone(timedelta(hours=-8)))
    assert d.timezone_name == '-08:00'
    assert_datetime(d, now.year, now.month, now.day, now.hour - 8, now.minute)
