# -*- coding: utf-8 -*-

from datetime import timezone
from pendulum import Pendulum

from .. import AbstractTestCase


class TimezoneTest(AbstractTestCase):

    def test_in_timezone(self):
        d = Pendulum(2015, 1, 15, 18, 15, 34)
        now = Pendulum(2015, 1, 15, 18, 15, 34)
        self.assertEqual('UTC', d.timezone_name)
        self.assertPendulum(d, now.year, now.month, now.day, now.hour, now.minute)

        d = d.in_timezone('Europe/Paris')
        self.assertEqual('Europe/Paris', d.timezone_name)
        self.assertPendulum(d, now.year, now.month, now.day, now.hour + 1, now.minute)

    def test_in_tz(self):
        d = Pendulum(2015, 1, 15, 18, 15, 34)
        now = Pendulum(2015, 1, 15, 18, 15, 34)
        self.assertEqual('UTC', d.timezone_name)
        self.assertPendulum(d, now.year, now.month, now.day, now.hour, now.minute)

        d = d.in_tz('Europe/Paris')
        self.assertEqual('Europe/Paris', d.timezone_name)
        self.assertPendulum(d, now.year, now.month, now.day, now.hour + 1, now.minute)

    def test_astimezone(self):
        d = Pendulum(2015, 1, 15, 18, 15, 34)
        now = Pendulum(2015, 1, 15, 18, 15, 34)
        self.assertEqual('UTC', d.timezone_name)
        self.assertPendulum(d, now.year, now.month, now.day, now.hour, now.minute)

        d = d.astimezone('Europe/Paris')
        self.assertEqual('Europe/Paris', d.timezone_name)
        self.assertPendulum(d, now.year, now.month, now.day, now.hour + 1, now.minute)

        d = d.astimezone(timezone.utc)
        self.assertEqual('+00:00', d.timezone_name)
        self.assertPendulum(d, now.year, now.month, now.day, now.hour, now.minute)
