import pytest

from pendulum import Duration
from pendulum import parse


@pytest.mark.parametrize(
    "dur, expected_iso",
    [
        (
            Duration(
                years=1,
                months=3,
                days=6,
                minutes=50,
                seconds=3,
                milliseconds=10,
                microseconds=10,
            ),
            "P1Y3M6DT0H50M3.010010S",
        ),
        (Duration(days=4, hours=12, minutes=30, seconds=5), "P0Y0M4DT12H30M5S"),
        (Duration(days=4, hours=12, minutes=30, seconds=5), "P0Y0M4DT12H30M5S"),
        (Duration(microseconds=10), "P0Y0M0DT0H0M0.000010S"),
        (Duration(milliseconds=1), "P0Y0M0DT0H0M0.001000S"),
        (Duration(minutes=1), "P0Y0M0DT0H1M0S"),
    ],
)
def test_isoformat(dur, expected_iso):
    fmt = dur.isoformat()
    assert fmt == expected_iso
    assert parse(fmt) == dur
