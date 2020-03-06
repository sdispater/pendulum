import struct

import pendulum
import pytest

from pendulum import DateTime
from pendulum.tz import timezone
from pendulum.utils._compat import _HAS_FOLD

from ..conftest import assert_date
from ..conftest import assert_time


def test_year():
    d = pendulum.datetime(1234, 5, 6, 7, 8, 9)
    assert d.year == 1234


def test_month():
    d = pendulum.datetime(1234, 5, 6, 7, 8, 9)
    assert d.month == 5


def test_day():
    d = pendulum.datetime(1234, 5, 6, 7, 8, 9)
    assert d.day == 6


def test_hour():
    d = pendulum.datetime(1234, 5, 6, 7, 8, 9)
    assert d.hour == 7


def test_minute():
    d = pendulum.datetime(1234, 5, 6, 7, 8, 9)
    assert d.minute == 8


def test_second():
    d = pendulum.datetime(1234, 5, 6, 7, 8, 9)
    assert d.second == 9


def test_microsecond():
    d = pendulum.datetime(1234, 5, 6, 7, 8, 9)
    assert d.microsecond == 0

    d = pendulum.datetime(1234, 5, 6, 7, 8, 9, 101112)
    assert d.microsecond == 101112


def test_tzinfo():
    d = pendulum.now()
    assert d.tzinfo.name == timezone("America/Toronto").name


def test_day_of_week():
    d = pendulum.datetime(2012, 5, 7, 7, 8, 9)
    assert d.day_of_week == pendulum.MONDAY


def test_day_of_year():
    d = pendulum.datetime(2012, 5, 7)
    assert d.day_of_year == 128


def test_days_in_month():
    d = pendulum.datetime(2012, 5, 7)
    assert d.days_in_month == 31


def test_timestamp():
    d = pendulum.datetime(1970, 1, 1, 0, 0, 0)
    assert d.timestamp() == 0
    assert d.add(minutes=1, microseconds=123456).timestamp() == 60.123456


def test_float_timestamp():
    d = pendulum.datetime(1970, 1, 1, 0, 0, 0, 123456)
    assert d.float_timestamp == 0.123456


def test_int_timestamp():
    d = pendulum.datetime(1970, 1, 1, 0, 0, 0)
    assert d.int_timestamp == 0
    assert d.add(minutes=1, microseconds=123456).int_timestamp == 60


@pytest.mark.skipif(
    struct.calcsize("P") * 8 == 32, reason="Test only available for 64bit systems"
)
def test_int_timestamp_accuracy():
    d = pendulum.datetime(3000, 10, 1, 12, 23, 10, 999999)

    assert d.int_timestamp == 32527311790


def test_timestamp_with_transition():
    d_pre = pendulum.datetime(
        2012, 10, 28, 2, 0, tz="Europe/Warsaw", dst_rule=pendulum.PRE_TRANSITION
    )
    d_post = pendulum.datetime(
        2012, 10, 28, 2, 0, tz="Europe/Warsaw", dst_rule=pendulum.POST_TRANSITION
    )

    if _HAS_FOLD:
        # the difference between the timestamps before and after is equal to one hour
        assert d_post.timestamp() - d_pre.timestamp() == pendulum.SECONDS_PER_HOUR
        assert d_post.float_timestamp - d_pre.float_timestamp == (
            pendulum.SECONDS_PER_HOUR
        )
        assert d_post.int_timestamp - d_pre.int_timestamp == pendulum.SECONDS_PER_HOUR
    else:
        # when the transition is not recognizable
        # then the difference should be equal to zero hours
        assert d_post.timestamp() - d_pre.timestamp() == 0
        assert d_post.float_timestamp - d_pre.float_timestamp == 0
        assert d_post.int_timestamp - d_pre.int_timestamp == 0


def test_age():
    d = pendulum.now()
    assert d.age == 0
    assert d.add(years=1).age == -1
    assert d.subtract(years=1).age == 1


def test_local():
    assert pendulum.datetime(2012, 1, 1, tz="America/Toronto").is_local()
    assert pendulum.datetime(2012, 1, 1, tz="America/New_York").is_local()
    assert not pendulum.datetime(2012, 1, 1, tz="UTC").is_local()
    assert not pendulum.datetime(2012, 1, 1, tz="Europe/London").is_local()


