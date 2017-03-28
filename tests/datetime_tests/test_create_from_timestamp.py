# -*- coding: utf-8 -*-

import pytz
from pendulum import DateTime, timezone

from .. import AbstractTestCase


class CreateFromTimestampTest(AbstractTestCase):

    def test_create_from_timestamp_returns_pendulum(self):
        d = DateTime.create_from_timestamp(DateTime(1975, 5, 21, 22, 32, 5).timestamp())
        self.assertDateTime(d, 1975, 5, 21, 22, 32, 5)
        self.assertEqual('UTC', d.timezone_name)

    def test_create_from_timestamp_with_timezone_string(self):
        d = DateTime.create_from_timestamp(0, 'America/Toronto')
        self.assertEqual('America/Toronto', d.timezone_name)
        self.assertDateTime(d, 1969, 12, 31, 19, 0, 0)

    def test_create_from_timestamp_with_timezone(self):
        d = DateTime.create_from_timestamp(0, timezone('America/Toronto'))
        self.assertEqual('America/Toronto', d.timezone_name)
        self.assertDateTime(d, 1969, 12, 31, 19, 0, 0)

    def test_create_from_timestamp_with_pytz_timezone(self):
        d = DateTime.create_from_timestamp(0, pytz.timezone('America/Toronto'))
        self.assertEqual('America/Toronto', d.timezone_name)
        self.assertDateTime(d, 1969, 12, 31, 19, 0, 0)
