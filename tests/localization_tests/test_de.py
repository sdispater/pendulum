# -*- coding: utf-8 -*-

from pendulum import DateTime

from .. import AbstractTestCase
from . import AbstractLocalizationTestCase



class DeTest(AbstractLocalizationTestCase, AbstractTestCase):

    locale = 'de'

    def diff_for_humans(self):
        d = DateTime.now().subtract(seconds=1)
        self.assertEqual('vor 1 Sekunde', d.diff_for_humans())

        d = DateTime.now().subtract(seconds=2)
        self.assertEqual('vor 2 Sekunden', d.diff_for_humans())

        d = DateTime.now().subtract(minutes=1)
        self.assertEqual('vor 1 Minute', d.diff_for_humans())

        d = DateTime.now().subtract(minutes=2)
        self.assertEqual('vor 2 Minuten', d.diff_for_humans())

        d = DateTime.now().subtract(hours=1)
        self.assertEqual('vor 1 Stunde', d.diff_for_humans())

        d = DateTime.now().subtract(hours=2)
        self.assertEqual('vor 2 Stunden', d.diff_for_humans())

        d = DateTime.now().subtract(days=1)
        self.assertEqual('vor 1 Tag', d.diff_for_humans())

        d = DateTime.now().subtract(days=2)
        self.assertEqual('vor 2 Tagen', d.diff_for_humans())

        d = DateTime.now().subtract(weeks=1)
        self.assertEqual('vor 1 Woche', d.diff_for_humans())

        d = DateTime.now().subtract(weeks=2)
        self.assertEqual('vor 2 Wochen', d.diff_for_humans())

        d = DateTime.now().subtract(months=1)
        self.assertEqual('vor 1 Monat', d.diff_for_humans())

        d = DateTime.now().subtract(months=2)
        self.assertEqual('vor 2 Monaten', d.diff_for_humans())

        d = DateTime.now().subtract(years=1)
        self.assertEqual('vor 1 Jahr', d.diff_for_humans())

        d = DateTime.now().subtract(years=2)
        self.assertEqual('vor 2 Jahren', d.diff_for_humans())

        d = DateTime.now().add(seconds=1)
        self.assertEqual('in 1 Sekunde', d.diff_for_humans())

        d = DateTime.now().add(seconds=1)
        d2 = DateTime.now()
        self.assertEqual('1 Sekunde später', d.diff_for_humans(d2))
        self.assertEqual('1 Sekunde zuvor', d2.diff_for_humans(d))

        self.assertEqual('1 Sekunde', d.diff_for_humans(d2, True))
        self.assertEqual('2 Sekunden', d2.diff_for_humans(d.add(seconds=1), True))
