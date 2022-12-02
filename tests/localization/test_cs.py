from __future__ import annotations

import pendulum

locale = "cs"


def test_diff_for_humans():
    with pendulum.travel_to(pendulum.datetime(2016, 8, 29), freeze=True):
        diff_for_humans()


def diff_for_humans():
    d = pendulum.now().subtract(seconds=1)
    assert d.diff_for_humans(locale=locale) == "pár vteřin zpět"

    d = pendulum.now().subtract(seconds=2)
    assert d.diff_for_humans(locale=locale) == "pár vteřin zpět"

    d = pendulum.now().subtract(seconds=20)
    assert d.diff_for_humans(locale=locale) == "před 20 sekundami"

    d = pendulum.now().subtract(minutes=1)
    assert d.diff_for_humans(locale=locale) == "před 1 minutou"

    d = pendulum.now().subtract(minutes=2)
    assert d.diff_for_humans(locale=locale) == "před 2 minutami"

    d = pendulum.now().subtract(minutes=5)
    assert d.diff_for_humans(locale=locale) == "před 5 minutami"

    d = pendulum.now().subtract(hours=1)
    assert d.diff_for_humans(locale=locale) == "před 1 hodinou"

    d = pendulum.now().subtract(hours=2)
    assert d.diff_for_humans(locale=locale) == "před 2 hodinami"

    d = pendulum.now().subtract(hours=5)
    assert d.diff_for_humans(locale=locale) == "před 5 hodinami"

    d = pendulum.now().subtract(days=1)
    assert d.diff_for_humans(locale=locale) == "před 1 dnem"

    d = pendulum.now().subtract(days=2)
    assert d.diff_for_humans(locale=locale) == "před 2 dny"

    d = pendulum.now().subtract(weeks=1)
    assert d.diff_for_humans(locale=locale) == "před 1 týdnem"

    d = pendulum.now().subtract(weeks=2)
    assert d.diff_for_humans(locale=locale) == "před 2 týdny"

    d = pendulum.now().subtract(months=1)
    assert d.diff_for_humans(locale=locale) == "před 1 měsícem"

    d = pendulum.now().subtract(months=2)
    assert d.diff_for_humans(locale=locale) == "před 2 měsíci"

    d = pendulum.now().subtract(months=5)
    assert d.diff_for_humans(locale=locale) == "před 5 měsíci"

    d = pendulum.now().subtract(years=1)
    assert d.diff_for_humans(locale=locale) == "před 1 rokem"

    d = pendulum.now().subtract(years=2)
    assert d.diff_for_humans(locale=locale) == "před 2 lety"

    d = pendulum.now().subtract(years=5)
    assert d.diff_for_humans(locale=locale) == "před 5 lety"

    d = pendulum.now().add(seconds=1)
    assert d.diff_for_humans(locale=locale) == "za pár vteřin"

    d = pendulum.now().add(seconds=1)
    d2 = pendulum.now()
    assert d.diff_for_humans(d2, locale=locale) == "pár vteřin po"
    assert d2.diff_for_humans(d, locale=locale) == "pár vteřin zpět"

    assert d.diff_for_humans(d2, True, locale=locale) == "pár vteřin"
    assert d2.diff_for_humans(d.add(seconds=1), True, locale=locale) == "pár vteřin"

    d = pendulum.now().add(seconds=20)
    d2 = pendulum.now()
    assert d.diff_for_humans(d2, locale=locale) == "20 sekund po"
    assert d2.diff_for_humans(d, locale=locale) == "20 sekund zpět"

    d = pendulum.now().add(seconds=10)
    d2 = pendulum.now()
    assert d.diff_for_humans(d2, True, locale=locale) == "pár vteřin"
    assert d2.diff_for_humans(d.add(seconds=1), True, locale=locale) == "11 sekund"


def test_format():
    d = pendulum.datetime(2016, 8, 29, 7, 3, 6, 123456)
    assert d.format("dddd", locale=locale) == "pondělí"
    assert d.format("ddd", locale=locale) == "po"
    assert d.format("MMMM", locale=locale) == "srpna"
    assert d.format("MMM", locale=locale) == "srp"
    assert d.format("A", locale=locale) == "dop."
    assert d.format("Qo", locale=locale) == "3."
    assert d.format("Mo", locale=locale) == "8."
    assert d.format("Do", locale=locale) == "29."

    assert d.format("LT", locale=locale) == "7:03"
    assert d.format("LTS", locale=locale) == "7:03:06"
    assert d.format("L", locale=locale) == "29. 8. 2016"
    assert d.format("LL", locale=locale) == "29. srpna, 2016"
    assert d.format("LLL", locale=locale) == "29. srpna, 2016 7:03"
    assert d.format("LLLL", locale=locale) == "pondělí, 29. srpna, 2016 7:03"
