from __future__ import annotations

from datetime import datetime

import pytest
import pytz

import pendulum

from pendulum import timezone
from pendulum.helpers import days_in_year
from pendulum.helpers import precise_diff
from pendulum.helpers import week_day


def assert_diff(
    diff, years=0, months=0, days=0, hours=0, minutes=0, seconds=0, microseconds=0
):
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
        years=2,
        months=8,
        days=16,
        hours=20,
        minutes=54,
        seconds=47,
        microseconds=282310,
    )

    dt1 = datetime(2017, 2, 17, 16, 5, 45, 123456)
    dt2 = datetime(2018, 2, 17, 16, 5, 45, 123256)

    diff = precise_diff(dt1, dt2)
    assert_diff(
        diff, months=11, days=30, hours=23, minutes=59, seconds=59, microseconds=999800
    )

    # DST
    tz = timezone("America/Toronto")
    dt1 = tz.datetime(2017, 3, 7)
    dt2 = tz.datetime(2017, 3, 13)

    diff = precise_diff(dt1, dt2)
    assert_diff(diff, days=6, hours=0)


def test_precise_diff_timezone():
    paris = pendulum.timezone("Europe/Paris")
    toronto = pendulum.timezone("America/Toronto")

    dt1 = paris.datetime(2013, 3, 31, 1, 30)
    dt2 = paris.datetime(2013, 4, 1, 1, 30)

    diff = precise_diff(dt1, dt2)
    assert_diff(diff, days=1, hours=0)

    dt2 = toronto.datetime(2013, 4, 1, 1, 30)

    diff = precise_diff(dt1, dt2)
    assert_diff(diff, days=1, hours=5)

    # pytz
    paris = pytz.timezone("Europe/Paris")
    toronto = pytz.timezone("America/Toronto")

    dt1 = paris.localize(datetime(2013, 3, 31, 1, 30))
    dt2 = paris.localize(datetime(2013, 4, 1, 1, 30))

    diff = precise_diff(dt1, dt2)
    assert_diff(diff, days=1, hours=0)

    dt2 = toronto.localize(datetime(2013, 4, 1, 1, 30))

    diff = precise_diff(dt1, dt2)
    assert_diff(diff, days=1, hours=5)

    # Issue238
    dt1 = timezone("UTC").datetime(2018, 6, 20, 1, 30)
    dt2 = timezone("Europe/Paris").datetime(2018, 6, 20, 3, 40)  # UTC+2
    diff = precise_diff(dt1, dt2)
    assert_diff(diff, minutes=10)


def test_week_day():
    assert week_day(2017, 6, 2) == 5
    assert week_day(2017, 1, 1) == 7


def test_days_in_years():
    assert days_in_year(2017) == 365
    assert days_in_year(2016) == 366


def test_locale():
    dt = pendulum.datetime(2000, 11, 10, 12, 34, 56, 123456)
    pendulum.set_locale("fr")

    assert pendulum.get_locale() == "fr"

    assert dt.format("MMMM") == "novembre"
    assert dt.date().format("MMMM") == "novembre"


def test_set_locale_invalid():
    with pytest.raises(ValueError):
        pendulum.set_locale("invalid")


@pytest.mark.parametrize(
    "locale", ["DE", "pt-BR", "pt-br", "PT-br", "PT-BR", "pt_br", "PT_BR", "PT_BR"]
)
def test_set_locale_malformed_locale(locale):
    pendulum.set_locale(locale)

    pendulum.set_locale("en")


def test_week_starts_at():
    pendulum.week_starts_at(pendulum.SATURDAY)

    dt = pendulum.now().start_of("week")
    assert dt.day_of_week == pendulum.SATURDAY
    assert dt.date().day_of_week == pendulum.SATURDAY


def test_week_starts_at_invalid_value():
    with pytest.raises(ValueError):
        pendulum.week_starts_at(-1)

    with pytest.raises(ValueError):
        pendulum.week_starts_at(11)


def test_week_ends_at():
    pendulum.week_ends_at(pendulum.SATURDAY)

    dt = pendulum.now().end_of("week")
    assert dt.day_of_week == pendulum.SATURDAY
    assert dt.date().day_of_week == pendulum.SATURDAY


def test_week_ends_at_invalid_value():
    with pytest.raises(ValueError):
        pendulum.week_ends_at(-1)

    with pytest.raises(ValueError):
        pendulum.week_ends_at(11)
