# -*- coding: utf-8 -*-

from datetime import datetime
from pendulum.helpers import precise_diff

from . import AbstractTestCase


class HelpersTestCase(AbstractTestCase):

    def test_precise_diff(self):
        dt1 = datetime(2003, 3, 1, 0, 0, 0)
        dt2 = datetime(2003, 1, 31, 23, 59, 59)

        diff = precise_diff(dt1, dt2)
        self.assert_diff(diff, months=-1, seconds=-1)

        diff = precise_diff(dt2, dt1)
        self.assert_diff(diff, months=1, seconds=1)

        dt1 = datetime(2012, 3, 1, 0, 0, 0)
        dt2 = datetime(2012, 1, 31, 23, 59, 59)

        diff = precise_diff(dt1, dt2)
        self.assert_diff(diff, months=-1, seconds=-1)

        diff = precise_diff(dt2, dt1)
        self.assert_diff(diff, months=1, seconds=1)

        dt1 = datetime(2001, 1, 1)
        dt2 = datetime(2003, 9, 17, 20, 54, 47, 282310)

        diff = precise_diff(dt1, dt2)
        self.assert_diff(
            diff,
            years=2, months=8, days=16,
            hours=20, minutes=54, seconds=47, microseconds=282310
        )

    def assert_diff(self, diff,
                    years=0, months=0, days=0,
                    hours=0, minutes=0, seconds=0, microseconds=0):
        self.assertEqual(diff['years'], years)
        self.assertEqual(diff['months'], months)
        self.assertEqual(diff['days'], days)
        self.assertEqual(diff['hours'], hours)
        self.assertEqual(diff['minutes'], minutes)
        self.assertEqual(diff['seconds'], seconds)
        self.assertEqual(diff['microseconds'], microseconds)
