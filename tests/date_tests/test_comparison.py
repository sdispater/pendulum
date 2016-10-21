# -*- coding: utf-8 -*-

from datetime import date
from pendulum import Date

from .. import AbstractTestCase


class ComparisonTest(AbstractTestCase):

    def test_equal_to_true(self):
        d1 = Date(2000, 1, 1)
        d2 = Date(2000, 1, 1)
        d3 = date(2000, 1, 1)

        self.assertEqual(d1, d2)
        self.assertEqual(d1, d3)

    def test_equal_to_false(self):
        d1 = Date(2000, 1, 1)
        d2 = Date(2000, 1, 2)
        d3 = date(2000, 1, 2)

        self.assertNotEqual(d1, d2)
        self.assertNotEqual(d1, d3)

    def test_not_equal_to_true(self):
        d1 = Date(2000, 1, 1)
        d2 = Date(2000, 1, 2)
        d3 = date(2000, 1, 2)

        self.assertNotEqual(d1, d2)
        self.assertNotEqual(d1, d3)

    def test_not_equal_to_false(self):
        d1 = Date(2000, 1, 1)
        d2 = Date(2000, 1, 1)
        d3 = date(2000, 1, 1)

        self.assertEqual(d1, d2)
        self.assertEqual(d1, d3)

    def test_not_equal_to_none(self):
        d1 = Date(2000, 1, 1)

        self.assertNotEqual(d1, None)

    def test_greater_than_true(self):
        d1 = Date(2000, 1, 1)
        d2 = Date(1999, 12, 31)
        d3 = date(1999, 12, 31)

        self.assertTrue(d1 > d2)
        self.assertTrue(d1 > d3)

    def test_greater_than_false(self):
        d1 = Date(2000, 1, 1)
        d2 = Date(2000, 1, 2)
        d3 = date(2000, 1, 2)

        self.assertFalse(d1 > d2)
        self.assertFalse(d1 > d3)

    def test_greater_than_or_equal_true(self):
        d1 = Date(2000, 1, 1)
        d2 = Date(1999, 12, 31)
        d3 = date(1999, 12, 31)

        self.assertTrue(d1 >= d2)
        self.assertTrue(d1 >= d3)

    def test_greater_than_or_equal_true_equal(self):
        d1 = Date(2000, 1, 1)
        d2 = Date(2000, 1, 1)
        d3 = date(2000, 1, 1)

        self.assertTrue(d1 >= d2)
        self.assertTrue(d1 >= d3)

    def test_greater_than_or_equal_false(self):
        d1 = Date(2000, 1, 1)
        d2 = Date(2000, 1, 2)
        d3 = date(2000, 1, 2)

        self.assertFalse(d1 >= d2)
        self.assertFalse(d1 >= d3)

    def test_less_than_true(self):
        d1 = Date(2000, 1, 1)
        d2 = Date(2000, 1, 2)
        d3 = date(2000, 1, 2)

        self.assertTrue(d1 < d2)
        self.assertTrue(d1 < d3)

    def test_less_than_false(self):
        d1 = Date(2000, 1, 2)
        d2 = Date(2000, 1, 1)
        d3 = date(2000, 1, 1)

        self.assertFalse(d1 < d2)
        self.assertFalse(d1 < d3)

    def test_less_than_or_equal_true(self):
        d1 = Date(2000, 1, 1)
        d2 = Date(2000, 1, 2)
        d3 = date(2000, 1, 2)

        self.assertTrue(d1 <= d2)
        self.assertTrue(d1 <= d3)

    def test_less_than_or_equal_true_equal(self):
        d1 = Date(2000, 1, 1)
        d2 = Date(2000, 1, 1)
        d3 = date(2000, 1, 1)

        self.assertTrue(d1 <= d2)
        self.assertTrue(d1 <= d3)

    def test_less_than_or_equal_false(self):
        d1 = Date(2000, 1, 2)
        d2 = Date(2000, 1, 1)
        d3 = date(2000, 1, 1)

        self.assertFalse(d1 <= d2)
        self.assertFalse(d1 <= d3)

    def test_between_equal_true(self):
        d1 = Date(2000, 1, 15)
        d2 = Date(2000, 1, 1)
        d3 = Date(2000, 1, 31)
        d4 = date(2000, 1, 1)
        d5 = date(2000, 1, 31)

        self.assertTrue(d1.between(d2, d3))
        self.assertTrue(d1.between(d4, d5))

    def test_between_not_equal_true(self):
        d1 = Date(2000, 1, 15)
        d2 = Date(2000, 1, 1)
        d3 = Date(2000, 1, 31)
        d4 = date(2000, 1, 1)
        d5 = date(2000, 1, 31)

        self.assertTrue(d1.between(d2, d3, False))
        self.assertTrue(d1.between(d4, d5, False))

    def test_between_equal_false(self):
        d1 = Date(1999, 12, 31)
        d2 = Date(2000, 1, 1)
        d3 = Date(2000, 1, 31)
        d4 = date(2000, 1, 1)
        d5 = date(2000, 1, 31)

        self.assertFalse(d1.between(d2, d3))
        self.assertFalse(d1.between(d4, d5))

    def test_between_not_equal_false(self):
        d1 = Date(2000, 1, 1)
        d2 = Date(2000, 1, 1)
        d3 = Date(2000, 1, 31)
        d4 = date(2000, 1, 1)
        d5 = date(2000, 1, 31)

        self.assertFalse(d1.between(d2, d3, False))
        self.assertFalse(d1.between(d4, d5, False))

    def test_between_equal_switch_true(self):
        d1 = Date(2000, 1, 15)
        d2 = Date(2000, 1, 1)
        d3 = Date(2000, 1, 31)
        d4 = date(2000, 1, 1)
        d5 = date(2000, 1, 31)

        self.assertTrue(d1.between(d3, d2))
        self.assertTrue(d1.between(d5, d4))

    def test_between_not_equal_switch_true(self):
        d1 = Date(2000, 1, 15)
        d2 = Date(2000, 1, 1)
        d3 = Date(2000, 1, 31)
        d4 = date(2000, 1, 1)
        d5 = date(2000, 1, 31)

        self.assertTrue(d1.between(d3, d2, False))
        self.assertTrue(d1.between(d5, d4, False))

    def test_between_equal_switch_false(self):
        d1 = Date(1999, 12, 31)
        d2 = Date(2000, 1, 1)
        d3 = Date(2000, 1, 31)
        d4 = date(2000, 1, 1)
        d5 = date(2000, 1, 31)

        self.assertFalse(d1.between(d3, d2))
        self.assertFalse(d1.between(d5, d4))

    def test_between_not_equal_switch_false(self):
        d1 = Date(2000, 1, 1)
        d2 = Date(2000, 1, 1)
        d3 = Date(2000, 1, 31)
        d4 = date(2000, 1, 1)
        d5 = date(2000, 1, 31)

        self.assertFalse(d1.between(d3, d2, False))
        self.assertFalse(d1.between(d5, d4, False))

    def test_min_is_fluid(self):
        d = Date.today()
        self.assertIsInstanceOfDate(d.min_())
        self.assertIsInstanceOfDate(d.min_(date(1975, 1, 1)))
        self.assertIsInstanceOfDate(d.minimum())
        self.assertIsInstanceOfDate(d.minimum(date(1975, 1, 1)))

    def test_min_with_now(self):
        d = Date(2012, 1, 1).min_()
        self.assertDate(d, 2012, 1, 1)
        d = Date(2012, 1, 1).minimum()
        self.assertDate(d, 2012, 1, 1)

    def test_min_with_instance(self):
        d1 = Date(2013, 12, 31)
        d2 = Date(2012, 1, 1).min_(d1)
        self.assertDate(d2, 2012, 1, 1)
        d2 = Date(2012, 1, 1).minimum(d1)
        self.assertDate(d2, 2012, 1, 1)

    def test_max_is_fluid(self):
        d = Date.today()
        self.assertIsInstanceOfDate(d.max_())
        self.assertIsInstanceOfDate(d.max_(date(2099, 12, 31)))
        self.assertIsInstanceOfDate(d.maximum())
        self.assertIsInstanceOfDate(d.maximum(date(2099, 12, 31)))

    def test_max_with_now(self):
        d = Date(2099, 12, 31).max_()
        self.assertDate(d, 2099, 12, 31)
        d = Date(2099, 12, 31).maximum()
        self.assertDate(d, 2099, 12, 31)

    def test_max_with_instance(self):
        d1 = Date(2012, 1, 1)
        d2 = Date(2099, 12, 31).max_(d1)
        self.assertDate(d2, 2099, 12, 31)
        d2 = Date(2099, 12, 31).maximum(d1)
        self.assertDate(d2, 2099, 12, 31)

    def test_is_birthday(self):
        d = Date.today()
        a_birthday = d.subtract(years=1)
        self.assertTrue(a_birthday.is_birthday())
        not_a_birthday = d.subtract(days=1)
        self.assertFalse(not_a_birthday.is_birthday())
        also_not_a_birthday = d.add(days=2)
        self.assertFalse(also_not_a_birthday.is_birthday())

        d1 = Date(1987, 4, 23)
        d2 = Date(2014, 9, 26)
        d3 = Date(2014, 4, 23)
        self.assertFalse(d2.is_birthday(d1))
        self.assertTrue(d3.is_birthday(d1))

    def test_closest(self):
        instance = Date.create(2015, 5, 28)
        dt1 = Date.create(2015, 5, 27)
        dt2 = Date.create(2015, 5, 30)
        closest = instance.closest(dt1, dt2)
        self.assertEqual(dt1, closest)

        closest = instance.closest(dt2, dt1)
        self.assertEqual(dt1, closest)

    def test_closest_with_date(self):
        instance = Date.create(2015, 5, 28)
        dt1 = date(2015, 5, 27)
        dt2 = date(2015, 5, 30)
        closest = instance.closest(dt1, dt2)
        self.assertIsInstanceOfDate(closest)
        self.assertDate(closest, 2015, 5, 27)

    def test_closest_with_equals(self):
        instance = Date.create(2015, 5, 28)
        dt1 = Date.create(2015, 5, 28)
        dt2 = Date.create(2015, 5, 30)
        closest = instance.closest(dt1, dt2)
        self.assertEqual(dt1, closest)

    def test_farthest(self):
        instance = Date.create(2015, 5, 28)
        dt1 = Date.create(2015, 5, 27)
        dt2 = Date.create(2015, 5, 30)
        closest = instance.farthest(dt1, dt2)
        self.assertEqual(dt2, closest)

        closest = instance.farthest(dt2, dt1)
        self.assertEqual(dt2, closest)

    def test_farthest_with_date(self):
        instance = Date.create(2015, 5, 28)
        dt1 = date(2015, 5, 27)
        dt2 = date(2015, 5, 30)
        closest = instance.farthest(dt1, dt2)
        self.assertIsInstanceOfDate(closest)
        self.assertDate(closest, 2015, 5, 30)

    def test_farthest_with_equals(self):
        instance = Date.create(2015, 5, 28)
        dt1 = Date.create(2015, 5, 28)
        dt2 = Date.create(2015, 5, 30)
        closest = instance.farthest(dt1, dt2)
        self.assertEqual(dt2, closest)

    def test_is_same_day(self):
        dt1 = Date.create(2015, 5, 28)
        dt2 = Date.create(2015, 5, 29)
        dt3 = Date.create(2015, 5, 28)
        dt4 = date(2015, 5, 28)
        dt5 = date(2015, 5, 29)

        self.assertFalse(dt1.is_same_day(dt2))
        self.assertTrue(dt1.is_same_day(dt3))
        self.assertTrue(dt1.is_same_day(dt4))
        self.assertFalse(dt1.is_same_day(dt5))

    def test_comparison_to_unsupported(self):
        dt1 = Date.today()

        self.assertFalse(dt1 == 'test')
        self.assertFalse(dt1 in ['test'])
