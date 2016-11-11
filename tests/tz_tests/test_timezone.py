# -*- coding: utf-8 -*-

import pendulum
from datetime import datetime, timedelta
from pendulum import timezone
from pendulum.tz.exceptions import NonExistingTime, AmbiguousTime

from .. import AbstractTestCase


class TimezoneTest(AbstractTestCase):

    def test_basic_convert(self):
        dt = datetime(2016, 6, 1, 12, 34, 56, 123456)
        tz = timezone('Europe/Paris')
        dt = tz.convert(dt)

        self.assertEqual(2016, dt.year)
        self.assertEqual(6, dt.month)
        self.assertEqual(1, dt.day)
        self.assertEqual(12, dt.hour)
        self.assertEqual(34, dt.minute)
        self.assertEqual(56, dt.second)
        self.assertEqual(123456, dt.microsecond)
        self.assertEqual('Europe/Paris', dt.tzinfo.tz.name)
        self.assertEqual(7200, dt.tzinfo.offset)
        self.assertTrue(dt.tzinfo.is_dst)

    def test_skipped_time(self):
        dt = datetime(2013, 3, 31, 2, 30, 45, 123456)
        tz = timezone('Europe/Paris')
        dt = tz.convert(dt)

        self.assertEqual(2013, dt.year)
        self.assertEqual(3, dt.month)
        self.assertEqual(31, dt.day)
        self.assertEqual(3, dt.hour)
        self.assertEqual(30, dt.minute)
        self.assertEqual(45, dt.second)
        self.assertEqual(123456, dt.microsecond)
        self.assertEqual('Europe/Paris', dt.tzinfo.tz.name)
        self.assertEqual(7200, dt.tzinfo.offset)
        self.assertTrue(dt.tzinfo.is_dst)

    def test_skipped_time_with_pre_rule(self):
        dt = datetime(2013, 3, 31, 2, 30, 45, 123456)
        tz = timezone('Europe/Paris')
        dt = tz.convert(dt, dst_rule=tz.PRE_TRANSITION)

        self.assertEqual(2013, dt.year)
        self.assertEqual(3, dt.month)
        self.assertEqual(31, dt.day)
        self.assertEqual(2, dt.hour)
        self.assertEqual(30, dt.minute)
        self.assertEqual(45, dt.second)
        self.assertEqual(123456, dt.microsecond)
        self.assertEqual('Europe/Paris', dt.tzinfo.tz.name)
        self.assertEqual(3600, dt.tzinfo.offset)
        self.assertFalse(dt.tzinfo.is_dst)

    def test_skipped_time_with_error(self):
        dt = datetime(2013, 3, 31, 2, 30, 45, 123456)
        tz = timezone('Europe/Paris')
        self.assertRaises(NonExistingTime, tz.convert, dt, tz.TRANSITION_ERROR)

    def test_repeated_time(self):
        dt = datetime(2013, 10, 27, 2, 30, 45, 123456)
        tz = timezone('Europe/Paris')
        dt = tz.convert(dt)

        self.assertEqual(2013, dt.year)
        self.assertEqual(10, dt.month)
        self.assertEqual(27, dt.day)
        self.assertEqual(2, dt.hour)
        self.assertEqual(30, dt.minute)
        self.assertEqual(45, dt.second)
        self.assertEqual(123456, dt.microsecond)
        self.assertEqual('Europe/Paris', dt.tzinfo.tz.name)
        self.assertEqual(3600, dt.tzinfo.offset)
        self.assertFalse(dt.tzinfo.is_dst)

    def test_repeated_time_pre_rule(self):
        dt = datetime(2013, 10, 27, 2, 30, 45, 123456)
        tz = timezone('Europe/Paris')
        dt = tz.convert(dt, dst_rule=tz.PRE_TRANSITION)

        self.assertEqual(2013, dt.year)
        self.assertEqual(10, dt.month)
        self.assertEqual(27, dt.day)
        self.assertEqual(2, dt.hour)
        self.assertEqual(30, dt.minute)
        self.assertEqual(45, dt.second)
        self.assertEqual(123456, dt.microsecond)
        self.assertEqual('Europe/Paris', dt.tzinfo.tz.name)
        self.assertEqual(7200, dt.tzinfo.offset)
        self.assertTrue(dt.tzinfo.is_dst)

    def test_repeated_time_with_error(self):
        dt = datetime(2013, 10, 27, 2, 30, 45, 123456)
        tz = timezone('Europe/Paris')
        self.assertRaises(AmbiguousTime, tz.convert, dt, tz.TRANSITION_ERROR)

    def test_pendulum_create_basic(self):
        dt = pendulum.create(2016, 6, 1, 12, 34, 56, 123456, 'Europe/Paris')

        self.assertPendulum(dt, 2016, 6, 1, 12, 34, 56, 123456)
        self.assertEqual('Europe/Paris', dt.timezone_name)
        self.assertEqual(7200, dt.offset)
        self.assertTrue(dt.is_dst)

    def test_pendulum_create_skipped(self):
        dt = pendulum.create(2013, 3, 31, 2, 30, 45, 123456, 'Europe/Paris')

        self.assertPendulum(dt, 2013, 3, 31, 3, 30, 45, 123456)
        self.assertEqual('Europe/Paris', dt.timezone_name)
        self.assertEqual(7200, dt.offset)
        self.assertTrue(dt.is_dst)

    def test_pendulum_create_repeated(self):
        dt = pendulum.create(2013, 10, 27, 2, 30, 45, 123456, 'Europe/Paris')

        self.assertPendulum(dt, 2013, 10, 27, 2, 30, 45, 123456)
        self.assertEqual('Europe/Paris', dt.timezone_name)
        self.assertEqual(3600, dt.offset)
        self.assertFalse(dt.is_dst)

    def test_convert_accept_pendulum_instance(self):
        dt = pendulum.create(2016, 8, 7, 12, 53, 54)
        tz = timezone('Europe/Paris')
        new = tz.convert(dt)

        self.assertIsInstanceOfPendulum(new)
        self.assertPendulum(new, 2016, 8, 7, 14, 53, 54)

    def test_create_uses_transition_rule(self):
        pendulum.set_transition_rule(pendulum.PRE_TRANSITION)
        dt = pendulum.create(2013, 3, 31, 2, 30, 45, 123456, 'Europe/Paris')

        self.assertEqual(2013, dt.year)
        self.assertEqual(3, dt.month)
        self.assertEqual(31, dt.day)
        self.assertEqual(2, dt.hour)
        self.assertEqual(30, dt.minute)
        self.assertEqual(45, dt.second)
        self.assertEqual(123456, dt.microsecond)
        self.assertEqual('Europe/Paris', dt.timezone_name)
        self.assertEqual(3600, dt.offset)
        self.assertFalse(dt.is_dst)

    def test_utcoffset(self):
        tz = pendulum.timezone('Europe/Paris')
        utcoffset = tz.utcoffset(pendulum.utcnow())
        self.assertEqual(utcoffset, timedelta(0, 3600))

    def test_dst(self):
        tz = pendulum.timezone('Europe/Amsterdam')
        dst = tz.dst(pendulum.create(1940, 7, 1))

        self.assertEqual(timedelta(0, 6000), dst)

    def test_short_timezones(self):
        tz = pendulum.timezone('CET')
        self.assertTrue(len(tz.transitions) > 0)

        tz = pendulum.timezone('EET')
        self.assertTrue(len(tz.transitions) > 0)
