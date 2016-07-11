# -*- coding: utf-8 -*-

from pendulum import Pendulum

from .. import AbstractTestCase


class TestingAidsTest(AbstractTestCase):

    def test_testing_aids_with_test_now_not_set(self):
        Pendulum.set_test_now()

        self.assertFalse(Pendulum.has_test_now())
        self.assertIsNone(Pendulum.get_test_now())

    def test_testing_aids_with_test_now_set(self):
        test_now = Pendulum.yesterday()
        Pendulum.set_test_now(test_now)

        self.assertTrue(Pendulum.has_test_now())
        self.assertEqual(test_now, Pendulum.get_test_now())

    def test_constructor_with_test_value_set(self):
        test_now = Pendulum.yesterday()
        Pendulum.set_test_now(test_now)

        self.assertEqual(test_now, Pendulum.now())

    def test_now_with_test_value_set(self):
        test_now = Pendulum.yesterday()
        Pendulum.set_test_now(test_now)

        self.assertEqual(test_now, Pendulum.now())

    def test_parse_with_test_value_set(self):
        test_now = Pendulum.yesterday()
        Pendulum.set_test_now(test_now)

        self.assertEqual(test_now, Pendulum.parse())
        self.assertEqual(test_now, Pendulum.parse('now'))

    def test_context_manager(self):
        test_now = Pendulum.yesterday()

        with Pendulum.test(test_now):
            self.assertEqual(test_now, Pendulum.now())

        self.assertNotEqual(test_now, Pendulum.now())
