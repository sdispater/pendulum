from __future__ import annotations

import pytz

from pendulum import _safe_timezone
from pendulum.tz.timezone import Timezone


def test_safe_timezone_with_tzinfo_objects():
    tz = _safe_timezone(pytz.timezone("Europe/Paris"))

    assert isinstance(tz, Timezone)
    assert tz.name == "Europe/Paris"
