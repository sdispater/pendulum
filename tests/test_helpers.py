import pytest
import pendulum

from datetime import datetime
from pendulum.helpers import precise_diff, week_day, days_in_year
from pendulum.tz.timezone import Timezone

from .conftest import assert_datetime, assert_date, assert_time


def assert_diff(diff,
                years=0, months=0, days=0,
                hours=0, minutes=0, seconds=0, microseconds=0):
    assert diff.years == years
    assert diff.months == months
    assert diff.days == days
    assert diff.hours == hours
    assert diff.minutes == minutes
    assert diff.seconds == seconds
    assert diff.microseconds == microseconds


def test_precise_diff():
    dt1 = datetime(2003, 3, 1, 0, 0, 0)
    dt2 = datetime(2003, 1, 31, 23, 59, 59)

    diff = precise_diff(dt1, dt2)
    assert_diff(diff, months=-1, seconds=-1)

    diff = precise_diff(dt2, dt1)
    assert_diff(diff, months=1, seconds=1)

    dt1 = datetime(2012, 3, 1, 0, 0, 0)
    dt2 = datetime(2012, 1, 31, 23, 59, 59)

    diff = precise_diff(dt1, dt2)
    assert_diff(diff, months=-1, seconds=-1)

    diff = precise_diff(dt2, dt1)
    assert_diff(diff, months=1, seconds=1)

    dt1 = datetime(2001, 1, 1)
    dt2 = datetime(2003, 9, 17, 20, 54, 47, 282310)

    diff = precise_diff(dt1, dt2)
    assert_diff(
        diff,
        years=2, months=8, days=16,
        hours=20, minutes=54, seconds=47, microseconds=282310
    )

    dt1 = datetime(2017, 2, 17, 16, 5, 45, 123456)
    dt2 = datetime(2018, 2, 17, 16, 5, 45, 123256)

    diff = precise_diff(dt1, dt2)
    assert_diff(
        diff,
        months=11, days=30, hours=23, minutes=59, seconds=59, microseconds=999800
    )

    # DST
    tz = Timezone.load('America/Toronto')
    dt1 = tz.datetime(2017, 3, 7)
    dt2 = tz.datetime(2017, 3, 13)

    diff = precise_diff(dt1, dt2)
    assert_diff(
        diff,
        days=5, hours=23
    )


def test_week_day():
    assert 5 == week_day(2017, 6, 2)
    assert 7 == week_day(2017, 1, 1)


def test_days_in_years():
    assert 365 == days_in_year(2017)
    assert 366 == days_in_year(2016)


def test_test_now():
    now = pendulum.create(2000, 11, 10, 12, 34, 56, 123456)
    pendulum.set_test_now(now)

    assert pendulum.has_test_now()
    assert now == pendulum.get_test_now()
    assert now.date() == pendulum.date.today()
    assert now.time() == pendulum.time.now()

    assert_datetime(
        pendulum.datetime.now(),
        2000, 11, 10, 12, 34, 56, 123456
    )
    assert_date(
        pendulum.date.today(),
        2000, 11, 10
    )
    assert_time(
        pendulum.time.now(),
        12, 34, 56, 123456
    )

    pendulum.set_test_now()

    assert not pendulum.has_test_now()
    assert pendulum.get_test_now() is None


def test_formatter():
    dt = pendulum.create(2000, 11, 10, 12, 34, 56, 123456)
    pendulum.set_formatter('alternative')

    assert pendulum.get_formatter() is pendulum.FORMATTERS['alternative']

    assert (
        dt.format('YYYY-MM-DD HH:mm:ss.SSSSSSZZ')
        ==
        '2000-11-10 12:34:56.123456+00:00'
    )
    assert (
        dt.date().format('YYYY-MM-DD')
        ==
        '2000-11-10'
    )
    assert(
        dt.time().format('HH:mm:ss.SSSSSS')
        ==
        '12:34:56.123456'
    )

    pendulum.set_formatter()

    assert pendulum.get_formatter() is pendulum.FORMATTERS['classic']

    assert (
        dt.format('YYYY-MM-DD HH:mm:ss.SSSSSSZZ')
        ==
        'YYYY-MM-DD HH:mm:ss.SSSSSSZZ'
    )
    assert (
        dt.date().format('YYYY-MM-DD')
        ==
        'YYYY-MM-DD'
    )
    assert (
        dt.time().format('HH:mm:ss.SSSSSS')
        ==
        'HH:mm:ss.SSSSSS'
    )


def test_set_formatter_invalid():
    with pytest.raises(ValueError):
        pendulum.set_formatter('invalid')

def test_locale():
    dt = pendulum.create(2000, 11, 10, 12, 34, 56, 123456)
    pendulum.set_formatter('alternative')
    pendulum.set_locale('fr')

    assert pendulum.get_locale() == 'fr'

    assert dt.format('MMMM') == 'novembre'
    assert dt.date().format('MMMM') == 'novembre'


def test_set_locale_invalid():
    with pytest.raises(ValueError):
        pendulum.set_locale('invalid')

@pytest.mark.parametrize('locale', [
    'DE',
    'pt-BR',
    'pt-br',
    'PT-br',
    'PT-BR',
    'pt_br',
    'PT_BR',
    'PT_BR'
])
def test_set_locale_malformed_locale(locale):
    pendulum.set_locale(locale)

    pendulum.set_locale('en')
