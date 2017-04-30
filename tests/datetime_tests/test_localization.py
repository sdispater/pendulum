from pendulum import DateTime

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
        self.assertEqual('en', DateTime.get_locale())

    def test_set_locale(self):
        DateTime.set_locale('fr')
        self.assertEqual('fr', DateTime.get_locale())
        DateTime.set_locale('en')

    def test_set_locale_malformed_locales(self):
        for locale in self.malformed_locales:
            self.assertTrue(DateTime.set_locale(locale))

        DateTime.set_locale('en')
