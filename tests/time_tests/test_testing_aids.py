# -*- coding: utf-8 -*-

from pendulum import Time, Date, Pendulum

from .. import AbstractTestCase


class TestingAidsTest(AbstractTestCase):

    def test_testing_aids_with_test_now_not_set(self):
        Time.set_test_now()

        self.assertFalse(Time.has_test_now())
        self.assertIsNone(Time.get_test_now())

    def test_testing_aids_with_test_now_set(self):
        test_now = Time.now().subtract(hours=1)
        Time.set_test_now(test_now)

        self.assertTrue(Time.has_test_now())
        self.assertEqual(test_now, Time.get_test_now())

    def test_constructor_with_test_value_set(self):
        test_now = Time.now().subtract(hours=1)
        Time.set_test_now(test_now)

        self.assertEqual(test_now, Time.now())

    def test_now_with_test_value_set(self):
        test_now = Time.now().subtract(hours=1)
        Time.set_test_now(test_now)

        self.assertEqual(test_now, Time.now())

    def test_context_manager(self):
        test_now = Time.now().subtract(hours=1)

        with Time.test(test_now):
            self.assertEqual(test_now, Time.now())

        self.assertNotEqual(test_now, Time.now())

    def test_set_test_now_pendulum_instance(self):
        test_now = Pendulum(2000, 11, 10, 12, 34, 56, 123456)

        Time.set_test_now(test_now)

        self.assertTime(Time.now(), 12, 34, 56, 123456)

    def test_set_test_now_wrong_type(self):
        self.assertRaises(TypeError, Time.set_test_now, Date.today())
