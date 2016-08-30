# -*- coding: utf-8 -*-

from pendulum import Pendulum


class AbstractLocalizationTestCase(object):

    locale = None

    def setUp(self):
        Pendulum.set_locale(self.locale)

    def tearDown(self):
        Pendulum.set_locale('en')

    def test_diff_for_humans_localized(self):
        with Pendulum.test(Pendulum(2016, 8, 29)):
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
