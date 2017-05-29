import pendulum

from pendulum import DateTime, timezone

from .. import AbstractTestCase


class CreateFromTimeTest(AbstractTestCase):

    def test_create_from_time_with_defaults(self):
        d = DateTime.create()
        self.assertEqual(d.timestamp, DateTime.utcnow().at(0, 0, 0, 0).timestamp)
        self.assertEqual('UTC', d.timezone_name)

    def test_create_from_time(self):
        d = DateTime.create(hour=23, minute=5, second=11)
        now = DateTime.utcnow()
        self.assertDateTime(d, now.year, now.month, now.day, 23, 5, 11)
        self.assertEqual('UTC', d.timezone_name)

    def test_create_from_time_with_hour(self):
        with pendulum.test(DateTime(2016, 8, 11, 12, 34, 56, 123456)):
            d = DateTime.create(hour=23)
            self.assertEqual(23, d.hour)
            self.assertEqual(0, d.minute)
            self.assertEqual(0, d.second)
            self.assertEqual(0, d.microsecond)

    def test_create_from_time_with_minute(self):
        d = DateTime.create(minute=5)
        self.assertEqual(5, d.minute)

    def test_create_from_time_with_second(self):
        d = DateTime.create(second=11)
        self.assertEqual(11, d.second)

    def test_create_from_time_with_timezone_string(self):
        d = DateTime.create(hour=23, minute=5, second=11, tz='Europe/London')
        now = DateTime.now('Europe/London')
        self.assertDateTime(d, now.year, now.month, now.day, 23, 5, 11)
        self.assertEqual('Europe/London', d.timezone_name)

    def test_create_from_time_with_timezone(self):
        d = DateTime.create(hour=23, minute=5, second=11, tz=timezone('Europe/London'))
        now = DateTime.now('Europe/London')
        self.assertDateTime(d, now.year, now.month, now.day, 23, 5, 11)
        self.assertEqual('Europe/London', d.timezone_name)
