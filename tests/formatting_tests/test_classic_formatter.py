# -*- coding: utf-8 -*-

import re
from pendulum import Pendulum, Date
from pendulum.formatting.classic_formatter import ClassicFormatter
from .. import AbstractTestCase


class ClassicFormatterTest(AbstractTestCase):

    def test_custom_formatters(self):
        d = Pendulum(1975, 12, 25, 14, 15, 16, tzinfo='local')
        f = ClassicFormatter()
        self.assertEqual(
            'Thursday 25th of December 1975 02:15:16 PM -05:00',
            f.format(d, '%A %d%_t of %B %Y %I:%M:%S %p %_z')
        )

    def test_format_with_locale(self):
        d = Pendulum(1975, 12, 25, 14, 15, 16, tzinfo='Europe/Paris')
        f = ClassicFormatter()
        self.assertEqual(
            'jeudi 25e jour de décembre 1975 02:15:16  +01:00',
            f.format(d, '%A %d%_t jour de %B %Y %I:%M:%S %p %_z', locale='fr')
        )

    def test_unlocalizable_directive(self):
        d = Pendulum(1975, 12, 25, 14, 15, 16, tzinfo='local')
        f = ClassicFormatter()
        self.assertRaises(ValueError, f._localize_directive, d, '%8', 'en')

    def test_day_of_week(self):
        f = ClassicFormatter()
        d = Pendulum(2016, 8, 28)

        self.assertEqual('Sun', f.format(d, '%a'))
        self.assertEqual('Sunday', f.format(d, '%A'))

        self.assertEqual('dim', f.format(d, '%a', locale='fr'))
        self.assertEqual('dimanche', f.format(d, '%A', locale='fr'))

    def test_month(self):
        f = ClassicFormatter()
        d = Pendulum(2016, 8, 28)

        self.assertEqual('Aug', f.format(d, '%b'))
        self.assertEqual('August', f.format(d, '%B'))

        self.assertEqual('août', f.format(d, '%b', locale='fr'))
        self.assertEqual('août', f.format(d, '%B', locale='fr'))

    def test_strftime(self):
        f = ClassicFormatter()
        d = Pendulum(2016, 8, 28)
        m = re.match('(.*)', '%_TTT')

        self.assertRaises(ValueError, f._strftime, d, m, 'fr')

    def test_accepts_dates(self):
        d = Date(1975, 12, 25)
        f = ClassicFormatter()
        self.assertEqual(
            'Thursday 25th of December 1975',
            f.format(d, '%A %d%_t of %B %Y')
        )
