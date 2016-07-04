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

    def test_set_locale_malformed_locales(self):
        for locale in self.malformed_locales:
            self.assertTrue(Pendulum.set_locale(locale))

        Pendulum.set_locale('en')
