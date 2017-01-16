# -*- coding: utf-8 -*-

import pendulum
from pendulum import Pendulum
from pendulum.tz.exceptions import NonExistingTime

from .. import AbstractTestCase


class FluentSettersTest(AbstractTestCase):

    def test_fluid_year_setter(self):
        d = Pendulum.now()
        new = d.year_(1995)
        self.assertIsInstanceOfPendulum(new)
        self.assertEqual(1995, new.year)
        self.assertNotEqual(d.year, new.year)

    def test_fluid_month_setter(self):
        d = Pendulum.create(2016, 7, 2, 0, 41, 20)
        new = d.month_(11)
        self.assertIsInstanceOfPendulum(new)
        self.assertEqual(11, new.month)
        self.assertEqual(7, d.month)

    def test_fluid_day_setter(self):
        d = Pendulum.create(2016, 7, 2, 0, 41, 20)
        new = d.day_(9)
        self.assertIsInstanceOfPendulum(new)
        self.assertEqual(9, new.day)
        self.assertEqual(2, d.day)

    def test_fluid_hour_setter(self):
        d = Pendulum.create(2016, 7, 2, 0, 41, 20)
        new = d.hour_(5)
        self.assertIsInstanceOfPendulum(new)
        self.assertEqual(5, new.hour)
        self.assertEqual(0, d.hour)

    def test_fluid_minute_setter(self):
        d = Pendulum.create(2016, 7, 2, 0, 41, 20)
        new = d.minute_(32)
        self.assertIsInstanceOfPendulum(new)
        self.assertEqual(32, new.minute)
        self.assertEqual(41, d.minute)

    def test_fluid_second_setter(self):
        d = Pendulum.create(2016, 7, 2, 0, 41, 20)
        new = d.second_(49)
        self.assertIsInstanceOfPendulum(new)
        self.assertEqual(49, new.second)
        self.assertEqual(20, d.second)

    def test_fluid_microsecond_setter(self):
        d = Pendulum.create(2016, 7, 2, 0, 41, 20, 123456)
        new = d.microsecond_(987654)
        self.assertIsInstanceOfPendulum(new)
        self.assertEqual(987654, new.microsecond)
        self.assertEqual(123456, d.microsecond)

    def test_fluid_setter_keeps_timezone(self):
        d = Pendulum.create(2016, 7, 2, 0, 41, 20, 123456, tz='Europe/Paris')
        new = d.microsecond_(987654)
        self.assertPendulum(new, 2016, 7, 2, 0, 41, 20, 987654)

    def test_fluid_timezone_setter(self):
        d = Pendulum.create(2016, 7, 2, 0, 41, 20)
        new = d.timezone_('Europe/Paris')
        self.assertIsInstanceOfPendulum(new)
        self.assertEqual('Europe/Paris', new.timezone_name)
        self.assertEqual('Europe/Paris', new.tzinfo.tz.name)

    def test_fluid_tz_setter(self):
        d = Pendulum.create(2016, 7, 2, 0, 41, 20)
        new = d.tz_('Europe/Paris')
        self.assertIsInstanceOfPendulum(new)
        self.assertEqual('Europe/Paris', new.timezone_name)

    def test_fluid_on(self):
        d = Pendulum.create(2016, 7, 2, 0, 41, 20)
        new = d.on(1995, 11, 9)
        self.assertIsInstanceOfPendulum(new)
        self.assertEqual(1995, new.year)
        self.assertEqual(11, new.month)
        self.assertEqual(9, new.day)
        self.assertEqual(2016, d.year)
        self.assertEqual(7, d.month)
        self.assertEqual(2, d.day)

    def test_fluid_on_with_transition(self):
        d = Pendulum.create(2013, 3, 31, 0, 0, 0, 0, 'Europe/Paris')
        new = d.on(2013, 4, 1)
        self.assertIsInstanceOfPendulum(new)
        self.assertEqual(2013, new.year)
        self.assertEqual(4, new.month)
        self.assertEqual(1, new.day)
        self.assertEqual(7200, new.offset)
        self.assertEqual(2013, d.year)
        self.assertEqual(3, d.month)
        self.assertEqual(31, d.day)
        self.assertEqual(3600, d.offset)

    def test_fluid_at(self):
        d = Pendulum.create(2016, 7, 2, 0, 41, 20)
        new = d.at(5, 32, 49)
        self.assertIsInstanceOfPendulum(new)
        self.assertEqual(5, new.hour)
        self.assertEqual(32, new.minute)
        self.assertEqual(49, new.second)
        self.assertEqual(0, d.hour)
        self.assertEqual(41, d.minute)
        self.assertEqual(20, d.second)

    def test_fluid_at_with_transition(self):
        d = Pendulum.create(2013, 3, 31, 0, 0, 0, 0, 'Europe/Paris')
        new = d.at(2, 30, 0)
        self.assertIsInstanceOfPendulum(new)
        self.assertEqual(3, new.hour)
        self.assertEqual(30, new.minute)
        self.assertEqual(0, new.second)

    def test_fluid_set_timestamp(self):
        d = Pendulum.create(2016, 7, 2, 0, 41, 20)
        new = d.timestamp_(0)
        self.assertIsInstanceOfPendulum(new)
        self.assertEqual(1970, new.year)
        self.assertEqual(1, new.month)
        self.assertEqual(1, new.day)
        self.assertEqual(0, new.hour)
        self.assertEqual(0, new.minute)
        self.assertEqual(0, new.second)
        self.assertEqual(2016, d.year)
        self.assertEqual(7, d.month)
        self.assertEqual(2, d.day)
        self.assertEqual(0, d.hour)
        self.assertEqual(41, d.minute)
        self.assertEqual(20, d.second)

    def test_with_time_from_string(self):
        d = Pendulum.create(2016, 7, 2, 0, 41, 20)
        new = d.with_time_from_string('05:32:49')
        self.assertIsInstanceOfPendulum(new)
        self.assertEqual(5, new.hour)
        self.assertEqual(32, new.minute)
        self.assertEqual(49, new.second)
        self.assertEqual(0, d.hour)
        self.assertEqual(41, d.minute)
        self.assertEqual(20, d.second)

    def test_with_timestamp(self):
        d = Pendulum.create(2016, 7, 2, 0, 41, 20)
        new = d.with_timestamp(0)

        self.assertIsInstanceOfPendulum(new)
        self.assertPendulum(new, 1970, 1, 1, 0, 0, 0)

    def test_replace_tzinfo(self):
        d = Pendulum.create(2016, 7, 2, 0, 41, 20)
        new = d.replace(tzinfo='Europe/Paris')

        self.assertEqual(new.timezone_name, 'Europe/Paris')

    def test_replace_tzinfo_dst(self):
        d = Pendulum.create(2013, 3, 31, 2, 30)
        new = d.replace(tzinfo='Europe/Paris')

        self.assertPendulum(new, 2013, 3, 31, 3, 30)
        self.assertTrue(new.is_dst)
        self.assertEqual(new.offset, 7200)
        self.assertEqual(new.timezone_name, 'Europe/Paris')

    def test_replace_tzinfo_dst_with_pre_transition_rule(self):
        Pendulum.set_transition_rule(pendulum.PRE_TRANSITION)
        d = Pendulum.create(2013, 3, 31, 2, 30)
        new = d.replace(tzinfo='Europe/Paris')

        self.assertPendulum(new, 2013, 3, 31, 1, 30)
        self.assertFalse(new.is_dst)
        self.assertEqual(new.offset, 3600)
        self.assertEqual(new.timezone_name, 'Europe/Paris')

    def test_replace_tzinfo_dst_with_error_transition_rule(self):
        Pendulum.set_transition_rule(pendulum.TRANSITION_ERROR)
        d = Pendulum.create(2013, 3, 31, 2, 30)

        self.assertRaises(NonExistingTime, d.replace, tzinfo='Europe/Paris')
