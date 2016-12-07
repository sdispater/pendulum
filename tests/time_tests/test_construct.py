# -*- coding: utf-8 -*-

from datetime import time
from pendulum import Time, timezone

from .. import AbstractTestCase


class ConstructTest(AbstractTestCase):

    def test_init(self):
        t = Time(12, 34, 56, 123456)

        self.assertIsInstanceOfTime(t)
        self.assertTime(t, 12, 34, 56, 123456)

    def test_init_with_missing_values(self):
        t = Time(12, 34, 56)

        self.assertTime(t, 12, 34, 56, 0)

        t = Time(12, 34)

        self.assertTime(t, 12, 34, 0, 0)

        t = Time(12)

        self.assertTime(t, 12, 0, 0, 0)

    def test_instance(self):
        native = time(12, 34, 56, 123456)
        t = Time.instance(native)

        self.assertIsInstanceOfTime(t)
        self.assertTime(t, 12, 34, 56, 123456)

    def test_instance_aware(self):
        tz = timezone('Europe/Paris')
        native = time(12, 34, 56, 123456, tzinfo=tz)

        self.assertEqual('Europe/Paris', Time.instance(native).tzinfo.name)

    def test_now(self):
        t = Time.now()

        self.assertIsInstanceOfTime(t)

    def test_now_microseconds(self):
        with Time.test(Time(1, 2, 3, 123456)):
            t = Time.now()
            self.assertTime(t, 1, 2, 3, 123456)

            t = Time.now(False)
            self.assertTime(t, 1, 2, 3, 0)
