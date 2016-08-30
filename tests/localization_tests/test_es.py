# -*- coding: utf-8 -*-

from pendulum import Pendulum

from .. import AbstractTestCase
from . import AbstractLocalizationTestCase



class EsTest(AbstractLocalizationTestCase, AbstractTestCase):

    locale = 'es'

    def diff_for_humans(self):
        d = Pendulum.now().subtract(seconds=1)
        self.assertEqual('hace 1 segundo', d.diff_for_humans())

        d = Pendulum.now().subtract(seconds=2)
        self.assertEqual('hace 2 segundos', d.diff_for_humans())

        d = Pendulum.now().subtract(minutes=1)
        self.assertEqual('hace 1 minuto', d.diff_for_humans())

        d = Pendulum.now().subtract(minutes=2)
        self.assertEqual('hace 2 minutos', d.diff_for_humans())

        d = Pendulum.now().subtract(hours=1)
        self.assertEqual('hace 1 hora', d.diff_for_humans())

        d = Pendulum.now().subtract(hours=2)
        self.assertEqual('hace 2 horas', d.diff_for_humans())

        d = Pendulum.now().subtract(days=1)
        self.assertEqual('hace 1 día', d.diff_for_humans())

        d = Pendulum.now().subtract(days=2)
        self.assertEqual('hace 2 días', d.diff_for_humans())

        d = Pendulum.now().subtract(weeks=1)
        self.assertEqual('hace 1 semana', d.diff_for_humans())

        d = Pendulum.now().subtract(weeks=2)
        self.assertEqual('hace 2 semanas', d.diff_for_humans())

        d = Pendulum.now().subtract(months=1)
        self.assertEqual('hace 1 mes', d.diff_for_humans())

        d = Pendulum.now().subtract(months=2)
        self.assertEqual('hace 2 meses', d.diff_for_humans())

        d = Pendulum.now().subtract(years=1)
        self.assertEqual('hace 1 año', d.diff_for_humans())

        d = Pendulum.now().subtract(years=2)
        self.assertEqual('hace 2 años', d.diff_for_humans())

        d = Pendulum.now().add(seconds=1)
        self.assertEqual('dentro de 1 segundo', d.diff_for_humans())

        d = Pendulum.now().add(seconds=1)
        d2 = Pendulum.now()
        self.assertEqual('1 segundo después', d.diff_for_humans(d2))
        self.assertEqual('1 segundo antes', d2.diff_for_humans(d))

        self.assertEqual('1 segundo', d.diff_for_humans(d2, True))
        self.assertEqual('2 segundos', d2.diff_for_humans(d.add(seconds=1), True))
