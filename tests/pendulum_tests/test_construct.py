# -*- coding: utf-8 -*-

import pytz
from datetime import datetime
from pendulum import Pendulum
from .. import AbstractTestCase


class ConstructTest(AbstractTestCase):

    def test_creates_an_instance_default_to_utcnow(self):
        p = Pendulum()
        now = Pendulum.utcnow()
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

    def test_setting_timezone(self):
        timezone = 'Europe/London'
        dtz = pytz.timezone(timezone)
        dt = datetime.utcnow()
        offset = dtz.utcoffset(dt).total_seconds() / 3600

        p = Pendulum(tzinfo=dtz)
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

        p = Pendulum(tzinfo=timezone)
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

