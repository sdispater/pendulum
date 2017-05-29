from pendulum.duration import Duration

from .. import AbstractTestCase


class InMethodsTest(AbstractTestCase):

    def test_in_weeks(self):
        it = Duration(days=17)
        self.assertEqual(2, it.in_weeks())

    def test_in_days(self):
        it = Duration(days=3)
        self.assertEqual(3, it.in_days())

    def test_in_hours(self):
        it = Duration(days=3, minutes=72)
        self.assertEqual(73, it.in_hours())

    def test_in_minutes(self):
        it = Duration(minutes=6, seconds=72)
        self.assertEqual(7, it.in_minutes())

    def test_in_seconds(self):
        it = Duration(seconds=72)
        self.assertEqual(72, it.in_seconds())
