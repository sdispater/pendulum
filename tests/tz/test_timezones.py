from __future__ import annotations

import pytest

import pendulum


def test_timezones():
    zones = pendulum.timezones()

    assert "America/Argentina/Buenos_Aires" in zones


@pytest.mark.parametrize("zone", list(pendulum.timezones()))
def test_timezones_are_loadable(zone):
    pendulum.timezone(zone)
