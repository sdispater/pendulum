from pendulum.duration import Duration

from .. import AbstractTestCase


class TotalMethodsTest(AbstractTestCase):

    def test_in_weeks(self):
        it = Duration(days=17)
        self.assertEqual(2.43, round(it.total_weeks(), 2))

    def test_in_days(self):
        it = Duration(days=3)
        self.assertEqual(3, it.total_days())

    def test_in_hours(self):
        it = Duration(days=3, minutes=72)
        self.assertEqual(73.2, it.total_hours())

    def test_in_minutes(self):
        it = Duration(minutes=6, seconds=72)
        self.assertEqual(7.2, it.total_minutes())

    def test_in_seconds(self):
        it = Duration(seconds=72, microseconds=123456)
        self.assertEqual(72.123456, it.total_seconds())
