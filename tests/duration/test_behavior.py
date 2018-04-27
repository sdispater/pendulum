import pickle
import pendulum

from datetime import timedelta


def test_pickle():
    it = pendulum.duration(days=3, seconds=2456, microseconds=123456)
    s = pickle.dumps(it)
    it2 = pickle.loads(s)

    assert it == it2


def test_comparison_to_timedelta():
    duration = pendulum.duration(days=3)

    assert duration < timedelta(days=4)
