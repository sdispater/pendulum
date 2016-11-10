# -*- coding: utf-8 -*-

import pytz
from datetime import time
from pendulum import Time

from .. import AbstractTestCase


class ComparisonTest(AbstractTestCase):

    def test_equal_to_true(self):
        t1 = Time(1, 2, 3)
        t2 = Time(1, 2, 3)
        t3 = time(1, 2, 3)

        self.assertEqual(t1, t2)
        self.assertEqual(t1, t3)

    def test_equal_to_false(self):
        t1 = Time(1, 2, 3)
        t2 = Time(1, 2, 4)
        t3 = time(1, 2, 4)

        self.assertNotEqual(t1, t2)
        self.assertNotEqual(t1, t3)

    def test_not_equal_to_none(self):
        t1 = Time(1, 2, 3)

        self.assertNotEqual(t1, None)

    def test_greater_than_true(self):
        t1 = Time(1, 2, 3)
        t2 = Time(1, 2, 2)
        t3 = time(1, 2, 2)

        self.assertTrue(t1 > t2)
        self.assertTrue(t1 > t3)

    def test_greater_than_false(self):
        t1 = Time(1, 2, 2)
        t2 = Time(1, 2, 3)
        t3 = time(1, 2, 3)

        self.assertFalse(t1 > t2)
        self.assertFalse(t1 > t3)

    def test_greater_than_or_equal_true(self):
        t1 = Time(1, 2, 3)
        t2 = Time(1, 2, 2)
        t3 = time(1, 2, 2)

        self.assertTrue(t1 >= t2)
        self.assertTrue(t1 >= t3)

    def test_greater_than_or_equal_true_equal(self):
        t1 = Time(1, 2, 3)
        t2 = Time(1, 2, 3)
        t3 = time(1, 2, 3)

        self.assertTrue(t1 >= t2)
        self.assertTrue(t1 >= t3)

    def test_greater_than_or_equal_false(self):
        t1 = Time(1, 2, 2)
        t2 = Time(1, 2, 3)
        t3 = time(1, 2, 3)

        self.assertFalse(t1 >= t2)
        self.assertFalse(t1 >= t3)

    def test_less_than_true(self):
        t1 = Time(1, 2, 2)
        t2 = Time(1, 2, 3)
        t3 = time(1, 2, 3)

        self.assertTrue(t1 < t2)
        self.assertTrue(t1 < t3)

    def test_less_than_false(self):
        t1 = Time(1, 2, 3)
        t2 = Time(1, 2, 2)
        t3 = time(1, 2, 2)

        self.assertFalse(t1 < t2)
        self.assertFalse(t1 < t3)

    def test_less_than_or_equal_true(self):
        t1 = Time(1, 2, 2)
        t2 = Time(1, 2, 3)
        t3 = time(1, 2, 3)

        self.assertTrue(t1 <= t2)
        self.assertTrue(t1 <= t3)

    def test_less_than_or_equal_true_equal(self):
        t1 = Time(1, 2, 3)
        t2 = Time(1, 2, 3)
        t3 = time(1, 2, 3)

        self.assertTrue(t1 <= t2)
        self.assertTrue(t1 <= t3)

    def test_less_than_or_equal_false(self):
        t1 = Time(1, 2, 3)
        t2 = Time(1, 2, 2)
        t3 = time(1, 2, 2)

        self.assertFalse(t1 <= t2)
        self.assertFalse(t1 <= t3)

    def test_between_equal_true(self):
        t1 = Time(1, 2, 3)
        t2 = Time(1, 2, 1)
        t3 = Time(1, 2, 4)
        t4 = time(1, 2, 1)
        t5 = time(1, 2, 4)

        self.assertTrue(t1.between(t2, t3))
        self.assertTrue(t1.between(t4, t5))

    def test_between_not_equal_true(self):
        t1 = Time(1, 2, 3)
        t2 = Time(1, 2, 1)
        t3 = Time(1, 2, 4)
        t4 = time(1, 2, 1)
        t5 = time(1, 2, 4)

        self.assertTrue(t1.between(t2, t3, False))
        self.assertTrue(t1.between(t4, t5, False))

    def test_between_equal_false(self):
        t1 = Time(1, 2, 5)
        t2 = Time(1, 2, 1)
        t3 = Time(1, 2, 4)
        t4 = time(1, 2, 1)
        t5 = time(1, 2, 4)

        self.assertFalse(t1.between(t2, t3))
        self.assertFalse(t1.between(t4, t5))

    def test_between_not_equal_false(self):
        t1 = Time(1, 2, 1)
        t2 = Time(1, 2, 1)
        t3 = Time(1, 2, 4)
        t4 = time(1, 2, 1)
        t5 = time(1, 2, 4)

        self.assertFalse(t1.between(t2, t3, False))
        self.assertFalse(t1.between(t4, t5, False))

    def test_between_equal_switch_true(self):
        t1 = Time(1, 2, 3)
        t2 = Time(1, 2, 1)
        t3 = Time(1, 2, 4)
        t4 = time(1, 2, 1)
        t5 = time(1, 2, 4)

        self.assertTrue(t1.between(t3, t2))
        self.assertTrue(t1.between(t5, t4))

    def test_between_not_equal_switch_true(self):
        t1 = Time(1, 2, 3)
        t2 = Time(1, 2, 1)
        t3 = Time(1, 2, 4)
        t4 = time(1, 2, 1)
        t5 = time(1, 2, 4)

        self.assertTrue(t1.between(t3, t2, False))
        self.assertTrue(t1.between(t5, t4, False))

    def test_between_equal_switch_false(self):
        t1 = Time(1, 2, 5)
        t2 = Time(1, 2, 1)
        t3 = Time(1, 2, 4)
        t4 = time(1, 2, 1)
        t5 = time(1, 2, 4)

        self.assertFalse(t1.between(t3, t2))
        self.assertFalse(t1.between(t5, t4))

    def test_between_not_equal_switch_false(self):
        t1 = Time(1, 2, 1)
        t2 = Time(1, 2, 1)
        t3 = Time(1, 2, 4)
        t4 = time(1, 2, 1)
        t5 = time(1, 2, 4)

        self.assertFalse(t1.between(t3, t2, False))
        self.assertFalse(t1.between(t5, t4, False))

    def test_min_is_fluid(self):
        t = Time.now()
        self.assertIsInstanceOfTime(t.min_())
        self.assertIsInstanceOfTime(t.min_(time(1, 2, 3)))
        self.assertIsInstanceOfTime(t.minimum())
        self.assertIsInstanceOfTime(t.minimum(time(1, 2, 3)))

    def test_min_with_now(self):
        with Time.test(Time(1, 2, 3)):
            t = Time(1, 1, 1).min_()
            self.assertTime(t, 1, 1, 1)
            t = Time(1, 1, 1).minimum()
            self.assertTime(t, 1, 1, 1)

    def test_min_with_instance(self):
        t1 = Time(2, 3, 4)
        t2 = Time(1, 2, 3).min_(t1)
        self.assertTime(t2, 1, 2, 3)
        t2 = Time(1, 2, 3).minimum(t1)
        self.assertTime(t2, 1, 2, 3)

    def test_max_is_fluid(self):
        t = Time.now()
        self.assertIsInstanceOfTime(t.max_())
        self.assertIsInstanceOfTime(t.max_(Time(1, 2, 3)))
        self.assertIsInstanceOfTime(t.maximum())
        self.assertIsInstanceOfTime(t.maximum(Time(1, 2, 3)))

    def test_max_with_now(self):
        with Time.test(Time(1, 2, 3)):
            t = Time(12, 34, 56).max_()
            self.assertTime(t, 12, 34, 56)
            t = Time(12, 34, 56).maximum()
            self.assertTime(t, 12, 34, 56)

    def test_max_with_instance(self):
        t1 = Time(1, 2, 3)
        t2 = Time(12, 34, 56).max_(t1)
        self.assertTime(t2, 12, 34, 56)
        t2 = Time(12, 34, 56).maximum(t1)
        self.assertTime(t2, 12, 34, 56)

    def test_closest(self):
        instance = Time(12, 34, 56)
        t1 = Time(12, 34, 54)
        t2 = Time(12, 34, 59)
        closest = instance.closest(t1, t2)
        self.assertEqual(t1, closest)

        closest = instance.closest(t2, t1)
        self.assertEqual(t1, closest)

    def test_closest_with_time(self):
        instance = Time(12, 34, 56)
        t1 = Time(12, 34, 54)
        t2 = Time(12, 34, 59)
        closest = instance.closest(t1, t2)

        self.assertIsInstanceOfTime(closest)
        self.assertTime(closest, 12, 34, 54)

    def test_closest_with_equals(self):
        instance = Time(12, 34, 56)
        t1 = Time(12, 34, 56)
        t2 = Time(12, 34, 59)
        closest = instance.closest(t1, t2)
        self.assertEqual(t1, closest)

    def test_farthest(self):
        instance = Time(12, 34, 56)
        t1 = Time(12, 34, 54)
        t2 = Time(12, 34, 59)
        farthest = instance.farthest(t1, t2)
        self.assertEqual(t2, farthest)

        farthest = instance.farthest(t2, t1)
        self.assertEqual(t2, farthest)

    def test_farthest_with_time(self):
        instance = Time(12, 34, 56)
        t1 = Time(12, 34, 54)
        t2 = Time(12, 34, 59)
        farthest = instance.farthest(t1, t2)

        self.assertIsInstanceOfTime(farthest)
        self.assertTime(farthest, 12, 34, 59)

    def test_farthest_with_equals(self):
        instance = Time(12, 34, 56)
        t1 = Time(12, 34, 56)
        t2 = Time(12, 34, 59)

        farthest = instance.farthest(t1, t2)
        self.assertEqual(t2, farthest)

    def test_comparison_to_unsupported(self):
        t1 = Time.now()

        self.assertFalse(t1 == 'test')
        self.assertTrue(t1 != 'test')
        self.assertFalse(t1 in ['test'])
