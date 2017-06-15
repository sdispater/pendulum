import pendulum
from pendulum import Date
from .. import AbstractTestCase


class StringsTest(AbstractTestCase):

    def test_to_string(self):
        d = Date(2016, 10, 16)
        self.assertEqual('2016-10-16', str(d))

    def test_set_to_string_format(self):
        Date.set_to_string_format('ddd, DD MMM YY')
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
            d.format('%A %d%_t of %B %Y', formatter='classic')
        )

    def test_repr(self):
        d = Date(1975, 12, 25)
        self.assertEqual('Date(1975, 12, 25)', repr(d))
        self.assertEqual('Date(1975, 12, 25)', d.__repr__())

    def test_format_with_locale(self):
        d = Date(1975, 12, 25)
        self.assertEqual('jeudi 25e jour de décembre 1975',
                         d.format('dddd Do [jour de] MMMM YYYY', locale='fr'))
        self.assertEqual('jeudi 25e jour de décembre 1975',
                         d.format('%A %d%_t jour de %B %Y', locale='fr', formatter='classic'))

    def test_strftime(self):
        d = Date(1975, 12, 25)
        self.assertEqual('25', d.strftime('%d'))

    def test_for_json(self):
        d = Date(1975, 12, 25)
        self.assertEqual('1975-12-25', d.for_json())

    def test_format(self):
        d = Date(1975, 12, 25)
        self.assertEqual('1975-12-25', '{}'.format(d))
        self.assertEqual('1975', '{:YYYY}'.format(d))
        self.assertEqual('%1975', '{:%Y}'.format(d))

    def test_format_classic_formatter(self):
        pendulum.set_formatter('classic')

        d = Date(1975, 12, 25)
        self.assertEqual('1975-12-25', '{}'.format(d))
        self.assertEqual('1975', '{:%Y}'.format(d))
        self.assertEqual('1975', '{:%Y}'.format(d))
