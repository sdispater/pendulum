import pendulum
from pendulum import DateTime
from pendulum.tz import timezone

from .. import AbstractTestCase


class GettersTest(AbstractTestCase):

    def test_year(self):
        d = pendulum.create(1234, 5, 6, 7, 8, 9)
        self.assertEqual(1234, d.year)

    def test_month(self):
        d = pendulum.create(1234, 5, 6, 7, 8, 9)
        self.assertEqual(5, d.month)

    def test_day(self):
        d = pendulum.create(1234, 5, 6, 7, 8, 9)
        self.assertEqual(6, d.day)

    def test_hour(self):
        d = pendulum.create(1234, 5, 6, 7, 8, 9)
        self.assertEqual(7, d.hour)

    def test_minute(self):
        d = pendulum.create(1234, 5, 6, 7, 8, 9)
        self.assertEqual(8, d.minute)

    def test_second(self):
        d = pendulum.create(1234, 5, 6, 7, 8, 9)
        self.assertEqual(9, d.second)

    def test_microsecond(self):
        d = pendulum.create(1234, 5, 6, 7, 8, 9)
        self.assertEqual(0, d.microsecond)

        d = pendulum.create(1234, 5, 6, 7, 8, 9, 101112)
        self.assertEqual(101112, d.microsecond)

    def test_tzinfo(self):
        d = pendulum.now()
        self.assertEqual(timezone('America/Toronto').name, d.tzinfo.name)

    def test_day_of_week(self):
        d = pendulum.create(2012, 5, 7, 7, 8, 9)
        self.assertEqual(pendulum.MONDAY, d.day_of_week)

    def test_day_of_year(self):
        d = pendulum.create(2012, 5, 7)
        self.assertEqual(128, d.day_of_year)

    def test_days_in_month(self):
        d = pendulum.create(2012, 5, 7)
        self.assertEqual(31, d.days_in_month)

    def test_timestamp(self):
        d = pendulum.create(1970, 1, 1, 0, 0, 0)
        self.assertEqual(0, d.timestamp())
        self.assertEqual(60.123456, d.add(minutes=1, microseconds=123456).timestamp())

    def test_float_timestamp(self):
        d = pendulum.create(1970, 1, 1, 0, 0, 0, 123456)
        self.assertEqual(0.123456, d.float_timestamp)

    def test_int_timestamp(self):
        d = pendulum.create(1970, 1, 1, 0, 0, 0)
        self.assertEqual(0, d.int_timestamp)
        self.assertEqual(60, d.add(minutes=1, microseconds=123456).int_timestamp)

    def test_int_timestamp_accuracy(self):
        self.skip_if_32bit()

        d = pendulum.create(3000, 10, 1, 12, 23, 10, 999999)

        self.assertEqual(32527311790, d.int_timestamp)

    def test_age(self):
        d = pendulum.now()
        self.assertEqual(0, d.age)
        self.assertEqual(1, d.add(years=1).age)

    def test_local(self):
        self.assertTrue(pendulum.create(2012, 1, 1, tz='America/Toronto').is_local())
        self.assertTrue(pendulum.create(2012, 1, 1, tz='America/New_York').is_local())
        self.assertFalse(pendulum.create(2012, 1, 1, tz='UTC').is_local())
        self.assertFalse(pendulum.create(2012, 1, 1, tz='Europe/London').is_local())

    def test_utc(self):
        self.assertFalse(pendulum.create(2012, 1, 1, tz='America/Toronto').is_utc())
        self.assertFalse(pendulum.create(2012, 1, 1, tz='Europe/Paris').is_utc())
        self.assertTrue(pendulum.create(2012, 1, 1, tz='Atlantic/Reykjavik').is_utc())
        self.assertTrue(pendulum.create(2012, 1, 1, tz='Europe/Lisbon').is_utc())
        self.assertTrue(pendulum.create(2012, 1, 1, tz='Africa/Casablanca').is_utc())
        self.assertTrue(pendulum.create(2012, 1, 1, tz='Africa/Dakar').is_utc())
        self.assertTrue(pendulum.create(2012, 1, 1, tz='UTC').is_utc())
        self.assertTrue(pendulum.create(2012, 1, 1, tz='GMT').is_utc())

    def test_is_dst(self):
        self.assertFalse(pendulum.create(2012, 1, 1, tz='America/Toronto').is_dst())
        self.assertTrue(pendulum.create(2012, 7, 1, tz='America/Toronto').is_dst())

    def test_offset_with_dst(self):
        self.assertEqual(-18000, pendulum.create(2012, 1, 1, tz='America/Toronto').offset)

    def test_offset_no_dst(self):
        self.assertEqual(-14400, pendulum.create(2012, 6, 1, tz='America/Toronto').offset)

    def test_offset_for_gmt(self):
        self.assertEqual(0, pendulum.create(2012, 6, 1, tz='GMT').offset)

    def test_offset_hours_with_dst(self):
        self.assertEqual(-5, pendulum.create(2012, 1, 1, tz='America/Toronto').offset_hours)

    def test_offset_hours_no_dst(self):
        self.assertEqual(-4, pendulum.create(2012, 6, 1, tz='America/Toronto').offset_hours)

    def test_offset_hours_for_gmt(self):
        self.assertEqual(0, pendulum.create(2012, 6, 1, tz='GMT').offset_hours)

    def test_offset_hours_float(self):
        self.assertEqual(9.5, pendulum.create(2012, 6, 1, tz=9.5).offset_hours)

    def test_is_leap_year(self):
        self.assertTrue(pendulum.create(2012, 1, 1).is_leap_year())
        self.assertFalse(pendulum.create(2011, 1, 1).is_leap_year())

    def test_is_long_year(self):
        self.assertTrue(pendulum.create(2015, 1, 1).is_long_year())
        self.assertFalse(pendulum.create(2016, 1, 1).is_long_year())

    def test_week_of_month(self):
        self.assertEqual(5, pendulum.create(2012, 9, 30).week_of_month)
        self.assertEqual(4, pendulum.create(2012, 9, 28).week_of_month)
        self.assertEqual(3, pendulum.create(2012, 9, 20).week_of_month)
        self.assertEqual(2, pendulum.create(2012, 9, 8).week_of_month)
        self.assertEqual(1, pendulum.create(2012, 9, 1).week_of_month)

    def test_week_of_year_first_week(self):
        self.assertEqual(52, pendulum.create(2012, 1, 1).week_of_year)
        self.assertEqual(1, pendulum.create(2012, 1, 2).week_of_year)

    def test_week_of_year_last_week(self):
        self.assertEqual(52, pendulum.create(2012, 12, 30).week_of_year)
        self.assertEqual(1, pendulum.create(2012, 12, 31).week_of_year)

    def test_timezone(self):
        d = pendulum.create(2000, 1, 1, tz='America/Toronto')
        self.assertEqual('America/Toronto', d.timezone.name)

        d = pendulum.create(2000, 1, 1, tz=-5)
        self.assertEqual('-05:00', d.timezone.name)

    def test_tz(self):
        d = pendulum.create(2000, 1, 1, tz='America/Toronto')
        self.assertEqual('America/Toronto', d.tz.name)

        d = pendulum.create(2000, 1, 1, tz=-5)
        self.assertEqual('-05:00', d.tz.name)

    def test_timezone_name(self):
        d = pendulum.create(2000, 1, 1, tz='America/Toronto')
        self.assertEqual('America/Toronto', d.timezone_name)

        d = pendulum.create(2000, 1, 1, tz=-5)
        self.assertEqual('-05:00', d.timezone_name)

    def test_is_future(self):
        with self.wrap_with_test_now(DateTime(2000, 1, 1)):
            d = pendulum.now()
            self.assertFalse(d.is_future())
            d = d.add(days=1)
            self.assertTrue(d.is_future())

    def test_is_past(self):
        with self.wrap_with_test_now(DateTime(2000, 1, 1)):
            d = pendulum.now()
            self.assertFalse(d.is_past())
            d = d.subtract(days=1)
            self.assertTrue(d.is_past())

    def test_date(self):
        dt = pendulum.create(2016, 10, 20, 10, 40, 34, 123456)
        d = dt.date()
        self.assertIsInstanceOfDate(d)
        self.assertDate(d, 2016, 10, 20)

    def test_time(self):
        dt = pendulum.create(2016, 10, 20, 10, 40, 34, 123456)
        t = dt.time()
        self.assertIsInstanceOfTime(t)
        self.assertTime(t, 10, 40, 34, 123456)
