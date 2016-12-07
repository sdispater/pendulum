# -*- coding: utf-8 -*-

from pendulum import Pendulum

from .. import AbstractTestCase


class StartEndOfTest(AbstractTestCase):

    def test_start_of_second(self):
        d = Pendulum.now()
        new = d.start_of('second')
        self.assertIsInstanceOfPendulum(new)
        self.assertPendulum(new, d.year, d.month, d.day, d.hour, d.minute, d.second, 0)

    def test_end_of_second(self):
        d = Pendulum.now()
        new = d.end_of('second')
        self.assertIsInstanceOfPendulum(new)
        self.assertPendulum(new, d.year, d.month, d.day, d.hour, d.minute, d.second, 999999)

    def test_start_of_minute(self):
        d = Pendulum.now()
        new = d.start_of('minute')
        self.assertIsInstanceOfPendulum(new)
        self.assertPendulum(new, d.year, d.month, d.day, d.hour, d.minute, 0, 0)

    def test_end_of_minute(self):
        d = Pendulum.now()
        new = d.end_of('minute')
        self.assertIsInstanceOfPendulum(new)
        self.assertPendulum(new, d.year, d.month, d.day, d.hour, d.minute, 59, 999999)

    def test_start_of_hour(self):
        d = Pendulum.now()
        new = d.start_of('hour')
        self.assertIsInstanceOfPendulum(new)
        self.assertPendulum(new, d.year, d.month, d.day, d.hour, 0, 0, 0)

    def test_end_of_hour(self):
        d = Pendulum.now()
        new = d.end_of('hour')
        self.assertIsInstanceOfPendulum(new)
        self.assertPendulum(new, d.year, d.month, d.day, d.hour, 59, 59, 999999)

    def test_start_of_day(self):
        d = Pendulum.now()
        new = d.start_of('day')
        self.assertIsInstanceOfPendulum(new)
        self.assertPendulum(new, d.year, d.month, d.day, 0, 0, 0)

    def test_end_of_day(self):
        d = Pendulum.now()
        new = d.end_of('day')
        self.assertIsInstanceOfPendulum(new)
        self.assertPendulum(new, d.year, d.month, d.day, 23, 59, 59, 999999)

    def test_start_of_month_is_fluid(self):
        d = Pendulum.now()
        self.assertIsInstanceOfPendulum(d.start_of('month'))

    def test_start_of_month_from_now(self):
        d = Pendulum.now()
        new = d.start_of('month')
        self.assertPendulum(new, d.year, d.month, 1, 0, 0, 0)

    def test_start_of_month_from_last_day(self):
        d = Pendulum(2000, 1, 31, 2, 3, 4)
        new = d.start_of('month')
        self.assertPendulum(new, 2000, 1, 1, 0, 0, 0)

    def test_start_of_year_is_fluid(self):
        d = Pendulum.now()
        new = d.start_of('year')
        self.assertIsInstanceOfPendulum(new)

    def test_start_of_year_from_now(self):
        d = Pendulum.now()
        new = d.start_of('year')
        self.assertPendulum(new, d.year, 1, 1, 0, 0, 0)

    def test_start_of_year_from_first_day(self):
        d = Pendulum(2000, 1, 1, 1, 1, 1)
        new = d.start_of('year')
        self.assertPendulum(new, 2000, 1, 1, 0, 0, 0)

    def test_start_of_year_from_last_day(self):
        d = Pendulum(2000, 12, 31, 23, 59, 59)
        new = d.start_of('year')
        self.assertPendulum(new, 2000, 1, 1, 0, 0, 0)

    def test_end_of_month_is_fluid(self):
        d = Pendulum.now()
        self.assertIsInstanceOfPendulum(d.end_of('month'))

    def test_end_of_month_from_now(self):
        d = Pendulum.now().start_of('month')
        new = d.start_of('month')
        self.assertPendulum(new, d.year, d.month, 1, 0, 0, 0)

    def test_end_of_month(self):
        d = Pendulum(2000, 1, 1, 2, 3, 4).end_of('month')
        new = d.end_of('month')
        self.assertPendulum(new, 2000, 1, 31, 23, 59, 59)

    def test_end_of_month_from_last_day(self):
        d = Pendulum(2000, 1, 31, 2, 3, 4)
        new = d.end_of('month')
        self.assertPendulum(new, 2000, 1, 31, 23, 59, 59)

    def test_end_of_year_is_fluid(self):
        d = Pendulum.now()
        self.assertIsInstanceOfPendulum(d.end_of('year'))

    def test_end_of_year_from_now(self):
        d = Pendulum.now().end_of('year')
        new = d.end_of('year')
        self.assertPendulum(new, d.year, 12, 31, 23, 59, 59, 999999)

    def test_end_of_year_from_first_day(self):
        d = Pendulum(2000, 1, 1, 1, 1, 1)
        new = d.end_of('year')
        self.assertPendulum(new, 2000, 12, 31, 23, 59, 59, 999999)

    def test_end_of_year_from_last_day(self):
        d = Pendulum(2000, 12, 31, 23, 59, 59, 999999)
        new = d.end_of('year')
        self.assertPendulum(new, 2000, 12, 31, 23, 59, 59, 999999)

    def test_start_of_decade_is_fluid(self):
        d = Pendulum.now()
        self.assertIsInstanceOfPendulum(d.start_of('decade'))

    def test_start_of_decade_from_now(self):
        d = Pendulum.now()
        new = d.start_of('decade')
        self.assertPendulum(new, d.year - d.year % 10, 1, 1, 0, 0, 0)

    def test_start_of_decade_from_first_day(self):
        d = Pendulum(2000, 1, 1, 1, 1, 1)
        new = d.start_of('decade')
        self.assertPendulum(new, 2000, 1, 1, 0, 0, 0)

    def test_start_of_decade_from_last_day(self):
        d = Pendulum(2009, 12, 31, 23, 59, 59)
        new = d.start_of('decade')
        self.assertPendulum(new, 2000, 1, 1, 0, 0, 0)

    def test_end_of_decade_is_fluid(self):
        d = Pendulum.now()
        self.assertIsInstanceOfPendulum(d.end_of('decade'))

    def test_end_of_decade_from_now(self):
        d = Pendulum.now()
        new  = d.end_of('decade')
        self.assertPendulum(new, d.year - d.year % 10 + 9, 12, 31, 23, 59, 59, 999999)

    def test_end_of_decade_from_first_day(self):
        d = Pendulum(2000, 1, 1, 1, 1, 1)
        new = d.end_of('decade')
        self.assertPendulum(new, 2009, 12, 31, 23, 59, 59, 999999)

    def test_end_of_decade_from_last_day(self):
        d = Pendulum(2009, 12, 31, 23, 59, 59, 999999)
        new = d.end_of('decade')
        self.assertPendulum(new, 2009, 12, 31, 23, 59, 59, 999999)

    def test_start_of_century_is_fluid(self):
        d = Pendulum.now()
        self.assertIsInstanceOfPendulum(d.start_of('century'))

    def test_start_of_century_from_now(self):
        d = Pendulum.now()
        new = d.start_of('century')
        self.assertPendulum(new, d.year - d.year % 100 + 1, 1, 1, 0, 0, 0)

    def test_start_of_century_from_first_day(self):
        d = Pendulum(2001, 1, 1, 1, 1, 1)
        new = d.start_of('century')
        self.assertPendulum(new, 2001, 1, 1, 0, 0, 0)

    def test_start_of_century_from_last_day(self):
        d = Pendulum(2100, 12, 31, 23, 59, 59)
        new = d.start_of('century')
        self.assertPendulum(new, 2001, 1, 1, 0, 0, 0)

    def test_end_of_century_is_fluid(self):
        d = Pendulum.now()
        self.assertIsInstanceOfPendulum(d.end_of('century'))

    def test_end_of_century_from_now(self):
        now = Pendulum.now()
        d = now.end_of('century')
        self.assertPendulum(d, now.year - now.year % 100 + 100, 12, 31, 23, 59, 59, 999999)

    def test_end_of_century_from_first_day(self):
        d = Pendulum(2001, 1, 1, 1, 1, 1)
        new = d.end_of('century')
        self.assertPendulum(new, 2100, 12, 31, 23, 59, 59, 999999)

    def test_end_of_century_from_last_day(self):
        d = Pendulum(2100, 12, 31, 23, 59, 59, 999999)
        new = d.end_of('century')
        self.assertPendulum(new, 2100, 12, 31, 23, 59, 59, 999999)

    def test_average_is_fluid(self):
        d = Pendulum.now().average()
        self.assertIsInstanceOfPendulum(d)

    def test_average_from_same(self):
        d1 = Pendulum.create(2000, 1, 31, 2, 3, 4)
        d2 = Pendulum.create(2000, 1, 31, 2, 3, 4).average(d1)
        self.assertPendulum(d2, 2000, 1, 31, 2, 3, 4)

    def test_average_from_greater(self):
        d1 = Pendulum.create(2000, 1, 1, 1, 1, 1, tz='local')
        d2 = Pendulum.create(2009, 12, 31, 23, 59, 59, tz='local').average(d1)
        self.assertPendulum(d2, 2004, 12, 31, 12, 30, 30)

    def test_average_from_lower(self):
        d1 = Pendulum.create(2009, 12, 31, 23, 59, 59, tz='local')
        d2 = Pendulum.create(2000, 1, 1, 1, 1, 1, tz='local').average(d1)
        self.assertPendulum(d2, 2004, 12, 31, 12, 30, 30)

    def start_of_with_invalid_unit(self):
        self.assertRaises(ValueError, Pendulum.now().start_of('invalid'))

    def end_of_with_invalid_unit(self):
        self.assertRaises(ValueError, Pendulum.now().end_of('invalid'))

    def test_start_of_with_transition(self):
        d = Pendulum(2013, 10, 27, 23, 59, 59, tzinfo='Europe/Paris')
        self.assertEqual(3600, d.offset)
        self.assertEqual(7200, d.start_of('month').offset)
        self.assertEqual(7200, d.start_of('day').offset)
        self.assertEqual(3600, d.start_of('year').offset)

    def test_end_of_with_transition(self):
        d = Pendulum(2013, 3, 31, tzinfo='Europe/Paris')
        self.assertEqual(3600, d.offset)
        self.assertEqual(7200, d.end_of('month').offset)
        self.assertEqual(7200, d.end_of('day').offset)
        self.assertEqual(3600, d.end_of('year').offset)

    def test_start_of_invalid_unit(self):
        d = Pendulum(2013, 3, 31, tzinfo='Europe/Paris')

        self.assertRaises(ValueError, d.start_of, 'invalid')

    def test_end_of_invalid_unit(self):
        d = Pendulum(2013, 3, 31, tzinfo='Europe/Paris')

        self.assertRaises(ValueError, d.end_of, 'invalid')
