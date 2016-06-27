# -*- coding: utf-8 -*-

import pytz
from pendulum import Pendulum
from . import AbstractTestCase


class CreateFromDateTest(AbstractTestCase):

    def test_create_from_date_with_defaults(self):
        d = Pendulum.create_from_date()
        self.assertEqual(d.timestamp, Pendulum().timestamp)

    def test_create_from_date(self):
        d = Pendulum.create_from_date(1975, 12, 25)
        self.assertPendulum(d, 1975, 12, 25)

    def test_create_from_date_with_year(self):
        d = Pendulum.create_from_date(1975)
        self.assertEqual(d.year, 1975)

    def test_create_from_date_with_month(self):
        d = Pendulum.create_from_date(None, 12)
        self.assertEqual(d.month, 12)
        d = Pendulum.create_from_date(month=12)
        self.assertEqual(d.month, 12)

    def test_create_from_date_with_day(self):
        d = Pendulum.create_from_date(None, None, 25)
        self.assertEqual(d.day, 25)
        d = Pendulum.create_from_date(day=25)
        self.assertEqual(d.day, 25)

    def test_create_from_date_with_timezone(self):
        d = Pendulum.create_from_date(1975, 12, 25, tz='Europe/London')
        self.assertPendulum(d, 1975, 12, 25)
        self.assertEqual('Europe/London', d.timezone_name)

    def test_create_from_date_with_tzinfo(self):
        d = Pendulum.create_from_date(1975, 12, 25, tz=pytz.timezone('Europe/London'))
        self.assertPendulum(d, 1975, 12, 25)
        self.assertEqual('Europe/London', d.timezone_name)
