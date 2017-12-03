import pytest
from datetime import datetime, timedelta

import pendulum
from pendulum import timezone
from pendulum.tz import Timezone, FixedTimezone
from pendulum.tz.exceptions import NonExistingTime, AmbiguousTime

from ..conftest import assert_datetime


def test_basic_convert():
    dt = datetime(2016, 6, 1, 12, 34, 56, 123456, fold=1)
    tz = timezone('Europe/Paris')
    dt = tz.convert(dt)

    assert dt.year == 2016
    assert dt.month == 6
    assert dt.day == 1
    assert dt.hour == 12
    assert dt.minute == 34
    assert dt.second == 56
    assert dt.microsecond == 123456
    assert dt.tzinfo.tz.name == 'Europe/Paris'
    assert dt.tzinfo.offset == 7200
    assert dt.tzinfo.is_dst()


def test_skipped_time_with_pre_rule():
    dt = datetime(2013, 3, 31, 2, 30, 45, 123456, fold=0)
    tz = timezone('Europe/Paris')
    dt = tz.convert(dt)

    assert dt.year == 2013
    assert dt.month == 3
    assert dt.day == 31
    assert dt.hour == 1
    assert dt.minute == 30
    assert dt.second == 45
    assert dt.microsecond == 123456
    assert dt.tzinfo.tz.name == 'Europe/Paris'
    assert dt.tzinfo.offset == 3600
    assert not dt.tzinfo.is_dst()


def test_skipped_time_with_error():
    dt = datetime(2013, 3, 31, 2, 30, 45, 123456)
    tz = timezone('Europe/Paris')
    with pytest.raises(NonExistingTime):
        tz.convert(dt, with_errors=True)


def test_repeated_time():
    dt = datetime(2013, 10, 27, 2, 30, 45, 123456, fold=1)
    tz = timezone('Europe/Paris')
    dt = tz.convert(dt)

    assert dt.year == 2013
    assert dt.month == 10
    assert dt.day == 27
    assert dt.hour == 2
    assert dt.minute == 30
    assert dt.second == 45
    assert dt.microsecond == 123456
    assert dt.tzinfo.tz.name == 'Europe/Paris'
    assert dt.tzinfo.offset == 3600
    assert not dt.tzinfo.is_dst()


def test_repeated_time_pre_rule():
    dt = datetime(2013, 10, 27, 2, 30, 45, 123456, fold=0)
    tz = timezone('Europe/Paris')
    dt = tz.convert(dt)

    assert dt.year == 2013
    assert dt.month == 10
    assert dt.day == 27
    assert dt.hour == 2
    assert dt.minute == 30
    assert dt.second == 45
    assert dt.microsecond == 123456
    assert dt.tzinfo.tz.name == 'Europe/Paris'
    assert dt.tzinfo.offset == 7200
    assert dt.tzinfo.is_dst()


def test_repeated_time_with_error():
    dt = datetime(2013, 10, 27, 2, 30, 45, 123456)
    tz = timezone('Europe/Paris')
    with pytest.raises(AmbiguousTime):
        tz.convert(dt, with_errors=True)


def test_pendulum_create_basic():
    dt = pendulum.create(2016, 6, 1, 12, 34, 56, 123456, tz='Europe/Paris')

    assert_datetime(dt, 2016, 6, 1, 12, 34, 56, 123456)
    assert dt.timezone_name == 'Europe/Paris'
    assert dt.offset == 7200
    assert dt.is_dst()


def test_pendulum_create_skipped():
    dt = pendulum.create(2013, 3, 31, 2, 30, 45, 123456, tz='Europe/Paris')

    assert_datetime(dt, 2013, 3, 31, 3, 30, 45, 123456)
    assert dt.timezone_name == 'Europe/Paris'
    assert dt.offset == 7200
    assert dt.is_dst()


def test_pendulum_create_repeated():
    dt = pendulum.create(2013, 10, 27, 2, 30, 45, 123456, tz='Europe/Paris')

    assert_datetime(dt, 2013, 10, 27, 2, 30, 45, 123456)
    assert dt.timezone_name == 'Europe/Paris'
    assert dt.offset == 3600
    assert not dt.is_dst()


def test_convert_accept_pendulum_instance():
    dt = pendulum.create(2016, 8, 7, 12, 53, 54)
    tz = timezone('Europe/Paris')
    new = tz.convert(dt)

    assert isinstance(new, pendulum.datetime)
    assert_datetime(new, 2016, 8, 7, 14, 53, 54)


def test_utcoffset():
    tz = pendulum.timezone('America/Guayaquil')
    utcoffset = tz.utcoffset(pendulum.utcnow())
    assert utcoffset == timedelta(0, -18000)


def test_dst():
    tz = pendulum.timezone('Europe/Amsterdam')
    dst = tz.dst(pendulum.create(1940, 7, 1))

    assert dst == timedelta(0, 6000)


def test_short_timezones():
    tz = pendulum.timezone('CET')
    assert len(tz.transitions) > 0

    tz = pendulum.timezone('EET')
    assert len(tz.transitions) > 0


