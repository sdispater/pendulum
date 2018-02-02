from datetime import datetime
from pendulum.tz.transition import Transition


def test_construct():
    t = Transition(3600, 1, datetime(1970, 1, 1), datetime(1970, 1, 1, 1), 0)

    assert t.unix_time == 3600
    assert t.time == datetime(1970, 1, 1, 1)
    assert t.pre_time == datetime(1970, 1, 1)
    assert t.utc_time == datetime(1970, 1, 1, 1)
    assert t.tzinfo_index == 1
    assert t.pre_tzinfo_index == 0


def test_repr():
    t = Transition(3600, 1, datetime(1970, 1, 1), datetime(1970, 1, 1, 1), 0)

    expected = '<Transition [1970-01-01 01:00:00 UTC, 1970-01-01 00:00:00 -> 1970-01-01 01:00:00]>'
    assert repr(t) == expected
