# -*- coding: utf-8 -*-

import pendulum
from .. import AbstractTestCase


class DayOfYearTest(AbstractTestCase):
    def test_non_leap_year(self):
        d = pendulum.create(1975, 3, 22)
        self.assertEqual(
            d.day_of_year, 81
        )

    def test_leap_year(self):
        d = pendulum.create(1972, 4, 24)
        self.assertEqual(
            d.day_of_year, 115
        )
