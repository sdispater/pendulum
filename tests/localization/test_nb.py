# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pendulum


locale = "nb"


def test_diff_for_humans():
    with pendulum.test(pendulum.datetime(2016, 8, 29)):
        diff_for_humans()


def diff_for_humans():
    d = pendulum.now().subtract(seconds=1)
    assert d.diff_for_humans(locale=locale) == "for 1 sekund siden"

    d = pendulum.now().subtract(seconds=2)
    assert d.diff_for_humans(locale=locale) == "for 2 sekunder siden"

    d = pendulum.now().subtract(minutes=1)
    assert d.diff_for_humans(locale=locale) == "for 1 minutt siden"

    d = pendulum.now().subtract(minutes=2)
    assert d.diff_for_humans(locale=locale) == "for 2 minutter siden"

    d = pendulum.now().subtract(hours=1)
    assert d.diff_for_humans(locale=locale) == "for 1 time siden"

    d = pendulum.now().subtract(hours=2)
    assert d.diff_for_humans(locale=locale) == "for 2 timer siden"

    d = pendulum.now().subtract(days=1)
    assert d.diff_for_humans(locale=locale) == "for 1 dag siden"

    d = pendulum.now().subtract(days=2)
    assert d.diff_for_humans(locale=locale) == "for 2 dager siden"

    d = pendulum.now().subtract(weeks=1)
    assert d.diff_for_humans(locale=locale) == "for 1 uke siden"

    d = pendulum.now().subtract(weeks=2)
    assert d.diff_for_humans(locale=locale) == "for 2 uker siden"

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
    assert d.diff_for_humans(d2, locale=locale) == "1 sekund etter"
    assert d2.diff_for_humans(d, locale=locale) == "1 sekund før"

    assert d.diff_for_humans(d2, True, locale=locale) == "1 sekund"
    assert d2.diff_for_humans(d.add(seconds=1), True, locale=locale) == "2 sekunder"


def test_format():
    d = pendulum.datetime(2016, 8, 28, 7, 3, 6, 123456)
    assert d.format("dddd", locale=locale) == "søndag"
    assert d.format("ddd", locale=locale) == "søn."
    assert d.format("MMMM", locale=locale) == "august"
    assert d.format("MMM", locale=locale) == "aug."
    assert d.format("A", locale=locale) == "a.m."
    assert d.format("Qo", locale=locale) == "3."
    assert d.format("Mo", locale=locale) == "8."
    assert d.format("Do", locale=locale) == "28."

    assert d.format("LT", locale=locale) == "07:03"
    assert d.format("LTS", locale=locale) == "07:03:06"
    assert d.format("L", locale=locale) == "28.08.2016"
    assert d.format("LL", locale=locale) == "28. august 2016"
    assert d.format("LLL", locale=locale) == "28. august 2016 07:03"
    assert d.format("LLLL", locale=locale) == "søndag 28. august 2016 07:03"
