import pytest
import pytz

from pendulum import _safe_timezone
from pendulum.tz.timezone import Timezone
from pendulum.utils._compat import zoneinfo


def test_safe_timezone_with_tzinfo_objects():
    tz = _safe_timezone(pytz.timezone("Europe/Paris"))

    assert isinstance(tz, Timezone)
    assert "Europe/Paris" == tz.name


@pytest.mark.parametrize("iana_name", zoneinfo.available_timezones())
def test_safe_timezone_converts_zoneinfo_objects(iana_name: str):
    zi = zoneinfo.ZoneInfo(iana_name)
    converted_tz = _safe_timezone(zi)

    assert isinstance(converted_tz, Timezone)
    assert iana_name == converted_tz.name
