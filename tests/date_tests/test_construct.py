# -*- coding: utf-8 -*-

from datetime import date
from pendulum import Date

from .. import AbstractTestCase


class ConstructTest(AbstractTestCase):

    def test_construct(self):
        d = Date(2016, 10, 20)

        self.assertIsInstanceOfDate(d)
        self.assertDate(d, 2016, 10, 20)

    def test_today(self):
        d = Date.today()

        self.assertIsInstanceOfDate(d)

    def test_instance(self):
        d = Date.instance(date(2016, 10, 20))

        self.assertIsInstanceOfDate(d)
        self.assertDate(d, 2016, 10, 20)

    def test_create(self):
        d = Date.create(2016, 10, 20)

        self.assertIsInstanceOfDate(d)
        self.assertDate(d, 2016, 10, 20)

    def test_create_empty_values(self):
        now = Date.today()
        d = Date.create()

        self.assertIsInstanceOfDate(d)
        self.assertDate(d, now.year, now.month, now.day)
