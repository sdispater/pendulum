# -*- coding: utf-8 -*-

import pendulum
from pendulum import DateTime
from .. import AbstractTestCase


class StringsTest(AbstractTestCase):

    def test_to_string(self):
        d = DateTime.create(microsecond=0)
        self.assertEqual(DateTime.create(microsecond=0).to_iso8601_string(), str(d))
        d = DateTime.create(microsecond=123456)
        self.assertEqual(DateTime.create(microsecond=123456).to_iso8601_string(True), str(d))

    def test_set_to_string_format(self):
        DateTime.set_to_string_format('%a, %d %b %y %H:%M:%S %z')
        d = DateTime(2016, 6, 27, 15, 39, 30)
        self.assertEqual('Mon, 27 Jun 16 15:39:30 +0000', str(d))

    def test_reset_to_string_format(self):
        d = DateTime.create(microsecond=0)
        DateTime.set_to_string_format('123')
        DateTime.reset_to_string_format()
        self.assertEqual(d.to_iso8601_string(), str(d))

    def test_to_date_string(self):
        d = DateTime(1975, 12, 25, 14, 15, 16)
        self.assertEqual('1975-12-25', d.to_date_string())

    def test_to_formatted_date_string(self):
        d = DateTime(1975, 12, 25, 14, 15, 16)
        self.assertEqual('Dec 25, 1975', d.to_formatted_date_string())

    def test_to_timestring(self):
        d = DateTime(1975, 12, 25, 14, 15, 16)
        self.assertEqual('14:15:16', d.to_time_string())

    def test_to_datetime_string(self):
        d = DateTime(1975, 12, 25, 14, 15, 16)
        self.assertEqual('1975-12-25 14:15:16', d.to_datetime_string())

    def test_to_datetime_string_with_padded_zeroes(self):
        d = DateTime(2000, 5, 2, 4, 3, 4)
        self.assertEqual('2000-05-02 04:03:04', d.to_datetime_string())

    def test_to_day_datetime_string(self):
        d = DateTime(1975, 12, 25, 14, 15, 16)
        self.assertEqual('Thu, Dec 25, 1975 2:15 PM', d.to_day_datetime_string())

    def test_to_atom_string(self):
        d = DateTime(1975, 12, 25, 14, 15, 16, tzinfo='local')
        self.assertEqual('1975-12-25T14:15:16-05:00', d.to_atom_string())

    def test_to_cookie_string(self):
        d = DateTime(1975, 12, 25, 14, 15, 16, tzinfo='local')
        self.assertEqual('Thursday, 25-Dec-1975 14:15:16 EST', d.to_cookie_string())

    def test_to_iso8601_string(self):
        d = DateTime(1975, 12, 25, 14, 15, 16, tzinfo='local')
        self.assertEqual('1975-12-25T14:15:16-05:00', d.to_iso8601_string())

    def test_to_iso8601_extended_string(self):
        d = DateTime(1975, 12, 25, 14, 15, 16, 123456, tzinfo='local')
        self.assertEqual('1975-12-25T14:15:16.123456-05:00', d.to_iso8601_string(True))

    def test_to_rfc822_string(self):
        d = DateTime(1975, 12, 25, 14, 15, 16, tzinfo='local')
        self.assertEqual('Thu, 25 Dec 75 14:15:16 -0500', d.to_rfc822_string())

    def test_to_rfc850_string(self):
        d = DateTime(1975, 12, 25, 14, 15, 16, tzinfo='local')
        self.assertEqual('Thursday, 25-Dec-75 14:15:16 EST', d.to_rfc850_string())

    def test_to_rfc1036_string(self):
        d = DateTime(1975, 12, 25, 14, 15, 16, tzinfo='local')
        self.assertEqual('Thu, 25 Dec 75 14:15:16 -0500', d.to_rfc1036_string())

    def test_to_rfc1123_string(self):
        d = DateTime(1975, 12, 25, 14, 15, 16, tzinfo='local')
        self.assertEqual('Thu, 25 Dec 1975 14:15:16 -0500', d.to_rfc1123_string())

    def test_to_rfc2822_string(self):
        d = DateTime(1975, 12, 25, 14, 15, 16, tzinfo='local')
        self.assertEqual('Thu, 25 Dec 1975 14:15:16 -0500', d.to_rfc2822_string())

    def test_to_rfc3339_string(self):
        d = DateTime(1975, 12, 25, 14, 15, 16, tzinfo='local')
        self.assertEqual('1975-12-25T14:15:16-05:00', d.to_rfc3339_string())

    def test_to_rfc3339_extended_string(self):
        d = DateTime(1975, 12, 25, 14, 15, 16, 123456, tzinfo='local')
        self.assertEqual('1975-12-25T14:15:16.123456-05:00', d.to_rfc3339_string(True))

    def test_to_rss_string(self):
        d = DateTime(1975, 12, 25, 14, 15, 16, tzinfo='local')
        self.assertEqual('Thu, 25 Dec 1975 14:15:16 -0500', d.to_rss_string())

    def test_to_w3c_string(self):
        d = DateTime(1975, 12, 25, 14, 15, 16, tzinfo='local')
        self.assertEqual('1975-12-25T14:15:16-05:00', d.to_w3c_string())

    def test_custom_formatters(self):
        d = DateTime(1975, 12, 25, 14, 15, 16, tzinfo='local')
        self.assertEqual(
            'Thursday 25th of December 1975 02:15:16 PM -05:00',
            d.format('%A %d%_t of %B %Y %I:%M:%S %p %_z')
        )

    def test_repr(self):
        d = DateTime(1975, 12, 25, 14, 15, 16, tzinfo='local')
        self.assertEqual('<DateTime [1975-12-25T14:15:16-05:00]>', repr(d))

    def test_format_with_locale(self):
        d = DateTime(1975, 12, 25, 14, 15, 16, tzinfo='local')
        self.assertEqual('jeudi 25e jour de décembre 1975 02:15:16  -05:00',
                         d.format('%A %d%_t jour de %B %Y %I:%M:%S %p %_z', locale='fr'))

    def test_set_formatter_globally(self):
        pendulum.DateTime.set_formatter('alternative')
        self.assertEqual('alternative', pendulum.DateTime.get_formatter())

        d = DateTime(1975, 12, 25, 14, 15, 16, tzinfo='local')
        self.assertEqual(
            'Thursday 25th of December 1975 02:15:16 PM -05:00',
            d.format('dddd Do [of] MMMM YYYY hh:mm:ss A ZZ')
        )
        pendulum.DateTime.set_formatter()
        self.assertEqual(
            'dddd Do [of] MMMM YYYY hh:mm:ss A ZZ',
            d.format('dddd Do [of] MMMM YYYY hh:mm:ss A ZZ')
        )

    def test_invalid_formatter(self):
        d = DateTime(1975, 12, 25, 14, 15, 16, tzinfo='local')
        self.assertRaises(ValueError, d.format, '', formatter='invalid')
        self.assertRaises(ValueError, pendulum.set_formatter, 'invalid')

    def test_strftime(self):
        d = DateTime(1975, 12, 25, 14, 15, 16, tzinfo='local')
        self.assertEqual('25', d.strftime('%d'))

    def test_for_json(self):
        d = DateTime(1975, 12, 25, 14, 15, 16, tzinfo='local')
        self.assertEqual('1975-12-25T14:15:16-05:00', d.for_json())

    def test_format(self):
        d = DateTime(1975, 12, 25, 14, 15, 16, tzinfo='Europe/Paris')
        self.assertEqual('1975-12-25T14:15:16+01:00', '{}'.format(d))
        self.assertEqual('1975', '{:%Y}'.format(d))

    def test_format_alternative_formatter(self):
        pendulum.set_formatter('alternative')
        d = DateTime(1975, 12, 25, 14, 15, 16, tzinfo='Europe/Paris')

        self.assertEqual('1975-12-25T14:15:16+01:00', '{}'.format(d))
        self.assertEqual('1975', '{:YYYY}'.format(d))
        self.assertEqual('%1975', '{:%Y}'.format(d))
