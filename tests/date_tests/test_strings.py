# -*- coding: utf-8 -*-

import pendulum
from pendulum import Date
from .. import AbstractTestCase


class StringsTest(AbstractTestCase):

    def test_to_string(self):
        d = Date(2016, 10, 16)
        self.assertEqual('2016-10-16', str(d))

    def test_set_to_string_format(self):
        Date.set_to_string_format('%a, %d %b %y')
        d = Date(2016, 6, 27)
        self.assertEqual('Mon, 27 Jun 16', str(d))

    def test_reset_to_string_format(self):
        d = Date(2016, 10, 16)
        Date.set_to_string_format('123')
        Date.reset_to_string_format()
        self.assertEqual('2016-10-16', str(d))

    def test_to_date_string(self):
        d = Date(1975, 12, 25)
        self.assertEqual('1975-12-25', d.to_date_string())

    def test_to_formatted_date_string(self):
        d = Date(1975, 12, 25)
        self.assertEqual('Dec 25, 1975', d.to_formatted_date_string())

    def test_custom_formatters(self):
        d = Date(1975, 12, 25)
        self.assertEqual(
            'Thursday 25th of December 1975',
            d.format('%A %d%_t of %B %Y')
        )

    def test_repr(self):
        d = Date(1975, 12, 25)
        self.assertEqual('<Date [1975-12-25]>', repr(d))
        self.assertEqual('<Date [1975-12-25]>', d.__repr__())

    def test_format_with_locale(self):
        d = Date(1975, 12, 25)
        self.assertEqual('jeudi 25e jour de décembre 1975',
                         d.format('%A %d%_t jour de %B %Y', locale='fr'))

    def test_set_formatter_globally(self):
        Date.set_formatter('alternative')
        self.assertEqual('alternative', Date.get_formatter())

        d = Date(1975, 12, 25)
        self.assertEqual(
            'Thursday 25th of December 1975',
            d.format('dddd Do [of] MMMM YYYY')
        )
        Date.set_formatter()
        self.assertEqual(
            'dddd Do [of] MMMM YYYY',
            d.format('dddd Do [of] MMMM YYYY')
        )

    def test_invalid_formatter(self):
        d = Date(1975, 12, 25)
        self.assertRaises(ValueError, d.format, '', formatter='invalid')
        self.assertRaises(ValueError, Date.set_formatter, 'invalid')

    def test_strftime(self):
        d = Date(1975, 12, 25)
        self.assertEqual('25', d.strftime('%d'))

    def test_for_json(self):
        d = Date(1975, 12, 25)
        self.assertEqual('1975-12-25', d.for_json())

    def test_format(self):
        d = Date(1975, 12, 25)
        self.assertEqual('1975-12-25', '{}'.format(d))
        self.assertEqual('1975', '{:%Y}'.format(d))

    def test_format_alternative_formatter(self):
        pendulum.set_formatter('alternative')

        d = Date(1975, 12, 25)
        self.assertEqual('1975-12-25', '{}'.format(d))
        self.assertEqual('1975', '{:YYYY}'.format(d))
        self.assertEqual('%1975', '{:%Y}'.format(d))
