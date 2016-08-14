# -*- coding: utf-8 -*-

from pendulum import Pendulum, timezone
from pendulum.tz.timezone_info import TimezoneInfo
from .. import AbstractTestCase


class CreateFromDateTest(AbstractTestCase):

    def test_create_from_date_with_defaults(self):
        d = Pendulum.create_from_date()
        self.assertEqual(d.timestamp, Pendulum.utcnow().timestamp)

    def test_create_from_date(self):
        d = Pendulum.create_from_date(1975, 12, 25)
        now = Pendulum.utcnow()
        self.assertPendulum(d, 1975, 12, 25, now.hour, now.minute)

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

    def test_create_from_date_with_timezone_string(self):
        d = Pendulum.create_from_date(1975, 12, 25, tz='Europe/London')
        self.assertPendulum(d, 1975, 12, 25)
        self.assertEqual('Europe/London', d.timezone_name)

    def test_create_from_date_with_timezone(self):
        d = Pendulum.create_from_date(1975, 12, 25, tz=timezone('Europe/London'))
        self.assertPendulum(d, 1975, 12, 25)
        self.assertEqual('Europe/London', d.timezone_name)

    def test_create_from_date_with_tzinfo(self):
        tz = timezone('Europe/London')
        d = Pendulum.create_from_date(1975, 12, 25, tz=TimezoneInfo.create(tz, 3600, True, ''))
        self.assertPendulum(d, 1975, 12, 25)
        self.assertEqual('Europe/London', d.timezone_name)
