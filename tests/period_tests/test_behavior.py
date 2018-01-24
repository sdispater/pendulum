# -*- coding: utf-8 -*-

import pickle
import pendulum

from datetime import timedelta

from .. import AbstractTestCase


class BehaviorTest(AbstractTestCase):

    def test_pickle(self):
        dt1 = pendulum.create(2016, 11, 18)
        dt2 = pendulum.create(2016, 11, 20)

        p = pendulum.period(dt1, dt2)
        s = pickle.dumps(p)
        p2 = pickle.loads(s)

        self.assertEqual(p.start, p2.start)
        self.assertEqual(p.end, p2.end)
        self.assertEqual(p.invert, p2.invert)

        p = pendulum.period(dt2, dt1)
        s = pickle.dumps(p)
        p2 = pickle.loads(s)

        self.assertEqual(p.start, p2.start)
        self.assertEqual(p.end, p2.end)
        self.assertEqual(p.invert, p2.invert)

        p = pendulum.period(dt2, dt1, True)
        s = pickle.dumps(p)
        p2 = pickle.loads(s)

        self.assertEqual(p.start, p2.start)
        self.assertEqual(p.end, p2.end)
        self.assertEqual(p.invert, p2.invert)

    def test_comparison_to_timedelta(self):
        dt1 = pendulum.create(2016, 11, 18)
        dt2 = pendulum.create(2016, 11, 20)

        period = dt2 - dt1

        assert period < timedelta(days=4)
