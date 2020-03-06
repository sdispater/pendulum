# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pendulum


locale = "nl"


def test_diff_for_humans():
    with pendulum.test(pendulum.datetime(2016, 8, 29)):
        diff_for_humans()


def diff_for_humans():
    d = pendulum.now().subtract(seconds=1)
    assert d.diff_for_humans(locale=locale) == "enkele seconden geleden"

    d = pendulum.now().subtract(seconds=2)
    assert d.diff_for_humans(locale=locale) == "enkele seconden geleden"

    d = pendulum.now().subtract(seconds=22)
    assert d.diff_for_humans(locale=locale) == "22 seconden geleden"

    d = pendulum.now().subtract(minutes=1)
    assert d.diff_for_humans(locale=locale) == "1 minuut geleden"

    d = pendulum.now().subtract(minutes=2)
    assert d.diff_for_humans(locale=locale) == "2 minuten geleden"

    d = pendulum.now().subtract(hours=1)
    assert d.diff_for_humans(locale=locale) == "1 uur geleden"

    d = pendulum.now().subtract(hours=2)
    assert d.diff_for_humans(locale=locale) == "2 uur geleden"

    d = pendulum.now().subtract(days=1)
    assert d.diff_for_humans(locale=locale) == "1 dag geleden"

    d = pendulum.now().subtract(days=2)
    assert d.diff_for_humans(locale=locale) == "2 dagen geleden"

    d = pendulum.now().subtract(weeks=1)
    assert d.diff_for_humans(locale=locale) == "1 week geleden"

    d = pendulum.now().subtract(weeks=2)
    assert d.diff_for_humans(locale=locale) == "2 weken geleden"

    d = pendulum.now().subtract(months=1)
    assert d.diff_for_humans(locale=locale) == "1 maand geleden"

    d = pendulum.now().subtract(months=2)
    assert d.diff_for_humans(locale=locale) == "2 maanden geleden"

    d = pendulum.now().subtract(years=1)
    assert d.diff_for_humans(locale=locale) == "1 jaar geleden"

    d = pendulum.now().subtract(years=2)
    assert d.diff_for_humans(locale=locale) == "2 jaar geleden"

    d = pendulum.now().add(seconds=1)
    assert d.diff_for_humans(locale=locale) == "over enkele seconden"

    d = pendulum.now().add(weeks=1)
    assert d.diff_for_humans(locale=locale) == "over 1 week"

    d = pendulum.now().add(seconds=1)
    d2 = pendulum.now()
    assert d.diff_for_humans(d2, locale=locale) == "enkele seconden later"
    assert d2.diff_for_humans(d, locale=locale) == "enkele seconden eerder"

    assert d.diff_for_humans(d2, True, locale=locale) == "enkele seconden"
    assert (
        d2.diff_for_humans(d.add(seconds=1), True, locale=locale) == "enkele seconden"
    )


def test_format():
    d = pendulum.datetime(2016, 8, 28, 7, 3, 6, 123456)
    assert d.format("dddd", locale=locale) == "zondag"
    assert d.format("ddd", locale=locale) == "zo"
    assert d.format("MMMM", locale=locale) == "augustus"
    assert d.format("MMM", locale=locale) == "aug."
    assert d.format("A", locale=locale) == "a.m."
    assert d.format("Do", locale=locale) == "28e"
