import pendulum

from pendulum import timezone

from ..conftest import assert_datetime


def test_create_from_time_with_defaults():
    d = pendulum.create()
    assert pendulum.now('UTC').at(0, 0, 0, 0).timestamp() == d.timestamp()
    assert d.timezone_name == 'UTC'


def test_create_from_time():
    d = pendulum.create(hour=23, minute=5, second=11)
    now = pendulum.now('UTC')
    assert_datetime(d, now.year, now.month, now.day, 23, 5, 11)
    assert d.timezone_name == 'UTC'


def test_create_from_time_with_hour():
    with pendulum.test(pendulum.datetime(2016, 8, 11, 12, 34, 56, 123456)):
        d = pendulum.create(hour=23)
        assert d.hour == 23
        assert d.minute == 0
        assert d.second == 0
        assert d.microsecond == 0


def test_create_from_time_with_minute():
    d = pendulum.create(minute=5)
    assert d.minute == 5


def test_create_from_time_with_second():
    d = pendulum.create(second=11)
    assert d.second == 11


def test_create_from_time_with_timezone_string():
    d = pendulum.create(hour=23, minute=5, second=11, tz='Europe/London')
    now = pendulum.now('Europe/London')
    assert_datetime(d, now.year, now.month, now.day, 23, 5, 11)
    assert d.timezone_name == 'Europe/London'


def test_create_from_time_with_timezone():
    d = pendulum.create(hour=23, minute=5, second=11, tz=timezone('Europe/London'))
    now = pendulum.now('Europe/London')
    assert_datetime(d, now.year, now.month, now.day, 23, 5, 11)
    assert d.timezone_name == 'Europe/London'
