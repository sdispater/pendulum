# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pendulum


locale = "pl"


def test_diff_for_humans():
    with pendulum.test(pendulum.datetime(2016, 8, 29)):
        diff_for_humans()


def diff_for_humans():
    d = pendulum.now().subtract(seconds=1)
    assert d.diff_for_humans(locale=locale) == "kilka sekund temu"

    d = pendulum.now().subtract(seconds=2)
    assert d.diff_for_humans(locale=locale) == "kilka sekund temu"

    d = pendulum.now().subtract(seconds=20)
    assert d.diff_for_humans(locale=locale) == "20 sekund temu"

    d = pendulum.now().subtract(minutes=1)
    assert d.diff_for_humans(locale=locale) == "1 minutę temu"

    d = pendulum.now().subtract(minutes=2)
    assert d.diff_for_humans(locale=locale) == "2 minuty temu"

    d = pendulum.now().subtract(minutes=5)
    assert d.diff_for_humans(locale=locale) == "5 minut temu"

    d = pendulum.now().subtract(hours=1)
    assert d.diff_for_humans(locale=locale) == "1 godzinę temu"

    d = pendulum.now().subtract(hours=2)
    assert d.diff_for_humans(locale=locale) == "2 godziny temu"

    d = pendulum.now().subtract(hours=5)
    assert d.diff_for_humans(locale=locale) == "5 godzin temu"

    d = pendulum.now().subtract(days=1)
    assert d.diff_for_humans(locale=locale) == "1 dzień temu"

    d = pendulum.now().subtract(days=2)
    assert d.diff_for_humans(locale=locale) == "2 dni temu"

    d = pendulum.now().subtract(weeks=1)
    assert d.diff_for_humans(locale=locale) == "1 tydzień temu"

    d = pendulum.now().subtract(weeks=2)
    assert d.diff_for_humans(locale=locale) == "2 tygodnie temu"

    d = pendulum.now().subtract(months=1)
    assert d.diff_for_humans(locale=locale) == "1 miesiąc temu"

    d = pendulum.now().subtract(months=2)
    assert d.diff_for_humans(locale=locale) == "2 miesiące temu"

    d = pendulum.now().subtract(months=5)
    assert d.diff_for_humans(locale=locale) == "5 miesięcy temu"

    d = pendulum.now().subtract(years=1)
    assert d.diff_for_humans(locale=locale) == "1 rok temu"

    d = pendulum.now().subtract(years=2)
    assert d.diff_for_humans(locale=locale) == "2 lata temu"

    d = pendulum.now().subtract(years=5)
    assert d.diff_for_humans(locale=locale) == "5 lat temu"

    d = pendulum.now().add(seconds=1)
    assert d.diff_for_humans(locale=locale) == "za kilka sekund"

    d = pendulum.now().add(seconds=1)
    d2 = pendulum.now()
    assert d.diff_for_humans(d2, locale=locale) == "kilka sekund po"
    assert d2.diff_for_humans(d, locale=locale) == "kilka sekund przed"

    assert d.diff_for_humans(d2, True, locale=locale) == "kilka sekund"
    assert d2.diff_for_humans(d.add(seconds=1), True, locale=locale) == "kilka sekund"

    d = pendulum.now().add(seconds=20)
    d2 = pendulum.now()
    assert d.diff_for_humans(d2, locale=locale) == "20 sekund po"
    assert d2.diff_for_humans(d, locale=locale) == "20 sekund przed"

    d = pendulum.now().add(seconds=10)
    d2 = pendulum.now()
    assert d.diff_for_humans(d2, True, locale=locale) == "kilka sekund"
    assert d2.diff_for_humans(d.add(seconds=1), True, locale=locale) == "11 sekund"


def test_format():
    d = pendulum.datetime(2016, 8, 29, 7, 3, 6, 123456)
    assert d.format("dddd", locale=locale) == "poniedziałek"
    assert d.format("ddd", locale=locale) == "pon."
    assert d.format("MMMM", locale=locale) == "sierpnia"
    assert d.format("MMM", locale=locale) == "sie"
    assert d.format("A", locale=locale) == "AM"
    assert d.format("Qo", locale=locale) == "3"
    assert d.format("Mo", locale=locale) == "8"
    assert d.format("Do", locale=locale) == "29"

    assert d.format("LT", locale=locale) == "07:03"
    assert d.format("LTS", locale=locale) == "07:03:06"
    assert d.format("L", locale=locale) == "29.08.2016"
    assert d.format("LL", locale=locale) == "29 sierpnia 2016"
    assert d.format("LLL", locale=locale) == "29 sierpnia 2016 07:03"
    assert d.format("LLLL", locale=locale) == "poniedziałek, 29 sierpnia 2016 07:03"
