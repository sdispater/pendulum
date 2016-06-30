# -*- coding: utf-8 -*-

from pendulum import Pendulum

from .. import AbstractTestCase


class StartEndOfTest(AbstractTestCase):

    def test_start_of_day(self):
        d = Pendulum.now()
        self.assertIsInstanceOfPendulum(d.start_of_day())
        self.assertPendulum(d, d.year, d.month, d.day, 0, 0, 0)

    def test_end_of_day(self):
        d = Pendulum.now()
        self.assertIsInstanceOfPendulum(d.end_of_day())
        self.assertPendulum(d, d.year, d.month, d.day, 23, 59, 59)

    def test_start_of_month_is_fluid(self):
        d = Pendulum.now()
        self.assertIsInstanceOfPendulum(d.start_of_month())

    def test_start_of_month_from_now(self):
        d = Pendulum.now().start_of_month()
        self.assertPendulum(d, d.year, d.month, 1, 0, 0, 0)

    def test_start_of_month_from_last_day(self):
        d = Pendulum(2000, 1, 31, 2, 3, 4).start_of_month()
        self.assertPendulum(d, 2000, 1, 1, 0, 0, 0)

    def test_start_of_year_is_fluid(self):
        d = Pendulum.now()
        self.assertIsInstanceOfPendulum(d.start_of_year())

    def test_start_of_year_from_now(self):
        d = Pendulum.now().start_of_year()
        self.assertPendulum(d, d.year, 1, 1, 0, 0, 0)

    def test_start_of_year_from_first_day(self):
        d = Pendulum(2000, 1, 1, 1, 1, 1).start_of_year()
        self.assertPendulum(d, 2000, 1, 1, 0, 0, 0)

    def test_start_of_year_from_last_day(self):
        d = Pendulum(2000, 12, 31, 23, 59, 59).start_of_year()
        self.assertPendulum(d, 2000, 1, 1, 0, 0, 0)

    def test_end_of_month_is_fluid(self):
        d = Pendulum.now()
        self.assertIsInstanceOfPendulum(d.end_of_month())

    def test_end_of_month_from_now(self):
        d = Pendulum.now().start_of_month()
        self.assertPendulum(d, d.year, d.month, 1, 0, 0, 0)

    def test_end_of_month(self):
        d = Pendulum(2000, 1, 1, 2, 3, 4).end_of_month()
        self.assertPendulum(d, 2000, 1, 31, 23, 59, 59)

    def test_end_of_month_from_last_day(self):
        d = Pendulum(2000, 1, 31, 2, 3, 4).end_of_month()
        self.assertPendulum(d, 2000, 1, 31, 23, 59, 59)

    def test_end_of_year_is_fluid(self):
        d = Pendulum.now()
        self.assertIsInstanceOfPendulum(d.end_of_year())

    def test_end_of_year_from_now(self):
        d = Pendulum.now().end_of_year()
        self.assertPendulum(d, d.year, 12, 31, 23, 59, 59)

    def test_end_of_year_from_first_day(self):
        d = Pendulum(2000, 1, 1, 1, 1, 1).end_of_year()
        self.assertPendulum(d, 2000, 12, 31, 23, 59, 59)

    def test_end_of_year_from_last_day(self):
        d = Pendulum(2000, 12, 31, 23, 59, 59).end_of_year()
        self.assertPendulum(d, 2000, 12, 31, 23, 59, 59)

    def test_start_of_decade_is_fluid(self):
        d = Pendulum.now()
        self.assertIsInstanceOfPendulum(d.start_of_decade())

    def test_start_of_decade_from_now(self):
        d = Pendulum.now().start_of_decade()
        self.assertPendulum(d, d.year - d.year % 10, 1, 1, 0, 0, 0)

    def test_start_of_decade_from_first_day(self):
        d = Pendulum(2000, 1, 1, 1, 1, 1).start_of_decade()
        self.assertPendulum(d, 2000, 1, 1, 0, 0, 0)

    def test_start_of_decade_from_last_day(self):
        d = Pendulum(2009, 12, 31, 23, 59, 59).start_of_decade()
        self.assertPendulum(d, 2000, 1, 1, 0, 0, 0)

    def test_end_of_decade_is_fluid(self):
        d = Pendulum.now()
        self.assertIsInstanceOfPendulum(d.end_of_decade())

    def test_end_of_decade_from_now(self):
        d = Pendulum.now().end_of_decade()
        self.assertPendulum(d, d.year - d.year % 10 + 9, 12, 31, 23, 59, 59)

    def test_end_of_decade_from_first_day(self):
        d = Pendulum(2000, 1, 1, 1, 1, 1).end_of_decade()
        self.assertPendulum(d, 2009, 12, 31, 23, 59, 59)

    def test_end_of_decade_from_last_day(self):
        d = Pendulum(2009, 12, 31, 23, 59, 59).end_of_decade()
        self.assertPendulum(d, 2009, 12, 31, 23, 59, 59)

    def test_start_of_century_is_fluid(self):
        d = Pendulum.now()
        self.assertIsInstanceOfPendulum(d.start_of_century())

    def test_start_of_century_from_now(self):
        d = Pendulum.now().start_of_century()
        self.assertPendulum(d, d.year - d.year % 100 + 1, 1, 1, 0, 0, 0)

    def test_start_of_century_from_first_day(self):
        d = Pendulum(2001, 1, 1, 1, 1, 1).start_of_century()
        self.assertPendulum(d, 2001, 1, 1, 0, 0, 0)

    def test_start_of_century_from_last_day(self):
        d = Pendulum(2100, 12, 31, 23, 59, 59).start_of_century()
        self.assertPendulum(d, 2001, 1, 1, 0, 0, 0)

    def test_end_of_century_is_fluid(self):
        d = Pendulum.now()
        self.assertIsInstanceOfPendulum(d.end_of_century())

    def test_end_of_century_from_now(self):
        now = Pendulum.now()
        d = Pendulum.now().end_of_century()
        self.assertPendulum(d, now.year - now.year % 100 + 100, 12, 31, 23, 59, 59)

    def test_end_of_century_from_first_day(self):
        d = Pendulum(2001, 1, 1, 1, 1, 1).end_of_century()
        self.assertPendulum(d, 2100, 12, 31, 23, 59, 59)

    def test_end_of_century_from_last_day(self):
        d = Pendulum(2100, 12, 31, 23, 59, 59).end_of_century()
        self.assertPendulum(d, 2100, 12, 31, 23, 59, 59)

    def test_average_is_fluid(self):
        self.skipTest('Not Implemented')

    def test_average_from_same(self):
        self.skipTest('Not Implemented')

    def test_average_from_greater(self):
        self.skipTest('Not Implemented')

    def test_average_from_lower(self):
        self.skipTest('Not Implemented')
