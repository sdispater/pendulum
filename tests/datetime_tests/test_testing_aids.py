# -*- coding: utf-8 -*-

from pendulum import DateTime

from .. import AbstractTestCase


class TestingAidsTest(AbstractTestCase):

    def test_testing_aids_with_test_now_not_set(self):
        DateTime.set_test_now()

        self.assertFalse(DateTime.has_test_now())
        self.assertIsNone(DateTime.get_test_now())

    def test_testing_aids_with_test_now_set(self):
        test_now = DateTime.yesterday()
        DateTime.set_test_now(test_now)

        self.assertTrue(DateTime.has_test_now())
        self.assertEqual(test_now, DateTime.get_test_now())

    def test_constructor_with_test_value_set(self):
        test_now = DateTime.yesterday()
        DateTime.set_test_now(test_now)

        self.assertEqual(test_now, DateTime.now())

    def test_now_with_test_value_set(self):
        test_now = DateTime.yesterday()
        DateTime.set_test_now(test_now)

        self.assertEqual(test_now, DateTime.now())

    def test_parse_with_test_value_set(self):
        test_now = DateTime.yesterday()
        DateTime.set_test_now(test_now)

        self.assertEqual(test_now, DateTime.parse())
        self.assertEqual(test_now, DateTime.parse('now'))

    def test_context_manager(self):
        test_now = DateTime.yesterday()

        with DateTime.test(test_now):
            self.assertEqual(test_now, DateTime.now())

        self.assertNotEqual(test_now, DateTime.now())
