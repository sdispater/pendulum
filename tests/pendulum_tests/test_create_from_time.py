# -*- coding: utf-8 -*-

import pytz
from pendulum import Pendulum

from .. import AbstractTestCase


class CreateFromTimeTest(AbstractTestCase):

    def test_create_from_time_with_defaults(self):
        d = Pendulum.create_from_time()
        self.assertEqual(d.timestamp, Pendulum().timestamp)
        self.assertEqual('UTC', d.timezone_name)

    def test_create_from_time(self):
        d = Pendulum.create_from_time(23, 5, 11)
        now = Pendulum.utcnow()
        self.assertPendulum(d, now.year, now.month, now.day, 23, 5, 11)
        self.assertEqual('UTC', d.timezone_name)

    def test_create_from_time_with_hour(self):
        d = Pendulum.create_from_time(23)
        self.assertEqual(23, d.hour)
        self.assertEqual(0, d.minute)
        self.assertEqual(0, d.second)
        self.assertEqual(0, d.microsecond)

    def test_create_from_time_with_minute(self):
        d = Pendulum.create_from_time(minute=5)
        self.assertEqual(5, d.minute)

    def test_create_from_time_with_second(self):
        d = Pendulum.create_from_time(second=11)
        self.assertEqual(11, d.second)

    def test_create_from_time_with_timezone_string(self):
        d = Pendulum.create_from_time(23, 5, 11, tz='Europe/London')
        now = Pendulum.now('Europe/London')
        self.assertPendulum(d, now.year, now.month, now.day, 23, 5, 11)
        self.assertEqual('Europe/London', d.timezone_name)

    def test_create_from_time_with_timezone(self):
        d = Pendulum.create_from_time(23, 5, 11, tz=pytz.timezone('Europe/London'))
        now = Pendulum.now('Europe/London')
        self.assertPendulum(d, now.year, now.month, now.day, 23, 5, 11)
        self.assertEqual('Europe/London', d.timezone_name)
