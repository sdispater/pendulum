# -*- coding: utf-8 -*-

from pendulum import Pendulum

from .. import AbstractTestCase
from . import AbstractLocalizationTestCase



class FrTest(AbstractLocalizationTestCase, AbstractTestCase):

    locale = 'fr'

    def diff_for_humans(self):
        with self.wrap_with_test_now():
            d = Pendulum.now().sub_second()
            self.assertEqual('il y a 1 seconde', d.diff_for_humans())

            d = Pendulum.now().sub_seconds(2)
            self.assertEqual('il y a 2 secondes', d.diff_for_humans())

            d = Pendulum.now().sub_minute()
            self.assertEqual('il y a 1 minute', d.diff_for_humans())

            d = Pendulum.now().sub_minutes(2)
            self.assertEqual('il y a 2 minutes', d.diff_for_humans())

            d = Pendulum.now().sub_hour()
            self.assertEqual('il y a 1 heure', d.diff_for_humans())

            d = Pendulum.now().sub_hours(2)
            self.assertEqual('il y a 2 heures', d.diff_for_humans())

            d = Pendulum.now().sub_day()
            self.assertEqual('il y a 1 jour', d.diff_for_humans())

            d = Pendulum.now().sub_days(2)
            self.assertEqual('il y a 2 jours', d.diff_for_humans())

            d = Pendulum.now().sub_week()
            self.assertEqual('il y a 1 semaine', d.diff_for_humans())

            d = Pendulum.now().sub_weeks(2)
            self.assertEqual('il y a 2 semaines', d.diff_for_humans())

            d = Pendulum.now().sub_month()
            self.assertEqual('il y a 1 mois', d.diff_for_humans())

            d = Pendulum.now().sub_months(2)
            self.assertEqual('il y a 2 mois', d.diff_for_humans())

            d = Pendulum.now().sub_year()
            self.assertEqual('il y a 1 an', d.diff_for_humans())

            d = Pendulum.now().sub_years(2)
            self.assertEqual('il y a 2 ans', d.diff_for_humans())

            d = Pendulum.now().add_second()
            self.assertEqual('dans 1 seconde', d.diff_for_humans())

            d = Pendulum.now().add_second()
            d2 = Pendulum.now()
            self.assertEqual('1 seconde après', d.diff_for_humans(d2))
            self.assertEqual('1 seconde avant', d2.diff_for_humans(d))

            self.assertEqual('1 seconde', d.diff_for_humans(d2, True))
            self.assertEqual('2 secondes', d2.diff_for_humans(d.add_second(), True))
