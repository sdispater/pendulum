# -*- coding: utf-8 -*-

import pendulum
from pendulum import Pendulum


class AbstractLocalizationTestCase(object):

    locale = None

    def setUp(self):
        pendulum.set_locale(self.locale)

    def tearDown(self):
        pendulum.set_locale('en')

    def test_diff_for_humans_localized(self):
        with pendulum.test(Pendulum(2016, 8, 29)):
            self.diff_for_humans()

    def diff_for_humans(self):
        raise NotImplementedError()

    def test_format(self):
        self.format()
        self.format_alternative()

    def format(self):
        pass

    def format_alternative(self):
        pass
