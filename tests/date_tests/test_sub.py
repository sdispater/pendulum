import pendulum

from datetime import timedelta
from pendulum import Date

from .. import AbstractTestCase
from ..conftest import assert_date


class SubTest(AbstractTestCase):

    def test_subtract_years_positive(self):
        self.assertEqual(1974, Date.create(1975).subtract(years=1).year)

    def test_subtract_years_zero(self):
        self.assertEqual(1975, Date.create(1975).subtract(years=0).year)

    def test_subtract_years_negative(self):
        self.assertEqual(1976, Date.create(1975).subtract(years=-1).year)

    def test_subtract_months_positive(self):
        self.assertEqual(12, Date.create(1975, 1).subtract(months=1).month)

    def test_subtract_months_zero(self):
        self.assertEqual(12, Date.create(1975, 12).subtract(months=0).month)

    def test_subtract_months_negative(self):
        self.assertEqual(12, Date.create(1975, 11, 1).subtract(months=-1).month)

    def test_subtract_days_positive(self):
        self.assertEqual(31, Date(1975, 6, 1).subtract(days=1).day)

    def test_subtract_days_zero(self):
        self.assertEqual(31, Date(1975, 5, 31).subtract(days=0).day)

    def test_subtract_days_negative(self):
        self.assertEqual(31, Date(1975, 5, 30).subtract(days=-1).day)

    def test_subtract_weeks_positive(self):
        self.assertEqual(21, Date(1975, 5, 28).subtract(weeks=1).day)

    def test_subtract_weeks_zero(self):
        self.assertEqual(21, Date(1975, 5, 21).subtract(weeks=0).day)

    def test_subtract_weeks_negative(self):
        self.assertEqual(21, Date(1975, 5, 14).subtract(weeks=-1).day)

    def test_subtract_timedelta(self):
        delta = timedelta(days=18)
        d = Date.create(2015, 3, 14)

        new = d - delta
        self.assertIsInstanceOfDate(new)
        self.assertDate(new, 2015, 2, 24)

    def test_subtract_duration(self):
        delta = pendulum.duration(years=2, months=3, days=18)
        d = pendulum.date(2015, 3, 14)

        new = d - delta
        assert_date(new, 2012, 11, 26)

    def test_addition_invalid_type(self):
        d = Date.create(2015, 3, 14)

        try:
            d - 'ab'
            self.fail()
        except TypeError:
            pass

        try:
            'ab' - d
            self.fail()
        except TypeError:
            pass
