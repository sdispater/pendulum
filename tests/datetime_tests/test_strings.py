import pendulum
import pytest

from pendulum import DateTime
from .. import AbstractTestCase


class StringsTest(AbstractTestCase):

    def test_to_string(self):
        d = DateTime.create(microsecond=0)
        self.assertEqual(DateTime.create(microsecond=0).to_string('iso8601'), str(d))
        d = DateTime.create(microsecond=123456)
        self.assertEqual(DateTime.create(microsecond=123456).to_string('iso8601'), str(d))

    def test_to_atom_string(self):
        d = DateTime(1975, 12, 25, 14, 15, 16, tzinfo='local')
        self.assertEqual('1975-12-25T14:15:16-05:00', d.to_string('atom'))

    def test_to_cookie_string(self):
        d = DateTime(1975, 12, 25, 14, 15, 16, tzinfo='local')
        self.assertEqual('Thursday, 25-Dec-1975 14:15:16 EST', d.to_string('cookie'))

    def test_to_iso8601_string(self):
        d = DateTime(1975, 12, 25, 14, 15, 16, tzinfo='local')
        self.assertEqual('1975-12-25T14:15:16-05:00', d.to_string('iso8601'))

    def test_to_iso8601_extended_string(self):
        d = DateTime(1975, 12, 25, 14, 15, 16, 123456, tzinfo='local')
        self.assertEqual('1975-12-25T14:15:16.123456-05:00', d.to_string('iso8601'))

    def test_to_rfc822_string(self):
        d = DateTime(1975, 12, 25, 14, 15, 16, tzinfo='local')
        self.assertEqual('Thu, 25 Dec 75 14:15:16 -0500', d.to_string('rfc822'))

    def test_to_rfc850_string(self):
        d = DateTime(1975, 12, 25, 14, 15, 16, tzinfo='local')
        self.assertEqual('Thursday, 25-Dec-75 14:15:16 EST', d.to_string('rfc850'))

    def test_to_rfc1036_string(self):
        d = DateTime(1975, 12, 25, 14, 15, 16, tzinfo='local')
        self.assertEqual('Thu, 25 Dec 75 14:15:16 -0500', d.to_string('rfc1036'))

    def test_to_rfc1123_string(self):
        d = DateTime(1975, 12, 25, 14, 15, 16, tzinfo='local')
        self.assertEqual('Thu, 25 Dec 1975 14:15:16 -0500', d.to_string('rfc1123'))

    def test_to_rfc2822_string(self):
        d = DateTime(1975, 12, 25, 14, 15, 16, tzinfo='local')
        self.assertEqual('Thu, 25 Dec 1975 14:15:16 -0500', d.to_string('rfc2822'))

    def test_to_rfc3339_string(self):
        d = DateTime(1975, 12, 25, 14, 15, 16, tzinfo='local')
        self.assertEqual('1975-12-25T14:15:16-05:00', d.to_string('rfc3339'))

    def test_to_rfc3339_extended_string(self):
        d = DateTime(1975, 12, 25, 14, 15, 16, 123456, tzinfo='local')
        self.assertEqual('1975-12-25T14:15:16.123456-05:00', d.to_string('rfc3339'))

    def test_to_rss_string(self):
        d = DateTime(1975, 12, 25, 14, 15, 16, tzinfo='local')
        self.assertEqual('Thu, 25 Dec 1975 14:15:16 -0500', d.to_string('rss'))

    def test_to_w3c_string(self):
        d = DateTime(1975, 12, 25, 14, 15, 16, tzinfo='local')
        self.assertEqual('1975-12-25T14:15:16-05:00', d.to_string('w3c'))

    def test_to_sting_invalid(self):
        d = pendulum.create(1975, 12, 25, 14, 15, 16, tz='local')

        with pytest.raises(ValueError):
            d.to_string('invalid')

    def test_custom_formatters(self):
        d = DateTime(1975, 12, 25, 14, 15, 16, tzinfo='local')
        self.assertEqual(
            'Thursday 25th of December 1975 02:15:16 PM -05:00',
            d.format('%A %d%_t of %B %Y %I:%M:%S %p %_z', formatter='classic')
        )

    def test_repr(self):
        d = DateTime(1975, 12, 25, 14, 15, 16, tzinfo='local')
        self.assertEqual("DateTime(1975, 12, 25, 14, 15, 16, tz='America/Toronto')", repr(d))

        d = DateTime(1975, 12, 25, 14, 15, 16, 123456, tzinfo='local')
        self.assertEqual("DateTime(1975, 12, 25, 14, 15, 16, 123456, tz='America/Toronto')", repr(d))

    def test_format_with_locale(self):
        d = DateTime(1975, 12, 25, 14, 15, 16, tzinfo='local')
        self.assertEqual('jeudi 25e jour de décembre 1975 02:15:16 PM -05:00',
                         d.format('dddd Do [jour de] MMMM YYYY hh:mm:ss A ZZ', locale='fr'))
        self.assertEqual('jeudi 25e jour de décembre 1975 02:15:16  -05:00',
                         d.format('%A %d%_t jour de %B %Y %I:%M:%S %p %_z', locale='fr', formatter='classic'))

    def test_strftime(self):
        d = DateTime(1975, 12, 25, 14, 15, 16, tzinfo='local')
        self.assertEqual('25', d.strftime('%d'))

    def test_for_json(self):
        d = DateTime(1975, 12, 25, 14, 15, 16, tzinfo='local')
        self.assertEqual('1975-12-25T14:15:16-05:00', d.for_json())

    def test_format(self):
        d = DateTime(1975, 12, 25, 14, 15, 16, tzinfo='Europe/Paris')
        self.assertEqual('1975-12-25T14:15:16+01:00', '{}'.format(d))
        self.assertEqual('1975', '{:YYYY}'.format(d))
        self.assertEqual('%1975', '{:%Y}'.format(d))

    def test_format_alternative_formatter(self):
        pendulum.set_formatter('classic')

        d = DateTime(1975, 12, 25, 14, 15, 16, tzinfo='Europe/Paris')
        self.assertEqual('1975-12-25T14:15:16+01:00', '{}'.format(d))
        self.assertEqual('1975', '{:%Y}'.format(d))
