# -*- coding: utf-8 -*-

from pendulum import Pendulum

from .. import AbstractTestCase
from . import AbstractLocalizationTestCase



class FrTest(AbstractLocalizationTestCase, AbstractTestCase):

    locale = 'fr'

    def diff_for_humans(self):
        with self.wrap_with_test_now():
            d = Pendulum.now().subtract(seconds=1)
            self.assertEqual('il y a 1 seconde', d.diff_for_humans())

            d = Pendulum.now().subtract(seconds=2)
            self.assertEqual('il y a 2 secondes', d.diff_for_humans())

            d = Pendulum.now().subtract(minutes=1)
            self.assertEqual('il y a 1 minute', d.diff_for_humans())

            d = Pendulum.now().subtract(minutes=2)
            self.assertEqual('il y a 2 minutes', d.diff_for_humans())

            d = Pendulum.now().subtract(hours=1)
            self.assertEqual('il y a 1 heure', d.diff_for_humans())

            d = Pendulum.now().subtract(hours=2)
            self.assertEqual('il y a 2 heures', d.diff_for_humans())

            d = Pendulum.now().subtract(days=1)
            self.assertEqual('il y a 1 jour', d.diff_for_humans())

            d = Pendulum.now().subtract(days=2)
            self.assertEqual('il y a 2 jours', d.diff_for_humans())

            d = Pendulum.now().subtract(weeks=1)
            self.assertEqual('il y a 1 semaine', d.diff_for_humans())

            d = Pendulum.now().subtract(weeks=2)
            self.assertEqual('il y a 2 semaines', d.diff_for_humans())

            d = Pendulum.now().subtract(months=1)
            self.assertEqual('il y a 1 mois', d.diff_for_humans())

            d = Pendulum.now().subtract(months=2)
            self.assertEqual('il y a 2 mois', d.diff_for_humans())

            d = Pendulum.now().subtract(years=1)
            self.assertEqual('il y a 1 an', d.diff_for_humans())

            d = Pendulum.now().subtract(years=2)
            self.assertEqual('il y a 2 ans', d.diff_for_humans())

            d = Pendulum.now().add(seconds=1)
            self.assertEqual('dans 1 seconde', d.diff_for_humans())

            d = Pendulum.now().add(seconds=1)
            d2 = Pendulum.now()
            self.assertEqual('1 seconde après', d.diff_for_humans(d2))
            self.assertEqual('1 seconde avant', d2.diff_for_humans(d))

            self.assertEqual('1 seconde', d.diff_for_humans(d2, True))
            self.assertEqual('2 secondes', d2.diff_for_humans(d.add(seconds=1), True))

    def format(self):
        d = Pendulum(2000, 1, 1, 12, 45, 31)
        self.assertEqual('samedi', d.format('%A'))
        self.assertEqual('sam', d.format('%a'))
        self.assertEqual('janvier', d.format('%B'))
        self.assertEqual('janv', d.format('%b'))
        self.assertEqual('', d.format('%p'))
        self.assertEqual('er', d.format('%t'))
        self.assertEqual('e', d.add(days=1).format('%t'))
