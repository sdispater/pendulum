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
         default_transition_type,
         utc_transition_times) = Loader.load_from_file(tz_file)

        self.assertGreater(len(transitions), 0)
        self.assertGreater(len(transition_types), 0)
        self.assertGreater(len(utc_transition_times), 0)
        self.assertIsNotNone(default_transition_type)

    def test_load_from_file_invalid(self):
        local_path = os.path.join(os.path.split(__file__)[0], '..')
        tz_file = os.path.join(local_path, 'fixtures', 'tz', 'NOT_A_TIMEZONE')
        self.assertRaises(ValueError, Loader.load_from_file, tz_file)

    def test_set_transitions_for_no_transition_database_file(self):
        tz = Loader.load('Etc/UTC')

        self.assertEqual(1, len(tz[0]))
        self.assertEqual(1, len(tz[1]))
