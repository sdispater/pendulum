# -*- coding: utf-8 -*-

import pendulum
from datetime import datetime
from pendulum import timezone

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

    def test_add_time_to_new_transition_skipped(self):
        dt = pendulum.create(2013, 3, 31, 1, 59, 59, 999999, 'Europe/Paris')

        self.assertPendulum(dt, 2013, 3, 31, 1, 59, 59, 999999)
        self.assertEqual('Europe/Paris', dt.timezone_name)
        self.assertEqual(3600, dt.offset)
        self.assertFalse(dt.is_dst)

        dt = dt.add(microseconds=1)

        self.assertPendulum(dt, 2013, 3, 31, 3, 0, 0, 0)
        self.assertEqual('Europe/Paris', dt.timezone_name)
        self.assertEqual(7200, dt.offset)
        self.assertTrue(dt.is_dst)

        dt = pendulum.create(2013, 3, 10, 1, 59, 59, 999999, 'America/New_York')

        self.assertPendulum(dt, 2013, 3, 10, 1, 59, 59, 999999)
        self.assertEqual('America/New_York', dt.timezone_name)
        self.assertEqual(-5 * 3600, dt.offset)
        self.assertFalse(dt.is_dst)

        dt = dt.add(microseconds=1)

        self.assertPendulum(dt, 2013, 3, 10, 3, 0, 0, 0)
        self.assertEqual('America/New_York', dt.timezone_name)
        self.assertEqual(- 4 * 3600, dt.offset)
        self.assertTrue(dt.is_dst)

        dt = pendulum.create(1957, 4, 28, 1, 59, 59, 999999, 'America/New_York')

        self.assertPendulum(dt, 1957, 4, 28, 1, 59, 59, 999999)
        self.assertEqual('America/New_York', dt.timezone_name)
        self.assertEqual(-5 * 3600, dt.offset)
        self.assertFalse(dt.is_dst)

        dt = dt.add(microseconds=1)

        self.assertPendulum(dt, 1957, 4, 28, 3, 0, 0, 0)
        self.assertEqual('America/New_York', dt.timezone_name)
        self.assertEqual(- 4 * 3600, dt.offset)
        self.assertTrue(dt.is_dst)

    def test_add_time_to_new_transition_repeated(self):
        dt = pendulum.create(2013, 10, 27, 1, 59, 59, 999999, 'Europe/Paris')
        dt = dt.add(hours=1)

        self.assertPendulum(dt, 2013, 10, 27, 2, 59, 59, 999999)
        self.assertEqual('Europe/Paris', dt.timezone_name)
        self.assertEqual(7200, dt.offset)
        self.assertTrue(dt.is_dst)

        dt = dt.add(microseconds=1)

        self.assertPendulum(dt, 2013, 10, 27, 2, 0, 0, 0)
        self.assertEqual('Europe/Paris', dt.timezone_name)
        self.assertEqual(3600, dt.offset)
        self.assertFalse(dt.is_dst)


        dt = pendulum.create(2013, 11, 3, 0, 59, 59, 999999, 'America/New_York')
        dt = dt.add(hours=1)

        self.assertPendulum(dt, 2013, 11, 3, 1, 59, 59, 999999)
        self.assertEqual('America/New_York', dt.timezone_name)
        self.assertEqual(-4 * 3600, dt.offset)
        self.assertTrue(dt.is_dst)

        dt = dt.add(microseconds=1)

        self.assertPendulum(dt, 2013, 11, 3, 1, 0, 0, 0)
        self.assertEqual('America/New_York', dt.timezone_name)
        self.assertEqual(-5 * 3600, dt.offset)
        self.assertFalse(dt.is_dst)

    def test_subtract_time_to_new_transition_skipped(self):
        dt = pendulum.create(2013, 3, 31, 3, 0, 0, 0, 'Europe/Paris')

        self.assertPendulum(dt, 2013, 3, 31, 3, 0, 0, 0)
        self.assertEqual('Europe/Paris', dt.timezone_name)
        self.assertEqual(7200, dt.offset)
        self.assertTrue(dt.is_dst)

        dt = dt.subtract(microseconds=1)

        self.assertPendulum(dt, 2013, 3, 31, 1, 59, 59, 999999)
        self.assertEqual('Europe/Paris', dt.timezone_name)
        self.assertEqual(3600, dt.offset)
        self.assertFalse(dt.is_dst)

        dt = pendulum.create(2013, 3, 10, 3, 0, 0, 0, 'America/New_York')

        self.assertPendulum(dt, 2013, 3, 10, 3, 0, 0, 0)
        self.assertEqual('America/New_York', dt.timezone_name)
        self.assertEqual(-4 * 3600, dt.offset)
        self.assertTrue(dt.is_dst)

        dt = dt.subtract(microseconds=1)

        self.assertPendulum(dt, 2013, 3, 10, 1, 59, 59, 999999)
        self.assertEqual('America/New_York', dt.timezone_name)
        self.assertEqual(-5 * 3600, dt.offset)
        self.assertFalse(dt.is_dst)

        dt = pendulum.create(1957, 4, 28, 3, 0, 0, 0, 'America/New_York')

        self.assertPendulum(dt, 1957, 4, 28, 3, 0, 0, 0)
        self.assertEqual('America/New_York', dt.timezone_name)
        self.assertEqual(-4 * 3600, dt.offset)
        self.assertTrue(dt.is_dst)

        dt = dt.subtract(microseconds=1)

        self.assertPendulum(dt, 1957, 4, 28, 1, 59, 59, 999999)
        self.assertEqual('America/New_York', dt.timezone_name)
        self.assertEqual(-5 * 3600, dt.offset)
        self.assertFalse(dt.is_dst)

    def test_subtract_time_to_new_transition_repeated(self):
        dt = pendulum.create(2013, 10, 27, 2, 0, 0, 0, 'Europe/Paris')

        self.assertPendulum(dt, 2013, 10, 27, 2, 0, 0, 0)
        self.assertEqual('Europe/Paris', dt.timezone_name)
        self.assertEqual(3600, dt.offset)
        self.assertFalse(dt.is_dst)

        dt = dt.subtract(microseconds=1)

        self.assertPendulum(dt, 2013, 10, 27, 2, 59, 59, 999999)
        self.assertEqual('Europe/Paris', dt.timezone_name)
        self.assertEqual(7200, dt.offset)
        self.assertTrue(dt.is_dst)

        dt = pendulum.create(2013, 11, 3, 1, 0, 0, 0, 'America/New_York')

        self.assertPendulum(dt, 2013, 11, 3, 1, 0, 0, 0)
        self.assertEqual('America/New_York', dt.timezone_name)
        self.assertEqual(-5 * 3600, dt.offset)
        self.assertFalse(dt.is_dst)

        dt = dt.subtract(microseconds=1)

        self.assertPendulum(dt, 2013, 11, 3, 1, 59, 59, 999999)
        self.assertEqual('America/New_York', dt.timezone_name)
        self.assertEqual(-4 * 3600, dt.offset)
        self.assertTrue(dt.is_dst)

    def test_convert_accept_pendulum_instance(self):
        dt = pendulum.create(2016, 8, 7, 12, 53, 54)
        tz = timezone('Europe/Paris')
        new = tz.convert(dt)

        self.assertIsInstanceOfPendulum(new)
        self.assertPendulum(new, 2016, 8, 7, 14, 53, 54)
