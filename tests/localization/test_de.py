from __future__ import annotations

import pendulum

locale = "de"


def test_diff_for_humans():
    with pendulum.travel_to(pendulum.datetime(2016, 8, 29), freeze=True):
        diff_for_humans()


def diff_for_humans():
    d = pendulum.now().subtract(seconds=1)
    assert d.diff_for_humans(locale=locale) == "vor 1 Sekunde"

    d = pendulum.now().subtract(seconds=2)
    assert d.diff_for_humans(locale=locale) == "vor 2 Sekunden"

    d = pendulum.now().subtract(minutes=1)
    assert d.diff_for_humans(locale=locale) == "vor 1 Minute"

    d = pendulum.now().subtract(minutes=2)
    assert d.diff_for_humans(locale=locale) == "vor 2 Minuten"

    d = pendulum.now().subtract(hours=1)
    assert d.diff_for_humans(locale=locale) == "vor 1 Stunde"

    d = pendulum.now().subtract(hours=2)
    assert d.diff_for_humans(locale=locale) == "vor 2 Stunden"

    d = pendulum.now().subtract(days=1)
    assert d.diff_for_humans(locale=locale) == "vor 1 Tag"

    d = pendulum.now().subtract(days=2)
    assert d.diff_for_humans(locale=locale) == "vor 2 Tagen"

    d = pendulum.now().subtract(weeks=1)
    assert d.diff_for_humans(locale=locale) == "vor 1 Woche"

    d = pendulum.now().subtract(weeks=2)
    assert d.diff_for_humans(locale=locale) == "vor 2 Wochen"

    d = pendulum.now().subtract(months=1)
    assert d.diff_for_humans(locale=locale) == "vor 1 Monat"

    d = pendulum.now().subtract(months=2)
    assert d.diff_for_humans(locale=locale) == "vor 2 Monaten"

    d = pendulum.now().subtract(years=1)
    assert d.diff_for_humans(locale=locale) == "vor 1 Jahr"

    d = pendulum.now().subtract(years=2)
    assert d.diff_for_humans(locale=locale) == "vor 2 Jahren"

    d = pendulum.now().add(seconds=1)
    assert d.diff_for_humans(locale=locale) == "in 1 Sekunde"

    d = pendulum.now().add(seconds=1)
    d2 = pendulum.now()
    assert d.diff_for_humans(d2, locale=locale) == "1 Sekunde später"
    assert d2.diff_for_humans(d, locale=locale) == "1 Sekunde zuvor"

    assert d.diff_for_humans(d2, True, locale=locale) == "1 Sekunde"
    assert d2.diff_for_humans(d.add(seconds=1), True, locale=locale) == "2 Sekunden"
