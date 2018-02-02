from datetime import datetime, timedelta
from pendulum.tz import Timezone
from pendulum.tz.timezone_info import TimezoneInfo, UTC


def test_construct():
    tz = Timezone.load('Europe/Paris')
    tzinfo = TimezoneInfo(tz, 7200, True, timedelta(0, 3600), 'CEST')

    assert tzinfo.offset == 7200
    assert tzinfo.adjusted_offset == timedelta(0, 7200)
    assert tzinfo.is_dst() is True
    assert tzinfo.dst_ == timedelta(0, 3600)
    assert tzinfo.tz == tz
    assert tzinfo.name == 'Europe/Paris'
    assert tzinfo.abbrev == 'CEST'
    assert tzinfo.tzname(None) == 'CEST'


def test_utcoffset():
    tz = Timezone.load('Europe/Paris')
    dt1 = tz.convert(datetime(2016, 7, 1))
    dt2 = tz.convert(datetime(2016, 3, 1))
    tzinfo = TimezoneInfo(tz, 7200, True, timedelta(0, 3600), 'CEST')

    assert tzinfo.utcoffset(dt1) == timedelta(0, 7200)
    assert tzinfo.utcoffset(dt2) == timedelta(0, 3600)
    assert tzinfo.utcoffset(None) is None


def test_dst():
    tz = Timezone.load('Europe/Paris')
    dt1 = tz.convert(datetime(2016, 7, 1))
    dt2 = tz.convert(datetime(2016, 3, 1))
    tzinfo = TimezoneInfo(tz, 7200, True, timedelta(0, 3600), 'CEST')

    assert tzinfo.dst(dt1) == timedelta(0, 3600)
    assert tzinfo.dst(dt2) == timedelta(0, -3600)
    assert tzinfo.dst(None) is None


def test_tzname():
    tz = Timezone.load('Europe/Paris')
    dt1 = tz.convert(datetime(2016, 7, 1))
    dt2 = tz.convert(datetime(2016, 3, 1))
    tzinfo = TimezoneInfo(tz, 7200, True, timedelta(0, 3600), 'CEST')

    assert tzinfo.tzname(dt1) == 'CEST'
    assert tzinfo.tzname(dt2) == 'CET'
    assert tzinfo.tzname(None) == 'CEST'


def test_repr():
    tz = Timezone.load('Europe/Paris')
    tzinfo = TimezoneInfo(tz, 7200, True, timedelta(0, 3600), 'CEST')

    expected = "TimezoneInfo('Europe/Paris', 'CEST', '+02:00:00', 'DST')"
    assert repr(tzinfo) == expected


def test_utc():
    tzinfo = UTC

    assert tzinfo.offset == 0
    assert tzinfo.adjusted_offset == timedelta()
    assert tzinfo.is_dst() is False
    assert tzinfo.dst_ is None
    assert tzinfo.name == 'UTC'
    assert tzinfo.abbrev == 'GMT'
    assert tzinfo.tzname(None) == 'GMT'