def test_utc():
    assert not pendulum.datetime(2012, 1, 1, tz="America/Toronto").is_utc()
    assert not pendulum.datetime(2012, 1, 1, tz="Europe/Paris").is_utc()
    assert pendulum.datetime(2012, 1, 1, tz="UTC").is_utc()
    assert pendulum.datetime(2012, 1, 1, tz=0).is_utc()
    assert not pendulum.datetime(2012, 1, 1, tz=5).is_utc()
    # There is no time difference between Greenwich Mean Time and Coordinated Universal Time
    assert pendulum.datetime(2012, 1, 1, tz="GMT").is_utc()


def test_is_dst():
    assert not pendulum.datetime(2012, 1, 1, tz="America/Toronto").is_dst()
    assert pendulum.datetime(2012, 7, 1, tz="America/Toronto").is_dst()


def test_offset_with_dst():
    assert pendulum.datetime(2012, 1, 1, tz="America/Toronto").offset == -18000


def test_offset_no_dst():
    assert pendulum.datetime(2012, 6, 1, tz="America/Toronto").offset == -14400


def test_offset_for_gmt():
    assert pendulum.datetime(2012, 6, 1, tz="GMT").offset == 0


def test_offset_hours_with_dst():
    assert pendulum.datetime(2012, 1, 1, tz="America/Toronto").offset_hours == -5


def test_offset_hours_no_dst():
    assert pendulum.datetime(2012, 6, 1, tz="America/Toronto").offset_hours == -4


def test_offset_hours_for_gmt():
    assert pendulum.datetime(2012, 6, 1, tz="GMT").offset_hours == 0


def test_offset_hours_float():
    assert pendulum.datetime(2012, 6, 1, tz=9.5).offset_hours == 9.5


def test_is_leap_year():
    assert pendulum.datetime(2012, 1, 1).is_leap_year()
    assert not pendulum.datetime(2011, 1, 1).is_leap_year()


def test_is_long_year():
    assert pendulum.datetime(2015, 1, 1).is_long_year()
    assert not pendulum.datetime(2016, 1, 1).is_long_year()


def test_week_of_month():
    assert pendulum.datetime(2012, 9, 30).week_of_month == 5
    assert pendulum.datetime(2012, 9, 28).week_of_month == 5
    assert pendulum.datetime(2012, 9, 20).week_of_month == 4
    assert pendulum.datetime(2012, 9, 8).week_of_month == 2
    assert pendulum.datetime(2012, 9, 1).week_of_month == 1
    assert pendulum.datetime(2020, 1, 1).week_of_month == 1
    assert pendulum.datetime(2020, 1, 7).week_of_month == 2
    assert pendulum.datetime(2020, 1, 14).week_of_month == 3


def test_week_of_year_first_week():
    assert pendulum.datetime(2012, 1, 1).week_of_year == 52
    assert pendulum.datetime(2012, 1, 2).week_of_year == 1


def test_week_of_year_last_week():
    assert pendulum.datetime(2012, 12, 30).week_of_year == 52
    assert pendulum.datetime(2012, 12, 31).week_of_year == 1


def test_timezone():
    d = pendulum.datetime(2000, 1, 1, tz="America/Toronto")
    assert d.timezone.name == "America/Toronto"

    d = pendulum.datetime(2000, 1, 1, tz=-5)
    assert d.timezone.name == "-05:00"


def test_tz():
    d = pendulum.datetime(2000, 1, 1, tz="America/Toronto")
    assert d.tz.name == "America/Toronto"

    d = pendulum.datetime(2000, 1, 1, tz=-5)
    assert d.tz.name == "-05:00"


def test_timezone_name():
    d = pendulum.datetime(2000, 1, 1, tz="America/Toronto")
    assert d.timezone_name == "America/Toronto"

    d = pendulum.datetime(2000, 1, 1, tz=-5)
    assert d.timezone_name == "-05:00"


def test_is_future():
    with pendulum.test(DateTime(2000, 1, 1)):
        d = pendulum.now()
        assert not d.is_future()
        d = d.add(days=1)
        assert d.is_future()


def test_is_past():
    with pendulum.test(DateTime(2000, 1, 1)):
        d = pendulum.now()
        assert not d.is_past()
        d = d.subtract(days=1)
        assert d.is_past()


def test_date():
    dt = pendulum.datetime(2016, 10, 20, 10, 40, 34, 123456)
    d = dt.date()
    assert isinstance(d, pendulum.Date)
    assert_date(d, 2016, 10, 20)


def test_time():
    dt = pendulum.datetime(2016, 10, 20, 10, 40, 34, 123456)
    t = dt.time()
    assert isinstance(t, pendulum.Time)
    assert_time(t, 10, 40, 34, 123456)
