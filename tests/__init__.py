# -*- coding: utf-8 -*-

import tzlocal
import pytz
from unittest import TestCase
from contextlib import contextmanager

from pendulum import Pendulum


class AbstractTestCase(TestCase):

    def setUp(self):
        self._save_tz = tzlocal.get_localzone

        tzlocal.get_localzone = lambda: pytz.timezone('America/Toronto')

        super(AbstractTestCase, self).setUp()

    def tearDown(self):
        tzlocal.get_localzone = self._save_tz
        Pendulum.reset_to_string_format()

    def assertPendulum(self, d, year, month, day, hour=None, minute=None, second=None):
        self.assertEqual(year, d.year)
        self.assertEqual(month, d.month)
        self.assertEqual(day, d.day)

        if hour is not None:
            self.assertEqual(hour, d.hour)

        if minute is not None:
            self.assertEqual(minute, d.minute)

        if second is not None:
            self.assertEqual(second, d.second)

    def assertIsInstanceOfPendulum(self, d):
        self.assertIsInstance(d, Pendulum)

    @contextmanager
    def wrap_with_test_now(self, dt=None):
        Pendulum.set_test_now(dt or Pendulum.now())

        yield

        Pendulum.set_test_now()
