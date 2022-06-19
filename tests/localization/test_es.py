from __future__ import annotations

import pendulum

locale = "es"


def test_diff_for_humans():
    with pendulum.travel_to(pendulum.datetime(2016, 8, 29), freeze=True):
        diff_for_humans()


def diff_for_humans():
    d = pendulum.now().subtract(seconds=1)
    assert d.diff_for_humans(locale=locale) == "hace unos segundos"

    d = pendulum.now().subtract(seconds=2)
    assert d.diff_for_humans(locale=locale) == "hace unos segundos"

    d = pendulum.now().subtract(minutes=1)
    assert d.diff_for_humans(locale=locale) == "hace 1 minuto"

    d = pendulum.now().subtract(minutes=2)
    assert d.diff_for_humans(locale=locale) == "hace 2 minutos"

    d = pendulum.now().subtract(hours=1)
    assert d.diff_for_humans(locale=locale) == "hace 1 hora"

    d = pendulum.now().subtract(hours=2)
    assert d.diff_for_humans(locale=locale) == "hace 2 horas"

    d = pendulum.now().subtract(days=1)
    assert d.diff_for_humans(locale=locale) == "hace 1 día"

    d = pendulum.now().subtract(days=2)
    assert d.diff_for_humans(locale=locale) == "hace 2 días"

    d = pendulum.now().subtract(weeks=1)
    assert d.diff_for_humans(locale=locale) == "hace 1 semana"

    d = pendulum.now().subtract(weeks=2)
    assert d.diff_for_humans(locale=locale) == "hace 2 semanas"

    d = pendulum.now().subtract(months=1)
    assert d.diff_for_humans(locale=locale) == "hace 1 mes"

    d = pendulum.now().subtract(months=2)
    assert d.diff_for_humans(locale=locale) == "hace 2 meses"

    d = pendulum.now().subtract(years=1)
    assert d.diff_for_humans(locale=locale) == "hace 1 año"

    d = pendulum.now().subtract(years=2)
    assert d.diff_for_humans(locale=locale) == "hace 2 años"

    d = pendulum.now().add(seconds=1)
    assert d.diff_for_humans(locale=locale) == "dentro de unos segundos"

    d = pendulum.now().add(seconds=1)
    d2 = pendulum.now()
    assert d.diff_for_humans(d2, locale=locale) == "unos segundos después"
    assert d2.diff_for_humans(d, locale=locale) == "unos segundos antes"

    assert d.diff_for_humans(d2, True, locale=locale) == "unos segundos"
    assert d2.diff_for_humans(d.add(seconds=1), True, locale=locale) == "unos segundos"
