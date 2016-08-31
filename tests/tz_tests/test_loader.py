# -*- coding: utf-8 -*-

import os
from .. import AbstractTestCase
from pendulum.tz.loader import Loader


class TimezoneLoaderTest(AbstractTestCase):

    def test_load_bad_timezone(self):
        self.assertRaises(ValueError, Loader.load, '---NOT A TIMEZONE---')

    def test_load_valid(self):
        self.assertTrue(Loader.load('America/Toronto'))

    def test_load_from_file(self):
        local_path = os.path.join(os.path.split(__file__)[0], '..')
        tz_file = os.path.join(local_path, 'fixtures', 'tz', 'Paris')
        (transitions,
         transition_types,
         default_transition_type) = Loader.load_from_file(tz_file)

        self.assertGreater(len(transitions), 0)
        self.assertGreater(len(transition_types), 0)
        self.assertIsNotNone(default_transition_type)

    def test_load_from_file_invalid(self):
        local_path = os.path.join(os.path.split(__file__)[0], '..')
        tz_file = os.path.join(local_path, 'fixtures', 'tz', 'NOT_A_TIMEZONE')
        self.assertRaises(ValueError, Loader.load_from_file, tz_file)
