# -*- coding: utf-8 -*-

from pendulum import Pendulum
from . import AbstractTestCase


class StringsTest(AbstractTestCase):

    def test_to_string(self):
        d = Pendulum(microsecond=0)
        self.assertEqual(Pendulum(microsecond=0).to_iso8601_string(True), str(d))

    def test_set_to_string_format(self):
        Pendulum.set_to_string_format('%a, %d %b %y %H:%M:%S %z')
        d = Pendulum(2016, 6, 27, 15, 39, 30)
        self.assertEqual('Mon, 27 Jun 16 15:39:30 +0000', str(d))

    def test_reset_to_string_format(self):
        d = Pendulum(microsecond=0)
        Pendulum.set_to_string_format('123')
        Pendulum.reset_to_string_format()
        self.assertEqual(d.to_iso8601_string(True), str(d))

    def test_to_date_string(self):
        d = Pendulum(1975, 12, 25, 14, 15, 16)
        self.assertEqual('1975-12-25', d.to_date_string())

    def test_to_formatted_date_string(self):
        d = Pendulum(1975, 12, 25, 14, 15, 16)
        self.assertEqual('Dec 25, 1975', d.to_formatted_date_string())

    def test_to_localized_formatted_date_string(self):
        # TODO
        self.skipTest('Not yet implemented')

    def test_to_localized_formatted_timezoned_date_string(self):
        # TODO
        self.skipTest('Not yet implemented')

    def test_to_timestring(self):
        d = Pendulum(1975, 12, 25, 14, 15, 16)
        self.assertEqual('14:15:16', d.to_time_string())

    def test_to_datetime_string(self):
        d = Pendulum(1975, 12, 25, 14, 15, 16)
        self.assertEqual('1975-12-25 14:15:16', d.to_datetime_string())

    def test_to_datetime_string_with_padded_zeroes(self):
        d = Pendulum(2000, 5, 2, 4, 3, 4)
        self.assertEqual('2000-05-02 04:03:04', d.to_datetime_string())

    def test_to_day_datetime_string(self):
        d = Pendulum(1975, 12, 25, 14, 15, 16)
        self.assertEqual('Thu, Dec 25, 1975 2:15 PM', d.to_day_datetime_string())

    def test_to_atom_string(self):
        d = Pendulum(1975, 12, 25, 14, 15, 16, tzinfo='local')
        self.assertEqual('1975-12-25T14:15:16-05:00', d.to_atom_string())

    def test_to_cookie_string(self):
        d = Pendulum(1975, 12, 25, 14, 15, 16, tzinfo='local')
        self.assertEqual('Thursday, 25-Dec-1975 14:15:16 EST', d.to_cookie_string())

    def test_to_iso8601_string(self):
        d = Pendulum(1975, 12, 25, 14, 15, 16, tzinfo='local')
        self.assertEqual('1975-12-25T14:15:16-05:00', d.to_iso8601_string())

    def test_to_iso8601_extended_string(self):
        d = Pendulum(1975, 12, 25, 14, 15, 16, 123456, tzinfo='local')
        self.assertEqual('1975-12-25T14:15:16.123456-05:00', d.to_iso8601_string(True))

    def test_to_rfc822_string(self):
        d = Pendulum(1975, 12, 25, 14, 15, 16, tzinfo='local')
        self.assertEqual('Thu, 25 Dec 75 14:15:16 -0500', d.to_rfc822_string())

    def test_to_rfc850_string(self):
        d = Pendulum(1975, 12, 25, 14, 15, 16, tzinfo='local')
        self.assertEqual('Thursday, 25-Dec-75 14:15:16 EST', d.to_rfc850_string())

    def test_to_rfc1036_string(self):
        d = Pendulum(1975, 12, 25, 14, 15, 16, tzinfo='local')
        self.assertEqual('Thu, 25 Dec 75 14:15:16 -0500', d.to_rfc1036_string())

    def test_to_rfc1123_string(self):
        d = Pendulum(1975, 12, 25, 14, 15, 16, tzinfo='local')
        self.assertEqual('Thu, 25 Dec 1975 14:15:16 -0500', d.to_rfc1123_string())

    def test_to_rfc2822_string(self):
        d = Pendulum(1975, 12, 25, 14, 15, 16, tzinfo='local')
        self.assertEqual('Thu, 25 Dec 1975 14:15:16 -0500', d.to_rfc2822_string())

    def test_to_rfc3339_string(self):
        d = Pendulum(1975, 12, 25, 14, 15, 16, tzinfo='local')
        self.assertEqual('1975-12-25T14:15:16-05:00', d.to_rfc3339_string())

    def test_to_rfc3339_extended_string(self):
        d = Pendulum(1975, 12, 25, 14, 15, 16, 123456, tzinfo='local')
        self.assertEqual('1975-12-25T14:15:16.123456-05:00', d.to_rfc3339_string(True))

    def test_to_rss_string(self):
        d = Pendulum(1975, 12, 25, 14, 15, 16, tzinfo='local')
        self.assertEqual('Thu, 25 Dec 1975 14:15:16 -0500', d.to_rss_string())

    def test_to_w3c_string(self):
        d = Pendulum(1975, 12, 25, 14, 15, 16, tzinfo='local')
        self.assertEqual('1975-12-25T14:15:16-05:00', d.to_w3c_string())
