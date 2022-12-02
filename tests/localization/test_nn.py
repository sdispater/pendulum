from __future__ import annotations

import pendulum

locale = "nn"


def test_diff_for_humans():
    with pendulum.travel_to(pendulum.datetime(2016, 8, 29), freeze=True):
        diff_for_humans()


def diff_for_humans():
    d = pendulum.now().subtract(seconds=1)
    assert d.diff_for_humans(locale=locale) == "for 1 sekund sidan"

    d = pendulum.now().subtract(seconds=2)
    assert d.diff_for_humans(locale=locale) == "for 2 sekund sidan"

    d = pendulum.now().subtract(minutes=1)
    assert d.diff_for_humans(locale=locale) == "for 1 minutt sidan"

    d = pendulum.now().subtract(minutes=2)
    assert d.diff_for_humans(locale=locale) == "for 2 minutt sidan"

    d = pendulum.now().subtract(hours=1)
    assert d.diff_for_humans(locale=locale) == "for 1 time sidan"

    d = pendulum.now().subtract(hours=2)
    assert d.diff_for_humans(locale=locale) == "for 2 timar sidan"

    d = pendulum.now().subtract(days=1)
    assert d.diff_for_humans(locale=locale) == "for 1 dag sidan"

    d = pendulum.now().subtract(days=2)
    assert d.diff_for_humans(locale=locale) == "for 2 dagar sidan"

    d = pendulum.now().subtract(weeks=1)
    assert d.diff_for_humans(locale=locale) == "for 1 veke sidan"

    d = pendulum.now().subtract(weeks=2)
    assert d.diff_for_humans(locale=locale) == "for 2 veker sidan"

    d = pendulum.now().subtract(months=1)
    assert d.diff_for_humans(locale=locale) == "for 1 månad sidan"

    d = pendulum.now().subtract(months=2)
    assert d.diff_for_humans(locale=locale) == "for 2 månadar sidan"

    d = pendulum.now().subtract(years=1)
    assert d.diff_for_humans(locale=locale) == "for 1 år sidan"

    d = pendulum.now().subtract(years=2)
    assert d.diff_for_humans(locale=locale) == "for 2 år sidan"

    d = pendulum.now().add(seconds=1)
    assert d.diff_for_humans(locale=locale) == "om 1 sekund"

    d = pendulum.now().add(seconds=1)
    d2 = pendulum.now()
    assert d.diff_for_humans(d2, locale=locale) == "1 sekund etter"
    assert d2.diff_for_humans(d, locale=locale) == "1 sekund før"

    assert d.diff_for_humans(d2, True, locale=locale) == "1 sekund"
    assert d2.diff_for_humans(d.add(seconds=1), True, locale=locale) == "2 sekund"


def test_format():
    d = pendulum.datetime(2016, 8, 29, 7, 3, 6, 123456)
    assert d.format("dddd", locale=locale) == "måndag"
    assert d.format("ddd", locale=locale) == "mån."
    assert d.format("MMMM", locale=locale) == "august"
    assert d.format("MMM", locale=locale) == "aug."
    assert d.format("A", locale=locale) == "formiddag"
    assert d.format("Qo", locale=locale) == "3."
    assert d.format("Mo", locale=locale) == "8."
    assert d.format("Do", locale=locale) == "29."

    assert d.format("LT", locale=locale) == "07:03"
    assert d.format("LTS", locale=locale) == "07:03:06"
    assert d.format("L", locale=locale) == "29.08.2016"
    assert d.format("LL", locale=locale) == "29. august 2016"
    assert d.format("LLL", locale=locale) == "29. august 2016 07:03"
    assert d.format("LLLL", locale=locale) == "måndag 29. august 2016 07:03"
