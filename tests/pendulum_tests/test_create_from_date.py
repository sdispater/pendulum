# -*- coding: utf-8 -*-

from pendulum import Pendulum, timezone
from pendulum.tz.timezone_info import TimezoneInfo
from .. import AbstractTestCase


class CreateFromDateTest(AbstractTestCase):

    def test_create_from_date_with_defaults(self):
        d = Pendulum.create()
        self.assertEqual(d.timestamp, Pendulum.utcnow().at(0, 0, 0, 0).timestamp)

    def test_create_from_date(self):
        d = Pendulum.create(1975, 12, 25)
        self.assertPendulum(d, 1975, 12, 25, 0, 0, 0)

    def test_create_from_date_with_year(self):
        d = Pendulum.create(1975)
        self.assertEqual(d.year, 1975)

    def test_create_from_date_with_month(self):
        d = Pendulum.create(month=12)
        self.assertEqual(d.month, 12)

    def test_create_from_date_with_day(self):
        d = Pendulum.create(day=25)
        self.assertEqual(d.day, 25)

    def test_create_from_date_with_timezone_string(self):
        d = Pendulum.create(1975, 12, 25, tz='Europe/London')
        self.assertPendulum(d, 1975, 12, 25)
        self.assertEqual('Europe/London', d.timezone_name)

    def test_create_from_date_with_timezone(self):
        d = Pendulum.create(1975, 12, 25, tz=timezone('Europe/London'))
        self.assertPendulum(d, 1975, 12, 25)
        self.assertEqual('Europe/London', d.timezone_name)

    def test_create_from_date_with_tzinfo(self):
        tz = timezone('Europe/London')
        d = Pendulum.create(1975, 12, 25, tz=TimezoneInfo(tz, 3600, True, None, ''))
        self.assertPendulum(d, 1975, 12, 25)
        self.assertEqual('Europe/London', d.timezone_name)
