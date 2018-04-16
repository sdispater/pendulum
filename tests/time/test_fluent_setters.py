from pendulum import Time

from ..conftest import assert_time


def test_replace():
    t = Time(12, 34, 56, 123456)
    t = t.replace(1, 2, 3, 654321)

    assert isinstance(t, Time)
    assert_time(t, 1, 2, 3, 654321)
