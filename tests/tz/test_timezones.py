# -*- coding: utf-8 -*-

import pendulum


def test_timezones():
    zones = pendulum.timezones

    assert "America/Argentina/Buenos_Aires" in zones


def test_timezones_are_loadable():
    zones = pendulum.timezones

    for zone in zones:
        pendulum.timezone(zone)
