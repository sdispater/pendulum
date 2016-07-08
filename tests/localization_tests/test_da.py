# -*- coding: utf-8 -*-

from pendulum import Pendulum

from .. import AbstractTestCase
from . import AbstractLocalizationTestCase



class DaTest(AbstractLocalizationTestCase, AbstractTestCase):

    locale = 'da'

    def diff_for_humans(self):
        with self.wrap_with_test_now():
            d = Pendulum.now().sub(seconds=1)
            self.assertEqual('1 sekund siden', d.diff_for_humans())

            d = Pendulum.now().sub(seconds=2)
            self.assertEqual('2 sekunder siden', d.diff_for_humans())

            d = Pendulum.now().sub(minutes=1)
            self.assertEqual('1 minut siden', d.diff_for_humans())

            d = Pendulum.now().sub(minutes=2)
            self.assertEqual('2 minutter siden', d.diff_for_humans())

            d = Pendulum.now().sub(hours=1)
            self.assertEqual('1 time siden', d.diff_for_humans())

            d = Pendulum.now().sub(hours=2)
            self.assertEqual('2 timer siden', d.diff_for_humans())

            d = Pendulum.now().sub(days=1)
            self.assertEqual('1 dag siden', d.diff_for_humans())

            d = Pendulum.now().sub(days=2)
            self.assertEqual('2 dage siden', d.diff_for_humans())

            d = Pendulum.now().sub(weeks=1)
            self.assertEqual('1 uge siden', d.diff_for_humans())

            d = Pendulum.now().sub(weeks=2)
            self.assertEqual('2 uger siden', d.diff_for_humans())

            d = Pendulum.now().sub(months=1)
            self.assertEqual('1 måned siden', d.diff_for_humans())

            d = Pendulum.now().sub(months=2)
            self.assertEqual('2 måneder siden', d.diff_for_humans())

            d = Pendulum.now().sub(years=1)
            self.assertEqual('1 år siden', d.diff_for_humans())

            d = Pendulum.now().sub(years=2)
            self.assertEqual('2 år siden', d.diff_for_humans())

            d = Pendulum.now().add(seconds=1)
            self.assertEqual('om 1 sekund', d.diff_for_humans())

            d = Pendulum.now().add(seconds=1)
            d2 = Pendulum.now()
            self.assertEqual('1 sekund efter', d.diff_for_humans(d2))
            self.assertEqual('1 sekund før', d2.diff_for_humans(d))

            self.assertEqual('1 sekund', d.diff_for_humans(d2, True))
            self.assertEqual('2 sekunder', d2.diff_for_humans(d.add(seconds=1), True))
