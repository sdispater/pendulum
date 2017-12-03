import pendulum
import pytest

from pendulum import DateTime
from .. import AbstractTestCase


class StringsTest(AbstractTestCase):

    def test_to_string(self):
        d = pendulum.create(microsecond=0)
        self.assertEqual(pendulum.create(microsecond=0).to_iso8601_string(), str(d))
        d = pendulum.create(microsecond=123456)
        self.assertEqual(pendulum.create(microsecond=123456).to_iso8601_string(), str(d))

    def test_to_date_string(self):
        d = pendulum.create(1975, 12, 25, 14, 15, 16)

        assert '1975-12-25' == d.to_date_string()

    def test_to_formatted_date_string(self):
        d = pendulum.create(1975, 12, 25, 14, 15, 16)

        assert 'Dec 25, 1975' == d.to_formatted_date_string()

    def test_to_timestring(self):
        d = pendulum.create(1975, 12, 25, 14, 15, 16)

        assert '14:15:16' == d.to_time_string()

    def test_to_atom_string(self):
        d = pendulum.create(1975, 12, 25, 14, 15, 16, tz='local')
        self.assertEqual('1975-12-25T14:15:16-05:00', d.to_atom_string())

    def test_to_cookie_string(self):
        d = pendulum.create(1975, 12, 25, 14, 15, 16, tz='local')
        self.assertEqual('Thursday, 25-Dec-1975 14:15:16 EST', d.to_cookie_string())

    def test_to_iso8601_string(self):
        d = pendulum.create(1975, 12, 25, 14, 15, 16, tz='local')
        self.assertEqual('1975-12-25T14:15:16-05:00', d.to_iso8601_string())

    def test_to_iso8601_extended_string(self):
        d = pendulum.create(1975, 12, 25, 14, 15, 16, 123456, tz='local')
        self.assertEqual('1975-12-25T14:15:16.123456-05:00', d.to_iso8601_string())

    def test_to_rfc822_string(self):
        d = pendulum.create(1975, 12, 25, 14, 15, 16, tz='local')
        self.assertEqual('Thu, 25 Dec 75 14:15:16 -0500', d.to_rfc822_string())

    def test_to_rfc850_string(self):
        d = pendulum.create(1975, 12, 25, 14, 15, 16, tz='local')
        self.assertEqual('Thursday, 25-Dec-75 14:15:16 EST', d.to_rfc850_string())

    def test_to_rfc1036_string(self):
        d = pendulum.create(1975, 12, 25, 14, 15, 16, tz='local')
        self.assertEqual('Thu, 25 Dec 75 14:15:16 -0500', d.to_rfc1036_string())

    def test_to_rfc1123_string(self):
        d = pendulum.create(1975, 12, 25, 14, 15, 16, tz='local')
        self.assertEqual('Thu, 25 Dec 1975 14:15:16 -0500', d.to_rfc1123_string())

    def test_to_rfc2822_string(self):
        d = pendulum.create(1975, 12, 25, 14, 15, 16, tz='local')
        self.assertEqual('Thu, 25 Dec 1975 14:15:16 -0500', d.to_rfc2822_string())

    def test_to_rfc3339_string(self):
        d = pendulum.create(1975, 12, 25, 14, 15, 16, tz='local')
        self.assertEqual('1975-12-25T14:15:16-05:00', d.to_rfc3339_string())

    def test_to_rfc3339_extended_string(self):
        d = pendulum.create(1975, 12, 25, 14, 15, 16, 123456, tz='local')
        self.assertEqual('1975-12-25T14:15:16.123456-05:00', d.to_rfc3339_string())

    def test_to_rss_string(self):
        d = pendulum.create(1975, 12, 25, 14, 15, 16, tz='local')
        self.assertEqual('Thu, 25 Dec 1975 14:15:16 -0500', d.to_rss_string())

    def test_to_w3c_string(self):
        d = pendulum.create(1975, 12, 25, 14, 15, 16, tz='local')
        self.assertEqual('1975-12-25T14:15:16-05:00', d.to_w3c_string())

    def test_to_string_invalid(self):
        d = pendulum.create(1975, 12, 25, 14, 15, 16, tz='local')

        with pytest.raises(ValueError):
            d._to_string('invalid')

    def test_custom_formatters(self):
        d = pendulum.create(1975, 12, 25, 14, 15, 16, tz='local')
        self.assertEqual(
            'Thursday 25th of December 1975 02:15:16 PM -05:00',
            d.format('%A %d%_t of %B %Y %I:%M:%S %p %_z', formatter='classic')
        )

    def test_repr(self):
        d = pendulum.create(1975, 12, 25, 14, 15, 16, tz='local')
        self.assertEqual(
            f"DateTime(1975, 12, 25, 14, 15, 16, tzinfo={repr(d.tzinfo)})",
            repr(d)
        )

        d = pendulum.create(1975, 12, 25, 14, 15, 16, 123456, tz='local')
        self.assertEqual(
            f"DateTime(1975, 12, 25, 14, 15, 16, 123456, tzinfo={repr(d.tzinfo)})",
            repr(d)
        )

    def test_format_with_locale(self):
        d = pendulum.create(1975, 12, 25, 14, 15, 16, tz='local')
        self.assertEqual('jeudi 25e jour de décembre 1975 02:15:16 PM -05:00',
                         d.format('dddd Do [jour de] MMMM YYYY hh:mm:ss A ZZ', locale='fr'))
        self.assertEqual('jeudi 25e jour de décembre 1975 02:15:16  -05:00',
                         d.format('%A %d%_t jour de %B %Y %I:%M:%S %p %_z', locale='fr', formatter='classic'))

    def test_strftime(self):
        d = pendulum.create(1975, 12, 25, 14, 15, 16, tz='local')
        self.assertEqual('25', d.strftime('%d'))

    def test_for_json(self):
        d = pendulum.create(1975, 12, 25, 14, 15, 16, tz='local')
        self.assertEqual('1975-12-25T14:15:16-05:00', d.for_json())

    def test_format(self):
        d = pendulum.create(1975, 12, 25, 14, 15, 16, tz='Europe/Paris')
        self.assertEqual('1975-12-25T14:15:16+01:00', '{}'.format(d))
        self.assertEqual('1975', '{:YYYY}'.format(d))
        self.assertEqual('%1975', '{:%Y}'.format(d))

    def test_format_alternative_formatter(self):
        pendulum.set_formatter('classic')

        d = pendulum.create(1975, 12, 25, 14, 15, 16, tz='Europe/Paris')
        self.assertEqual('1975-12-25T14:15:16+01:00', '{}'.format(d))
        self.assertEqual('1975', '{:%Y}'.format(d))
