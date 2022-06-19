from __future__ import annotations

import pendulum

locale = "fr"


def test_diff_for_humans():
    with pendulum.travel_to(pendulum.datetime(2016, 8, 29), freeze=True):
        diff_for_humans()


def diff_for_humans():
    d = pendulum.now().subtract(seconds=1)
    assert d.diff_for_humans(locale=locale) == "il y a quelques secondes"

    d = pendulum.now().subtract(seconds=2)
    assert d.diff_for_humans(locale=locale) == "il y a quelques secondes"

    d = pendulum.now().subtract(minutes=1)
    assert d.diff_for_humans(locale=locale) == "il y a 1 minute"

    d = pendulum.now().subtract(minutes=2)
    assert d.diff_for_humans(locale=locale) == "il y a 2 minutes"

    d = pendulum.now().subtract(hours=1)
    assert d.diff_for_humans(locale=locale) == "il y a 1 heure"

    d = pendulum.now().subtract(hours=2)
    assert d.diff_for_humans(locale=locale) == "il y a 2 heures"

    d = pendulum.now().subtract(days=1)
    assert d.diff_for_humans(locale=locale) == "il y a 1 jour"

    d = pendulum.now().subtract(days=2)
    assert d.diff_for_humans(locale=locale) == "il y a 2 jours"

    d = pendulum.now().subtract(weeks=1)
    assert d.diff_for_humans(locale=locale) == "il y a 1 semaine"

    d = pendulum.now().subtract(weeks=2)
    assert d.diff_for_humans(locale=locale) == "il y a 2 semaines"

    d = pendulum.now().subtract(months=1)
    assert d.diff_for_humans(locale=locale) == "il y a 1 mois"

    d = pendulum.now().subtract(months=2)
    assert d.diff_for_humans(locale=locale) == "il y a 2 mois"

    d = pendulum.now().subtract(years=1)
    assert d.diff_for_humans(locale=locale) == "il y a 1 an"

    d = pendulum.now().subtract(years=2)
    assert d.diff_for_humans(locale=locale) == "il y a 2 ans"

    d = pendulum.now().add(seconds=1)
    assert d.diff_for_humans(locale=locale) == "dans quelques secondes"

    d = pendulum.now().add(seconds=1)
    d2 = pendulum.now()
    assert d.diff_for_humans(d2, locale=locale) == "quelques secondes après"
    assert d2.diff_for_humans(d, locale=locale) == "quelques secondes avant"

    assert d.diff_for_humans(d2, True, locale=locale) == "quelques secondes"
    assert (
        d2.diff_for_humans(d.add(seconds=1), True, locale=locale) == "quelques secondes"
    )


def test_format():
    d = pendulum.datetime(2016, 8, 28, 7, 3, 6, 123456)
    assert d.format("dddd", locale=locale) == "dimanche"
    assert d.format("ddd", locale=locale) == "dim."
    assert d.format("MMMM", locale=locale) == "août"
    assert d.format("MMM", locale=locale) == "août"
    assert d.format("A", locale=locale) == "AM"
    assert d.format("Do", locale=locale) == "28e"

    assert d.format("LT", locale=locale) == "07:03"
    assert d.format("LTS", locale=locale) == "07:03:06"
    assert d.format("L", locale=locale) == "28/08/2016"
    assert d.format("LL", locale=locale) == "28 août 2016"
    assert d.format("LLL", locale=locale) == "28 août 2016 07:03"
    assert d.format("LLLL", locale=locale) == "dimanche 28 août 2016 07:03"
