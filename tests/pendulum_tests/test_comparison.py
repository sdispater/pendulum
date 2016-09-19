# -*- coding: utf-8 -*-

import pytz
from datetime import datetime
from time import sleep
from pendulum import Pendulum

from .. import AbstractTestCase


class ComparisonTest(AbstractTestCase):

    def test_equal_to_true(self):
        d1 = Pendulum(2000, 1, 1, 1, 2, 3)
        d2 = Pendulum(2000, 1, 1, 1, 2, 3)
        d3 = datetime(2000, 1, 1, 1, 2, 3)

        self.assertEqual(d1, d2)
        self.assertEqual(d1, d3)

    def test_equal_to_false(self):
        d1 = Pendulum(2000, 1, 1, 1, 2, 3)
        d2 = Pendulum(2000, 1, 2, 1, 2, 3)
        d3 = datetime(2000, 1, 2, 1, 2, 3)

        self.assertNotEqual(d1, d2)
        self.assertNotEqual(d1, d3)

    def test_equal_with_timezone_true(self):
        d1 = Pendulum(2000, 1, 1, 12, 0, 0, tzinfo='America/Toronto')
        d2 = Pendulum(2000, 1, 1, 9, 0, 0, tzinfo='America/Vancouver')
        d3 = datetime(2000, 1, 1, 12, 0, 0)

        self.assertEqual(d1, d2)
        self.assertEqual(d1, d3)

    def test_equal_with_timezone_false(self):
        d1 = Pendulum(2000, 1, 1, tzinfo='America/Toronto')
        d2 = Pendulum(2000, 1, 1, tzinfo='America/Vancouver')
        d3 = datetime(2000, 1, 1)

        self.assertNotEqual(d1, d2)
        self.assertEqual(d1, d3)

    def test_not_equal_to_true(self):
        d1 = Pendulum(2000, 1, 1, 1, 2, 3)
        d2 = Pendulum(2000, 1, 2, 1, 2, 3)
        d3 = datetime(2000, 1, 2, 1, 2, 3)

        self.assertNotEqual(d1, d2)
        self.assertNotEqual(d1, d3)

    def test_not_equal_to_false(self):
        d1 = Pendulum(2000, 1, 1, 1, 2, 3)
        d2 = Pendulum(2000, 1, 1, 1, 2, 3)
        d3 = datetime(2000, 1, 1, 1, 2, 3)

        self.assertEqual(d1, d2)
        self.assertEqual(d1, d3)

    def test_not_equal_with_timezone_true(self):
        d1 = Pendulum(2000, 1, 1, tzinfo='America/Toronto')
        d2 = Pendulum(2000, 1, 1, tzinfo='America/Vancouver')
        d3 = datetime(2000, 1, 1)

        self.assertNotEqual(d1, d2)
        self.assertEqual(d1, d3)

    def test_not_equal_to_none(self):
        d1 = Pendulum(2000, 1, 1, 1, 2, 3)

        self.assertNotEqual(d1, None)

    def test_greater_than_true(self):
        d1 = Pendulum(2000, 1, 1)
        d2 = Pendulum(1999, 12, 31)
        d3 = datetime(1999, 12, 31)

        self.assertTrue(d1 > d2)
        self.assertTrue(d1 > d3)

    def test_greater_than_false(self):
        d1 = Pendulum(2000, 1, 1)
        d2 = Pendulum(2000, 1, 2)
        d3 = datetime(2000, 1, 2)

        self.assertFalse(d1 > d2)
        self.assertFalse(d1 > d3)

    def test_greater_than_with_timezone_true(self):
        d1 = Pendulum(2000, 1, 1, 12, 0, 0, tzinfo='America/Toronto')
        d2 = Pendulum(2000, 1, 1, 8, 59, 59, tzinfo='America/Vancouver')
        d3 = pytz.timezone('America/Vancouver').localize(datetime(2000, 1, 1, 8, 59, 59))

        self.assertTrue(d1 > d2)
        self.assertTrue(d1 > d3)

    def test_greater_than_with_timezone_false(self):
        d1 = Pendulum(2000, 1, 1, 12, 0, 0, tzinfo='America/Toronto')
        d2 = Pendulum(2000, 1, 1, 9, 0, 1, tzinfo='America/Vancouver')
        d3 = pytz.timezone('America/Vancouver').localize(datetime(2000, 1, 1, 9, 0, 1))

        self.assertFalse(d1 > d2)
        self.assertFalse(d1 > d3)

    def test_greater_than_or_equal_true(self):
        d1 = Pendulum(2000, 1, 1)
        d2 = Pendulum(1999, 12, 31)
        d3 = datetime(1999, 12, 31)

        self.assertTrue(d1 >= d2)
        self.assertTrue(d1 >= d3)

    def test_greater_than_or_equal_true_equal(self):
        d1 = Pendulum(2000, 1, 1)
        d2 = Pendulum(2000, 1, 1)
        d3 = datetime(2000, 1, 1)

        self.assertTrue(d1 >= d2)
        self.assertTrue(d1 >= d3)

    def test_greater_than_or_equal_false(self):
        d1 = Pendulum(2000, 1, 1)
        d2 = Pendulum(2000, 1, 2)
        d3 = datetime(2000, 1, 2)

        self.assertFalse(d1 >= d2)
        self.assertFalse(d1 >= d3)

    def test_greater_than_or_equal_with_timezone_true(self):
        d1 = Pendulum(2000, 1, 1, 12, 0, 0, tzinfo='America/Toronto')
        d2 = Pendulum(2000, 1, 1, 8, 59, 59, tzinfo='America/Vancouver')
        d3 = pytz.timezone('America/Vancouver').localize(datetime(2000, 1, 1, 8, 59, 59))

        self.assertTrue(d1 >= d2)
        self.assertTrue(d1 >= d3)

    def test_greater_than_or_equal_with_timezone_false(self):
        d1 = Pendulum(2000, 1, 1, 12, 0, 0, tzinfo='America/Toronto')
        d2 = Pendulum(2000, 1, 1, 9, 0, 1, tzinfo='America/Vancouver')
        d3 = pytz.timezone('America/Vancouver').localize(datetime(2000, 1, 1, 9, 0, 1))

        self.assertFalse(d1 >= d2)
        self.assertFalse(d1 >= d3)

    def test_less_than_true(self):
        d1 = Pendulum(2000, 1, 1)
        d2 = Pendulum(2000, 1, 2)
        d3 = datetime(2000, 1, 2)

        self.assertTrue(d1 < d2)
        self.assertTrue(d1 < d3)

    def test_less_than_false(self):
        d1 = Pendulum(2000, 1, 2)
        d2 = Pendulum(2000, 1, 1)
        d3 = datetime(2000, 1, 1)

        self.assertFalse(d1 < d2)
        self.assertFalse(d1 < d3)

    def test_less_than_with_timezone_true(self):
        d1 = Pendulum(2000, 1, 1, 8, 59, 59, tzinfo='America/Vancouver')
        d2 = Pendulum(2000, 1, 1, 12, 0, 0, tzinfo='America/Toronto')
        d3 = pytz.timezone('America/Toronto').localize(datetime(2000, 1, 1, 12, 0, 0))

        self.assertTrue(d1 < d2)
        self.assertTrue(d1 < d3)

    def test_less_than_with_timezone_false(self):
        d1 = Pendulum(2000, 1, 1, 9, 0, 1, tzinfo='America/Vancouver')
        d2 = Pendulum(2000, 1, 1, 12, 0, 0, tzinfo='America/Toronto')
        d3 = pytz.timezone('America/Toronto').localize(datetime(2000, 1, 1, 12, 0, 0))

        self.assertFalse(d1 < d2)
        self.assertFalse(d1 < d3)

    def test_less_than_or_equal_true(self):
        d1 = Pendulum(2000, 1, 1)
        d2 = Pendulum(2000, 1, 2)
        d3 = datetime(2000, 1, 2)

        self.assertTrue(d1 <= d2)
        self.assertTrue(d1 <= d3)

    def test_less_than_or_equal_true_equal(self):
        d1 = Pendulum(2000, 1, 1)
        d2 = Pendulum(2000, 1, 1)
        d3 = datetime(2000, 1, 1)

        self.assertTrue(d1 <= d2)
        self.assertTrue(d1 <= d3)

    def test_less_than_or_equal_false(self):
        d1 = Pendulum(2000, 1, 2)
        d2 = Pendulum(2000, 1, 1)
        d3 = datetime(2000, 1, 1)

        self.assertFalse(d1 <= d2)
        self.assertFalse(d1 <= d3)

    def test_less_than_or_equal_with_timezone_true(self):
        d1 = Pendulum(2000, 1, 1, 8, 59, 59, tzinfo='America/Vancouver')
        d2 = Pendulum(2000, 1, 1, 12, 0, 0, tzinfo='America/Toronto')
        d3 = pytz.timezone('America/Toronto').localize(datetime(2000, 1, 1, 12, 0, 0))

        self.assertTrue(d1 <= d2)
        self.assertTrue(d1 <= d3)

    def test_less_than_or_equal_with_timezone_false(self):
        d1 = Pendulum(2000, 1, 1, 9, 0, 1, tzinfo='America/Vancouver')
        d2 = Pendulum(2000, 1, 1, 12, 0, 0, tzinfo='America/Toronto')
        d3 = pytz.timezone('America/Toronto').localize(datetime(2000, 1, 1, 12, 0, 0))

        self.assertFalse(d1 <= d2)
        self.assertFalse(d1 <= d3)

    def test_between_equal_true(self):
        d1 = Pendulum(2000, 1, 15)
        d2 = Pendulum(2000, 1, 1)
        d3 = Pendulum(2000, 1, 31)
        d4 = datetime(2000, 1, 1)
        d5 = datetime(2000, 1, 31)

        self.assertTrue(d1.between(d2, d3))
        self.assertTrue(d1.between(d4, d5))

    def test_between_not_equal_true(self):
        d1 = Pendulum(2000, 1, 15)
        d2 = Pendulum(2000, 1, 1)
        d3 = Pendulum(2000, 1, 31)
        d4 = datetime(2000, 1, 1)
        d5 = datetime(2000, 1, 31)

        self.assertTrue(d1.between(d2, d3, False))
        self.assertTrue(d1.between(d4, d5, False))

    def test_between_equal_false(self):
        d1 = Pendulum(1999, 12, 31)
        d2 = Pendulum(2000, 1, 1)
        d3 = Pendulum(2000, 1, 31)
        d4 = datetime(2000, 1, 1)
        d5 = datetime(2000, 1, 31)

        self.assertFalse(d1.between(d2, d3))
        self.assertFalse(d1.between(d4, d5))

    def test_between_not_equal_false(self):
        d1 = Pendulum(2000, 1, 1)
        d2 = Pendulum(2000, 1, 1)
        d3 = Pendulum(2000, 1, 31)
        d4 = datetime(2000, 1, 1)
        d5 = datetime(2000, 1, 31)

        self.assertFalse(d1.between(d2, d3, False))
        self.assertFalse(d1.between(d4, d5, False))

    def test_between_equal_switch_true(self):
        d1 = Pendulum(2000, 1, 15)
        d2 = Pendulum(2000, 1, 1)
        d3 = Pendulum(2000, 1, 31)
        d4 = datetime(2000, 1, 1)
        d5 = datetime(2000, 1, 31)

        self.assertTrue(d1.between(d3, d2))
        self.assertTrue(d1.between(d5, d4))

    def test_between_not_equal_switch_true(self):
        d1 = Pendulum(2000, 1, 15)
        d2 = Pendulum(2000, 1, 1)
        d3 = Pendulum(2000, 1, 31)
        d4 = datetime(2000, 1, 1)
        d5 = datetime(2000, 1, 31)

        self.assertTrue(d1.between(d3, d2, False))
        self.assertTrue(d1.between(d5, d4, False))

    def test_between_equal_switch_false(self):
        d1 = Pendulum(1999, 12, 31)
        d2 = Pendulum(2000, 1, 1)
        d3 = Pendulum(2000, 1, 31)
        d4 = datetime(2000, 1, 1)
        d5 = datetime(2000, 1, 31)

        self.assertFalse(d1.between(d3, d2))
        self.assertFalse(d1.between(d5, d4))

    def test_between_not_equal_switch_false(self):
        d1 = Pendulum(2000, 1, 1)
        d2 = Pendulum(2000, 1, 1)
        d3 = Pendulum(2000, 1, 31)
        d4 = datetime(2000, 1, 1)
        d5 = datetime(2000, 1, 31)

        self.assertFalse(d1.between(d3, d2, False))
        self.assertFalse(d1.between(d5, d4, False))

    def test_between_issue_39(self):
        old = Pendulum.instance(datetime.utcnow())
        sleep(0.2)
        mid = Pendulum.now('UTC')
        sleep(0.2)
        new = Pendulum.instance(datetime.utcnow())

        self.assertTrue(mid.between(old, new))

    def test_min_is_fluid(self):
        d = Pendulum.now()
        self.assertIsInstanceOfPendulum(d.min_())
        self.assertIsInstanceOfPendulum(d.min_(datetime(1975, 1, 1)))
        self.assertIsInstanceOfPendulum(d.minimum())
        self.assertIsInstanceOfPendulum(d.minimum(datetime(1975, 1, 1)))

    def test_min_with_now(self):
        d = Pendulum(2012, 1, 1, 0, 0, 0).min_()
        self.assertPendulum(d, 2012, 1, 1, 0, 0, 0)
        d = Pendulum(2012, 1, 1, 0, 0, 0).minimum()
        self.assertPendulum(d, 2012, 1, 1, 0, 0, 0)

    def test_min_with_instance(self):
        d1 = Pendulum(2013, 12, 31, 23, 59, 59)
        d2 = Pendulum(2012, 1, 1, 0, 0, 0).min_(d1)
        self.assertPendulum(d2, 2012, 1, 1, 0, 0, 0)
        d2 = Pendulum(2012, 1, 1, 0, 0, 0).minimum(d1)
        self.assertPendulum(d2, 2012, 1, 1, 0, 0, 0)

    def test_max_is_fluid(self):
        d = Pendulum.now()
        self.assertIsInstanceOfPendulum(d.max_())
        self.assertIsInstanceOfPendulum(d.max_(datetime(2099, 12, 31, 23, 59, 59)))
        self.assertIsInstanceOfPendulum(d.maximum())
        self.assertIsInstanceOfPendulum(d.maximum(datetime(2099, 12, 31, 23, 59, 59)))

    def test_max_with_now(self):
        d = Pendulum(2099, 12, 31, 23, 59, 59).max_()
        self.assertPendulum(d, 2099, 12, 31, 23, 59, 59)
        d = Pendulum(2099, 12, 31, 23, 59, 59).maximum()
        self.assertPendulum(d, 2099, 12, 31, 23, 59, 59)

    def test_max_with_instance(self):
        d1 = Pendulum(2012, 1, 1, 0, 0, 0)
        d2 = Pendulum(2099, 12, 31, 23, 59, 59).max_(d1)
        self.assertPendulum(d2, 2099, 12, 31, 23, 59, 59)
        d2 = Pendulum(2099, 12, 31, 23, 59, 59).maximum(d1)
        self.assertPendulum(d2, 2099, 12, 31, 23, 59, 59)

    def test_is_birthday(self):
        with self.wrap_with_test_now():
            d = Pendulum.now()
            a_birthday = d.subtract(years=1)
            self.assertTrue(a_birthday.is_birthday())
            not_a_birthday = d.subtract(days=1)
            self.assertFalse(not_a_birthday.is_birthday())
            also_not_a_birthday = d.add(days=2)
            self.assertFalse(also_not_a_birthday.is_birthday())

        d1 = Pendulum(1987, 4, 23)
        d2 = Pendulum(2014, 9, 26)
        d3 = Pendulum(2014, 4, 23)
        self.assertFalse(d2.is_birthday(d1))
        self.assertTrue(d3.is_birthday(d1))

    def test_closest(self):
        instance = Pendulum.create(2015, 5, 28, 12, 0, 0)
        dt1 = Pendulum.create(2015, 5, 28, 11, 0, 0)
        dt2 = Pendulum.create(2015, 5, 28, 14, 0, 0)
        closest = instance.closest(dt1, dt2)
        self.assertEqual(dt1, closest)

        closest = instance.closest(dt2, dt1)
        self.assertEqual(dt1, closest)

    def test_closest_with_datetime(self):
        instance = Pendulum.create(2015, 5, 28, 12, 0, 0)
        dt1 = datetime(2015, 5, 28, 11, 0, 0)
        dt2 = datetime(2015, 5, 28, 14, 0, 0)
        closest = instance.closest(dt1, dt2)
        self.assertIsInstanceOfPendulum(closest)
        self.assertPendulum(closest, 2015, 5, 28, 11, 0, 0)

    def test_closest_with_equals(self):
        instance = Pendulum.create(2015, 5, 28, 12, 0, 0)
        dt1 = Pendulum.create(2015, 5, 28, 12, 0, 0)
        dt2 = Pendulum.create(2015, 5, 28, 14, 0, 0)
        closest = instance.closest(dt1, dt2)
        self.assertEqual(dt1, closest)

    def test_farthest(self):
        instance = Pendulum.create(2015, 5, 28, 12, 0, 0)
        dt1 = Pendulum.create(2015, 5, 28, 11, 0, 0)
        dt2 = Pendulum.create(2015, 5, 28, 14, 0, 0)
        closest = instance.farthest(dt1, dt2)
        self.assertEqual(dt2, closest)

        closest = instance.farthest(dt2, dt1)
        self.assertEqual(dt2, closest)

    def test_farthest_with_datetime(self):
        instance = Pendulum.create(2015, 5, 28, 12, 0, 0)
        dt1 = datetime(2015, 5, 28, 11, 0, 0)
        dt2 = datetime(2015, 5, 28, 14, 0, 0)
        closest = instance.farthest(dt1, dt2)
        self.assertIsInstanceOfPendulum(closest)
        self.assertPendulum(closest, 2015, 5, 28, 14, 0, 0)

    def test_farthest_with_equals(self):
        instance = Pendulum.create(2015, 5, 28, 12, 0, 0)
        dt1 = Pendulum.create(2015, 5, 28, 12, 0, 0)
        dt2 = Pendulum.create(2015, 5, 28, 14, 0, 0)
        closest = instance.farthest(dt1, dt2)
        self.assertEqual(dt2, closest)

    def test_is_same_day(self):
        dt1 = Pendulum.create(2015, 5, 28, 12, 0, 0)
        dt2 = Pendulum.create(2015, 5, 29, 12, 0, 0)
        dt3 = Pendulum.create(2015, 5, 28, 12, 0, 0)
        dt4 = datetime(2015, 5, 28, 12, 0, 0)
        dt5 = datetime(2015, 5, 29, 12, 0, 0)

        self.assertFalse(dt1.is_same_day(dt2))
        self.assertTrue(dt1.is_same_day(dt3))
        self.assertTrue(dt1.is_same_day(dt4))
        self.assertFalse(dt1.is_same_day(dt5))

    def test_comparison_to_unsupported(self):
        dt1 = Pendulum.now()

        self.assertFalse(dt1 == 'test')
        self.assertFalse(dt1 in ['test'])
