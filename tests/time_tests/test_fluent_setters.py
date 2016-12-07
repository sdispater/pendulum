# -*- coding: utf-8 -*-

from .. import AbstractTestCase

from pendulum import Time


class FluentSettersTest(AbstractTestCase):

    def test_replace(self):
        t = Time(12, 34, 56, 123456)
        t = t.replace(1, 2, 3, 654321)

        self.assertIsInstanceOfTime(t)
        self.assertTime(t, 1, 2, 3, 654321)
