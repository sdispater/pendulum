# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from pendulum.tz import Timezone
from pendulum.tz.timezone_info import TimezoneInfo, UTC

from .. import AbstractTestCase


class TimezoneInfoTest(AbstractTestCase):

    def test_construct(self):
        tz = Timezone.load('Europe/Paris')
        tzinfo = TimezoneInfo(tz, 7200, True, timedelta(0, 3600), 'CEST')

        self.assertEqual(7200, tzinfo.offset)
        self.assertEqual(timedelta(0, 7200), tzinfo.adjusted_offset)
        self.assertEqual(True, tzinfo.is_dst)
        self.assertEqual(timedelta(0, 3600), tzinfo.dst_)
        self.assertEqual(tz, tzinfo.tz)
        self.assertEqual('Europe/Paris', tzinfo.name)
        self.assertEqual('CEST', tzinfo.abbrev)
        self.assertEqual('CEST', tzinfo.tzname(None))

    def test_utcoffset(self):
        tz = Timezone.load('Europe/Paris')
        dt1 = tz.convert(datetime(2016, 7, 1))
        dt2 = tz.convert(datetime(2016, 3, 1))
        tzinfo = TimezoneInfo(tz, 7200, True, timedelta(0, 3600), 'CEST')

        self.assertEqual(timedelta(0, 7200), tzinfo.utcoffset(dt1))
        self.assertEqual(timedelta(0, 3600), tzinfo.utcoffset(dt2))
        self.assertEqual(None, tzinfo.utcoffset(None))

    def test_dst(self):
        tz = Timezone.load('Europe/Paris')
        dt1 = tz.convert(datetime(2016, 7, 1))
        dt2 = tz.convert(datetime(2016, 3, 1))
        tzinfo = TimezoneInfo(tz, 7200, True, timedelta(0, 3600), 'CEST')

        self.assertEqual(timedelta(0, 3600), tzinfo.dst(dt1))
        self.assertEqual(timedelta(0, -3600), tzinfo.dst(dt2))
        self.assertEqual(None, tzinfo.dst(None))

    def test_tzname(self):
        tz = Timezone.load('Europe/Paris')
        dt1 = tz.convert(datetime(2016, 7, 1))
        dt2 = tz.convert(datetime(2016, 3, 1))
        tzinfo = TimezoneInfo(tz, 7200, True, timedelta(0, 3600), 'CEST')

        self.assertEqual('CEST', tzinfo.tzname(dt1))
        self.assertEqual('CET', tzinfo.tzname(dt2))
        self.assertEqual('CEST', tzinfo.tzname(None))

    def test_repr(self):
        tz = Timezone.load('Europe/Paris')
        tzinfo = TimezoneInfo(tz, 7200, True, timedelta(0, 3600), 'CEST')

        self.assertEqual(
            '<TimezoneInfo [Europe/Paris, CEST, +02:00:00, DST]>',
            repr(tzinfo)
        )

    def test_utc(self):
        tzinfo = UTC

        self.assertEqual(0, tzinfo.offset)
        self.assertEqual(timedelta(), tzinfo.adjusted_offset)
        self.assertEqual(False, tzinfo.is_dst)
        self.assertEqual(None, tzinfo.dst_)
        self.assertEqual('UTC', tzinfo.name)
        self.assertEqual('GMT', tzinfo.abbrev)
        self.assertEqual('GMT', tzinfo.tzname(None))
