# -*- coding: utf-8 -*-

import os
import pytz
from datetime import datetime
from pendulum import Pendulum
from pendulum.tz import timezone
from pendulum.tz.timezone_info import TimezoneInfo
from .. import AbstractTestCase


class ConstructTest(AbstractTestCase):

    def tearDown(self):
        super(ConstructTest, self).tearDown()

        if os.getenv('TZ'):
            del os.environ['TZ']

    def test_creates_an_instance_default_to_utcnow(self):
        now = Pendulum.utcnow()
        p = Pendulum(now.year, now.month, now.day, now.hour, now.minute, now.second)
        self.assertIsInstanceOfPendulum(p)
        self.assertEqual(p.timezone_name, now.timezone_name)

        self.assertPendulum(p, now.year, now.month, now.day, now.hour, now.minute, now.second)

    def test_parse_creates_an_instance_default_to_utcnow(self):
        p = Pendulum.parse()
        now = Pendulum.utcnow()
        self.assertIsInstanceOfPendulum(p)
        self.assertEqual(p.timezone_name, p.timezone_name)

        self.assertPendulum(p, now.year, now.month, now.day, now.hour, now.minute, now.second)

    def test_parse_with_default_timezone(self):
        p = Pendulum.parse('now')
        self.assertEqual('America/Toronto', p.timezone_name)

    def test_parse_with_offset_in_string(self):
        p = Pendulum.parse('2016-04-15T18:21:08.7454873-05:00')
        self.assertPendulum(p, 2016, 4, 15, 18, 21, 8)
        self.assertEqual('-05:00', p.timezone_name)
        self.assertEqual(-18000, p.offset)

    def test_parse_with_partial_offset_in_string(self):
        p = Pendulum.parse('2016-04-15T18:21:08.7454873-00:30')
        self.assertPendulum(p, 2016, 4, 15, 18, 21, 8)
        self.assertEqual('-00:30', p.timezone_name)
        self.assertEqual(-1800, p.offset)

    def test_setting_timezone(self):
        tz = 'Europe/London'
        dtz = timezone(tz)
        dt = datetime.utcnow()
        offset = dtz.convert(dt).tzinfo.offset / 3600

        p = Pendulum(dt.year, dt.month, dt.day, tzinfo=dtz)
        self.assertEqual(tz, p.timezone_name)
        self.assertEqual(int(offset), p.offset_hours)

    def test_parse_setting_timezone(self):
        tz = 'Europe/London'
        dtz = timezone(tz)
        dt = datetime.utcnow()
        offset = dtz.convert(dt).tzinfo.offset / 3600

        p = Pendulum.parse(tz=dtz)
        self.assertEqual(tz, p.timezone_name)
        self.assertEqual(int(offset), p.offset_hours)

    def test_setting_timezone_with_string(self):
        tz = 'Europe/London'
        dtz = timezone(tz)
        dt = datetime.utcnow()
        offset = dtz.convert(dt).tzinfo.offset / 3600

        p = Pendulum(dt.year, dt.month, dt.day, tzinfo=tz)
        self.assertEqual(tz, p.timezone_name)
        self.assertEqual(int(offset), p.offset_hours)

    def test_parse_setting_timezone_with_string(self):
        tz = 'Europe/London'
        dtz = timezone(tz)
        dt = datetime.utcnow()
        offset = dtz.convert(dt).tzinfo.offset / 3600

        p = Pendulum.parse(tz=tz)
        self.assertEqual(tz, p.timezone_name)
        self.assertEqual(int(offset), p.offset_hours)

    def test_parse_with_invalid_string(self):
        self.assertRaises(ValueError, Pendulum.parse, 'Invalid_string')

    def test_today(self):
        today = Pendulum.today()
        self.assertIsInstanceOfPendulum(today)

    def test_tomorrow(self):
        now = Pendulum.now().start_of('day')
        tomorrow = Pendulum.tomorrow()
        self.assertIsInstanceOfPendulum(tomorrow)
        self.assertEqual(1, now.diff(tomorrow).in_days())

    def test_yesterday(self):
        now = Pendulum.now().start_of('day')
        yesterday = Pendulum.yesterday()
        self.assertIsInstanceOfPendulum(yesterday)
        self.assertEqual(-1, now.diff(yesterday, False).in_days())

    def test_instance_naive_datetime_defaults_to_utc(self):
        now = Pendulum.instance(datetime.now())
        self.assertEqual('UTC', now.timezone_name)

    def test_instance_timezone_aware_datetime(self):
        now = Pendulum.instance(datetime.now(TimezoneInfo.create(timezone('Europe/Paris'), 7200, True, 'EST')))
        self.assertEqual('Europe/Paris', now.timezone_name)

    def test_instance_foreign_tz_aware_datetime(self):
        for tz in ('America/Chicago', 'UTC', 'Australia/Melbourne'):
            from_naive = Pendulum.instance(
                datetime(year=2016, month=1, day=1, hour=0, minute=0, second=0),
                tz
            )

            aware_pytz = pytz.timezone(tz).localize(
                datetime(year=2016, month=1, day=1, hour=0, minute=0, second=0)
            )

            from_aware_pytz = Pendulum.instance(aware_pytz)

            self.assertEqual(from_aware_pytz.isoformat(), from_naive.isoformat())

    def test_now(self):
        now = Pendulum.now()
        in_paris = Pendulum.now('Europe/Paris')

        self.assertNotEqual(now.hour, in_paris.hour)
