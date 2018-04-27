import pickle
import pendulum

from datetime import timedelta


def test_pickle():
    dt1 = pendulum.datetime(2016, 11, 18)
    dt2 = pendulum.datetime(2016, 11, 20)

    p = pendulum.period(dt1, dt2)
    s = pickle.dumps(p)
    p2 = pickle.loads(s)

    assert p.start == p2.start
    assert p.end == p2.end
    assert p.invert == p2.invert

    p = pendulum.period(dt2, dt1)
    s = pickle.dumps(p)
    p2 = pickle.loads(s)

    assert p.start == p2.start
    assert p.end == p2.end
    assert p.invert == p2.invert

    p = pendulum.period(dt2, dt1, True)
    s = pickle.dumps(p)
    p2 = pickle.loads(s)

    assert p.start == p2.start
    assert p.end == p2.end
    assert p.invert == p2.invert


def test_comparison_to_timedelta():
    dt1 = pendulum.datetime(2016, 11, 18)
    dt2 = pendulum.datetime(2016, 11, 20)

    period = dt2 - dt1

    assert period < timedelta(days=4)
