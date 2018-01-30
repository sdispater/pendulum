import os
import pytz

import pendulum
import pytest

from datetime import datetime, timedelta
from dateutil import tz
from pendulum import DateTime
from pendulum.tz import timezone
from pendulum.tz.timezone_info import TimezoneInfo

from ..conftest import assert_datetime


@pytest.fixture(autouse=True)
def setup():
    yield
    
    if os.getenv('TZ'):
        del os.environ['TZ']


def test_creates_an_instance_default_to_utcnow():
    now = pendulum.now('UTC')
    p = pendulum.create(
        now.year, now.month, now.day,
        now.hour, now.minute, now.second
    )
    assert now.timezone_name == p.timezone_name

    assert_datetime(p, now.year, now.month, now.day, now.hour, now.minute, now.second)


def test_setting_timezone():
    tz = 'Europe/London'
    dtz = timezone(tz)
    dt = datetime.utcnow()
    offset = dtz.convert(dt).tzinfo.offset / 3600

    p = pendulum.create(dt.year, dt.month, dt.day, tz=dtz)
    assert p.timezone_name == tz
    assert p.offset_hours == int(offset)


def test_setting_timezone_with_string():
    tz = 'Europe/London'
    dtz = timezone(tz)
    dt = datetime.utcnow()
    offset = dtz.convert(dt).tzinfo.offset / 3600

    p = pendulum.create(dt.year, dt.month, dt.day, tz=tz)
    assert p.timezone_name == tz
    assert p.offset_hours == int(offset)


def test_today():
    today = DateTime.today()
    assert isinstance(today, DateTime)


def test_tomorrow():
    now = pendulum.now().start_of('day')
    tomorrow = pendulum.tomorrow()
    assert isinstance(tomorrow, DateTime)
    assert now.diff(tomorrow).in_days() == 1


def test_yesterday():
    now = pendulum.now().start_of('day')
    yesterday = pendulum.yesterday()

    assert isinstance(yesterday, DateTime)
    assert now.diff(yesterday, False).in_days() == -1


def test_instance_naive_datetime_defaults_to_utc():
    now = pendulum.instance(datetime.now())
    assert now.timezone_name == 'UTC'


def test_instance_timezone_aware_datetime():
    now = pendulum.instance(
        datetime.now(TimezoneInfo(timezone('Europe/Paris'), 7200, True, timedelta(0, 3600), 'EST'))
    )
    assert now.timezone_name == 'Europe/Paris'


def test_instance_timezone_aware_datetime_pytz():
    now = pendulum.instance(
        datetime.now(pytz.timezone('Europe/Paris'))
    )
    assert now.timezone_name == 'Europe/Paris'


def test_instance_timezone_aware_datetime_any_tzinfo():
    dt = datetime(2016, 8, 7, 12, 34, 56, tzinfo=tz.gettz('Europe/Paris'))
    now = pendulum.instance(dt)
    assert now.timezone_name == '+02:00'


def test_now():
    now = pendulum.now('America/Toronto')
    in_paris = pendulum.now('Europe/Paris')

    assert now.hour != in_paris.hour


def test_now_with_fixed_offset():
    now = pendulum.now(6)

    assert '+06:00' == now.timezone_name


def test_create():
    with pendulum.test(DateTime(2016, 8, 7, 12, 34, 56)):
        now = pendulum.now()
        d = pendulum.create()
        assert_datetime(d, now.year, now.month, now.day, 0, 0, 0, 0)

        d = pendulum.create(year=1975)
        assert_datetime(d, 1975, now.month, now.day, 0, 0, 0, 0)

        d = pendulum.create(month=11)
        assert_datetime(d, now.year, 11, now.day, 0, 0, 0, 0)

        d = pendulum.create(day=27)
        assert_datetime(d, now.year, now.month, 27, 0, 0, 0, 0)

        d = pendulum.create(hour=12)
        assert_datetime(d, now.year, now.month, now.day, 12, 0, 0, 0)

        d = pendulum.create(minute=12)
        assert_datetime(d, now.year, now.month, now.day, 0, 12, 0, 0)

        d = pendulum.create(second=12)
        assert_datetime(d, now.year, now.month, now.day, 0, 0, 12, 0)

        d = pendulum.create(microsecond=123456)
        assert_datetime(d, now.year, now.month, now.day, 0, 0, 0, 123456)


def test_create_with_not_transition_timezone():
    dt = pendulum.create(tz='Etc/UTC')

    assert dt.timezone_name == 'Etc/UTC'


def test_create_maintains_microseconds():
    d = pendulum.create(2016, 11, 12, 2, 9, 39, 594000, 'America/Panama')
    assert_datetime(d, 2016, 11, 12, 2, 9, 39, 594000)

    d = pendulum.create(2316, 11, 12, 2, 9, 39, 857, 'America/Panama')
    assert_datetime(d, 2316, 11, 12, 2, 9, 39, 857)


def test_second_inaccuracy_on_past_datetimes():
    dt = pendulum.create(1901, 12, 13, 0, 0, 0, 555555, tz='US/Central')

    assert_datetime(dt, 1901, 12, 13, 0, 0, 0, 555555)
