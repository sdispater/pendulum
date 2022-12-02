from __future__ import annotations

import pendulum

locale = "da"


def test_diff_for_humans():
    with pendulum.travel_to(pendulum.datetime(2016, 8, 29), freeze=True):
        diff_for_humans()


def diff_for_humans():
    d = pendulum.now().subtract(seconds=1)
    assert d.diff_for_humans(locale=locale) == "for 1 sekund siden"

    d = pendulum.now().subtract(seconds=2)
    assert d.diff_for_humans(locale=locale) == "for 2 sekunder siden"

    d = pendulum.now().subtract(minutes=1)
    assert d.diff_for_humans(locale=locale) == "for 1 minut siden"

    d = pendulum.now().subtract(minutes=2)
    assert d.diff_for_humans(locale=locale) == "for 2 minutter siden"

    d = pendulum.now().subtract(hours=1)
    assert d.diff_for_humans(locale=locale) == "for 1 time siden"

    d = pendulum.now().subtract(hours=2)
    assert d.diff_for_humans(locale=locale) == "for 2 timer siden"

    d = pendulum.now().subtract(days=1)
    assert d.diff_for_humans(locale=locale) == "for 1 dag siden"

    d = pendulum.now().subtract(days=2)
    assert d.diff_for_humans(locale=locale) == "for 2 dage siden"

    d = pendulum.now().subtract(weeks=1)
    assert d.diff_for_humans(locale=locale) == "for 1 uge siden"

    d = pendulum.now().subtract(weeks=2)
    assert d.diff_for_humans(locale=locale) == "for 2 uger siden"

    d = pendulum.now().subtract(months=1)
    assert d.diff_for_humans(locale=locale) == "for 1 måned siden"

    d = pendulum.now().subtract(months=2)
    assert d.diff_for_humans(locale=locale) == "for 2 måneder siden"

    d = pendulum.now().subtract(years=1)
    assert d.diff_for_humans(locale=locale) == "for 1 år siden"

    d = pendulum.now().subtract(years=2)
    assert d.diff_for_humans(locale=locale) == "for 2 år siden"

    d = pendulum.now().add(seconds=1)
    assert d.diff_for_humans(locale=locale) == "om 1 sekund"

    d = pendulum.now().add(seconds=1)
    d2 = pendulum.now()
    assert d.diff_for_humans(d2, locale=locale) == "1 sekund efter"
    assert d2.diff_for_humans(d, locale=locale) == "1 sekund før"

    assert d.diff_for_humans(d2, True, locale=locale) == "1 sekund"
    assert d2.diff_for_humans(d.add(seconds=1), True, locale=locale) == "2 sekunder"
