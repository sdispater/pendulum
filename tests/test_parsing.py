from __future__ import annotations

import pendulum

from tests.conftest import assert_date
from tests.conftest import assert_datetime
from tests.conftest import assert_duration
from tests.conftest import assert_time


def test_parse():
    text = "2016-10-16T12:34:56.123456+01:30"

    dt = pendulum.parse(text)

    assert isinstance(dt, pendulum.DateTime)
    assert_datetime(dt, 2016, 10, 16, 12, 34, 56, 123456)
    assert dt.tz.name == "+01:30"
    assert dt.offset == 5400

    text = "2016-10-16"

    dt = pendulum.parse(text)

    assert isinstance(dt, pendulum.DateTime)
    assert_datetime(dt, 2016, 10, 16, 0, 0, 0, 0)
    assert dt.offset == 0

    with pendulum.travel_to(pendulum.datetime(2015, 11, 12), freeze=True):
        text = "12:34:56.123456"

        dt = pendulum.parse(text)

    assert isinstance(dt, pendulum.DateTime)
    assert_datetime(dt, 2015, 11, 12, 12, 34, 56, 123456)
    assert dt.offset == 0


def test_parse_with_timezone():
    text = "2016-10-16T12:34:56.123456"

    dt = pendulum.parse(text, tz="Europe/Paris")
    assert_datetime(dt, 2016, 10, 16, 12, 34, 56, 123456)
    assert dt.tz.name == "Europe/Paris"
    assert dt.offset == 7200


def test_parse_exact():
    text = "2016-10-16T12:34:56.123456+01:30"

    dt = pendulum.parse(text, exact=True)

    assert isinstance(dt, pendulum.DateTime)
    assert_datetime(dt, 2016, 10, 16, 12, 34, 56, 123456)
    assert dt.offset == 5400

    text = "2016-10-16"

    dt = pendulum.parse(text, exact=True)

    assert isinstance(dt, pendulum.Date)
    assert_date(dt, 2016, 10, 16)

    text = "12:34:56.123456"

    dt = pendulum.parse(text, exact=True)

    assert isinstance(dt, pendulum.Time)
    assert_time(dt, 12, 34, 56, 123456)

    text = "13:00"

    dt = pendulum.parse(text, exact=True)

    assert isinstance(dt, pendulum.Time)
    assert_time(dt, 13, 0, 0)


def test_parse_duration():
    text = "P2Y3M4DT5H6M7S"

    duration = pendulum.parse(text)

    assert isinstance(duration, pendulum.Duration)
    assert_duration(duration, 2, 3, 0, 4, 5, 6, 7)

    text = "P2W"

    duration = pendulum.parse(text)

    assert isinstance(duration, pendulum.Duration)
    assert_duration(duration, 0, 0, 2, 0, 0, 0, 0)


def test_parse_interval():
    text = "2008-05-11T15:30:00Z/P1Y2M10DT2H30M"

    period = pendulum.parse(text)

    assert isinstance(period, pendulum.Interval)
    assert_datetime(period.start, 2008, 5, 11, 15, 30, 0, 0)
    assert period.start.offset == 0
    assert_datetime(period.end, 2009, 7, 21, 18, 0, 0, 0)
    assert period.end.offset == 0

    text = "P1Y2M10DT2H30M/2008-05-11T15:30:00Z"

    period = pendulum.parse(text)

    assert isinstance(period, pendulum.Interval)
    assert_datetime(period.start, 2007, 3, 1, 13, 0, 0, 0)
    assert period.start.offset == 0
    assert_datetime(period.end, 2008, 5, 11, 15, 30, 0, 0)
    assert period.end.offset == 0

    text = "2007-03-01T13:00:00Z/2008-05-11T15:30:00Z"

    period = pendulum.parse(text)

    assert isinstance(period, pendulum.Interval)
    assert_datetime(period.start, 2007, 3, 1, 13, 0, 0, 0)
    assert period.start.offset == 0
    assert_datetime(period.end, 2008, 5, 11, 15, 30, 0, 0)
    assert period.end.offset == 0


def test_parse_now():
    dt = pendulum.parse("now")

    assert dt.timezone_name == "America/Toronto"

    mock_now = pendulum.yesterday()

    with pendulum.travel_to(mock_now, freeze=True):
        assert pendulum.parse("now") == mock_now


def test_parse_with_utc_timezone():
    dt = pendulum.parse("2020-02-05T20:05:37.364951Z")

    assert dt.to_iso8601_string() == "2020-02-05T20:05:37.364951Z"
