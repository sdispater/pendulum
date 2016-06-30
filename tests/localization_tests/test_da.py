# -*- coding: utf-8 -*-

from pendulum import Pendulum

from .. import AbstractTestCase
from . import AbstractLocalizationTestCase



class DaTest(AbstractLocalizationTestCase, AbstractTestCase):

    locale = 'da'

    def diff_for_humans(self):
        with self.wrap_with_test_now():
            d = Pendulum.now().sub_second()
            self.assertEqual('1 sekund siden', d.diff_for_humans())

            d = Pendulum.now().sub_seconds(2)
            self.assertEqual('2 sekunder siden', d.diff_for_humans())

            d = Pendulum.now().sub_minute()
            self.assertEqual('1 minut siden', d.diff_for_humans())

            d = Pendulum.now().sub_minutes(2)
            self.assertEqual('2 minutter siden', d.diff_for_humans())

            d = Pendulum.now().sub_hour()
            self.assertEqual('1 time siden', d.diff_for_humans())

            d = Pendulum.now().sub_hours(2)
            self.assertEqual('2 timer siden', d.diff_for_humans())

            d = Pendulum.now().sub_day()
            self.assertEqual('1 dag siden', d.diff_for_humans())

            d = Pendulum.now().sub_days(2)
            self.assertEqual('2 dage siden', d.diff_for_humans())

            d = Pendulum.now().sub_week()
            self.assertEqual('1 uge siden', d.diff_for_humans())

            d = Pendulum.now().sub_weeks(2)
            self.assertEqual('2 uger siden', d.diff_for_humans())

            d = Pendulum.now().sub_month()
            self.assertEqual('1 måned siden', d.diff_for_humans())

            d = Pendulum.now().sub_months(2)
            self.assertEqual('2 måneder siden', d.diff_for_humans())

            d = Pendulum.now().sub_year()
            self.assertEqual('1 år siden', d.diff_for_humans())

            d = Pendulum.now().sub_years(2)
            self.assertEqual('2 år siden', d.diff_for_humans())

            d = Pendulum.now().add_second()
            self.assertEqual('om 1 sekund', d.diff_for_humans())

            d = Pendulum.now().add_second()
            d2 = Pendulum.now()
            self.assertEqual('1 sekund efter', d.diff_for_humans(d2))
            self.assertEqual('1 sekund før', d2.diff_for_humans(d))

            self.assertEqual('1 sekund', d.diff_for_humans(d2, True))
            self.assertEqual('2 sekunder', d2.diff_for_humans(d.add_second(), True))
