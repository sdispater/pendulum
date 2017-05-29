from pendulum import Duration

from .. import AbstractTestCase


class ArithmeticTestCase(AbstractTestCase):

    def test_multiply(self):
        it = Duration(days=6, seconds=34, microseconds=522222)
        mul = it * 2
        self.assertIsInstanceOfDuration(mul)
        self.assertDuration(mul, 1, 5, 0, 1, 9, 44444)

        it = Duration(days=6, seconds=34, microseconds=522222)
        mul = 2 * it
        self.assertIsInstanceOfDuration(mul)
        self.assertDuration(mul, 1, 5, 0, 1, 9, 44444)

    def test_divide(self):
        it = Duration(days=2, seconds=34, microseconds=522222)
        mul = it / 2
        self.assertIsInstanceOfDuration(mul)
        self.assertDuration(mul, 0, 1, 0, 0, 17, 261111)

        it = Duration(days=2, seconds=35, microseconds=522222)
        mul = it / 2
        self.assertIsInstanceOfDuration(mul)
        self.assertDuration(mul, 0, 1, 0, 0, 17, 761111)

    def test_floor_divide(self):
        it = Duration(days=2, seconds=34, microseconds=522222)
        mul = it // 2
        self.assertIsInstanceOfDuration(mul)
        self.assertDuration(mul, 0, 1, 0, 0, 17, 261111)

        it = Duration(days=2, seconds=35, microseconds=522222)
        mul = it // 3
        self.assertIsInstanceOfDuration(mul)
        self.assertDuration(mul, 0, 0, 16, 0, 11, 840740)
