from __future__ import annotations

import pytest

from pendulum.tz import timezone
from pendulum.tz.exceptions import InvalidTimezone
from pendulum.tz.timezone import FixedTimezone
from pendulum.tz.timezone import Timezone


def test_timezone_with_name():
    tz = timezone("Europe/Paris")

    assert isinstance(tz, Timezone)
    assert tz.name == "Europe/Paris"


def test_timezone_with_invalid_name():
    with pytest.raises(InvalidTimezone):
        timezone("Invalid")


def test_timezone_with_offset():
    tz = timezone(-19800)

    assert isinstance(tz, FixedTimezone)
    assert tz.name == "-05:30"
