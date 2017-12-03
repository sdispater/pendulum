import pendulum
from pendulum import timezone
from pendulum.tz.timezone_info import TimezoneInfo
from .. import AbstractTestCase


class CreateFromDateTest(AbstractTestCase):

    def test_create_from_date_with_defaults(self):
        d = pendulum.create()
        self.assertEqual(d.timestamp(), pendulum.utcnow().at(0, 0, 0, 0).timestamp())

    def test_create_from_date(self):
        d = pendulum.create(1975, 12, 25)
        self.assertDateTime(d, 1975, 12, 25, 0, 0, 0)

    def test_create_from_date_with_year(self):
        d = pendulum.create(1975)
        self.assertEqual(d.year, 1975)

    def test_create_from_date_with_month(self):
        d = pendulum.create(month=12)
        self.assertEqual(d.month, 12)

    def test_create_from_date_with_day(self):
        d = pendulum.create(day=25)
        self.assertEqual(d.day, 25)

    def test_create_from_date_with_timezone_string(self):
        d = pendulum.create(1975, 12, 25, tz='Europe/London')
        self.assertDateTime(d, 1975, 12, 25)
        self.assertEqual('Europe/London', d.timezone_name)

    def test_create_from_date_with_timezone(self):
        d = pendulum.create(1975, 12, 25, tz=timezone('Europe/London'))
        self.assertDateTime(d, 1975, 12, 25)
        self.assertEqual('Europe/London', d.timezone_name)

    def test_create_from_date_with_tzinfo(self):
        tz = timezone('Europe/London')
        d = pendulum.create(1975, 12, 25, tz=TimezoneInfo(tz, 3600, True, None, ''))
        self.assertDateTime(d, 1975, 12, 25)
        self.assertEqual('Europe/London', d.timezone_name)
