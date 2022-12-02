from __future__ import annotations

import pendulum

locale = "lt"


def test_diff_for_humans():
    with pendulum.travel_to(pendulum.datetime(2016, 8, 29), freeze=True):
        diff_for_humans()


def diff_for_humans():
    d = pendulum.now().subtract(seconds=1)
    assert d.diff_for_humans(locale=locale) == "prieš 1 sekundę"

    d = pendulum.now().subtract(seconds=2)
    assert d.diff_for_humans(locale=locale) == "prieš 2 sekundes"

    d = pendulum.now().subtract(seconds=21)
    assert d.diff_for_humans(locale=locale) == "prieš 21 sekundę"

    d = pendulum.now().subtract(minutes=1)
    assert d.diff_for_humans(locale=locale) == "prieš 1 minutę"

    d = pendulum.now().subtract(minutes=2)
    assert d.diff_for_humans(locale=locale) == "prieš 2 minutes"

    d = pendulum.now().subtract(hours=1)
    assert d.diff_for_humans(locale=locale) == "prieš 1 valandą"

    d = pendulum.now().subtract(hours=2)
    assert d.diff_for_humans(locale=locale) == "prieš 2 valandas"

    d = pendulum.now().subtract(days=1)
    assert d.diff_for_humans(locale=locale) == "prieš 1 dieną"

    d = pendulum.now().subtract(days=2)
    assert d.diff_for_humans(locale=locale) == "prieš 2 dienas"

    d = pendulum.now().subtract(weeks=1)
    assert d.diff_for_humans(locale=locale) == "prieš 1 savaitę"

    d = pendulum.now().subtract(weeks=2)
    assert d.diff_for_humans(locale=locale) == "prieš 2 savaites"

    d = pendulum.now().subtract(months=1)
    assert d.diff_for_humans(locale=locale) == "prieš 1 mėnesį"

    d = pendulum.now().subtract(months=2)
    assert d.diff_for_humans(locale=locale) == "prieš 2 mėnesius"

    d = pendulum.now().subtract(years=1)
    assert d.diff_for_humans(locale=locale) == "prieš 1 metus"

    d = pendulum.now().subtract(years=2)
    assert d.diff_for_humans(locale=locale) == "prieš 2 metus"

    d = pendulum.now().add(seconds=1)
    assert d.diff_for_humans(locale=locale) == "po 1 sekundės"

    d = pendulum.now().add(seconds=1)
    d2 = pendulum.now()
    assert d.diff_for_humans(d2, locale=locale) == "po 1 sekundės"
    assert d2.diff_for_humans(d, locale=locale) == "1 sekundę nuo dabar"

    assert d.diff_for_humans(d2, True, locale=locale) == "1 sekundė"
    assert d2.diff_for_humans(d.add(seconds=1), True, locale=locale) == "2 sekundės"