def test_short_timezones_should_not_modify_time():
    tz = pendulum.timezone('EST')
    dt = tz.datetime(2017, 6, 15, 14, 0, 0)

    assert dt.year == 2017
    assert dt.month == 6
    assert dt.day == 15
    assert dt.hour == 14
    assert dt.minute == 0
    assert dt.second == 0

    tz = pendulum.timezone('HST')
    dt = tz.datetime(2017, 6, 15, 14, 0, 0)

    assert dt.year == 2017
    assert dt.month == 6
    assert dt.day == 15
    assert dt.hour == 14
    assert dt.minute == 0
    assert dt.second == 0


def test_after_last_transition():
    tz = pendulum.timezone('Europe/Paris')
    dt = tz.datetime(2135, 6, 15, 14, 0, 0)

    assert dt.year == 2135
    assert dt.month == 6
    assert dt.day == 15
    assert dt.hour == 14
    assert dt.minute == 0
    assert dt.second == 0
    assert dt.microsecond == 0


def test_on_last_transition():
    tz = pendulum.timezone('Europe/Paris')
    dt = datetime(2037, 10, 25, 3, 0, 0, fold=1)
    dt = tz.convert(dt)

    assert dt.year == 2037
    assert dt.month == 10
    assert dt.day == 25
    assert dt.hour == 3
    assert dt.minute == 0
    assert dt.second == 0
    assert dt.microsecond == 0
    assert dt.utcoffset().total_seconds() == 3600

    dt = datetime(2037, 10, 25, 3, 0, 0, fold=0)
    dt = tz.convert(dt)

    assert dt.year == 2037
    assert dt.month == 10
    assert dt.day == 25
    assert dt.hour == 3
    assert dt.minute == 0
    assert dt.second == 0
    assert dt.microsecond == 0
    assert dt.utcoffset().total_seconds() == 7200


def test_convert_fold_attribute_is_honored():
    tz = pendulum.timezone('US/Eastern')
    dt = datetime(2014, 11, 2, 1, 30)

    new = tz.convert(dt)
    assert new.strftime('%z') == '-0400'

    new = tz.convert(dt.replace(fold=1))
    assert new.strftime('%z') == '-0500'


def test_utcoffset_fold_attribute_is_honored():
    tz = pendulum.timezone('US/Eastern')
    dt = datetime(2014, 11, 2, 1, 30)

    offset = tz.utcoffset(dt)

    assert offset.total_seconds() == -4 * 3600

    offset = tz.utcoffset(dt.replace(fold=1))

    assert offset.total_seconds() == -5 * 3600


def test_dst_fold_attribute_is_honored():
    tz = pendulum.timezone('US/Eastern')
    dt = datetime(2014, 11, 2, 1, 30)

    offset = tz.dst(dt)

    assert offset.total_seconds() == 3600

    offset = tz.dst(dt.replace(fold=1))

    assert offset.total_seconds() == -3600


def test_tzname_fold_attribute_is_honored():
    tz = pendulum.timezone('US/Eastern')
    dt = datetime(2014, 11, 2, 1, 30)

    name = tz.tzname(dt)

    assert name == 'EDT'

    name = tz.tzname(dt.replace(fold=1))

    assert name == 'EST'


def test_constructor_fold_attribute_is_honored():
    tz = pendulum.timezone('US/Eastern')
    dt = datetime(2014, 11, 2, 1, 30, tzinfo=tz)

    assert dt.strftime('%z') == '-0400'

    dt = datetime(2014, 11, 2, 1, 30, tzinfo=tz, fold=1)

    assert dt.strftime('%z') == '-0500'


def test_timezone_with_no_transitions():
    tz = Timezone('Test', (), ((0, False, None, ''),), 0, [])

    dt = datetime(2016, 11, 26)
    dt = tz.convert(dt)

    assert 2016 == dt.year
    assert 11 == dt.month
    assert 26 == dt.day
    assert 0 == dt.hour
    assert 0 == dt.minute
    assert 0 == dt.second


def test_datetime():
    tz = timezone('Europe/Paris')

    dt = tz.datetime(2013, 3, 24, 1, 30)
    assert dt.year == 2013
    assert dt.month == 3
    assert dt.day == 24
    assert dt.hour == 1
    assert dt.minute == 30
    assert dt.second == 0
    assert dt.microsecond == 0

    dt = tz.datetime(2013, 3, 31, 2, 30)
    assert dt.year == 2013
    assert dt.month == 3
    assert dt.day == 31
    assert dt.hour == 3
    assert dt.minute == 30
    assert dt.second == 0
    assert dt.microsecond == 0


def test_fixed_timezone():
    tz = FixedTimezone.load(19800)
    tz2 = FixedTimezone.load(18000)
    dt = datetime(2016, 11, 26, tzinfo=tz)

    assert 18000 == tz2.utcoffset(dt).total_seconds()
    assert tz2.dst(dt) is None


def test_repr():
    tz = timezone('Europe/Paris')

    assert "Timezone('Europe/Paris')" == repr(tz)
