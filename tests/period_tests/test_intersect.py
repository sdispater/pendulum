from pendulum import Period, DateTime

from .. import AbstractTestCase


class IntersectTestCase(AbstractTestCase):

    def test_intersect_included(self):
        start = DateTime(2016, 8, 7)
        end = start.add(weeks=1)
        p1 = Period(start, end)
        intersection = p1.intersect(Period(start.add(days=2), start.add(days=4)))

        self.assertDateTime(intersection.start, 2016, 8, 9)
        self.assertDateTime(intersection.end, 2016, 8, 11)

    def test_intersect_overlap(self):
        start = DateTime(2016, 8, 7)
        end = start.add(weeks=1)
        p1 = Period(start, end)
        intersection = p1.intersect(Period(start.add(days=-2), start.add(days=2)))

        self.assertDateTime(intersection.start, 2016, 8, 7)
        self.assertDateTime(intersection.end, 2016, 8, 9)

    def test_intersect_multiple(self):
        start = DateTime(2016, 8, 7)
        end = start.add(weeks=1)
        p1 = Period(start, end)
        intersection = p1.intersect(
            Period(start.add(days=-2), start.add(days=2)),
            Period(start.add(days=1), start.add(days=2))
        )

        self.assertDateTime(intersection.start, 2016, 8, 8)
        self.assertDateTime(intersection.end, 2016, 8, 9)

    def test_intersect_excluded(self):
        start = DateTime(2016, 8, 7)
        end = start.add(weeks=1)
        p1 = Period(start, end)
        intersection = p1.intersect(
            Period(start.add(days=-2), start.add(days=-1))
        )

        self.assertIsNone(intersection)

    def test_intersect_same(self):
        start = DateTime(2016, 8, 7)
        end = start.add(weeks=1)
        p1 = Period(start, end)
        intersection = p1.intersect(
            Period(start.copy(), end.copy())
        )

        self.assertDateTime(intersection.start, 2016, 8, 7)
        self.assertDateTime(intersection.end, 2016, 8, 14)
