# -*- coding: utf-8 -*-

from pendulum import Pendulum

from .. import AbstractTestCase
from . import AbstractLocalizationTestCase



class EsTest(AbstractLocalizationTestCase, AbstractTestCase):

    locale = 'es'

    def diff_for_humans(self):
        with self.wrap_with_test_now():
            d = Pendulum.now().sub_second()
            self.assertEqual('hace 1 segundo', d.diff_for_humans())

            d = Pendulum.now().sub_seconds(2)
            self.assertEqual('hace 2 segundos', d.diff_for_humans())

            d = Pendulum.now().sub_minute()
            self.assertEqual('hace 1 minuto', d.diff_for_humans())

            d = Pendulum.now().sub_minutes(2)
            self.assertEqual('hace 2 minutos', d.diff_for_humans())

            d = Pendulum.now().sub_hour()
            self.assertEqual('hace 1 hora', d.diff_for_humans())

            d = Pendulum.now().sub_hours(2)
            self.assertEqual('hace 2 horas', d.diff_for_humans())

            d = Pendulum.now().sub_day()
            self.assertEqual('hace 1 día', d.diff_for_humans())

            d = Pendulum.now().sub_days(2)
            self.assertEqual('hace 2 días', d.diff_for_humans())

            d = Pendulum.now().sub_week()
            self.assertEqual('hace 1 semana', d.diff_for_humans())

            d = Pendulum.now().sub_weeks(2)
            self.assertEqual('hace 2 semanas', d.diff_for_humans())

            d = Pendulum.now().sub_month()
            self.assertEqual('hace 1 mes', d.diff_for_humans())

            d = Pendulum.now().sub_months(2)
            self.assertEqual('hace 2 meses', d.diff_for_humans())

            d = Pendulum.now().sub_year()
            self.assertEqual('hace 1 año', d.diff_for_humans())

            d = Pendulum.now().sub_years(2)
            self.assertEqual('hace 2 años', d.diff_for_humans())

            d = Pendulum.now().add_second()
            self.assertEqual('dentro de 1 segundo', d.diff_for_humans())

            d = Pendulum.now().add_second()
            d2 = Pendulum.now()
            self.assertEqual('1 segundo después', d.diff_for_humans(d2))
            self.assertEqual('1 segundo antes', d2.diff_for_humans(d))

            self.assertEqual('1 segundo', d.diff_for_humans(d2, True))
            self.assertEqual('2 segundos', d2.diff_for_humans(d.add_second(), True))
