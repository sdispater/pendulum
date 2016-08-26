# -*- coding: utf-8 -*-

from pendulum import Pendulum
from pendulum.formatting.classic_formatter import ClassicFormatter
from .. import AbstractTestCase


class ClassicFormatterTest(AbstractTestCase):

    def test_custom_formatters(self):
        d = Pendulum(1975, 12, 25, 14, 15, 16, tzinfo='local')
        f = ClassicFormatter()
        self.assertEqual(
            'Thursday 25th of December 1975 02:15:16 PM -05:00',
            f.format(d, '%A %-d%_t of %B %Y %I:%M:%S %p %_z')
        )

    def test_format_with_locale(self):
        d = Pendulum(1975, 12, 25, 14, 15, 16, tzinfo='local')
        f = ClassicFormatter()
        self.assertEqual(
            'jeudi 25e jour de décembre 1975 02:15:16  -05:00',
            f.format(d, '%A %-d%_t jour de %B %Y %I:%M:%S %p %_z', locale='fr')
        )

    def test_unlocalizable_directive(self):
        d = Pendulum(1975, 12, 25, 14, 15, 16, tzinfo='local')
        f = ClassicFormatter()
        self.assertRaises(ValueError, f._localize_directive, d, '%8', 'en')
