import pendulum
from pendulum import timezone
from pendulum.tz.timezone_info import TimezoneInfo

from ..conftest import assert_datetime


def test_create_from_date_with_defaults():
    d = pendulum.create()
    assert pendulum.utcnow().at(0, 0, 0, 0).timestamp() == d.timestamp()


def test_create_from_date():
    d = pendulum.create(1975, 12, 25)
    assert_datetime(d, 1975, 12, 25, 0, 0, 0)


def test_create_from_date_with_year():
    d = pendulum.create(1975)
    assert 1975 == d.year


def test_create_from_date_with_month():
    d = pendulum.create(month=12)
    assert 12 == d.month


def test_create_from_date_with_day():
    d = pendulum.create(day=25)
    assert 25 == d.day


def test_create_from_date_with_timezone_string():
    d = pendulum.create(1975, 12, 25, tz='Europe/London')
    assert_datetime(d, 1975, 12, 25)
    assert d.timezone_name == 'Europe/London'


def test_create_from_date_with_timezone():
    d = pendulum.create(1975, 12, 25, tz=timezone('Europe/London'))
    assert_datetime(d, 1975, 12, 25)
    assert d.timezone_name == 'Europe/London'


def test_create_from_date_with_tzinfo():
    tz = timezone('Europe/London')
    d = pendulum.create(1975, 12, 25, tz=TimezoneInfo(tz, 3600, True, None, ''))
    assert_datetime(d, 1975, 12, 25)
    assert d.timezone_name == 'Europe/London'
