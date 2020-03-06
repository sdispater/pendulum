from pendulum.tz.zoneinfo.posix_timezone import JPosixTransition
from pendulum.tz.zoneinfo.posix_timezone import MPosixTransition
from pendulum.tz.zoneinfo.posix_timezone import posix_spec


def test_posix_spec_m():
    spec = "CET-1CEST,M3.5.0,M10.5.0/3"
    tz = posix_spec(spec)

    assert tz.std_abbr == "CET"
    assert tz.std_offset == 3600
    assert tz.dst_abbr == "CEST"
    assert tz.dst_offset == 7200

    assert isinstance(tz.dst_start, MPosixTransition)
    assert tz.dst_start.month == 3
    assert tz.dst_start.week == 5
    assert tz.dst_start.weekday == 0
    assert tz.dst_start.offset == 7200

    assert isinstance(tz.dst_end, MPosixTransition)
    assert tz.dst_end.month == 10
    assert tz.dst_end.week == 5
    assert tz.dst_end.weekday == 0
    assert tz.dst_end.offset == 3 * 3600


def test_posix_spec_m_no_abbr():
    spec = "<+12>-12<+13>,M11.1.0,M1.2.1/147"
    tz = posix_spec(spec)

    assert tz.std_abbr == "+12"
    assert tz.std_offset == 12 * 3600
    assert tz.dst_abbr == "+13"
    assert tz.dst_offset == 13 * 3600

    assert isinstance(tz.dst_start, MPosixTransition)
    assert tz.dst_start.month == 11
    assert tz.dst_start.week == 1
    assert tz.dst_start.weekday == 0
    assert tz.dst_start.offset == 7200

    assert isinstance(tz.dst_end, MPosixTransition)
    assert tz.dst_end.month == 1
    assert tz.dst_end.week == 2
    assert tz.dst_end.weekday == 1
    assert tz.dst_end.offset == 147 * 3600


def test_posix_spec_j_no_abbr():
    spec = "<+0330>-3:30<+0430>,J80/0,J264/0"
    tz = posix_spec(spec)

    assert tz.std_abbr == "+0330"
    assert tz.std_offset == 3 * 3600 + 30 * 60
    assert tz.dst_abbr == "+0430"
    assert tz.dst_offset == 4 * 3600 + 30 * 60

    assert isinstance(tz.dst_start, JPosixTransition)
    assert tz.dst_start.day == 80
    assert tz.dst_start.offset == 0

    assert isinstance(tz.dst_end, JPosixTransition)
    assert tz.dst_end.day == 264
    assert tz.dst_end.offset == 0
