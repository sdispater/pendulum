# -*- coding: utf-8 -*-

from pendulum import PendulumInterval
from pendulum.translator import Translator

from .. import AbstractTestCase


class LocaleTest(AbstractTestCase):

    def test_get_locale(self):
        pi = PendulumInterval
        self.assertEqual('en', pi.get_locale())

        pi.set_locale('fr')
        self.assertEqual('fr', pi.get_locale())

        pi.set_locale('en')

    def test_set_invalid_locale(self):
        pi = PendulumInterval
        self.assertFalse(pi.set_locale('invalid'))

    def test_set_translator(self):
        pi = PendulumInterval
        t = Translator('en')
        pi.set_translator(t)
        self.assertIs(t, pi.translator())


