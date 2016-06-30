# -*- coding: utf-8 -*-

from pendulum import Pendulum

from .. import AbstractTestCase
from . import AbstractLocalizationTestCase



class FaTest(AbstractLocalizationTestCase, AbstractTestCase):

    locale = 'fa'

    def diff_for_humans(self):
        with self.wrap_with_test_now():
            d = Pendulum.now().sub_second()
            self.assertEqual('1 ثانیه پیش', d.diff_for_humans())

            d = Pendulum.now().sub_seconds(2)
            self.assertEqual('2 ثانیه پیش', d.diff_for_humans())

            d = Pendulum.now().sub_minute()
            self.assertEqual('1 دقیقه پیش', d.diff_for_humans())

            d = Pendulum.now().sub_minutes(2)
            self.assertEqual('2 دقیقه پیش', d.diff_for_humans())

            d = Pendulum.now().sub_hour()
            self.assertEqual('1 ساعت پیش', d.diff_for_humans())

            d = Pendulum.now().sub_hours(2)
            self.assertEqual('2 ساعت پیش', d.diff_for_humans())

            d = Pendulum.now().sub_day()
            self.assertEqual('1 روز پیش', d.diff_for_humans())

            d = Pendulum.now().sub_days(2)
            self.assertEqual('2 روز پیش', d.diff_for_humans())

            d = Pendulum.now().sub_week()
            self.assertEqual('1 هفته پیش', d.diff_for_humans())

            d = Pendulum.now().sub_weeks(2)
            self.assertEqual('2 هفته پیش', d.diff_for_humans())

            d = Pendulum.now().sub_month()
            self.assertEqual('1 ماه پیش', d.diff_for_humans())

            d = Pendulum.now().sub_months(2)
            self.assertEqual('2 ماه پیش', d.diff_for_humans())

            d = Pendulum.now().sub_year()
            self.assertEqual('1 سال پیش', d.diff_for_humans())

            d = Pendulum.now().sub_years(2)
            self.assertEqual('2 سال پیش', d.diff_for_humans())

            d = Pendulum.now().add_second()
            self.assertEqual('1 ثانیه بعد', d.diff_for_humans())

            d = Pendulum.now().add_second()
            d2 = Pendulum.now()
            self.assertEqual('1 ثانیه پس از', d.diff_for_humans(d2))
            self.assertEqual('1 ثانیه پیش از', d2.diff_for_humans(d))

            self.assertEqual('1 ثانیه', d.diff_for_humans(d2, True))
            self.assertEqual('2 ثانیه', d2.diff_for_humans(d.add_second(), True))
