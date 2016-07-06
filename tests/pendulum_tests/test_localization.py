# -*- coding: utf-8 -*-

from pendulum import Pendulum

from .. import AbstractTestCase


class LocalizationTest(AbstractTestCase):

    malformed_locales = [
        'DE',
        'pt-BR',
        'pt-br',
        'PT-br',
        'PT-BR',
        'pt_br',
        'PT_BR',
        'PT_BR'
    ]

    def test_get_locale(self):
        self.assertEqual('en', Pendulum.get_locale())

    def test_set_locale(self):
        Pendulum.set_locale('fr')
        self.assertEqual('fr', Pendulum.get_locale())
        Pendulum.set_locale('en')

    def test_set_locale_malformed_locales(self):
        for locale in self.malformed_locales:
            self.assertTrue(Pendulum.set_locale(locale))

        Pendulum.set_locale('en')
