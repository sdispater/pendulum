# -*- coding: utf-8 -*-

from pendulum import Pendulum

from .. import AbstractTestCase
from . import AbstractLocalizationTestCase



class LtTest(AbstractLocalizationTestCase, AbstractTestCase):

    locale = 'lt'

    def diff_for_humans(self):
        d = Pendulum.now().subtract(seconds=1)
        self.assertEqual('prieš 1 sekundę', d.diff_for_humans())

        d = Pendulum.now().subtract(seconds=2)
        self.assertEqual('prieš 2 sekundes', d.diff_for_humans())

        d = Pendulum.now().subtract(seconds=21)
        self.assertEqual('prieš 21 sekundę', d.diff_for_humans())

        d = Pendulum.now().subtract(minutes=1)
        self.assertEqual('prieš 1 minutę', d.diff_for_humans())

        d = Pendulum.now().subtract(minutes=2)
        self.assertEqual('prieš 2 minutes', d.diff_for_humans())

        d = Pendulum.now().subtract(hours=1)
        self.assertEqual('prieš 1 valandą', d.diff_for_humans())

        d = Pendulum.now().subtract(hours=2)
        self.assertEqual('prieš 2 valandas', d.diff_for_humans())

        d = Pendulum.now().subtract(days=1)
        self.assertEqual('prieš 1 dieną', d.diff_for_humans())

        d = Pendulum.now().subtract(days=2)
        self.assertEqual('prieš 2 dienas', d.diff_for_humans())

        d = Pendulum.now().subtract(weeks=1)
        self.assertEqual('prieš 1 savaitę', d.diff_for_humans())

        d = Pendulum.now().subtract(weeks=2)
        self.assertEqual('prieš 2 savaites', d.diff_for_humans())

        d = Pendulum.now().subtract(months=1)
        self.assertEqual('prieš 1 mėnesį', d.diff_for_humans())

        d = Pendulum.now().subtract(months=2)
        self.assertEqual('prieš 2 mėnesius', d.diff_for_humans())

        d = Pendulum.now().subtract(years=1)
        self.assertEqual('prieš 1 metus', d.diff_for_humans())

        d = Pendulum.now().subtract(years=2)
        self.assertEqual('prieš 2 metus', d.diff_for_humans())

        d = Pendulum.now().add(seconds=1)
        self.assertEqual('už 1 sekundės', d.diff_for_humans())

        d = Pendulum.now().add(seconds=1)
        d2 = Pendulum.now()
        self.assertEqual('po 1 sekundę', d.diff_for_humans(d2))
        self.assertEqual('1 sekundę nuo dabar', d2.diff_for_humans(d))

        self.assertEqual('1 sekundę', d.diff_for_humans(d2, True))
        self.assertEqual('2 sekundes', d2.diff_for_humans(d.add(seconds=1), True))
