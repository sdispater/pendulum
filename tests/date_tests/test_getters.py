import pendulum
from pendulum import Date

from .. import AbstractTestCase


class GettersTest(AbstractTestCase):

    def test_year(self):
        d = Date(1234, 5, 6)
        self.assertEqual(1234, d.year)

    def test_month(self):
        d = Date(1234, 5, 6)
        self.assertEqual(5, d.month)

    def test_day(self):
        d = Date(1234, 5, 6)
        self.assertEqual(6, d.day)

    def test_day_of_week(self):
        d = Date(2012, 5, 7)
        self.assertEqual(pendulum.MONDAY, d.day_of_week)

    def test_day_of_year(self):
        d = Date(2015, 12, 31)
        self.assertEqual(365, d.day_of_year)
        d = Date(2016, 12, 31)
        self.assertEqual(366, d.day_of_year)

    def test_days_in_month(self):
        d = Date(2012, 5, 7)
        self.assertEqual(31, d.days_in_month)

    def test_age(self):
        d = Date.today()
        self.assertEqual(0, d.age)
        self.assertEqual(1, d.add(years=1).age)

    def test_is_leap_year(self):
        self.assertTrue(Date(2012, 1, 1).is_leap_year())
        self.assertFalse(Date(2011, 1, 1).is_leap_year())

    def test_is_long_year(self):
        self.assertTrue(Date(2015, 1, 1).is_long_year())
        self.assertFalse(Date(2016, 1, 1).is_long_year())

    def test_week_of_month(self):
        self.assertEqual(5, Date(2012, 9, 30).week_of_month)
        self.assertEqual(4, Date(2012, 9, 28).week_of_month)
        self.assertEqual(3, Date(2012, 9, 20).week_of_month)
        self.assertEqual(2, Date(2012, 9, 8).week_of_month)
        self.assertEqual(1, Date(2012, 9, 1).week_of_month)

    def test_week_of_year_first_week(self):
        self.assertEqual(52, Date(2012, 1, 1).week_of_year)
        self.assertEqual(1, Date(2012, 1, 2).week_of_year)

    def test_week_of_year_last_week(self):
        self.assertEqual(52, Date(2012, 12, 30).week_of_year)
        self.assertEqual(1, Date(2012, 12, 31).week_of_year)

    def test_is_future(self):
        d = Date.today()
        self.assertFalse(d.is_future())
        d = d.add(days=1)
        self.assertTrue(d.is_future())

    def test_is_past(self):
        d = Date.today()
        self.assertFalse(d.is_past())
        d = d.subtract(days=1)
        self.assertTrue(d.is_past())
