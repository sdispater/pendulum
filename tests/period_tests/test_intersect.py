import pendulum

from ..conftest import assert_datetime


def test_intersect_included():
    start = pendulum.create(2016, 8, 7)
    end = start.add(weeks=1)
    p1 = pendulum.period(start, end)
    intersection = p1.intersect(pendulum.period(start.add(days=2), start.add(days=4)))

    assert_datetime(intersection.start, 2016, 8, 9)
    assert_datetime(intersection.end, 2016, 8, 11)


def test_intersect_overlap():
    start = pendulum.create(2016, 8, 7)
    end = start.add(weeks=1)
    p1 = pendulum.period(start, end)
    intersection = p1.intersect(pendulum.period(start.add(days=-2), start.add(days=2)))

    assert_datetime(intersection.start, 2016, 8, 7)
    assert_datetime(intersection.end, 2016, 8, 9)


def test_intersect_multiple():
    start = pendulum.create(2016, 8, 7)
    end = start.add(weeks=1)
    p1 = pendulum.period(start, end)
    intersection = p1.intersect(
        pendulum.period(start.add(days=-2), start.add(days=2)),
        pendulum.period(start.add(days=1), start.add(days=2))
    )

    assert_datetime(intersection.start, 2016, 8, 8)
    assert_datetime(intersection.end, 2016, 8, 9)


def test_intersect_excluded():
    start = pendulum.create(2016, 8, 7)
    end = start.add(weeks=1)
    p1 = pendulum.period(start, end)
    intersection = p1.intersect(
        pendulum.period(start.add(days=-2), start.add(days=-1))
    )

    assert intersection is None


def test_intersect_same():
    start = pendulum.create(2016, 8, 7)
    end = start.add(weeks=1)
    p1 = pendulum.period(start, end)
    intersection = p1.intersect(
        pendulum.period(start, end)
    )

    assert_datetime(intersection.start, 2016, 8, 7)
    assert_datetime(intersection.end, 2016, 8, 14)
