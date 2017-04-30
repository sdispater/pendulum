import pytz
from pendulum import DateTime, timezone
from .. import AbstractTestCase


class CreateFromFormatTest(AbstractTestCase):

    def test_create_from_format_returns_pendulum(self):
        d = DateTime.create_from_format('1975-05-21 22:32:11', '%Y-%m-%d %H:%M:%S')
        self.assertDateTime(d, 1975, 5, 21, 22, 32, 11)
        self.assertIsInstanceOfDateTime(d)
        self.assertEqual('UTC', d.timezone_name)

    def test_create_from_format_with_timezone_string(self):
        d = DateTime.create_from_format('1975-05-21 22:32:11', '%Y-%m-%d %H:%M:%S', 'Europe/London')
        self.assertDateTime(d, 1975, 5, 21, 22, 32, 11)
        self.assertEqual('Europe/London', d.timezone_name)

    def test_create_from_format_with_timezone(self):
        d = DateTime.create_from_format(
            '1975-05-21 22:32:11', '%Y-%m-%d %H:%M:%S', timezone('Europe/London')
        )
        self.assertDateTime(d, 1975, 5, 21, 22, 32, 11)
        self.assertEqual('Europe/London', d.timezone_name)

    def test_create_from_format_with_millis(self):
        d = DateTime.create_from_format(
            '1975-05-21 22:32:11.123456', '%Y-%m-%d %H:%M:%S.%f'
        )
        self.assertDateTime(d, 1975, 5, 21, 22, 32, 11)
        self.assertEqual(123456, d.microsecond)

    def test_strptime_is_create_from_format(self):
        d = DateTime.strptime('1975-05-21 22:32:11', '%Y-%m-%d %H:%M:%S')
        self.assertDateTime(d, 1975, 5, 21, 22, 32, 11)
        self.assertIsInstanceOfDateTime(d)
        self.assertEqual('UTC', d.timezone_name)
