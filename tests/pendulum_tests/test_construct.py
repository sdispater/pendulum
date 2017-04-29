# -*- coding: utf-8 -*-

import os
import pytz
from datetime import datetime, timedelta
from dateutil import tz
from pendulum import Pendulum, PRE_TRANSITION, POST_TRANSITION
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

    def test_parse_with_options(self):
        p = Pendulum.parse('2016-04-11T18:21:08.7454873-05:00', day_first=True)

        self.assertPendulum(p, 2016, 11, 4, 18, 21, 8, 745487)
        self.assertEqual('-05:00', p.timezone_name)
        self.assertEqual(p.offset, -18000)

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
        now = Pendulum.instance(
            datetime.now(TimezoneInfo(timezone('Europe/Paris'), 7200, True, timedelta(0, 3600), 'EST'))
        )
        self.assertEqual('Europe/Paris', now.timezone_name)

    def test_instance_timezone_aware_datetime_pytz(self):
        now = Pendulum.instance(
            datetime.now(pytz.timezone('Europe/Paris'))
        )
        self.assertEqual('Europe/Paris', now.timezone_name)

    def test_instance_timezone_aware_datetime_any_tzinfo(self):
        dt = datetime(2016, 8, 7, 12, 34, 56, tzinfo=tz.gettz('Europe/Paris'))
        now = Pendulum.instance(dt)
        self.assertEqual('+02:00', now.timezone_name)

    def test_now(self):
        now = Pendulum.now('America/Toronto')
        in_paris = Pendulum.now('Europe/Paris')

        self.assertNotEqual(now.hour, in_paris.hour)

    def test_now_with_fixed_offset(self):
        now = Pendulum.now(6)

        self.assertEqual(now.timezone_name, '+06:00')

    def test_create(self):
        with self.wrap_with_test_now(Pendulum(2016, 8, 7, 12, 34, 56)):
            now = Pendulum.now()
            d = Pendulum.create()
            self.assertPendulum(d, now.year, now.month, now.day, 0, 0, 0, 0)

            d = Pendulum.create(year=1975)
            self.assertPendulum(d, 1975, now.month, now.day, 0, 0, 0, 0)

            d = Pendulum.create(month=11)
            self.assertPendulum(d, now.year, 11, now.day, 0, 0, 0, 0)

            d = Pendulum.create(day=27)
            self.assertPendulum(d, now.year, now.month, 27, 0, 0, 0, 0)

            d = Pendulum.create(hour=12)
            self.assertPendulum(d, now.year, now.month, now.day, 12, 0, 0, 0)

            d = Pendulum.create(minute=12)
            self.assertPendulum(d, now.year, now.month, now.day, 0, 12, 0, 0)

            d = Pendulum.create(second=12)
            self.assertPendulum(d, now.year, now.month, now.day, 0, 0, 12, 0)

            d = Pendulum.create(microsecond=123456)
            self.assertPendulum(d, now.year, now.month, now.day, 0, 0, 0, 123456)

    def test_create_with_not_transition_timezone(self):
        dt = Pendulum.create(tz='Etc/UTC')

        self.assertEqual('Etc/UTC', dt.timezone_name)

    def test_create_maintains_microseconds(self):
        d = Pendulum.create(2016, 11, 12, 2, 9, 39, 594000, 'America/Panama')
        self.assertPendulum(d, 2016, 11, 12, 2, 9, 39, 594000)

        d = Pendulum.create(2316, 11, 12, 2, 9, 39, 857, 'America/Panama')
        self.assertPendulum(d, 2316, 11, 12, 2, 9, 39, 857)

    def test_init_fold_is_honored_if_explicit(self):
        d = Pendulum(2013, 3, 31, 2, 30, tzinfo='Europe/Paris')
        # Default value of None for Pendulum instances
        # so default rule will be applied
        self.assertPendulum(d, 2013, 3, 31, 3, 30)

        Pendulum.set_transition_rule(PRE_TRANSITION)

        d = Pendulum(2013, 3, 31, 2, 30, tzinfo='Europe/Paris')
        self.assertPendulum(d, 2013, 3, 31, 1, 30)

        Pendulum.set_transition_rule(POST_TRANSITION)

        d = Pendulum(2013, 3, 31, 2, 30, tzinfo='Europe/Paris', fold=0)
        self.assertPendulum(d, 2013, 3, 31, 1, 30)
        self.assertEqual(d.fold, 0)

        d = Pendulum(2013, 3, 31, 2, 30, tzinfo='Europe/Paris', fold=1)
        self.assertPendulum(d, 2013, 3, 31, 3, 30)
        self.assertEqual(d.fold, 1)
