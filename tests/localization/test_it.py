from __future__ import annotations

import pendulum

locale = "it"


def test_diff_for_humans():
    with pendulum.travel_to(pendulum.datetime(2016, 8, 29), freeze=True):
        diff_for_humans()


def diff_for_humans():
    d = pendulum.now().subtract(seconds=1)
    assert d.diff_for_humans(locale=locale) == "alcuni secondi fa"

    d = pendulum.now().subtract(seconds=2)
    assert d.diff_for_humans(locale=locale) == "alcuni secondi fa"

    d = pendulum.now().subtract(minutes=1)
    assert d.diff_for_humans(locale=locale) == "1 minuto fa"

    d = pendulum.now().subtract(minutes=2)
    assert d.diff_for_humans(locale=locale) == "2 minuti fa"

    d = pendulum.now().subtract(hours=1)
    assert d.diff_for_humans(locale=locale) == "1 ora fa"

    d = pendulum.now().subtract(hours=2)
    assert d.diff_for_humans(locale=locale) == "2 ore fa"

    d = pendulum.now().subtract(days=1)
    assert d.diff_for_humans(locale=locale) == "1 giorno fa"

    d = pendulum.now().subtract(days=2)
    assert d.diff_for_humans(locale=locale) == "2 giorni fa"

    d = pendulum.now().subtract(weeks=1)
    assert d.diff_for_humans(locale=locale) == "1 settimana fa"

    d = pendulum.now().subtract(weeks=2)
    assert d.diff_for_humans(locale=locale) == "2 settimane fa"

    d = pendulum.now().subtract(months=1)
    assert d.diff_for_humans(locale=locale) == "1 mese fa"

    d = pendulum.now().subtract(months=2)
    assert d.diff_for_humans(locale=locale) == "2 mesi fa"

    d = pendulum.now().subtract(years=1)
    assert d.diff_for_humans(locale=locale) == "1 anno fa"

    d = pendulum.now().subtract(years=2)
    assert d.diff_for_humans(locale=locale) == "2 anni fa"

    d = pendulum.now().add(seconds=1)
    assert d.diff_for_humans(locale=locale) == "in alcuni secondi"

    d = pendulum.now().add(seconds=1)
    d2 = pendulum.now()
    assert d.diff_for_humans(d2, locale=locale) == "alcuni secondi dopo"
    assert d2.diff_for_humans(d, locale=locale) == "alcuni secondi prima"

    assert d.diff_for_humans(d2, True, locale=locale) == "alcuni secondi"
    assert d2.diff_for_humans(d.add(seconds=1), True, locale=locale) == "alcuni secondi"


def test_format():
    d = pendulum.datetime(2016, 8, 28, 7, 3, 6, 123456)
    assert d.format("dddd", locale=locale) == "domenica"
    assert d.format("ddd", locale=locale) == "dom"
    assert d.format("MMMM", locale=locale) == "agosto"
    assert d.format("MMM", locale=locale) == "ago"
    assert d.format("A", locale=locale) == "AM"

    assert d.format("LT", locale=locale) == "7:03"
    assert d.format("LTS", locale=locale) == "7:03:06"
    assert d.format("L", locale=locale) == "28/08/2016"
    assert d.format("LL", locale=locale) == "28 agosto 2016"
    assert d.format("LLL", locale=locale) == "28 agosto 2016 alle 7:03"
    assert d.format("LLLL", locale=locale) == "domenica, 28 agosto 2016 alle 7:03"

    assert d.format("Do", locale=locale) == "28°"
    d = pendulum.datetime(2019, 1, 1, 7, 3, 6, 123456)
    assert d.format("Do", locale=locale) == "1°"
