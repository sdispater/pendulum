# -*- coding: utf-8 -*-

from pendulum import Period

from .. import (AbstractTestCase, eighth, eleventh, fifth, first, fourteenth,
                fourth, ninth, second, seventh, sixth, tenth, third,
                thirteenth, twelfth)


class SortTestCase(AbstractTestCase):

    def test_sort(self):
        first_second = Period(
            start=first,
            end=second
        )
        first_third = Period(
            start=first,
            end=third
        )

        self.assertFalse(first_second < first_second)
        self.assertTrue(first_second < first_third)

        second_third = Period(
            start=second,
            end=third
        )

        self.assertTrue(first_second < second_third)

        third_fourth = Period(
            start=third,
            end=fourth
        )

        self.assertTrue(first_second < third_fourth)
        self.assertTrue(second_third < third_fourth)
