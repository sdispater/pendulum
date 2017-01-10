# -*- coding: utf-8 -*-

import pendulum
from pendulum import Pendulum
from pendulum.tz import timezone

from .. import AbstractTestCase


class GettersTest(AbstractTestCase):

    def test_year(self):
        d = Pendulum(1234, 5, 6, 7, 8, 9)
        self.assertEqual(1234, d.year)

    def test_month(self):
        d = Pendulum(1234, 5, 6, 7, 8, 9)
        self.assertEqual(5, d.month)

    def test_day(self):
        d = Pendulum(1234, 5, 6, 7, 8, 9)
        self.assertEqual(6, d.day)

    def test_hour(self):
        d = Pendulum(1234, 5, 6, 7, 8, 9)
        self.assertEqual(7, d.hour)

    def test_minute(self):
        d = Pendulum(1234, 5, 6, 7, 8, 9)
        self.assertEqual(8, d.minute)

    def test_second(self):
        d = Pendulum(1234, 5, 6, 7, 8, 9)
        self.assertEqual(9, d.second)

    def test_microsecond(self):
        d = Pendulum(1234, 5, 6, 7, 8, 9)
        self.assertEqual(0, d.microsecond)

        d = Pendulum(1234, 5, 6, 7, 8, 9, 101112)
        self.assertEqual(101112, d.microsecond)

    def test_tzinfo(self):
        d = Pendulum.now()
        self.assertEqual(timezone('America/Toronto').name, d.tzinfo.name)

    def test_day_of_week(self):
        d = Pendulum(2012, 5, 7, 7, 8, 9)
        self.assertEqual(pendulum.MONDAY, d.day_of_week)

    def test_day_of_year(self):
        d = Pendulum(2012, 5, 7)
        self.assertEqual(128, d.day_of_year)

    def test_days_in_month(self):
        d = Pendulum(2012, 5, 7)
        self.assertEqual(31, d.days_in_month)

    def test_timestamp(self):
        d = Pendulum(1970, 1, 1, 0, 0, 0)
        self.assertEqual(0, d.timestamp())
        self.assertEqual(60.123456, d.add(minutes=1, microseconds=123456).timestamp())

    def test_float_timestamp(self):
        d = Pendulum(1970, 1, 1, 0, 0, 0, 123456)
        self.assertEqual(0.123456, d.float_timestamp)

    def test_int_timestamp(self):
        d = Pendulum(1970, 1, 1, 0, 0, 0)
        self.assertEqual(0, d.int_timestamp)
        self.assertEqual(60, d.add(minutes=1, microseconds=123456).int_timestamp)

    def test_int_timestamp_accuracy(self):
        self.skip_if_32bit()

        d = Pendulum(3000, 10, 1, 12, 23, 10, 999999)

        self.assertEqual(32527311790, d.int_timestamp)

    def test_age(self):
        d = Pendulum.now()
        self.assertEqual(0, d.age)
        self.assertEqual(1, d.add(years=1).age)

    def test_local(self):
        self.assertTrue(Pendulum.create(2012, 1, 1, tz='America/Toronto').local)
        self.assertTrue(Pendulum.create(2012, 1, 1, tz='America/New_York').local)
        self.assertFalse(Pendulum.create(2012, 1, 1, tz='UTC').local)
        self.assertFalse(Pendulum.create(2012, 1, 1, tz='Europe/London').local)

    def test_utc(self):
        self.assertFalse(Pendulum.create(2012, 1, 1, tz='America/Toronto').utc)
        self.assertFalse(Pendulum.create(2012, 1, 1, tz='Europe/Paris').utc)
        self.assertTrue(Pendulum.create(2012, 1, 1, tz='Atlantic/Reykjavik').utc)
        self.assertTrue(Pendulum.create(2012, 1, 1, tz='Europe/Lisbon').utc)
        self.assertTrue(Pendulum.create(2012, 1, 1, tz='Africa/Casablanca').utc)
        self.assertTrue(Pendulum.create(2012, 1, 1, tz='Africa/Dakar').utc)
        self.assertTrue(Pendulum.create(2012, 1, 1, tz='UTC').utc)
        self.assertTrue(Pendulum.create(2012, 1, 1, tz='GMT').utc)

    def test_is_dst(self):
        self.assertFalse(Pendulum.create(2012, 1, 1, tz='America/Toronto').is_dst)
        self.assertTrue(Pendulum.create(2012, 7, 1, tz='America/Toronto').is_dst)

    def test_offset_with_dst(self):
        self.assertEqual(-18000, Pendulum.create(2012, 1, 1, tz='America/Toronto').offset)

    def test_offset_no_dst(self):
        self.assertEqual(-14400, Pendulum.create(2012, 6, 1, tz='America/Toronto').offset)

    def test_offset_for_gmt(self):
        self.assertEqual(0, Pendulum.create(2012, 6, 1, tz='GMT').offset)

    def test_offset_hours_with_dst(self):
        self.assertEqual(-5, Pendulum.create(2012, 1, 1, tz='America/Toronto').offset_hours)

    def test_offset_hours_no_dst(self):
        self.assertEqual(-4, Pendulum.create(2012, 6, 1, tz='America/Toronto').offset_hours)

    def test_offset_hours_for_gmt(self):
        self.assertEqual(0, Pendulum.create(2012, 6, 1, tz='GMT').offset_hours)

    def test_offset_hours_float(self):
        self.assertEqual(9.5, Pendulum.create(2012, 6, 1, tz=9.5).offset_hours)

    def test_is_leap_year(self):
        self.assertTrue(Pendulum.create(2012, 1, 1).is_leap_year())
        self.assertFalse(Pendulum.create(2011, 1, 1).is_leap_year())

    def test_is_long_year(self):
        self.assertTrue(Pendulum.create(2015, 1, 1).is_long_year())
        self.assertFalse(Pendulum.create(2016, 1, 1).is_long_year())

    def test_week_of_month(self):
        self.assertEqual(5, Pendulum.create(2012, 9, 30).week_of_month)
        self.assertEqual(4, Pendulum.create(2012, 9, 28).week_of_month)
        self.assertEqual(3, Pendulum.create(2012, 9, 20).week_of_month)
        self.assertEqual(2, Pendulum.create(2012, 9, 8).week_of_month)
        self.assertEqual(1, Pendulum.create(2012, 9, 1).week_of_month)

    def test_week_of_year_first_week(self):
        self.assertEqual(52, Pendulum.create(2012, 1, 1).week_of_year)
        self.assertEqual(1, Pendulum.create(2012, 1, 2).week_of_year)

    def test_week_of_year_last_week(self):
        self.assertEqual(52, Pendulum.create(2012, 12, 30).week_of_year)
        self.assertEqual(1, Pendulum.create(2012, 12, 31).week_of_year)

    def test_timezone(self):
        d = Pendulum.create(2000, 1, 1, tz='America/Toronto')
        self.assertEqual('America/Toronto', d.timezone.name)

        d = Pendulum.create(2000, 1, 1, tz=-5)
        self.assertEqual('-05:00', d.timezone.name)

    def test_tz(self):
        d = Pendulum.create(2000, 1, 1, tz='America/Toronto')
        self.assertEqual('America/Toronto', d.tz.name)

        d = Pendulum.create(2000, 1, 1, tz=-5)
        self.assertEqual('-05:00', d.tz.name)

    def test_timezone_name(self):
        d = Pendulum.create(2000, 1, 1, tz='America/Toronto')
        self.assertEqual('America/Toronto', d.timezone_name)

        d = Pendulum.create(2000, 1, 1, tz=-5)
        self.assertEqual('-05:00', d.timezone_name)

    def test_is_weekday(self):
        d = Pendulum.now().next(pendulum.MONDAY)
        self.assertTrue(d.is_weekday())
        d = d.next(pendulum.SATURDAY)
        self.assertFalse(d.is_weekday())

    def test_is_weekend(self):
        d = Pendulum.now().next(pendulum.MONDAY)
        self.assertFalse(d.is_weekend())
        d = d.next(pendulum.SATURDAY)
        self.assertTrue(d.is_weekend())

    def test_is_today(self):
        with self.wrap_with_test_now():
            d = Pendulum.now()
            self.assertTrue(d.is_today())
            d = d.subtract(days=1)
            self.assertFalse(d.is_today())

    def test_is_yesterday(self):
        with self.wrap_with_test_now():
            d = Pendulum.now()
            self.assertFalse(d.is_yesterday())
            d = d.subtract(days=1)
            self.assertTrue(d.is_yesterday())

    def test_is_tomorrow(self):
        with self.wrap_with_test_now():
            d = Pendulum.now()
            self.assertFalse(d.is_tomorrow())
            d = d.add(days=1)
            self.assertTrue(d.is_tomorrow())

    def test_is_future(self):
        with self.wrap_with_test_now(Pendulum(2000, 1, 1)):
            d = Pendulum.now()
            self.assertFalse(d.is_future())
            d = d.add(days=1)
            self.assertTrue(d.is_future())

    def test_is_past(self):
        with self.wrap_with_test_now(Pendulum(2000, 1, 1)):
            d = Pendulum.now()
            self.assertFalse(d.is_past())
            d = d.subtract(days=1)
            self.assertTrue(d.is_past())

    def test_is_day_of_week(self):
        d = pendulum.now()
        monday = d.next(pendulum.MONDAY)
        tuesday = d.next(pendulum.TUESDAY)
        wednesday = d.next(pendulum.WEDNESDAY)
        thursday = d.next(pendulum.THURSDAY)
        friday = d.next(pendulum.FRIDAY)
        saturday = d.next(pendulum.SATURDAY)
        sunday = d.next(pendulum.SUNDAY)

        self.assertTrue(monday.is_monday())
        self.assertFalse(tuesday.is_monday())

        self.assertTrue(tuesday.is_tuesday())
        self.assertFalse(wednesday.is_tuesday())

        self.assertTrue(wednesday.is_wednesday())
        self.assertFalse(thursday.is_wednesday())

        self.assertTrue(thursday.is_thursday())
        self.assertFalse(friday.is_thursday())

        self.assertTrue(thursday.is_thursday())
        self.assertFalse(friday.is_thursday())

        self.assertTrue(friday.is_friday())
        self.assertFalse(saturday.is_friday())

        self.assertTrue(saturday.is_saturday())
        self.assertFalse(sunday.is_saturday())

        self.assertTrue(sunday.is_sunday())
        self.assertFalse(monday.is_sunday())

    def test_date(self):
        dt = Pendulum(2016, 10, 20, 10, 40, 34, 123456)
        d = dt.date()
        self.assertIsInstanceOfDate(d)
        self.assertDate(d, 2016, 10, 20)

    def test_time(self):
        dt = Pendulum(2016, 10, 20, 10, 40, 34, 123456)
        t = dt.time()
        self.assertIsInstanceOfTime(t)
        self.assertTime(t, 10, 40, 34, 123456)
