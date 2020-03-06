# -*- coding: utf-8 -*-
import pendulum
import pytest


def test_timezones():
    zones = pendulum.timezones

    assert "America/Argentina/Buenos_Aires" in zones


@pytest.mark.parametrize("zone", [zone for zone in pendulum.timezones])
def test_timezones_are_loadable(zone):
    pendulum.timezone(zone)
