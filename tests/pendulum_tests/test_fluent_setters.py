# -*- coding: utf-8 -*-

from pendulum import Pendulum

from .. import AbstractTestCase


class FluentSettersTest(AbstractTestCase):

    def test_fluid_year_setter(self):
        d = Pendulum.now()
        self.assertIsInstanceOfPendulum(d.year_(1995))
        self.assertEqual(1995, d.year)

    def test_fluid_month_setter(self):
        d = Pendulum.create(2016, 7, 2, 0, 41, 20)
        self.assertIsInstanceOfPendulum(d.month_(11))
        self.assertEqual(11, d.month)

    def test_fluid_day_setter(self):
        d = Pendulum.create(2016, 7, 2, 0, 41, 20)
        self.assertIsInstanceOfPendulum(d.day_(9))
        self.assertEqual(9, d.day)

    def test_fluid_hour_setter(self):
        d = Pendulum.create(2016, 7, 2, 0, 41, 20)
        self.assertIsInstanceOfPendulum(d.hour_(5))
        self.assertEqual(5, d.hour)

    def test_fluid_minute_setter(self):
        d = Pendulum.create(2016, 7, 2, 0, 41, 20)
        self.assertIsInstanceOfPendulum(d.minute_(32))
        self.assertEqual(32, d.minute)

    def test_fluid_second_setter(self):
        d = Pendulum.create(2016, 7, 2, 0, 41, 20)
        self.assertIsInstanceOfPendulum(d.second_(49))
        self.assertEqual(49, d.second)

    def test_fluid_set_date(self):
        d = Pendulum.create(2016, 7, 2, 0, 41, 20)
        self.assertIsInstanceOfPendulum(d.set_date(1995, 11, 9))
        self.assertEqual(1995, d.year)
        self.assertEqual(11, d.month)
        self.assertEqual(9, d.day)

    def test_fluid_set_time(self):
        d = Pendulum.create(2016, 7, 2, 0, 41, 20)
        self.assertIsInstanceOfPendulum(d.set_time(5, 32, 49))
        self.assertEqual(5, d.hour)
        self.assertEqual(32, d.minute)
        self.assertEqual(49, d.second)

    def test_fluid_set_timestamp(self):
        d = Pendulum.create(2016, 7, 2, 0, 41, 20)
        self.assertIsInstanceOfPendulum(d.timestamp_(0))
        self.assertEqual(1970, d.year)
        self.assertEqual(1, d.month)
        self.assertEqual(1, d.day)
        self.assertEqual(0, d.hour)
        self.assertEqual(0, d.minute)
        self.assertEqual(0, d.second)
