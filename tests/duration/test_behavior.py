import pickle
import pendulum


def test_pickle():
    it = pendulum.duration(days=3, seconds=2456, microseconds=123456)
    s = pickle.dumps(it)
    it2 = pickle.loads(s)

    assert it == it2
