# -*- coding: utf-8 -*-

import os
import pytz
from datetime import datetime
from pendulum import Pendulum
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
        self.assertIsNone(p.timezone_name)
        self.assertEqual(-18000, p.offset)

    def test_setting_timezone(self):
        timezone = 'Europe/London'
        dtz = pytz.timezone(timezone)
        dt = datetime.utcnow()
        offset = dtz.utcoffset(dt).total_seconds() / 3600

        p = Pendulum(dt.year, dt.month, dt.day, tzinfo=dtz)
        self.assertEqual(timezone, p.timezone_name)
        self.assertEqual(int(offset), p.offset_hours)

    def test_parse_setting_timezone(self):
        timezone = 'Europe/London'
        dtz = pytz.timezone(timezone)
        dt = datetime.utcnow()
        offset = dtz.utcoffset(dt).total_seconds() / 3600

        p = Pendulum.parse(tz=dtz)
        self.assertEqual(timezone, p.timezone_name)
        self.assertEqual(int(offset), p.offset_hours)

    def test_setting_timezone_with_string(self):
        timezone = 'Europe/London'
        dtz = pytz.timezone(timezone)
        dt = datetime.utcnow()
        offset = dtz.utcoffset(dt).total_seconds() / 3600

        p = Pendulum(dt.year, dt.month, dt.day, tzinfo=timezone)
        self.assertEqual(timezone, p.timezone_name)
        self.assertEqual(int(offset), p.offset_hours)

    def test_parse_setting_timezone_with_string(self):
        timezone = 'Europe/London'
        dtz = pytz.timezone(timezone)
        dt = datetime.utcnow()
        offset = dtz.utcoffset(dt).total_seconds() / 3600

        p = Pendulum.parse(tz=timezone)
        self.assertEqual(timezone, p.timezone_name)
        self.assertEqual(int(offset), p.offset_hours)

    def test_parse_with_invalid_string(self):
        self.assertRaises(ValueError, Pendulum.parse, 'Invalid_string')

    def test_honor_tz_env_variable(self):
        os.environ['TZ'] = 'Europe/Paris'
        with self.wrap_with_test_now():
            now = Pendulum.now()
            self.assertEqual(now.timezone_name, 'Europe/Paris')

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
