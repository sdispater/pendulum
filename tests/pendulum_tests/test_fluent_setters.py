# -*- coding: utf-8 -*-

from pendulum import Pendulum

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

    def test_fluid_with_date(self):
        d = Pendulum.create(2016, 7, 2, 0, 41, 20)
        new = d.with_date(1995, 11, 9)
        self.assertIsInstanceOfPendulum(new)
        self.assertEqual(1995, new.year)
        self.assertEqual(11, new.month)
        self.assertEqual(9, new.day)
        self.assertEqual(2016, d.year)
        self.assertEqual(7, d.month)
        self.assertEqual(2, d.day)

    def test_fluid_set_time(self):
        d = Pendulum.create(2016, 7, 2, 0, 41, 20)
        new = d.with_time(5, 32, 49)
        self.assertIsInstanceOfPendulum(new)
        self.assertEqual(5, new.hour)
        self.assertEqual(32, new.minute)
        self.assertEqual(49, new.second)
        self.assertEqual(0, d.hour)
        self.assertEqual(41, d.minute)
        self.assertEqual(20, d.second)

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
