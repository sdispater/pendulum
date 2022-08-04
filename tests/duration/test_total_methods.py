import pendulum


def test_in_weeks():
    it = pendulum.duration(days=17)
    assert round(it.total_weeks(), 2) == 2.43


def test_in_days():
    it = pendulum.duration(days=3)
    assert it.total_days() == 3


def test_in_hours():
    it = pendulum.duration(days=3, minutes=72)
    assert it.total_hours() == 73.2


def test_in_minutes():
    it = pendulum.duration(minutes=6, seconds=72)
    assert it.total_minutes() == 7.2


def test_in_seconds():
    it = pendulum.duration(seconds=72, microseconds=123456)
    assert it.total_seconds() == 72.123456


def test_in_milliseconds():
    it = pendulum.duration(seconds=1, milliseconds=234)
    assert it.total_milliseconds() == 1234


def test_in_microseconds():
    it = pendulum.duration(seconds=1, milliseconds=234, microseconds=567)
    assert it.total_microseconds() == 1234567
