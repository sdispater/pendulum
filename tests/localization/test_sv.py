from __future__ import annotations

import pendulum

locale = "sv"


def test_diff_for_humans():
    with pendulum.travel_to(pendulum.datetime(2016, 8, 29), freeze=True):
        diff_for_humans()


def diff_for_humans():
    d = pendulum.now().subtract(seconds=1)
    assert d.diff_for_humans(locale=locale) == "för 1 sekund sedan"

    d = pendulum.now().subtract(seconds=2)
    assert d.diff_for_humans(locale=locale) == "för 2 sekunder sedan"

    d = pendulum.now().subtract(seconds=5)
    assert d.diff_for_humans(locale=locale) == "för 5 sekunder sedan"

    d = pendulum.now().subtract(seconds=21)
    assert d.diff_for_humans(locale=locale) == "för 21 sekunder sedan"

    d = pendulum.now().subtract(minutes=1)
    assert d.diff_for_humans(locale=locale) == "för 1 minut sedan"

    d = pendulum.now().subtract(minutes=2)
    assert d.diff_for_humans(locale=locale) == "för 2 minuter sedan"

    d = pendulum.now().subtract(minutes=5)
    assert d.diff_for_humans(locale=locale) == "för 5 minuter sedan"

    d = pendulum.now().subtract(hours=1)
    assert d.diff_for_humans(locale=locale) == "för 1 timme sedan"

    d = pendulum.now().subtract(hours=2)
    assert d.diff_for_humans(locale=locale) == "för 2 timmar sedan"

    d = pendulum.now().subtract(hours=5)
    assert d.diff_for_humans(locale=locale) == "för 5 timmar sedan"

    d = pendulum.now().subtract(days=1)
    assert d.diff_for_humans(locale=locale) == "för 1 dag sedan"

    d = pendulum.now().subtract(days=2)
    assert d.diff_for_humans(locale=locale) == "för 2 dagar sedan"

    d = pendulum.now().subtract(days=5)
    assert d.diff_for_humans(locale=locale) == "för 5 dagar sedan"

    d = pendulum.now().subtract(weeks=1)
    assert d.diff_for_humans(locale=locale) == "för 1 vecka sedan"

    d = pendulum.now().subtract(weeks=2)
    assert d.diff_for_humans(locale=locale) == "för 2 veckor sedan"

    d = pendulum.now().subtract(months=1)
    assert d.diff_for_humans(locale=locale) == "för 1 månad sedan"

    d = pendulum.now().subtract(months=2)
    assert d.diff_for_humans(locale=locale) == "för 2 månader sedan"

    d = pendulum.now().subtract(months=5)
    assert d.diff_for_humans(locale=locale) == "för 5 månader sedan"

    d = pendulum.now().subtract(years=1)
    assert d.diff_for_humans(locale=locale) == "för 1 år sedan"

    d = pendulum.now().subtract(years=2)
    assert d.diff_for_humans(locale=locale) == "för 2 år sedan"

    d = pendulum.now().subtract(years=5)
    assert d.diff_for_humans(locale=locale) == "för 5 år sedan"

    d = pendulum.now().add(seconds=1)
    assert d.diff_for_humans(locale=locale) == "om 1 sekund"

    d = pendulum.now().add(seconds=1)
    d2 = pendulum.now()
    assert d.diff_for_humans(d2, locale=locale) == "1 sekund efter"
    assert d2.diff_for_humans(d, locale=locale) == "1 sekund innan"

    assert d.diff_for_humans(d2, True, locale=locale) == "1 sekund"
    assert d2.diff_for_humans(d.add(seconds=1), True, locale=locale) == "2 sekunder"
