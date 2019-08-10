# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pendulum


locale = "ru"


def test_diff_for_humans():
    with pendulum.test(pendulum.datetime(2016, 8, 29)):
        diff_for_humans()


def diff_for_humans():
    d = pendulum.now().subtract(seconds=1)
    assert d.diff_for_humans(locale=locale) == "1 секунду назад"

    d = pendulum.now().subtract(seconds=2)
    assert d.diff_for_humans(locale=locale) == "2 секунды назад"

    d = pendulum.now().subtract(seconds=5)
    assert d.diff_for_humans(locale=locale) == "5 секунд назад"

    d = pendulum.now().subtract(seconds=21)
    assert d.diff_for_humans(locale=locale) == "21 секунду назад"

    d = pendulum.now().subtract(minutes=1)
    assert d.diff_for_humans(locale=locale) == "1 минуту назад"

    d = pendulum.now().subtract(minutes=2)
    assert d.diff_for_humans(locale=locale) == "2 минуты назад"

    d = pendulum.now().subtract(minutes=5)
    assert d.diff_for_humans(locale=locale) == "5 минут назад"

    d = pendulum.now().subtract(hours=1)
    assert d.diff_for_humans(locale=locale) == "1 час назад"

    d = pendulum.now().subtract(hours=2)
    assert d.diff_for_humans(locale=locale) == "2 часа назад"

    d = pendulum.now().subtract(hours=5)
    assert d.diff_for_humans(locale=locale) == "5 часов назад"

    d = pendulum.now().subtract(days=1)
    assert d.diff_for_humans(locale=locale) == "1 день назад"

    d = pendulum.now().subtract(days=2)
    assert d.diff_for_humans(locale=locale) == "2 дня назад"

    d = pendulum.now().subtract(days=5)
    assert d.diff_for_humans(locale=locale) == "5 дней назад"

    d = pendulum.now().subtract(weeks=1)
    assert d.diff_for_humans(locale=locale) == "1 неделю назад"

    d = pendulum.now().subtract(weeks=2)
    assert d.diff_for_humans(locale=locale) == "2 недели назад"

    d = pendulum.now().subtract(months=1)
    assert d.diff_for_humans(locale=locale) == "1 месяц назад"

    d = pendulum.now().subtract(months=2)
    assert d.diff_for_humans(locale=locale) == "2 месяца назад"

    d = pendulum.now().subtract(months=5)
    assert d.diff_for_humans(locale=locale) == "5 месяцев назад"

    d = pendulum.now().subtract(years=1)
    assert d.diff_for_humans(locale=locale) == "1 год назад"

    d = pendulum.now().subtract(years=2)
    assert d.diff_for_humans(locale=locale) == "2 года назад"

    d = pendulum.now().subtract(years=5)
    assert d.diff_for_humans(locale=locale) == "5 лет назад"

    d = pendulum.now().add(seconds=1)
    assert d.diff_for_humans(locale=locale) == "через 1 секунду"

    d = pendulum.now().add(seconds=1)
    d2 = pendulum.now()
    assert d.diff_for_humans(d2, locale=locale) == "1 секунда после"
    assert d2.diff_for_humans(d, locale=locale) == "1 секунда до"

    assert d.diff_for_humans(d2, True, locale=locale) == "1 секунда"
    assert d2.diff_for_humans(d.add(seconds=1), True, locale=locale) == "2 секунды"
