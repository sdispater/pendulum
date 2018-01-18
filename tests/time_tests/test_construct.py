import pendulum

from datetime import time
from pendulum import Time, timezone

from ..conftest import assert_time


def test_init():
    t = pendulum.time(12, 34, 56, 123456)

    assert_time(t, 12, 34, 56, 123456)


def test_init_with_missing_values():
    t = pendulum.time(12, 34, 56)
    assert_time(t, 12, 34, 56, 0)

    t = pendulum.time(12, 34)
    assert_time(t, 12, 34, 0, 0)

    t = pendulum.time(12)
    assert_time(t, 12, 0, 0, 0)


def test_instance():
    native = time(12, 34, 56, 123456)
    t = pendulum.time.instance(native)

    assert_time(t, 12, 34, 56, 123456)


def test_instance_aware():
    tz = timezone('Europe/Paris')
    native = time(12, 34, 56, 123456, tzinfo=tz)

    assert 'Europe/Paris' == pendulum.time.instance(native).tzinfo.name


def test_now():
    t = pendulum.time.now()

    assert isinstance(t, Time)


def test_now_microseconds():
    with pendulum.test(pendulum.today().at(1, 2, 3, 123456)):
        t = pendulum.time.now()
        assert_time(t, 1, 2, 3, 123456)

        t = pendulum.time.now(False)
        assert_time(t, 1, 2, 3, 0)
