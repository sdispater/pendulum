# -*- coding: utf-8 -*-

from pendulum import DateTime

from .. import AbstractTestCase
from . import AbstractLocalizationTestCase



class FoTest(AbstractLocalizationTestCase, AbstractTestCase):

    locale = 'fo'

    def diff_for_humans(self):
        d = DateTime.now().subtract(seconds=1)
        self.assertEqual('1 sekund síðan', d.diff_for_humans())

        d = DateTime.now().subtract(seconds=2)
        self.assertEqual('2 sekundir síðan', d.diff_for_humans())

        d = DateTime.now().subtract(minutes=1)
        self.assertEqual('1 minutt síðan', d.diff_for_humans())

        d = DateTime.now().subtract(minutes=2)
        self.assertEqual('2 minuttir síðan', d.diff_for_humans())

        d = DateTime.now().subtract(hours=1)
        self.assertEqual('1 tími síðan', d.diff_for_humans())

        d = DateTime.now().subtract(hours=2)
        self.assertEqual('2 tímar síðan', d.diff_for_humans())

        d = DateTime.now().subtract(days=1)
        self.assertEqual('1 dag síðan', d.diff_for_humans())

        d = DateTime.now().subtract(days=2)
        self.assertEqual('2 dagar síðan', d.diff_for_humans())

        d = DateTime.now().subtract(weeks=1)
        self.assertEqual('1 vika síðan', d.diff_for_humans())

        d = DateTime.now().subtract(weeks=2)
        self.assertEqual('2 vikur síðan', d.diff_for_humans())

        d = DateTime.now().subtract(months=1)
        self.assertEqual('1 mánaður síðan', d.diff_for_humans())

        d = DateTime.now().subtract(months=2)
        self.assertEqual('2 mánaðir síðan', d.diff_for_humans())

        d = DateTime.now().subtract(years=1)
        self.assertEqual('1 ár síðan', d.diff_for_humans())

        d = DateTime.now().subtract(years=2)
        self.assertEqual('2 ár síðan', d.diff_for_humans())

        d = DateTime.now().add(seconds=1)
        self.assertEqual('um 1 sekund', d.diff_for_humans())

        d = DateTime.now().add(seconds=1)
        d2 = DateTime.now()
        self.assertEqual('1 sekund aftaná', d.diff_for_humans(d2))
        self.assertEqual('1 sekund áðrenn', d2.diff_for_humans(d))

        self.assertEqual('1 sekund', d.diff_for_humans(d2, True))
        self.assertEqual('2 sekundir', d2.diff_for_humans(d.add(seconds=1), True))
