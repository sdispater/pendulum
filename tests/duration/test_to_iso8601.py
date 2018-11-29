import pytest

import pendulum


def test_all():
    d = pendulum.duration(
        years=2, months=3, days=4, hours=5, minutes=6, seconds=7, microseconds=50
    )

    expected = "P2Y3M4DT5H6M7.00005S"
    assert d.to_iso8601_string() == expected


def test_basic():
    d = pendulum.Duration(years=2, months=3, days=4, hours=5, minutes=6, seconds=7)

    expected = "P2Y3M4DT5H6M7S"
    assert d.to_iso8601_string() == expected


def test_microsecond_alone():
    d = pendulum.duration(microseconds=5)

    expected = "PT0.000005S"
    assert d.to_iso8601_string() == expected


def test_microsecond_trailing_zeros():
    d = pendulum.duration(microseconds=500)

    expected = "PT0.0005S"
    assert d.to_iso8601_string() == expected


def test_second_and_microsecond():
    d = pendulum.duration(seconds=50, microseconds=5)

    expected = "PT50.000005S"
    assert d.to_iso8601_string() == expected


def test_lots_of_days():
    d = pendulum.duration(days=500)
    # should not be coverted to months, years as info is lost

    expected = "P500D"
    assert d.to_iso8601_string() == expected

    d = pendulum.duration(days=40)

    expected = "P40D"
    assert d.to_iso8601_string() == expected


@pytest.mark.skip(reason="This test will fail until large changes to normalization")
def test_lots_of_hours():
    # NOTE: this will fail until total_seconds normalization
    # no longer occurs
    d = pendulum.duration(hours=36)
    # should not be coverted to days, as can be different
    # depending on daylight savings changes

    expected = "PT36H"
    assert d.to_iso8601_string() == expected


def test_days_and_months():
    d = pendulum.duration(months=1, days=40)
    # not equivalent to P2M10D

    expected = "P1M40D"
    assert d.to_iso8601_string() == expected


def test_weeks_alone():
    d = pendulum.duration(days=21)

    # Could also validly be P21D
    expected = "P3W"
    assert d.to_iso8601_string() == expected


def test_weeks_and_other():
    d = pendulum.duration(years=2, days=21)

    expected = "P2Y21D"
    assert d.to_iso8601_string() == expected


def test_weeks_and_time():
    d = pendulum.duration(days=21, minutes=7)

    expected = "P21DT7M"
    assert d.to_iso8601_string() == expected


def test_empty():
    # NOTE: can't validly test this in isolation,
    # as "P0D" and "PT0S" etc. are equally valid
    # ISO8601 representations
    d = pendulum.duration()
    s = d.to_iso8601_string()
    # should be something like "PT0S" or "P0D"
    parsed = pendulum.parse(s)

    assert parsed.years == 0
    assert parsed.months == 0
    assert parsed.weeks == 0
    assert parsed.remaining_days == 0
    assert parsed.hours == 0
    assert parsed.minutes == 0
    assert parsed.remaining_seconds == 0
    assert parsed.microseconds == 0
