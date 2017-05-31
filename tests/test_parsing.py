import pendulum

from .conftest import (
    assert_datetime, assert_date, assert_time,
    assert_duration
)


def test_parse():
    text = '2016-10-16T12:34:56.123456+01:30'

    dt = pendulum.parse(text)

    assert isinstance(dt, pendulum.datetime)
    assert_datetime(dt, 2016, 10, 16, 12, 34, 56, 123456)
    assert 5400 == dt.offset

    text = '2016-10-16'

    dt = pendulum.parse(text)

    assert isinstance(dt, pendulum.datetime)
    assert_datetime(dt, 2016, 10, 16, 0, 0, 0, 0)
    assert 0 == dt.offset

    with pendulum.test(pendulum.create(2015, 11, 12)):
        text = '12:34:56.123456'

        dt = pendulum.parse(text)

    assert isinstance(dt, pendulum.datetime)
    assert_datetime(dt, 2015, 11, 12, 12, 34, 56, 123456)
    assert 0 == dt.offset


def test_parse_exact():
    text = '2016-10-16T12:34:56.123456+01:30'

    dt = pendulum.parse(text, exact=True)

    assert isinstance(dt, pendulum.datetime)
    assert_datetime(dt, 2016, 10, 16, 12, 34, 56, 123456)
    assert 5400 == dt.offset

    text = '2016-10-16'

    dt = pendulum.parse(text, exact=True)

    assert isinstance(dt, pendulum.date)
    assert_date(dt, 2016, 10, 16)

    text = '12:34:56.123456'

    dt = pendulum.parse(text, exact=True)

    assert isinstance(dt, pendulum.time)
    assert_time(dt, 12, 34, 56, 123456)


def test_parse_duration():
    text = 'P2Y3M4DT5H6M7S'

    duration = pendulum.parse(text)

    assert isinstance(duration, pendulum.duration)
    assert_duration(duration, 2, 3, 0, 4, 5, 6, 7)
