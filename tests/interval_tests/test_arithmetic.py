# -*- coding: utf-8 -*-

from pendulum import Interval

from .. import AbstractTestCase


class ArithmeticTestCase(AbstractTestCase):

    def test_multiply(self):
        it = Interval(days=6, seconds=34, microseconds=522222)
        mul = it * 2
        self.assertIsInstanceOfInterval(mul)
        self.assertInterval(mul, 1, 5, 0, 1, 9, 44444)

        it = Interval(days=6, seconds=34, microseconds=522222)
        mul = 2 * it
        self.assertIsInstanceOfInterval(mul)
        self.assertInterval(mul, 1, 5, 0, 1, 9, 44444)

    def test_divide(self):
        it = Interval(days=2, seconds=34, microseconds=522222)
        mul = it / 2
        self.assertIsInstanceOfInterval(mul)
        self.assertInterval(mul, 0, 1, 0, 0, 17, 261111)

        it = Interval(days=2, seconds=35, microseconds=522222)
        mul = it / 2
        self.assertIsInstanceOfInterval(mul)
        self.assertInterval(mul, 0, 1, 0, 0, 17, 761111)

    def test_floor_divide(self):
        it = Interval(days=2, seconds=34, microseconds=522222)
        mul = it // 2
        self.assertIsInstanceOfInterval(mul)
        self.assertInterval(mul, 0, 1, 0, 0, 17, 261111)

        it = Interval(days=2, seconds=35, microseconds=522222)
        mul = it // 3
        self.assertIsInstanceOfInterval(mul)
        self.assertInterval(mul, 0, 0, 16, 0, 11, 840740)
