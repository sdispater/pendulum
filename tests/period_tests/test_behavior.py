import pickle
import pendulum


def test_pickle():
    dt1 = pendulum.create(2016, 11, 18)
    dt2 = pendulum.create(2016, 11, 20)

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
