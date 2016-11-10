# -*- coding: utf-8 -*-

import pickle
import pytz
from datetime import time
from pendulum import Time
from .. import AbstractTestCase


class BehaviorTest(AbstractTestCase):

    def setUp(self):
        super(BehaviorTest, self).setUp()

        self.p = Time(12, 34, 56, 123456, pytz.timezone('Europe/Paris'))
        self.d = time(12, 34, 56, 123456, pytz.timezone('Europe/Paris'))

    def test_hash(self):
        self.assertEqual(hash(self.p), hash(self.d))
        dt1 = Time(12, 34, 57, 123456)

        self.assertNotEqual(hash(self.p), hash(dt1))

    def test_pickle(self):
        dt1 = Time(12, 34, 56, 123456)
        s = pickle.dumps(dt1)
        dt2 = pickle.loads(s)

        self.assertEqual(dt1, dt2)

    def test_utcoffset(self):
        self.assertEqual(self.p.utcoffset(), self.d.utcoffset())

    def test_dst(self):
        self.assertEqual(self.p.dst(), self.d.dst())

    def test_tzname(self):
        self.assertEqual(self.p.tzname(), self.d.tzname())
        self.assertEqual(
            Time(12, 34, 56, 123456).tzname(),
            time(12, 34, 56, 123456).tzname()
        )
