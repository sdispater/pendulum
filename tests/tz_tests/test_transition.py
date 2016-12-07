# -*- coding: utf-8 -*-

from datetime import datetime
from pendulum.tz.transition import Transition

from .. import AbstractTestCase


class TransitionTest(AbstractTestCase):

    def test_construct(self):
        t = Transition(3600, 1, datetime(1970, 1, 1), datetime(1970, 1, 1, 1), 0)

        self.assertEqual(3600, t.unix_time)
        self.assertEqual(datetime(1970, 1, 1, 1), t.time)
        self.assertEqual(datetime(1970, 1, 1), t.pre_time)
        self.assertEqual(datetime(1970, 1, 1, 1), t.utc_time)
        self.assertEqual(1, t.tzinfo_index)
        self.assertEqual(0, t.pre_tzinfo_index)

    def test_repr(self):
        t = Transition(3600, 1, datetime(1970, 1, 1), datetime(1970, 1, 1, 1), 0)

        self.assertEqual(
            '<Transition [1970-01-01 01:00:00 UTC, 1970-01-01 00:00:00 -> 1970-01-01 01:00:00]>',
            repr(t)
        )
