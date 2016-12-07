# -*- coding: utf-8 -*-

from pendulum import Date, Pendulum, Time

from .. import AbstractTestCase


class TestingAidsTest(AbstractTestCase):

    def test_testing_aids_with_test_now_not_set(self):
        Date.set_test_now()

        self.assertFalse(Date.has_test_now())
        self.assertIsNone(Date.get_test_now())

    def test_testing_aids_with_test_now_set(self):
        test_now = Date.yesterday()
        Date.set_test_now(test_now)

        self.assertTrue(Date.has_test_now())
        self.assertEqual(test_now, Date.get_test_now())

    def test_constructor_with_test_value_set(self):
        test_now = Date.yesterday()
        Date.set_test_now(test_now)

        self.assertEqual(test_now, Date.today())

    def test_now_with_test_value_set(self):
        test_now = Date.yesterday()
        Date.set_test_now(test_now)

        self.assertEqual(test_now, Date.today())

    def test_context_manager(self):
        test_now = Date.yesterday()

        with Date.test(test_now):
            self.assertEqual(test_now, Date.today())

        self.assertNotEqual(test_now, Date.today())

    def test_set_test_now_pendulum_instance(self):
        test_now = Pendulum(2000, 11, 10, 12, 34, 56, 123456)

        Date.set_test_now(test_now)

        self.assertDate(Date.today(), 2000, 11, 10)

    def test_set_test_now_wrong_type(self):
        self.assertRaises(TypeError, Date.set_test_now, Time.now())
