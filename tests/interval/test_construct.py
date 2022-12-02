from __future__ import annotations

from datetime import datetime

import pendulum

from tests.conftest import assert_datetime


def test_with_datetimes():
    dt1 = datetime(2000, 1, 1)
    dt2 = datetime(2000, 1, 31)
    p = pendulum.interval(dt1, dt2)

    assert isinstance(p.start, pendulum.DateTime)
    assert isinstance(p.end, pendulum.DateTime)
    assert_datetime(p.start, 2000, 1, 1)
    assert_datetime(p.end, 2000, 1, 31)


def test_with_pendulum():
    dt1 = pendulum.DateTime(2000, 1, 1)
    dt2 = pendulum.DateTime(2000, 1, 31)
    p = pendulum.interval(dt1, dt2)

    assert_datetime(p.start, 2000, 1, 1)
    assert_datetime(p.end, 2000, 1, 31)


def test_inverted():
    dt1 = pendulum.DateTime(2000, 1, 1)
    dt2 = pendulum.DateTime(2000, 1, 31)
    p = pendulum.interval(dt2, dt1)

    assert_datetime(p.start, 2000, 1, 31)
    assert_datetime(p.end, 2000, 1, 1)


def test_inverted_and_absolute():
    dt1 = pendulum.DateTime(2000, 1, 1)
    dt2 = pendulum.DateTime(2000, 1, 31)
    p = pendulum.interval(dt2, dt1, True)

    assert_datetime(p.start, 2000, 1, 1)
    assert_datetime(p.end, 2000, 1, 31)


def test_accuracy():
    dt1 = pendulum.DateTime(2000, 11, 20)
    dt2 = pendulum.DateTime(2000, 11, 25)
    dt3 = pendulum.DateTime(2016, 11, 5)
    p1 = pendulum.interval(dt1, dt3)
    p2 = pendulum.interval(dt2, dt3)

    assert p1.years == 15
    assert p1.in_years() == 15
    assert p1.months == 11
    assert p1.in_months() == 191
    assert p1.days == 5829
    assert p1.remaining_days == 2
    assert p1.in_days() == 5829

    assert p2.years == 15
    assert p2.in_years() == 15
    assert p2.months == 11
    assert p2.in_months() == 191
    assert p2.days == 5824
    assert p2.remaining_days == 4
    assert p2.in_days() == 5824


def test_dst_transition():
    start = pendulum.datetime(2017, 3, 7, tz="America/Toronto")
    end = start.add(days=6)
    period = end - start

    assert period.days == 5
    assert period.seconds == 82800

    assert period.remaining_days == 6
    assert period.hours == 0
    assert period.remaining_seconds == 0

    assert period.in_days() == 6
    assert period.in_hours() == 5 * 24 + 23


def test_timedelta_behavior():
    dt1 = pendulum.DateTime(2000, 11, 20, 1)
    dt2 = pendulum.DateTime(2000, 11, 25, 2)
    dt3 = pendulum.DateTime(2016, 11, 5, 3)

    p1 = pendulum.interval(dt1, dt3)
    p2 = pendulum.interval(dt2, dt3)
    it1 = p1.as_timedelta()
    it2 = p2.as_timedelta()

    assert it1.total_seconds() == p1.total_seconds()
    assert it2.total_seconds() == p2.total_seconds()
    assert it1.days == p1.days
    assert it2.days == p2.days
    assert it1.seconds == p1.seconds
    assert it2.seconds == p2.seconds
    assert it1.microseconds == p1.microseconds
    assert it2.microseconds == p2.microseconds


def test_different_timezones_same_time():
    dt1 = pendulum.datetime(2013, 3, 31, 1, 30, tz="Europe/Paris")
    dt2 = pendulum.datetime(2013, 4, 1, 1, 30, tz="Europe/Paris")
    period = dt2 - dt1

    assert period.in_words() == "1 day"
    assert period.in_hours() == 23

    dt1 = pendulum.datetime(2013, 3, 31, 1, 30, tz="Europe/Paris")
    dt2 = pendulum.datetime(2013, 4, 1, 1, 30, tz="America/Toronto")
    period = dt2 - dt1

    assert period.in_words() == "1 day 5 hours"
    assert period.in_hours() == 29
