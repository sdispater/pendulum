# -*- coding: utf-8 -*-

from pendulum import Pendulum

from .. import AbstractTestCase


class DayOfWeekModifiersTest(AbstractTestCase):

    def test_get_weekend_days(self):
        self.assertEqual(
            [Pendulum.SATURDAY, Pendulum.SUNDAY],
            Pendulum.get_weekend_days()
        )

    def test_get_week_ends_at(self):
        Pendulum.set_week_ends_at(Pendulum.SATURDAY)
        self.assertEqual(Pendulum.get_week_ends_at(), Pendulum.SATURDAY)
        Pendulum.set_week_ends_at(Pendulum.SUNDAY)

    def test_get_week_starts_at(self):
        Pendulum.set_week_starts_at(Pendulum.TUESDAY)
        self.assertEqual(Pendulum.get_week_starts_at(), Pendulum.TUESDAY)
        Pendulum.set_week_starts_at(Pendulum.MONDAY)

    def test_start_of_week(self):
        d = Pendulum(1980, 8, 7, 12, 11, 9).start_of_week()
        self.assertPendulum(d, 1980, 8, 4, 0, 0, 0)

    def test_start_of_week_from_week_start(self):
        d = Pendulum(1980, 8, 4).start_of_week()
        self.assertPendulum(d, 1980, 8, 4, 0, 0, 0)

    def test_start_of_week_crossing_year_boundary(self):
        d = Pendulum.create_from_date(2014, 1, 1).start_of_week()
        self.assertPendulum(d, 2013, 12, 30, 0, 0, 0)

    def test_end_of_week(self):
        d = Pendulum(1980, 8, 7, 12, 11, 9).end_of_week()
        self.assertPendulum(d, 1980, 8, 10, 23, 59, 59)

    def test_end_of_week_from_week_end(self):
        d = Pendulum(1980, 8, 10).end_of_week()
        self.assertPendulum(d, 1980, 8, 10, 23, 59, 59)

    def test_end_of_week_crossing_year_boundary(self):
        d = Pendulum.create_from_date(2013, 12, 31).end_of_week()
        self.assertPendulum(d, 2014, 1, 5, 23, 59, 59)

    def test_next(self):
        d = Pendulum.create_from_date(1975, 5, 21).next()
        self.assertPendulum(d, 1975, 5, 28, 0, 0, 0)

    def test_next_monday(self):
        d = Pendulum.create_from_date(1975, 5, 21).next(Pendulum.MONDAY)
        self.assertPendulum(d, 1975, 5, 26, 0, 0, 0)

    def test_next_saturday(self):
        d = Pendulum.create_from_date(1975, 5, 21).next(6)
        self.assertPendulum(d, 1975, 5, 24, 0, 0, 0)

    def test_previous(self):
        d = Pendulum.create_from_date(1975, 5, 21).previous()
        self.assertPendulum(d, 1975, 5, 14, 0, 0, 0)

    def test_previous_monday(self):
        d = Pendulum.create_from_date(1975, 5, 21).previous(Pendulum.MONDAY)
        self.assertPendulum(d, 1975, 5, 19, 0, 0, 0)

    def test_previous_saturday(self):
        d = Pendulum.create_from_date(1975, 5, 21).previous(6)
        self.assertPendulum(d, 1975, 5, 17, 0, 0, 0)

    def test_first_day_of_month(self):
        d = Pendulum.create_from_date(1975, 11, 21).first_of_month()
        self.assertPendulum(d, 1975, 11, 1, 0, 0, 0)

    def test_first_wednesday_of_month(self):
        d = Pendulum.create_from_date(1975, 11, 21).first_of_month(Pendulum.WEDNESDAY)
        self.assertPendulum(d, 1975, 11, 5, 0, 0, 0)

    def test_first_friday_of_month(self):
        d = Pendulum.create_from_date(1975, 11, 21).first_of_month(5)
        self.assertPendulum(d, 1975, 11, 7, 0, 0, 0)

    def test_last_day_of_month(self):
        d = Pendulum.create_from_date(1975, 12, 5).last_of_month()
        self.assertPendulum(d, 1975, 12, 31, 0, 0, 0)

    def test_last_tuesday_of_month(self):
        d = Pendulum.create_from_date(1975, 12, 1).last_of_month(Pendulum.TUESDAY)
        self.assertPendulum(d, 1975, 12, 30, 0, 0, 0)

    def test_last_friday_of_month(self):
        d = Pendulum.create_from_date(1975, 12, 5).last_of_month(5)
        self.assertPendulum(d, 1975, 12, 26, 0, 0, 0)

    def test_nth_of_month_outside_scope(self):
        d = Pendulum.create_from_date(1975, 12, 5)

        self.assertFalse(d.nth_of_month(6, Pendulum.MONDAY))

    def test_nth_of_month_outside_year(self):
        d = Pendulum.create_from_date(1975, 12, 5)

        self.assertFalse(d.nth_of_month(55, Pendulum.MONDAY))

    def test_2nd_monday_of_month(self):
        d = Pendulum.create_from_date(1975, 12, 5).nth_of_month(2, Pendulum.MONDAY)

        self.assertPendulum(d, 1975, 12, 8, 0, 0, 0)

    def test_3rd_wednesday_of_month(self):
        d = Pendulum.create_from_date(1975, 12, 5).nth_of_month(3, 3)

        self.assertPendulum(d, 1975, 12, 17, 0, 0, 0)

    def test_first_day_of_quarter(self):
        d = Pendulum.create_from_date(1975, 11, 21).first_of_quarter()
        self.assertPendulum(d, 1975, 10, 1, 0, 0, 0)

    def test_first_wednesday_of_quarter(self):
        d = Pendulum.create_from_date(1975, 11, 21).first_of_quarter(Pendulum.WEDNESDAY)
        self.assertPendulum(d, 1975, 10, 1, 0, 0, 0)

    def test_first_friday_of_quarter(self):
        d = Pendulum.create_from_date(1975, 11, 21).first_of_quarter(5)
        self.assertPendulum(d, 1975, 10, 3, 0, 0, 0)

    def test_first_of_quarter_from_a_day_that_will_not_exist_in_the_first_month(self):
        d = Pendulum.create_from_date(2014, 5, 31).first_of_quarter()
        self.assertPendulum(d, 2014, 4, 1, 0, 0, 0)

    def test_last_day_of_quarter(self):
        d = Pendulum.create_from_date(1975, 8, 5).last_of_quarter()
        self.assertPendulum(d, 1975, 9, 30, 0, 0, 0)

    def test_last_tuesday_of_quarter(self):
        d = Pendulum.create_from_date(1975, 8, 5).last_of_quarter(Pendulum.TUESDAY)
        self.assertPendulum(d, 1975, 9, 30, 0, 0, 0)

    def test_last_friday_of_quarter(self):
        d = Pendulum.create_from_date(1975, 8, 5).last_of_quarter(Pendulum.FRIDAY)
        self.assertPendulum(d, 1975, 9, 26, 0, 0, 0)

    def test_last_day_of_quarter_that_will_not_exist_in_the_last_month(self):
        d = Pendulum.create_from_date(2014, 5, 31).last_of_quarter()
        self.assertPendulum(d, 2014, 6, 30, 0, 0, 0)

    def test_nth_of_quarter_outside_scope(self):
        d = Pendulum.create_from_date(1975, 1, 5)

        self.assertFalse(d.nth_of_quarter(20, Pendulum.MONDAY))

    def test_nth_of_quarter_outside_year(self):
        d = Pendulum.create_from_date(1975, 1, 5)

        self.assertFalse(d.nth_of_quarter(55, Pendulum.MONDAY))

    def test_nth_of_quarter_from_a_day_that_will_not_exist_in_the_first_month(self):
        d = Pendulum.create_from_date(2014, 5, 31).nth_of_quarter(2, Pendulum.MONDAY)
        self.assertPendulum(d, 2014, 4, 14, 0, 0, 0)

    def test_2nd_monday_of_quarter(self):
        d = Pendulum.create_from_date(1975, 8, 5).nth_of_quarter(2, Pendulum.MONDAY)
        self.assertPendulum(d, 1975, 7, 14, 0, 0, 0)

    def test_3rd_wednesday_of_quarter(self):
        d = Pendulum.create_from_date(1975, 8, 5).nth_of_quarter(3, 3)
        self.assertPendulum(d, 1975, 7, 16, 0, 0, 0)

    def test_first_day_of_year(self):
        d = Pendulum.create_from_date(1975, 11, 21).first_of_year()
        self.assertPendulum(d, 1975, 1, 1, 0, 0, 0)

    def test_first_wednesday_of_year(self):
        d = Pendulum.create_from_date(1975, 11, 21).first_of_year(Pendulum.WEDNESDAY)
        self.assertPendulum(d, 1975, 1, 1, 0, 0, 0)

    def test_first_friday_of_year(self):
        d = Pendulum.create_from_date(1975, 11, 21).first_of_year(5)
        self.assertPendulum(d, 1975, 1, 3, 0, 0, 0)

    def test_last_day_of_year(self):
        d = Pendulum.create_from_date(1975, 8, 5).last_of_year()
        self.assertPendulum(d, 1975, 12, 31, 0, 0, 0)

    def test_last_tuesday_of_year(self):
        d = Pendulum.create_from_date(1975, 8, 5).last_of_year(Pendulum.TUESDAY)
        self.assertPendulum(d, 1975, 12, 30, 0, 0, 0)

    def test_last_friday_of_year(self):
        d = Pendulum.create_from_date(1975, 8, 5).last_of_year(5)
        self.assertPendulum(d, 1975, 12, 26, 0, 0, 0)

    def test_nth_of_year_outside_scope(self):
        d = Pendulum.create_from_date(1975, 1, 5)

        self.assertFalse(d.nth_of_year(55, Pendulum.MONDAY))

    def test_2nd_monday_of_year(self):
        d = Pendulum.create_from_date(1975, 8, 5).nth_of_year(2, Pendulum.MONDAY)
        self.assertPendulum(d, 1975, 1, 13, 0, 0, 0)

    def test_2rd_wednesday_of_year(self):
        d = Pendulum.create_from_date(1975, 8, 5).nth_of_year(3, Pendulum.WEDNESDAY)
        self.assertPendulum(d, 1975, 1, 15, 0, 0, 0)

    def test_7th_thursday_of_year(self):
        d = Pendulum.create_from_date(1975, 8, 31).nth_of_year(7, Pendulum.THURSDAY)
        self.assertPendulum(d, 1975, 2, 13, 0, 0, 0)
