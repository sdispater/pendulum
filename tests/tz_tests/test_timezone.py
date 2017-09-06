# -*- coding: utf-8 -*-

import pendulum
from datetime import datetime, timedelta
from pendulum import timezone
from pendulum.tz import Timezone, FixedTimezone
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
        self.skip_if_36()

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
        self.assertEqual(1, dt.hour)
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
        dt = tz.convert(dt, dst_rule=pendulum.POST_TRANSITION)

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
        self.assertEqual(1, dt.hour)
        self.assertEqual(30, dt.minute)
        self.assertEqual(45, dt.second)
        self.assertEqual(123456, dt.microsecond)
        self.assertEqual('Europe/Paris', dt.timezone_name)
        self.assertEqual(3600, dt.offset)
        self.assertFalse(dt.is_dst)

    def test_utcoffset(self):
        tz = pendulum.timezone('Europe/Paris')
        utcoffset = tz.utcoffset(pendulum.create(2017, 1, 1))
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

    def test_short_timezones_should_not_modify_time(self):
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

    def test_after_last_transition(self):
        tz = pendulum.timezone('Europe/Paris')
        dt = tz.datetime(2135, 6, 15, 14, 0, 0)

        assert dt.year == 2135
        assert dt.month == 6
        assert dt.day == 15
        assert dt.hour == 14
        assert dt.minute == 0
        assert dt.second == 0
        assert dt.microsecond == 0

    def test_on_last_transition(self):
        tz = pendulum.timezone('Europe/Paris')
        dt = datetime(2037, 10, 25, 3, 0, 0)
        dt = tz.convert(dt, dst_rule=tz.POST_TRANSITION)

        assert dt.year == 2037
        assert dt.month == 10
        assert dt.day == 25
        assert dt.hour == 3
        assert dt.minute == 0
        assert dt.second == 0
        assert dt.microsecond == 0
        assert dt.utcoffset().total_seconds() == 3600

        dt = datetime(2037, 10, 25, 3, 0, 0)
        dt = tz.convert(dt, dst_rule=tz.PRE_TRANSITION)

        assert dt.year == 2037
        assert dt.month == 10
        assert dt.day == 25
        assert dt.hour == 3
        assert dt.minute == 0
        assert dt.second == 0
        assert dt.microsecond == 0
        assert dt.utcoffset().total_seconds() == 7200

    def test_convert_fold_attribute_is_honored(self):
        self.skip_if_not_36()

        tz = pendulum.timezone('US/Eastern')
        dt = datetime(2014, 11, 2, 1, 30)

        new = tz.convert(dt)
        self.assertEqual('-0400', new.strftime('%z'))

        new = tz.convert(dt.replace(fold=1))
        self.assertEqual('-0500', new.strftime('%z'))

    def test_skipped_time_36_explicit_rule(self):
        self.skip_if_not_36()

        dt = datetime(2013, 3, 31, 2, 30, 45, 123456)
        tz = timezone('Europe/Paris')
        dt = tz.convert(dt, dst_rule=pendulum.POST_TRANSITION)

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

    def test_repeated_time_36_explicit_rule(self):
        self.skip_if_not_36()

        dt = datetime(2013, 10, 27, 2, 30, 45, 123456)
        tz = timezone('Europe/Paris')
        dt = tz.convert(dt, dst_rule=pendulum.POST_TRANSITION)

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

    def test_utcoffset_fold_attribute_is_honored(self):
        self.skip_if_not_36()

        tz = pendulum.timezone('US/Eastern')
        dt = datetime(2014, 11, 2, 1, 30)

        offset = tz.utcoffset(dt)

        self.assertEqual(-4 * 3600, offset.total_seconds())

        offset = tz.utcoffset(dt.replace(fold=1))

        self.assertEqual(-5 * 3600, offset.total_seconds())

    def test_dst_fold_attribute_is_honored(self):
        self.skip_if_not_36()

        tz = pendulum.timezone('US/Eastern')
        dt = datetime(2014, 11, 2, 1, 30)

        offset = tz.dst(dt)

        self.assertEqual(3600, offset.total_seconds())

        offset = tz.dst(dt.replace(fold=1))

        self.assertEqual(-3600, offset.total_seconds())

    def test_tzname_fold_attribute_is_honored(self):
        self.skip_if_not_36()

        tz = pendulum.timezone('US/Eastern')
        dt = datetime(2014, 11, 2, 1, 30)

        name = tz.tzname(dt)

        self.assertEqual('EDT', name)

        name = tz.tzname(dt.replace(fold=1))

        self.assertEqual('EST', name)

    def test_constructor_fold_attribute_is_honored(self):
        self.skip_if_not_36()

        tz = pendulum.timezone('US/Eastern')
        dt = datetime(2014, 11, 2, 1, 30, tzinfo=tz)

        self.assertEqual('-0400', dt.strftime('%z'))

        dt = datetime(2014, 11, 2, 1, 30, tzinfo=tz, fold=1)

        self.assertEqual('-0500', dt.strftime('%z'))

    def test_timezone_with_no_transitions(self):
        tz = Timezone('Test', (), ((0, False, None, ''),), 0, [])

        dt = datetime(2016, 11, 26)
        dt = tz.convert(dt)

        self.assertEqual(dt.year, 2016)
        self.assertEqual(dt.month, 11)
        self.assertEqual(dt.day, 26)
        self.assertEqual(dt.hour, 0)
        self.assertEqual(dt.minute, 0)
        self.assertEqual(dt.second, 0)

    def test_datetime(self):
        tz = timezone('Europe/Paris')

        dt = tz.datetime(2013, 3, 24, 1, 30)
        self.assertEqual(2013, dt.year)
        self.assertEqual(3, dt.month)
        self.assertEqual(24, dt.day)
        self.assertEqual(1, dt.hour)
        self.assertEqual(30, dt.minute)
        self.assertEqual(0, dt.second)
        self.assertEqual(0, dt.microsecond)

        dt = tz.datetime(2013, 3, 31, 2, 30)
        self.assertEqual(2013, dt.year)
        self.assertEqual(3, dt.month)
        self.assertEqual(31, dt.day)
        self.assertEqual(3, dt.hour)
        self.assertEqual(30, dt.minute)
        self.assertEqual(0, dt.second)
        self.assertEqual(0, dt.microsecond)

    def test_fixed_timezone(self):
        tz = FixedTimezone.load(19800)
        tz2 = FixedTimezone.load(18000)
        dt = datetime(2016, 11, 26, tzinfo=tz)

        self.assertEqual(tz2.utcoffset(dt).total_seconds(), 18000)
        self.assertIsNone(tz2.dst(dt))
