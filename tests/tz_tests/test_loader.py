# -*- coding: utf-8 -*-

from .. import AbstractTestCase
from pendulum.tz.loader import Loader


class TimezoneLoaderTest(AbstractTestCase):

    def test_load_bad_timezone(self):
        self.assertRaises(ValueError, Loader.load, '---NOT A TIMEZONE---')

    def test_load_valid(self):
        self.assertTrue(Loader.load('America/Toronto'))
